"""
DeepGuard Multi-Agentic System - FastAPI Backend
REST API for deepfake detection with real-time agent transparency
"""

import os
import uuid
import logging
from typing import Dict, Any
from datetime import datetime
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import aiofiles

from core.orchestrator import get_orchestrator
from core.state import MediaType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="DeepGuard API",
    description="Multi-Agentic Deepfake Detection System with RAI Guardrails",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory
UPLOAD_DIR = "/home/claude/deepguard/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory="/home/claude/deepguard/static"), name="static")


class AnalysisRequest(BaseModel):
    """Request model for media analysis"""
    media_id: str
    media_type: str


class AnalysisResponse(BaseModel):
    """Response model for analysis results"""
    success: bool
    session_id: str
    results: Dict[str, Any]
    message: str


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "DeepGuard Multi-Agentic Deepfake Detection",
        "version": "1.0.0",
        "status": "operational",
        "rai_principles": [
            "Fairness",
            "Accountability",
            "Transparency",
            "Privacy",
            "Robustness",
            "Non-Maleficence"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "agents_available": 8
    }


@app.post("/api/upload", response_model=Dict[str, Any])
async def upload_media(file: UploadFile = File(...)):
    """
    Upload media file for deepfake detection
    
    Args:
        file: Media file (image, video, or audio)
    
    Returns:
        Upload confirmation with media_id
    """
    try:
        # Validate file type
        allowed_extensions = {
            'image': ['.jpg', '.jpeg', '.png', '.bmp', '.webp'],
            'video': ['.mp4', '.avi', '.mov', '.mkv', '.webm'],
            'audio': ['.mp3', '.wav', '.ogg', '.m4a']
        }
        
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        # Determine media type
        media_type = None
        for mtype, extensions in allowed_extensions.items():
            if file_ext in extensions:
                media_type = mtype
                break
        
        if not media_type:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_ext}"
            )
        
        # Generate unique media ID
        media_id = str(uuid.uuid4())
        
        # Save file
        file_path = os.path.join(UPLOAD_DIR, f"{media_id}{file_ext}")
        
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        logger.info(f"Uploaded {media_type} file: {media_id}")
        
        return {
            "success": True,
            "media_id": media_id,
            "media_type": media_type,
            "filename": file.filename,
            "file_size": len(content),
            "message": "Media uploaded successfully"
        }
    
    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_media(request: AnalysisRequest):
    """
    Analyze uploaded media for deepfake detection
    
    Args:
        request: Analysis request with media_id and media_type
    
    Returns:
        Complete analysis results from all agents
    """
    try:
        # Find uploaded file
        media_files = [
            f for f in os.listdir(UPLOAD_DIR)
            if f.startswith(request.media_id)
        ]
        
        if not media_files:
            raise HTTPException(
                status_code=404,
                detail=f"Media not found: {request.media_id}"
            )
        
        media_path = os.path.join(UPLOAD_DIR, media_files[0])
        session_id = str(uuid.uuid4())
        
        logger.info(f"Starting analysis for {request.media_id}")
        
        # Get orchestrator and run analysis
        orchestrator = get_orchestrator()
        
        final_state = orchestrator.analyze_media(
            media_id=request.media_id,
            media_type=request.media_type,
            media_path=media_path,
            session_id=session_id
        )
        
        # Format results for UI
        results = orchestrator.get_state_for_ui(final_state)
        
        logger.info(f"Analysis complete for {request.media_id}")
        
        return AnalysisResponse(
            success=True,
            session_id=session_id,
            results=results,
            message="Analysis completed successfully"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/session/{session_id}")
async def get_session_results(session_id: str):
    """
    Retrieve analysis results for a specific session
    
    Args:
        session_id: Session identifier
    
    Returns:
        Session analysis results
    """
    # In production: Retrieve from database
    # For now, return placeholder
    return {
        "session_id": session_id,
        "status": "completed",
        "message": "Session results would be retrieved from persistent storage"
    }


@app.get("/api/agents/status")
async def get_agents_status():
    """
    Get status of all DeepGuard agents
    
    Returns:
        Agent availability and configuration
    """
    orchestrator = get_orchestrator()
    
    return {
        "agents": [
            {
                "name": config["name"],
                "type": agent_type,
                "enabled": config["enabled"],
                "confidence_threshold": config["confidence_threshold"],
                "rai_principles": config["rai_principles"],
                "requires_gpu": config["requires_gpu"]
            }
            for agent_type, config in orchestrator.agent_configs.items()
        ],
        "total_agents": len(orchestrator.agent_configs),
        "active_agents": sum(
            1 for c in orchestrator.agent_configs.values() if c["enabled"]
        )
    }


@app.get("/api/rai/principles")
async def get_rai_principles():
    """
    Get Responsible AI principles implemented in DeepGuard
    
    Returns:
        RAI principles with descriptions
    """
    return {
        "principles": [
            {
                "name": "Fairness",
                "description": "Demographic bias testing across gender, age, ethnicity & skin tone to ensure equitable detection accuracy for all.",
                "agents": ["Bias Auditor Agent"]
            },
            {
                "name": "Accountability",
                "description": "Immutable audit logs, agent-level traceability, and clear escalation paths to human reviewers for every high-stakes decision.",
                "agents": ["Governance & Compliance Agent", "Report Generation Agent"]
            },
            {
                "name": "Transparency",
                "description": "Grad-CAM & SHAP explanations convert black-box verdicts into interpretable evidence for journalists, judges, and policymakers.",
                "agents": ["Explainability Agent"]
            },
            {
                "name": "Privacy",
                "description": "Minimal biometric retention, GDPR-aligned data handling, and anonymization of all test subjects throughout the pipeline.",
                "agents": ["Provenance Verification Agent"]
            },
            {
                "name": "Robustness",
                "description": "Adversarial deepfake testing, confidence gating before action, and dynamic adaptation to evolving forgery techniques.",
                "agents": ["Visual Forensics Agent", "Audio Analysis Agent"]
            },
            {
                "name": "Non-Maleficence",
                "description": "Mandatory human-in-the-loop for political, legal, and NCII detections. No automated action without verified confidence threshold.",
                "agents": ["Governance & Compliance Agent"]
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
