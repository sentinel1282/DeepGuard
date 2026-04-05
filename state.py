"""
DeepGuard Multi-Agentic System - State Management
Core state graph and agent communication structures
"""

from typing import TypedDict, List, Dict, Any, Optional, Annotated
from datetime import datetime
from enum import Enum
import operator


class MediaType(str, Enum):
    """Supported media types for deepfake detection"""
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"


class DetectionVerdict(str, Enum):
    """Final detection verdicts"""
    AUTHENTIC = "authentic"
    DEEPFAKE = "deepfake"
    SUSPICIOUS = "suspicious"
    REQUIRES_HUMAN_REVIEW = "requires_human_review"


class RAIPrinciple(str, Enum):
    """Responsible AI Principles"""
    FAIRNESS = "fairness"
    ACCOUNTABILITY = "accountability"
    TRANSPARENCY = "transparency"
    PRIVACY = "privacy"
    ROBUSTNESS = "robustness"
    NON_MALEFICENCE = "non_maleficence"


class AgentLog(TypedDict):
    """Individual agent activity log"""
    agent_name: str
    timestamp: str
    action: str
    findings: Dict[str, Any]
    confidence: float
    execution_time_ms: float
    rai_flags: List[str]


class BiasMetrics(TypedDict):
    """Demographic bias analysis metrics"""
    demographic_group: str
    false_positive_rate: float
    false_negative_rate: float
    accuracy: float
    confidence_distribution: List[float]


class ExplanationOutput(TypedDict):
    """Explainability outputs from XAI methods"""
    method: str  # grad_cam, shap, lime
    visualization_path: Optional[str]
    feature_importance: Dict[str, float]
    natural_language_explanation: str
    technical_details: Dict[str, Any]


class GovernanceAlert(TypedDict):
    """Alerts from governance and compliance agent"""
    severity: str  # low, medium, high, critical
    principle_violated: RAIPrinciple
    description: str
    recommended_action: str
    requires_human_review: bool


class DeepGuardState(TypedDict):
    """
    Central state graph for DeepGuard multi-agent system
    Tracks all agent activities, findings, and RAI compliance
    """
    # Input Media
    media_id: str
    media_type: MediaType
    media_path: str
    media_metadata: Dict[str, Any]
    
    # Agent Orchestration
    active_agents: List[str]
    completed_agents: List[str]
    current_agent: Optional[str]
    agent_logs: Annotated[List[AgentLog], operator.add]
    
    # Detection Findings
    visual_forensics_score: float
    audio_analysis_score: float
    provenance_authenticity: Dict[str, Any]
    manipulation_indicators: Annotated[List[str], operator.add]
    
    # RAI Compliance
    bias_metrics: List[BiasMetrics]
    fairness_flags: Annotated[List[str], operator.add]
    governance_alerts: Annotated[List[GovernanceAlert], operator.add]
    privacy_compliant: bool
    
    # Explainability
    explanations: Annotated[List[ExplanationOutput], operator.add]
    grad_cam_outputs: List[str]
    shap_values: Optional[Dict[str, Any]]
    
    # Final Verdict
    overall_confidence: float
    final_verdict: Optional[DetectionVerdict]
    human_review_required: bool
    human_review_reason: Optional[str]
    
    # Audit Trail
    session_id: str
    start_time: str
    end_time: Optional[str]
    total_processing_time_ms: float
    
    # Report Generation
    report_ready: bool
    report_path: Optional[str]


def create_initial_state(
    media_id: str,
    media_type: MediaType,
    media_path: str,
    session_id: str
) -> DeepGuardState:
    """Initialize DeepGuard state for new media analysis"""
    
    return DeepGuardState(
        media_id=media_id,
        media_type=media_type,
        media_path=media_path,
        media_metadata={},
        active_agents=[],
        completed_agents=[],
        current_agent=None,
        agent_logs=[],
        visual_forensics_score=0.0,
        audio_analysis_score=0.0,
        provenance_authenticity={},
        manipulation_indicators=[],
        bias_metrics=[],
        fairness_flags=[],
        governance_alerts=[],
        privacy_compliant=True,
        explanations=[],
        grad_cam_outputs=[],
        shap_values=None,
        overall_confidence=0.0,
        final_verdict=None,
        human_review_required=False,
        human_review_reason=None,
        session_id=session_id,
        start_time=datetime.now().isoformat(),
        end_time=None,
        total_processing_time_ms=0.0,
        report_ready=False,
        report_path=None
    )


class AgentConfig(TypedDict):
    """Configuration for individual agents"""
    name: str
    enabled: bool
    confidence_threshold: float
    timeout_seconds: int
    rai_principles: List[RAIPrinciple]
    requires_gpu: bool
