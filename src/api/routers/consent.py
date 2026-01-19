"""
FastAPI router for privacy consent management.
"""
from __future__ import annotations

from typing import Optional, List, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from consent.llm_consent_manager import LLMConsentManager
from consent.directory_consent_manager import DirectoryConsentManager

router = APIRouter(prefix="/privacy-consent", tags=["privacy-consent"])


# ============================================================================
# Pydantic Models
# ============================================================================

class ConsentGrantRequest(BaseModel):
    """Request to grant privacy consent."""
    consent_type: Literal["llm", "directory", "all"] = Field(
        ...,
        description="Type of consent to grant: 'llm' for LLM data access, 'directory' for directory access, 'all' for both"
    )
    allowed_paths: Optional[List[str]] = Field(
        default=None,
        description="List of allowed directory paths (only applicable for directory consent)"
    )


class ConsentRevokeRequest(BaseModel):
    """Request to revoke privacy consent."""
    consent_type: Literal["llm", "directory", "all"] = Field(
        ...,
        description="Type of consent to revoke: 'llm', 'directory', or 'all'"
    )


class ConsentStatusResponse(BaseModel):
    """Response with consent status information."""
    llm_consent: dict
    directory_consent: dict


# ============================================================================
# Endpoints
# ============================================================================

@router.post("/")
def grant_consent(request: ConsentGrantRequest):
    """
    Grant privacy consent for LLM data access and/or directory access.
    
    - **consent_type**: Type of consent to grant ('llm', 'directory', or 'all')
    - **allowed_paths**: Optional list of directory paths (only for directory consent)
    
    Returns consent status after granting.
    """
    llm_manager = LLMConsentManager()
    dir_manager = DirectoryConsentManager()
    
    try:
        if request.consent_type in ("llm", "all"):
            llm_manager.grant()
        
        if request.consent_type in ("directory", "all"):
            dir_manager.grant(allowed_paths=request.allowed_paths)
        
        return {
            "status": "ok",
            "message": f"Successfully granted {request.consent_type} consent",
            "llm_consent": llm_manager.get_consent_info(),
            "directory_consent": dir_manager.get_consent_info(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to grant consent: {str(e)}")


@router.delete("/")
def revoke_consent(request: ConsentRevokeRequest):
    """
    Revoke privacy consent for LLM data access and/or directory access.
    
    - **consent_type**: Type of consent to revoke ('llm', 'directory', or 'all')
    
    Returns consent status after revoking.
    """
    llm_manager = LLMConsentManager()
    dir_manager = DirectoryConsentManager()
    
    try:
        if request.consent_type in ("llm", "all"):
            llm_manager.revoke()
        
        if request.consent_type in ("directory", "all"):
            dir_manager.revoke()
        
        return {
            "status": "ok",
            "message": f"Successfully revoked {request.consent_type} consent",
            "llm_consent": llm_manager.get_consent_info(),
            "directory_consent": dir_manager.get_consent_info(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to revoke consent: {str(e)}")


@router.get("/")
def get_consent_status():
    """
    Get current privacy consent status for both LLM and directory access.
    
    Returns detailed information about all consent types.
    """
    llm_manager = LLMConsentManager()
    dir_manager = DirectoryConsentManager()
    
    return {
        "status": "ok",
        "llm_consent": llm_manager.get_consent_info(),
        "directory_consent": dir_manager.get_consent_info(),
        "has_all_consents": llm_manager.has_consent() and dir_manager.has_consent(),
    }


@router.get("/llm")
def get_llm_consent_status():
    """
    Get current LLM consent status.
    
    Returns detailed information about LLM data access consent.
    """
    llm_manager = LLMConsentManager()
    return llm_manager.get_consent_info()


@router.get("/directory")
def get_directory_consent_status():
    """
    Get current directory consent status.
    
    Returns detailed information about directory access consent, including allowed paths.
    """
    dir_manager = DirectoryConsentManager()
    return dir_manager.get_consent_info()


@router.post("/reset")
def reset_all_consents():
    """
    Reset all consents to their default (revoked) state.
    
    This is useful for testing or when users want to start fresh.
    """
    llm_manager = LLMConsentManager()
    dir_manager = DirectoryConsentManager()
    
    try:
        llm_manager.reset()
        dir_manager.reset()
        
        return {
            "status": "ok",
            "message": "Successfully reset all consents to default state",
            "llm_consent": llm_manager.get_consent_info(),
            "directory_consent": dir_manager.get_consent_info(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset consents: {str(e)}")


@router.patch("/directory/paths")
def update_allowed_paths(allowed_paths: List[str] = Field(..., description="List of allowed directory paths")):
    """
    Update the list of allowed directory paths without changing consent status.
    
    - **allowed_paths**: New list of directory paths to allow
    
    Note: This only works if directory consent has already been granted.
    """
    dir_manager = DirectoryConsentManager()
    
    if not dir_manager.has_consent():
        raise HTTPException(
            status_code=400,
            detail="Directory consent must be granted before updating allowed paths"
        )
    
    try:
        # Re-grant with new paths
        dir_manager.grant(allowed_paths=allowed_paths)
        return {
            "status": "ok",
            "message": "Successfully updated allowed paths",
            "directory_consent": dir_manager.get_consent_info(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update paths: {str(e)}")
