"""
Tests for privacy consent API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from api.app import app

client = TestClient(app)


class TestConsentAPI:
    """Test cases for privacy consent API endpoints."""
    
    def test_get_consent_status_default(self):
        """Test getting default consent status."""
        response = client.get("/privacy-consent/")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "llm_consent" in data
        assert "directory_consent" in data
        assert "has_all_consents" in data
    
    def test_grant_llm_consent(self):
        """Test granting LLM consent."""
        response = client.post(
            "/privacy-consent/",
            json={"consent_type": "llm"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert "Successfully granted llm consent" in data["message"]
        assert data["llm_consent"]["consent_given"] is True
    
    def test_grant_directory_consent_with_paths(self):
        """Test granting directory consent with allowed paths."""
        response = client.post(
            "/privacy-consent/",
            json={
                "consent_type": "directory",
                "allowed_paths": ["/test/path1", "/test/path2"]
            }
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert data["directory_consent"]["consent_given"] is True
        assert len(data["directory_consent"]["allowed_paths"]) == 2
    
    def test_grant_all_consents(self):
        """Test granting all consents at once."""
        response = client.post(
            "/privacy-consent/",
            json={
                "consent_type": "all",
                "allowed_paths": ["/test/projects"]
            }
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert data["llm_consent"]["consent_given"] is True
        assert data["directory_consent"]["consent_given"] is True
    
    def test_get_llm_consent_only(self):
        """Test getting LLM consent status only."""
        response = client.get("/privacy-consent/llm")
        assert response.status_code == 200
        
        data = response.json()
        assert "consent_given" in data
        assert "consent_type" in data
        assert data["consent_type"] == "external_llm_data_access"
    
    def test_get_directory_consent_only(self):
        """Test getting directory consent status only."""
        response = client.get("/privacy-consent/directory")
        assert response.status_code == 200
        
        data = response.json()
        assert "consent_given" in data
        assert "consent_type" in data
        assert data["consent_type"] == "directory_access"
        assert "allowed_paths" in data
    
    def test_revoke_llm_consent(self):
        """Test revoking LLM consent."""
        # First grant consent
        client.post("/privacy-consent/", json={"consent_type": "llm"})
        
        # Then revoke it
        response = client.delete(
            "/privacy-consent/",
            json={"consent_type": "llm"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert "Successfully revoked llm consent" in data["message"]
        assert data["llm_consent"]["consent_given"] is False
    
    def test_revoke_all_consents(self):
        """Test revoking all consents."""
        # First grant all consents
        client.post(
            "/privacy-consent/",
            json={"consent_type": "all", "allowed_paths": ["/test"]}
        )
        
        # Then revoke all
        response = client.delete(
            "/privacy-consent/",
            json={"consent_type": "all"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert data["llm_consent"]["consent_given"] is False
        assert data["directory_consent"]["consent_given"] is False
    
    def test_update_allowed_paths_requires_consent(self):
        """Test that updating paths requires existing consent."""
        # First ensure consent is revoked
        client.delete("/privacy-consent/", json={"consent_type": "directory"})
        
        # Try to update paths without consent
        response = client.patch(
            "/privacy-consent/directory/paths",
            json=["/new/path"]
        )
        assert response.status_code == 400
        assert "must be granted" in response.json()["detail"]
    
    def test_update_allowed_paths_with_consent(self):
        """Test updating allowed paths with existing consent."""
        # First grant consent
        client.post(
            "/privacy-consent/",
            json={"consent_type": "directory", "allowed_paths": ["/old/path"]}
        )
        
        # Then update paths
        response = client.patch(
            "/privacy-consent/directory/paths",
            json=["/new/path1", "/new/path2"]
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert len(data["directory_consent"]["allowed_paths"]) == 2
    
    def test_reset_all_consents(self):
        """Test resetting all consents to default."""
        # First grant some consents
        client.post(
            "/privacy-consent/",
            json={"consent_type": "all", "allowed_paths": ["/test"]}
        )
        
        # Reset all
        response = client.post("/privacy-consent/reset")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "ok"
        assert "reset" in data["message"].lower()
        assert data["llm_consent"]["consent_given"] is False
        assert data["directory_consent"]["consent_given"] is False
    
    def test_invalid_consent_type_returns_422(self):
        """Test that invalid consent type returns validation error."""
        response = client.post(
            "/privacy-consent/",
            json={"consent_type": "invalid_type"}
        )
        assert response.status_code == 422  # Validation error
    
    def test_consent_timestamps_are_set(self):
        """Test that timestamps are properly set when granting consent."""
        response = client.post(
            "/privacy-consent/",
            json={"consent_type": "llm"}
        )
        assert response.status_code == 200
        
        data = response.json()
        assert data["llm_consent"]["consent_timestamp"] is not None
        assert data["llm_consent"]["last_updated"] is not None

