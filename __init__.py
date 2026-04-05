"""
DeepGuard Multi-Agentic Deepfake Detection System
Core module initialization
"""

__version__ = "1.0.0"
__author__ = "DeepGuard Team - AAI-531"

from .state import (
    DeepGuardState,
    MediaType,
    DetectionVerdict,
    RAIPrinciple,
    create_initial_state
)

from .agents import (
    BaseAgent,
    OrchestratorAgent,
    VisualForensicsAgent,
    AudioAnalysisAgent,
    ProvenanceVerificationAgent,
    BiasAuditorAgent,
    ExplainabilityAgent,
    GovernanceComplianceAgent,
    ReportGenerationAgent,
    create_agent
)

from .orchestrator import (
    DeepGuardOrchestrator,
    get_orchestrator
)

__all__ = [
    "DeepGuardState",
    "MediaType",
    "DetectionVerdict",
    "RAIPrinciple",
    "create_initial_state",
    "BaseAgent",
    "OrchestratorAgent",
    "VisualForensicsAgent",
    "AudioAnalysisAgent",
    "ProvenanceVerificationAgent",
    "BiasAuditorAgent",
    "ExplainabilityAgent",
    "GovernanceComplianceAgent",
    "ReportGenerationAgent",
    "create_agent",
    "DeepGuardOrchestrator",
    "get_orchestrator"
]
