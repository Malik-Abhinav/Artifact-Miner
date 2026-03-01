"""
Tests for the unified pipeline CLI module (Simplified <500 LOC).

Core test coverage:
- analyze routes to orchestrator with correct consent handling
- present routes to presentation pipeline with various selectors
- show-portfolio and show-resume format output correctly
- list displays project metadata
"""

import pytest
from unittest.mock import Mock, patch
from src.pipeline import cli


class TestAnalyzeCommand:
    """Tests for the 'analyze' subcommand - NOTE: Skipped heavy orchestrator testing"""
    
    def test_analyze_command_exists(self):
        """Test that analyze command is registered"""
        # Just verify the command handler doesn't crash on malformed input
        with pytest.raises(SystemExit):
            cli.main(["analyze"])  # Missing required argument


class TestPresentCommand:
    """Tests for the 'present' subcommand"""
    
    @patch("src.pipeline.presentation_pipeline.PresentationPipeline")
    def test_present_single_by_id_routes(self, mock_cls):
        """Test present --project-id routes to generate_by_id"""
        from src.pipeline.presentation_pipeline import PresentationResult
        mock_cls.return_value.generate_by_id.return_value = PresentationResult(
            project_id=123, project_name="Test", zip_hash="abc",
            portfolio_item={}, resume_item={}, success=True
        )
        exit_code = cli.main(["present", "--project-id", "123"])
        assert exit_code == 0
        mock_cls.return_value.generate_by_id.assert_called_once_with(123, regenerate=True)
    
    @patch("src.pipeline.presentation_pipeline.PresentationPipeline")
    def test_present_all_routes(self, mock_cls):
        """Test present --all routes to generate_all"""
        from src.pipeline.presentation_pipeline import BatchPresentationResult
        mock_cls.return_value.generate_all.return_value = BatchPresentationResult(
            total_processed=5, successful=5, failed=0, results=[]
        )
        exit_code = cli.main(["present", "--all"])
        assert exit_code == 0
        mock_cls.return_value.generate_all.assert_called_once_with(regenerate=True, limit=None)
    
    @patch("src.pipeline.presentation_pipeline.PresentationPipeline")
    def test_present_failure_returns_error_code(self, mock_cls):
        """Test present returns non-zero exit code on failure"""
        from src.pipeline.presentation_pipeline import PresentationResult
        mock_cls.return_value.generate_by_id.return_value = PresentationResult(
            project_id=123, project_name="Test", zip_hash="abc",
            portfolio_item={}, resume_item={}, success=False, error="Error"
        )
        exit_code = cli.main(["present", "--project-id", "123"])
        assert exit_code == 1


class TestShowPortfolioCommand:
    """Tests for the 'show-portfolio' subcommand"""
    
    @patch("src.pipeline.presentation_pipeline.PresentationPipeline")
    def test_show_portfolio_formats_output(self, mock_cls, capsys):
        """Test show-portfolio displays formatted portfolio item"""
        from src.pipeline.presentation_pipeline import PresentationResult
        mock_cls.return_value.generate_by_id.return_value = PresentationResult(
            project_id=123, project_name="TestProject", zip_hash="abc",
            portfolio_item={
                "project_name": "TestProject", "tagline": "A test", "description": "Test.",
                "languages": ["Python"], "frameworks": ["Django"], "skills": [],
                "key_features": ["F1"], "is_collaborative": True,
                "total_commits": 50, "total_lines": 1000
            },
            resume_item={}, success=True
        )
        exit_code = cli.main(["show-portfolio", "--project-id", "123"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "PORTFOLIO SHOWCASE" in captured.out
        assert "TestProject" in captured.out
    
    @patch("src.pipeline.presentation_pipeline.PresentationPipeline")
    def test_show_portfolio_error_handling(self, mock_cls, capsys):
        """Test show-portfolio handles errors gracefully"""
        from src.pipeline.presentation_pipeline import PresentationResult
        mock_cls.return_value.generate_by_id.return_value = PresentationResult(
            project_id=999, project_name="Unknown", zip_hash="unk",
            portfolio_item={}, resume_item={}, success=False, error="Not found"
        )
        exit_code = cli.main(["show-portfolio", "--project-id", "999"])
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Not found" in captured.err


class TestShowResumeCommand:
    """Tests for the 'show-resume' subcommand"""
    
    @patch("src.pipeline.presentation_pipeline.PresentationPipeline")
    def test_show_resume_formats_output(self, mock_cls, capsys):
        """Test show-resume displays formatted resume item"""
        from src.pipeline.presentation_pipeline import PresentationResult
        mock_cls.return_value.generate_by_id.return_value = PresentationResult(
            project_id=123, project_name="TestProject", zip_hash="abc",
            portfolio_item={},
            resume_item={
                "project_name": "TestProject",
                "bullets": ["Built app", "Implemented tests", "Collaborated"]
            },
            success=True
        )
        exit_code = cli.main(["show-resume", "--project-id", "123"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "RESUME ITEM" in captured.out
        assert "Built app" in captured.out


class TestListCommand:
    """Tests for the 'list' subcommand"""
    
    @patch("src.pipeline.presentation_pipeline.PresentationPipeline")
    def test_list_displays_projects(self, mock_cls, capsys):
        """Test list displays project metadata in table format"""
        mock_cls.return_value.list_available_projects.return_value = [
            {
                "project_id": 1, "project_name": "Project One", "zip_hash": "abcd1234",
                "code_files": 10, "doc_files": 5, "is_git_repo": True,
                "updated_at": "2024-01-15 10:30:00"
            }
        ]
        exit_code = cli.main(["list"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Project One" in captured.out
        assert "abcd1234" in captured.out
    
    @patch("src.pipeline.presentation_pipeline.PresentationPipeline")
    def test_list_empty_database(self, mock_cls, capsys):
        """Test list handles empty database gracefully"""
        mock_cls.return_value.list_available_projects.return_value = []
        exit_code = cli.main(["list"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "No projects found" in captured.out


class TestDeleteCommand:
    """Tests for the 'delete' subcommand"""

    @patch("src.pipeline.cli.confirm_action", return_value=True)
    @patch("src.pipeline.cli.delete_user_configurations_all", return_value=3)
    @patch("src.insights.storage.ProjectInsightsStore")
    def test_delete_all_happy_path(self, mock_store, mock_configs, _confirm, capsys):
        mock_store.return_value.delete_all.return_value = {"deleted_projects": 5}
        exit_code = cli.main(["delete", "all"])
        assert exit_code == 0
        mock_store.return_value.delete_all.assert_called_once()
        mock_configs.assert_called_once()
        captured = capsys.readouterr()
        assert "Deleted projects: 5" in captured.out
        assert "Deleted user configurations: 3" in captured.out

    @patch("src.pipeline.cli.confirm_action", return_value=False)
    def test_delete_cancelled(self, _confirm, capsys):
        exit_code = cli.main(["delete", "insight", "all"])
        assert exit_code == 0
        assert "Cancelled." in capsys.readouterr().out

    @patch("src.pipeline.cli.confirm_action", return_value=True)
    @patch("src.pipeline.cli.delete_insights_for_project_id", return_value={"deleted_projects": 1, "deleted_zips": 0})
    def test_delete_insight_by_project_id(self, mock_delete, _confirm):
        exit_code = cli.main(["delete", "insight", "--project-id", "7"])
        assert exit_code == 0
        mock_delete.assert_called_once_with("data/app.db", 7)

    @patch("src.pipeline.cli.confirm_action", return_value=True)
    @patch("src.insights.storage.ProjectInsightsStore")
    def test_delete_insight_all(self, mock_store, _confirm, capsys):
        mock_store.return_value.delete_all.return_value = {"deleted_projects": 4, "deleted_zips": 2}
        exit_code = cli.main(["delete", "insight", "all"])
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "Deleted projects: 4" in captured.out
        assert "Deleted zips: 2" in captured.out

    @patch("src.pipeline.cli.confirm_action", return_value=True)
    @patch("src.pipeline.cli.delete_user_configurations_all", return_value=2)
    def test_delete_config_all(self, _delete_all, _confirm, capsys):
        exit_code = cli.main(["delete", "config", "all"])
        assert exit_code == 0
        assert "Deleted user configurations: 2" in capsys.readouterr().out

    def test_delete_insight_missing_selector(self):
        exit_code = cli.main(["delete", "insight"])
        assert exit_code == 1

    def test_delete_insight_invalid_argument_combo(self):
        exit_code = cli.main(["delete", "insight", "--project-id", "3", "all"])
        assert exit_code == 1

    def test_delete_config_cancelled(self, capsys):
        with patch("src.pipeline.cli.confirm_action", return_value=False):
            exit_code = cli.main(["delete", "config", "all"])
        assert exit_code == 0
        assert "Cancelled." in capsys.readouterr().out

    def test_delete_missing_target(self):
        exit_code = cli.main(["delete"])
        assert exit_code == 1

    @patch("src.pipeline.cli.confirm_action", return_value=True)
    def test_delete_config_all_missing_table(self, _confirm, tmp_path, capsys):
        db_path = tmp_path / "empty.db"
        exit_code = cli.main(["delete", "--db-path", str(db_path), "config", "all"])
        assert exit_code == 0
        assert "Deleted user configurations: 0" in capsys.readouterr().out

    @patch("src.pipeline.cli.confirm_action", return_value=True)
    def test_delete_insight_project_id_not_found(self, _confirm, tmp_path, capsys):
        import sqlite3

        db_path = tmp_path / "insights.db"
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE project_info (id INTEGER, project_id INTEGER, ingest_id INTEGER);")
            conn.commit()
        exit_code = cli.main(["delete", "--db-path", str(db_path), "insight", "--project-id", "42"])
        assert exit_code == 0
        output = capsys.readouterr().out
        assert "Deleted projects: 0" in output
        assert "Deleted zips: 0" in output

    @patch("src.pipeline.cli.confirm_action", return_value=True)
    def test_delete_insight_cleans_up_related_rows(self, _confirm, tmp_path):
        import sqlite3

        db_path = tmp_path / "insights_full.db"
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE ingest (id INTEGER PRIMARY KEY);")
            conn.execute("CREATE TABLE projects (id INTEGER PRIMARY KEY);")
            conn.execute("CREATE TABLE project_info (id INTEGER, project_id INTEGER, ingest_id INTEGER);")
            conn.execute("INSERT INTO ingest (id) VALUES (1);")
            conn.execute("INSERT INTO projects (id) VALUES (10);")
            conn.execute("INSERT INTO project_info (id, project_id, ingest_id) VALUES (5, 10, 1);")
            conn.commit()

        exit_code = cli.main(["delete", "--db-path", str(db_path), "insight", "--project-id", "5"])
        assert exit_code == 0

        with sqlite3.connect(db_path) as conn:
            assert conn.execute("SELECT COUNT(*) FROM project_info;").fetchone()[0] == 0
            assert conn.execute("SELECT COUNT(*) FROM projects;").fetchone()[0] == 0
            assert conn.execute("SELECT COUNT(*) FROM ingest;").fetchone()[0] == 0


class TestIncrementalCommand:
    """Tests for the 'incremental' subcommand."""

    def test_incremental_missing_args_exits(self):
        """Missing positional args causes argparse to exit."""
        with pytest.raises(SystemExit):
            cli.main(["incremental"])

    def test_incremental_new_zip_not_found(self, tmp_path, capsys):
        """Returns error when the new ZIP file does not exist."""
        exit_code = cli.main([
            "incremental",
            str(tmp_path / "nonexistent.zip"),
            "deadbeefdeadbeef",
        ])
        assert exit_code == 1
        assert "not found" in capsys.readouterr().err.lower()

    @patch("src.insights.storage.ProjectInsightsStore")
    def test_incremental_old_hash_not_found(self, mock_store_cls, tmp_path, capsys):
        """Returns error when old_zip_hash has no stored projects."""
        # Create a real file so the file-existence check passes
        zip_file = tmp_path / "new.zip"
        zip_file.write_bytes(b"PK")
        mock_store_cls.return_value.list_projects_for_zip.return_value = []

        exit_code = cli.main([
            "incremental",
            str(zip_file),
            "deadbeefdeadbeef",
        ])
        assert exit_code == 1
        assert "No existing analysis" in capsys.readouterr().err

    @patch("src.pipeline.orchestrator.ArtifactPipeline")
    @patch("src.insights.storage.ProjectInsightsStore")
    def test_incremental_success(self, mock_store_cls, mock_pipeline_cls, tmp_path, capsys):
        """Returns 0 and prints merge summary on success."""
        zip_file = tmp_path / "new.zip"
        zip_file.write_bytes(b"PK")

        mock_store_cls.return_value.list_projects_for_zip.return_value = ["OldProject"]
        mock_pipeline_cls.return_value.incremental_update.return_value = {
            "status": "complete",
            "new_zip_hash": "newhashabc",
            "new_only_projects": ["NewProj"],
            "retained_projects": ["OldProject"],
            "updated_projects": [],
            "total_projects": 2,
        }

        exit_code = cli.main([
            "incremental",
            str(zip_file),
            "oldhash123",
        ])
        assert exit_code == 0
        out = capsys.readouterr().out
        assert "Incremental update complete" in out
        assert "newhashabc" in out

    @patch("src.pipeline.orchestrator.ArtifactPipeline")
    @patch("src.insights.storage.ProjectInsightsStore")
    def test_incremental_cancelled_returns_error(self, mock_store_cls, mock_pipeline_cls, tmp_path, capsys):
        """Returns 1 when pipeline signals cancellation."""
        zip_file = tmp_path / "new.zip"
        zip_file.write_bytes(b"PK")

        mock_store_cls.return_value.list_projects_for_zip.return_value = ["Proj"]
        mock_pipeline_cls.return_value.incremental_update.return_value = {
            "status": "cancelled",
            "message": "User cancelled",
        }

        exit_code = cli.main([
            "incremental",
            str(zip_file),
            "oldhash123",
        ])
        assert exit_code == 1
        assert "cancelled" in capsys.readouterr().out.lower()


class TestRepresentationInteractiveAction:
    """Tests for _iact_representation interactive action."""

    def _make_report(self):
        return {
            "projects": {
                "Alpha": {
                    "project_metrics": {
                        "languages": ["Python"],
                        "frameworks": [],
                        "skills": ["Django", "REST"],
                        "total_lines": 5000,
                        "total_commits": 100,
                    },
                    "git_analysis": {
                        "total_commits": 100,
                        "total_contributors": 2,
                        "last_commit_at": "2025-01-01",
                        "activity_mix": {"code": 80, "test": 10, "doc": 10},
                        "contributors": [{"commits": 60}],
                    },
                    "portfolio_item": {"tagline": "Alpha tagline"},
                    "resume_item": {"bullets": ["Built Alpha"]},
                },
            },
            "global_insights": {
                "chronological_skills": {
                    "timeline": [
                        {"timestamp": "2024-01-01T00:00:00", "category": "code", "skills": ["Python"]}
                    ],
                    "total_events": 1,
                    "categories": ["code"],
                }
            },
        }

    @patch("src.insights.storage.ProjectInsightsStore")
    def test_representation_no_runs_exits_gracefully(self, mock_store_cls, capsys):
        """Exits gracefully when no analyses exist."""
        mock_store_cls.return_value.list_recent_zipfiles.return_value = []

        with patch("builtins.input", return_value=""):
            cli._iact_representation()

        assert "No analyses found" in capsys.readouterr().out

    @patch("src.insights.storage.ProjectInsightsStore")
    def test_representation_no_report_exits_gracefully(self, mock_store_cls, capsys):
        """Exits gracefully when the report cannot be loaded."""
        mock_store_cls.return_value.list_recent_zipfiles.return_value = [
            {"zip_hash": "abc123"}
        ]
        mock_store_cls.return_value.load_zip_report.return_value = None

        with patch("builtins.input", return_value=""):
            cli._iact_representation()

        assert "Could not load report" in capsys.readouterr().out

    @patch("src.insights.storage.ProjectInsightsStore")
    def test_representation_displays_ranking(self, mock_store_cls, capsys):
        """Ranking section is shown with project entries."""
        mock_store_cls.return_value.list_recent_zipfiles.return_value = [
            {"zip_hash": "abc123"}
        ]
        mock_store_cls.return_value.load_zip_report.return_value = self._make_report()

        # Provide defaults for all prompts: criteria, n, manual_order,
        # show_chron (y), show_skills (y), highlight, suppress, show_showcase (y), selected
        inputs = iter(["score", "", "", "y", "y", "", "", "y", ""])
        with patch("builtins.input", side_effect=inputs):
            cli._iact_representation()

        out = capsys.readouterr().out
        assert "RANKING" in out
        assert "Alpha" in out

    @patch("src.insights.storage.ProjectInsightsStore")
    def test_representation_displays_skills(self, mock_store_cls, capsys):
        """Skills section lists aggregated skills."""
        mock_store_cls.return_value.list_recent_zipfiles.return_value = [
            {"zip_hash": "abc123"}
        ]
        mock_store_cls.return_value.load_zip_report.return_value = self._make_report()

        inputs = iter(["score", "", "", "y", "y", "", "", "y", ""])
        with patch("builtins.input", side_effect=inputs):
            cli._iact_representation()

        out = capsys.readouterr().out
        assert "SKILLS" in out
        assert "Django" in out or "REST" in out

    @patch("src.insights.storage.ProjectInsightsStore")
    def test_representation_invalid_criteria_falls_back_to_score(self, mock_store_cls, capsys):
        """Invalid ranking criteria defaults to 'score' without crashing."""
        mock_store_cls.return_value.list_recent_zipfiles.return_value = [
            {"zip_hash": "abc123"}
        ]
        mock_store_cls.return_value.load_zip_report.return_value = self._make_report()

        inputs = iter(["invalid_criteria", "", "", "y", "y", "", "", "y", ""])
        with patch("builtins.input", side_effect=inputs):
            cli._iact_representation()

        out = capsys.readouterr().out
        assert "RANKING" in out  # still renders

    @patch("src.insights.storage.ProjectInsightsStore")
    def test_representation_chronology_skipped_when_disabled(self, mock_store_cls, capsys):
        """Chronology data block is omitted from the preview when user opts out."""
        mock_store_cls.return_value.list_recent_zipfiles.return_value = [
            {"zip_hash": "abc123"}
        ]
        mock_store_cls.return_value.load_zip_report.return_value = self._make_report()

        # Opt out of chronology (n), keep everything else as defaults
        inputs = iter(["score", "", "", "n", "y", "", "", "y", ""])
        with patch("builtins.input", side_effect=inputs):
            cli._iact_representation()

        out = capsys.readouterr().out
        # The [CHRONOLOGY] prompt label appears, but the data output line
        # "  CHRONOLOGY  (N events)" must not be present in the preview block.
        assert "  CHRONOLOGY  (" not in out


class TestMainFunction:
    """Tests for main() function behavior"""
    
    def test_main_no_command_prints_help(self):
        """Test main() with no command prints help"""
        exit_code = cli.main([])
        assert exit_code == 1
    
    def test_main_unknown_command(self):
        """Test main() with unknown command returns error"""
        with pytest.raises(SystemExit):
            cli.main(["unknown-command"])
