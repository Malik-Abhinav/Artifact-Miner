"""
Test suite for the Incremental ZIP Update feature.

Covers:
    - Storage layer: list_projects_for_zip_detailed, reassign_projects_to_zip_hash,
      delete_projects_by_names, delete_zip_if_empty
    - Orchestrator layer: incremental_update() merge logic
    - API layer: POST /projects/update/{old_zip_hash}

Run from the project root:
    docker compose run --rm backend pytest -v tests/test_incremental_update.py
"""

import os
import sys
import inspect
import shutil
import sqlite3
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import httpx
import pytest
from fastapi.testclient import TestClient

project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

# Compatibility shim: older httpx versions don't accept the 'app' kwarg used by Starlette's TestClient
if "app" not in inspect.signature(httpx.Client.__init__).parameters:
    _orig_httpx_init = httpx.Client.__init__

    def _patched_httpx_init(self, *args, **kwargs):
        kwargs.pop("app", None)
        return _orig_httpx_init(self, *args, **kwargs)

    httpx.Client.__init__ = _patched_httpx_init

from src.insights.storage import (
    ProjectInsightsStore,
    PROJECTS_TABLE,
    INGEST_TABLE,
    PROJECT_INFO_TABLE,
)
from src.config.config_manager import UserConfigManager
from tests.insights.utils import build_pipeline_payload


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def temp_store(tmp_path):
    """Create a fresh ProjectInsightsStore backed by a temp database."""
    db_path = tmp_path / "test.db"
    store = ProjectInsightsStore(db_path=str(db_path), encryption_key=b"test-key")
    return store


def _seed_zip(store, zip_path, project_names):
    """Record a synthetic pipeline run with the given project names under zip_path."""
    payload = build_pipeline_payload(project_names=tuple(project_names))
    store.record_pipeline_run(zip_path, payload)


def _get_zip_hash(store, zip_path):
    """Resolve the zip hash stored for a given zip_path."""
    runs = store.list_recent_zipfiles(limit=10)
    for run in runs:
        if run.get("zip_path") == zip_path:
            return run["zip_hash"]
    return None


def _project_names_for_hash(store, zip_hash):
    """Return the set of project names associated with a zip hash."""
    return set(store.list_projects_for_zip(zip_hash))


def _project_count_in_db(store):
    """Count total rows in the projects table."""
    with store._connect() as conn:
        return conn.execute(f"SELECT COUNT(*) FROM {PROJECTS_TABLE};").fetchone()[0]


# ===========================================================================
# 1. Storage Layer Tests
# ===========================================================================


class TestListProjectsForZipDetailed:
    """Tests for list_projects_for_zip_detailed()."""

    def test_returns_detailed_records(self, temp_store):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha", "Beta"])
        zip_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        detailed = temp_store.list_projects_for_zip_detailed(zip_hash)
        assert len(detailed) == 2
        names = {d["project_name"] for d in detailed}
        assert names == {"Alpha", "Beta"}
        for d in detailed:
            assert "project_id" in d
            assert "zip_hash" in d
            assert d["zip_hash"] == zip_hash

    def test_returns_empty_for_unknown_hash(self, temp_store):
        assert temp_store.list_projects_for_zip_detailed("nonexistent") == []


class TestReassignProjectsToZipHash:
    """Tests for reassign_projects_to_zip_hash()."""

    def test_reassign_moves_projects(self, temp_store):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha", "Beta", "Gamma"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        moved = temp_store.reassign_projects_to_zip_hash(old_hash, "new-hash-123", ["Alpha", "Gamma"])
        assert moved == 2

        # Alpha and Gamma now under new hash
        with temp_store._connect() as conn:
            rows = conn.execute(
                f"SELECT project_name FROM {PROJECTS_TABLE} WHERE source_hash = ?;",
                ("new-hash-123",),
            ).fetchall()
        assert {r[0] for r in rows} == {"Alpha", "Gamma"}

        # Beta still under old hash
        with temp_store._connect() as conn:
            rows = conn.execute(
                f"SELECT project_name FROM {PROJECTS_TABLE} WHERE source_hash = ?;",
                (old_hash,),
            ).fetchall()
        assert {r[0] for r in rows} == {"Beta"}

    def test_reassign_empty_list_returns_zero(self, temp_store):
        assert temp_store.reassign_projects_to_zip_hash("old", "new", []) == 0

    def test_reassign_nonexistent_project_returns_zero(self, temp_store):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")
        moved = temp_store.reassign_projects_to_zip_hash(old_hash, "new-hash", ["NoSuchProject"])
        assert moved == 0


class TestDeleteProjectsByNames:
    """Tests for delete_projects_by_names()."""

    def test_deletes_specific_projects(self, temp_store):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha", "Beta", "Gamma"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        deleted = temp_store.delete_projects_by_names(old_hash, ["Alpha", "Gamma"])
        assert deleted == 2

        remaining = _project_names_for_hash(temp_store, old_hash)
        assert remaining == {"Beta"}

    def test_delete_empty_list_returns_zero(self, temp_store):
        assert temp_store.delete_projects_by_names("hash", []) == 0

    def test_delete_nonexistent_returns_zero(self, temp_store):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")
        deleted = temp_store.delete_projects_by_names(old_hash, ["Nope"])
        assert deleted == 0


class TestDeleteZipIfEmpty:
    """Tests for delete_zip_if_empty()."""

    def test_deletes_when_no_projects_remain(self, temp_store):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        # Remove all projects first
        temp_store.delete_projects_by_names(old_hash, ["Alpha"])

        # Now the zip record should be cleaned up
        cleaned = temp_store.delete_zip_if_empty(old_hash)
        assert cleaned is True

        # Verify ingest records are gone
        with temp_store._connect() as conn:
            count = conn.execute(
                f"SELECT COUNT(*) FROM {INGEST_TABLE} WHERE source_hash = ?;",
                (old_hash,),
            ).fetchone()[0]
        assert count == 0

    def test_does_not_delete_when_projects_remain(self, temp_store):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha", "Beta"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        cleaned = temp_store.delete_zip_if_empty(old_hash)
        assert cleaned is False

    def test_handles_nonexistent_hash(self, temp_store):
        cleaned = temp_store.delete_zip_if_empty("nonexistent")
        # No projects exist for this hash, but also no ingest records
        # So it will try to delete ingest records (0 affected) and return True
        assert cleaned is True


# ===========================================================================
# 2. Orchestrator Layer Tests
# ===========================================================================


class TestIncrementalUpdate:
    """Tests for ArtifactPipeline.incremental_update() merge logic."""

    def _make_pipeline(self, store):
        """Create an ArtifactPipeline with the given store, patching heavy deps."""
        from src.pipeline.orchestrator import ArtifactPipeline
        pipeline = ArtifactPipeline(insights_store=store, enable_insights=False)
        pipeline.insights_store = store
        return pipeline

    def test_no_overlap_all_retained(self, temp_store, tmp_path):
        """Old: {A, B}, New: {C} → result has {A, B, C}."""
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha", "Beta"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        # Create a new zip with a single project "Gamma"
        new_zip = tmp_path / "new.zip"
        _create_test_zip(new_zip, ["Gamma"])

        pipeline = self._make_pipeline(temp_store)

        # Mock start() to simulate pipeline running and persisting
        def mock_start(zip_path, **kwargs):
            payload = build_pipeline_payload(project_names=("Gamma",))
            temp_store.record_pipeline_run(str(zip_path), payload)
            return {"projects": {"Gamma": {}, "_misc_files": {}}}

        with patch.object(pipeline, "start", side_effect=mock_start):
            with patch.object(pipeline, "_get_zip_hash", return_value="new-hash-abc"):
                result = pipeline.incremental_update(
                    new_zip_path=str(new_zip),
                    old_zip_hash=old_hash,
                )

        assert result["status"] == "complete"
        assert sorted(result["retained_projects"]) == ["Alpha", "Beta"]
        assert result["new_only_projects"] == ["Gamma"]
        assert result["updated_projects"] == []
        assert result["total_projects"] == 3

    def test_full_overlap_all_updated(self, temp_store, tmp_path):
        """Old: {A, B}, New: {A, B} → result has new {A, B}."""
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha", "Beta"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        new_zip = tmp_path / "new.zip"
        _create_test_zip(new_zip, ["Alpha", "Beta"])

        pipeline = self._make_pipeline(temp_store)

        def mock_start(zip_path, **kwargs):
            payload = build_pipeline_payload(project_names=("Alpha", "Beta"))
            temp_store.record_pipeline_run(str(zip_path), payload)
            return {"projects": {"Alpha": {}, "Beta": {}}}

        with patch.object(pipeline, "start", side_effect=mock_start):
            with patch.object(pipeline, "_get_zip_hash", return_value="new-hash-def"):
                result = pipeline.incremental_update(
                    new_zip_path=str(new_zip),
                    old_zip_hash=old_hash,
                )

        assert result["status"] == "complete"
        assert result["retained_projects"] == []
        assert result["new_only_projects"] == []
        assert sorted(result["updated_projects"]) == ["Alpha", "Beta"]
        assert result["total_projects"] == 2

    def test_partial_overlap(self, temp_store, tmp_path):
        """Old: {A, B, C}, New: {B, D} → result has {A, new-B, C, D}."""
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha", "Beta", "Gamma"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        new_zip = tmp_path / "new.zip"
        _create_test_zip(new_zip, ["Beta", "Delta"])

        pipeline = self._make_pipeline(temp_store)

        def mock_start(zip_path, **kwargs):
            payload = build_pipeline_payload(project_names=("Beta", "Delta"))
            temp_store.record_pipeline_run(str(zip_path), payload)
            return {"projects": {"Beta": {}, "Delta": {}}}

        with patch.object(pipeline, "start", side_effect=mock_start):
            with patch.object(pipeline, "_get_zip_hash", return_value="new-hash-ghi"):
                result = pipeline.incremental_update(
                    new_zip_path=str(new_zip),
                    old_zip_hash=old_hash,
                )

        assert result["status"] == "complete"
        assert sorted(result["retained_projects"]) == ["Alpha", "Gamma"]
        assert result["new_only_projects"] == ["Delta"]
        assert result["updated_projects"] == ["Beta"]
        assert result["total_projects"] == 4

    def test_cancelled_pipeline(self, temp_store, tmp_path):
        """If the inner pipeline is cancelled, return cancelled status."""
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        new_zip = tmp_path / "new.zip"
        _create_test_zip(new_zip, ["Beta"])

        pipeline = self._make_pipeline(temp_store)

        with patch.object(pipeline, "start", return_value={"status": "cancelled"}):
            result = pipeline.incremental_update(
                new_zip_path=str(new_zip),
                old_zip_hash=old_hash,
            )

        assert result["status"] == "cancelled"

    def test_no_store_raises(self, tmp_path):
        """incremental_update() requires an insights store."""
        from src.pipeline.orchestrator import ArtifactPipeline
        pipeline = ArtifactPipeline(insights_store=None, enable_insights=False)

        with pytest.raises(RuntimeError, match="Insights store is required"):
            pipeline.incremental_update(
                new_zip_path="/tmp/fake.zip",
                old_zip_hash="abc123",
            )

    def test_old_zip_cleaned_up(self, temp_store, tmp_path):
        """After update, old zip record should be deleted if no projects remain."""
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        # Verify old hash has ingest records
        with temp_store._connect() as conn:
            count = conn.execute(
                f"SELECT COUNT(*) FROM {INGEST_TABLE} WHERE source_hash = ?;",
                (old_hash,),
            ).fetchone()[0]
        assert count >= 1

        new_zip = tmp_path / "new.zip"
        _create_test_zip(new_zip, ["Alpha"])

        pipeline = self._make_pipeline(temp_store)

        def mock_start(zip_path, **kwargs):
            payload = build_pipeline_payload(project_names=("Alpha",))
            temp_store.record_pipeline_run(str(zip_path), payload)
            return {"projects": {"Alpha": {}}}

        with patch.object(pipeline, "start", side_effect=mock_start):
            with patch.object(pipeline, "_get_zip_hash", return_value="new-hash-cleanup"):
                result = pipeline.incremental_update(
                    new_zip_path=str(new_zip),
                    old_zip_hash=old_hash,
                )

        assert result["status"] == "complete"

        # Old hash should have no projects left
        remaining = _project_names_for_hash(temp_store, old_hash)
        assert remaining == set()


# ===========================================================================
# 3. API Endpoint Tests
# ===========================================================================


class TestUpdateEndpoint:
    """Tests for POST /projects/update/{old_zip_hash}."""

    def _get_client(self, store, manager):
        """Create a test client with dependency overrides."""
        from src.api import deps
        from src.api.app import app

        app.dependency_overrides[deps.get_store] = lambda: store
        app.dependency_overrides[deps.get_config_manager] = lambda: manager
        client = TestClient(app)
        return client, app

    def _make_manager(self, tmp_path, user_id="1"):
        """Create a UserConfigManager and seed consent for the given user."""
        db_path = str(tmp_path / "config.db")
        manager = UserConfigManager(db_path=db_path)
        manager.create_config(
            user_id,
            zip_file="/tmp/test.zip",
            llm_consent=False,
            llm_consent_asked=False,
            data_access_consent=True,
        )
        return manager

    def test_404_when_old_zip_not_found(self, temp_store, tmp_path):
        manager = self._make_manager(tmp_path)
        client, app = self._get_client(temp_store, manager)
        try:
            response = client.post(
                "/projects/update/nonexistent-hash",
                json={
                    "user_id": "1",
                    "old_zip_hash": "nonexistent-hash",
                    "new_zip_path": "/tmp/new.zip",
                },
            )
            assert response.status_code == 404
            assert "No existing analysis found" in response.json()["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_404_when_user_consent_missing(self, temp_store, tmp_path):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        # Manager without consent for user "99"
        db_path = str(tmp_path / "config_empty.db")
        manager = UserConfigManager(db_path=db_path)

        client, app = self._get_client(temp_store, manager)
        try:
            response = client.post(
                f"/projects/update/{old_hash}",
                json={
                    "user_id": "99",
                    "old_zip_hash": old_hash,
                    "new_zip_path": "/tmp/new.zip",
                },
            )
            assert response.status_code == 404
            assert "Consent not found" in response.json()["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_successful_update(self, temp_store, tmp_path):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha", "Beta"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        manager = self._make_manager(tmp_path)

        mock_summary = {
            "status": "complete",
            "new_zip_hash": "new-hash-xyz",
            "old_zip_hash": old_hash,
            "new_only_projects": ["Gamma"],
            "retained_projects": ["Alpha"],
            "updated_projects": ["Beta"],
            "total_projects": 3,
        }

        client, app = self._get_client(temp_store, manager)
        try:
            with patch(
                "src.pipeline.orchestrator.ArtifactPipeline",
                autospec=False,
            ) as MockPipeline:
                mock_instance = MagicMock()
                mock_instance.incremental_update.return_value = mock_summary
                MockPipeline.return_value = mock_instance

                response = client.post(
                    f"/projects/update/{old_hash}",
                    json={
                        "user_id": "1",
                        "old_zip_hash": old_hash,
                        "new_zip_path": "/tmp/new.zip",
                    },
                )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "ok"
            assert data["new_zip_hash"] == "new-hash-xyz"
            assert data["total_projects"] == 3
            assert "Alpha" in data["retained_projects"]
            assert "Beta" in data["updated_projects"]
            assert "Gamma" in data["new_only_projects"]
        finally:
            app.dependency_overrides.clear()

    def test_cancelled_update(self, temp_store, tmp_path):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        manager = self._make_manager(tmp_path)

        client, app = self._get_client(temp_store, manager)
        try:
            with patch(
                "src.pipeline.orchestrator.ArtifactPipeline",
                autospec=False,
            ) as MockPipeline:
                mock_instance = MagicMock()
                mock_instance.incremental_update.return_value = {
                    "status": "cancelled",
                    "message": "Pipeline was cancelled during update",
                }
                MockPipeline.return_value = mock_instance

                response = client.post(
                    f"/projects/update/{old_hash}",
                    json={
                        "user_id": "1",
                        "old_zip_hash": old_hash,
                        "new_zip_path": "/tmp/new.zip",
                    },
                )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "cancelled"
        finally:
            app.dependency_overrides.clear()

    def test_pipeline_failure_returns_500(self, temp_store, tmp_path):
        _seed_zip(temp_store, "/tmp/old.zip", ["Alpha"])
        old_hash = _get_zip_hash(temp_store, "/tmp/old.zip")

        manager = self._make_manager(tmp_path)

        client, app = self._get_client(temp_store, manager)
        try:
            with patch(
                "src.pipeline.orchestrator.ArtifactPipeline",
                autospec=False,
            ) as MockPipeline:
                mock_instance = MagicMock()
                mock_instance.incremental_update.side_effect = Exception("boom")
                MockPipeline.return_value = mock_instance

                response = client.post(
                    f"/projects/update/{old_hash}",
                    json={
                        "user_id": "1",
                        "old_zip_hash": old_hash,
                        "new_zip_path": "/tmp/new.zip",
                    },
                )

            assert response.status_code == 500
        finally:
            app.dependency_overrides.clear()


# ===========================================================================
# Helpers
# ===========================================================================


def _create_test_zip(zip_path: Path, project_names: list):
    """Create a minimal valid ZIP with one file per project directory."""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for name in project_names:
            zf.writestr(f"{name}/main.py", f"# {name}\nprint('hello')\n")
            zf.writestr(f"{name}/README.md", f"# {name}\nA test project.\n")
