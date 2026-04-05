"""
DeepGuard Multi-Agentic System - LangGraph Orchestration
Coordinates agent workflow using LangGraph StateGraph
"""

import logging
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage

from core.state import DeepGuardState, MediaType, AgentConfig, create_initial_state
from core.agents import create_agent

logger = logging.getLogger(__name__)


class DeepGuardOrchestrator:
    """
    LangGraph-based orchestration for DeepGuard multi-agent system
    Manages conditional routing, human-in-the-loop checkpoints
    """
    
    def __init__(self):
        self.graph = self._build_graph()
        self.agent_configs = self._initialize_agent_configs()
    
    def _initialize_agent_configs(self) -> Dict[str, AgentConfig]:
        """Initialize configuration for all agents"""
        return {
            "orchestrator": AgentConfig(
                name="Orchestrator Agent",
                enabled=True,
                confidence_threshold=0.0,
                timeout_seconds=30,
                rai_principles=[],
                requires_gpu=False
            ),
            "visual_forensics": AgentConfig(
                name="Visual Forensics Agent",
                enabled=True,
                confidence_threshold=0.7,
                timeout_seconds=120,
                rai_principles=["fairness", "robustness"],
                requires_gpu=True
            ),
            "audio_analysis": AgentConfig(
                name="Audio Analysis Agent",
                enabled=True,
                confidence_threshold=0.7,
                timeout_seconds=90,
                rai_principles=["robustness"],
                requires_gpu=False
            ),
            "provenance_verification": AgentConfig(
                name="Provenance Verification Agent",
                enabled=True,
                confidence_threshold=0.6,
                timeout_seconds=60,
                rai_principles=["accountability", "privacy"],
                requires_gpu=False
            ),
            "bias_auditor": AgentConfig(
                name="Bias Auditor Agent",
                enabled=True,
                confidence_threshold=0.9,
                timeout_seconds=45,
                rai_principles=["fairness"],
                requires_gpu=False
            ),
            "explainability": AgentConfig(
                name="Explainability Agent",
                enabled=True,
                confidence_threshold=0.85,
                timeout_seconds=60,
                rai_principles=["transparency"],
                requires_gpu=True
            ),
            "governance_compliance": AgentConfig(
                name="Governance & Compliance Agent",
                enabled=True,
                confidence_threshold=0.95,
                timeout_seconds=30,
                rai_principles=["accountability", "non_maleficence"],
                requires_gpu=False
            ),
            "report_generation": AgentConfig(
                name="Report Generation Agent",
                enabled=True,
                confidence_threshold=1.0,
                timeout_seconds=45,
                rai_principles=["transparency", "accountability"],
                requires_gpu=False
            )
        }
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph state graph for agent coordination"""
        
        # Create state graph
        workflow = StateGraph(DeepGuardState)
        
        # Add nodes for each agent
        workflow.add_node("orchestrator", self._orchestrator_node)
        workflow.add_node("visual_forensics", self._visual_forensics_node)
        workflow.add_node("audio_analysis", self._audio_analysis_node)
        workflow.add_node("provenance_verification", self._provenance_node)
        workflow.add_node("bias_auditor", self._bias_auditor_node)
        workflow.add_node("explainability", self._explainability_node)
        workflow.add_node("governance_compliance", self._governance_node)
        workflow.add_node("report_generation", self._report_generation_node)
        
        # Define workflow edges
        workflow.set_entry_point("orchestrator")
        
        # Orchestrator routes to appropriate agents based on media type
        workflow.add_conditional_edges(
            "orchestrator",
            self._route_after_orchestrator,
            {
                "visual_forensics": "visual_forensics",
                "audio_analysis": "audio_analysis",
                "end": END
            }
        )
        
        # Visual forensics -> Provenance verification
        workflow.add_edge("visual_forensics", "provenance_verification")
        
        # Audio analysis -> Provenance verification
        workflow.add_edge("audio_analysis", "provenance_verification")
        
        # Provenance -> Bias Auditor
        workflow.add_edge("provenance_verification", "bias_auditor")
        
        # Bias Auditor -> Explainability
        workflow.add_edge("bias_auditor", "explainability")
        
        # Explainability -> Governance
        workflow.add_edge("explainability", "governance_compliance")
        
        # Governance -> Report Generation or Human Review
        workflow.add_conditional_edges(
            "governance_compliance",
            self._check_human_review_required,
            {
                "report": "report_generation",
                "human_review": END  # Pause for human review
            }
        )
        
        # Report Generation -> End
        workflow.add_edge("report_generation", END)
        
        return workflow.compile()
    
    def _orchestrator_node(self, state: DeepGuardState) -> DeepGuardState:
        """Execute orchestrator agent"""
        agent = create_agent("orchestrator", self.agent_configs["orchestrator"])
        return agent.process(state)
    
    def _visual_forensics_node(self, state: DeepGuardState) -> DeepGuardState:
        """Execute visual forensics agent"""
        agent = create_agent("visual_forensics", self.agent_configs["visual_forensics"])
        return agent.process(state)
    
    def _audio_analysis_node(self, state: DeepGuardState) -> DeepGuardState:
        """Execute audio analysis agent"""
        agent = create_agent("audio_analysis", self.agent_configs["audio_analysis"])
        return agent.process(state)
    
    def _provenance_node(self, state: DeepGuardState) -> DeepGuardState:
        """Execute provenance verification agent"""
        agent = create_agent("provenance_verification", self.agent_configs["provenance_verification"])
        return agent.process(state)
    
    def _bias_auditor_node(self, state: DeepGuardState) -> DeepGuardState:
        """Execute bias auditor agent"""
        agent = create_agent("bias_auditor", self.agent_configs["bias_auditor"])
        return agent.process(state)
    
    def _explainability_node(self, state: DeepGuardState) -> DeepGuardState:
        """Execute explainability agent"""
        agent = create_agent("explainability", self.agent_configs["explainability"])
        return agent.process(state)
    
    def _governance_node(self, state: DeepGuardState) -> DeepGuardState:
        """Execute governance & compliance agent"""
        agent = create_agent("governance_compliance", self.agent_configs["governance_compliance"])
        return agent.process(state)
    
    def _report_generation_node(self, state: DeepGuardState) -> DeepGuardState:
        """Execute report generation agent"""
        agent = create_agent("report_generation", self.agent_configs["report_generation"])
        return agent.process(state)
    
    def _route_after_orchestrator(self, state: DeepGuardState) -> str:
        """Route to appropriate agent based on media type"""
        media_type = state["media_type"]
        
        if media_type == MediaType.IMAGE:
            return "visual_forensics"
        elif media_type == MediaType.VIDEO:
            return "visual_forensics"  # Video includes visual analysis
        elif media_type == MediaType.AUDIO:
            return "audio_analysis"
        else:
            return "end"
    
    def _check_human_review_required(self, state: DeepGuardState) -> str:
        """Check if human review is required before final report"""
        if state.get("human_review_required", False):
            logger.info(f"Human review required: {state.get('human_review_reason')}")
            return "human_review"
        return "report"
    
    def analyze_media(
        self,
        media_id: str,
        media_type: str,
        media_path: str,
        session_id: str
    ) -> DeepGuardState:
        """
        Main entry point for deepfake detection
        
        Args:
            media_id: Unique identifier for media
            media_type: Type of media (image/video/audio)
            media_path: Path to media file
            session_id: Session identifier for audit trail
        
        Returns:
            Final DeepGuardState with detection results
        """
        logger.info(f"Starting DeepGuard analysis for {media_id}")
        
        # Create initial state
        initial_state = create_initial_state(
            media_id=media_id,
            media_type=MediaType(media_type),
            media_path=media_path,
            session_id=session_id
        )
        
        # Execute graph
        final_state = self.graph.invoke(initial_state)
        
        logger.info(f"DeepGuard analysis complete for {media_id}")
        logger.info(f"Final verdict: {final_state.get('final_verdict')}")
        logger.info(f"Overall confidence: {final_state.get('overall_confidence'):.2%}")
        
        return final_state
    
    def get_state_for_ui(self, state: DeepGuardState) -> Dict[str, Any]:
        """Format state for UI consumption"""
        return {
            "sessionId": state["session_id"],
            "mediaId": state["media_id"],
            "mediaType": state["media_type"],
            "finalVerdict": state.get("final_verdict"),
            "overallConfidence": state.get("overall_confidence", 0.0),
            "humanReviewRequired": state.get("human_review_required", False),
            "humanReviewReason": state.get("human_review_reason"),
            "agentLogs": [
                {
                    "agentName": log["agent_name"],
                    "timestamp": log["timestamp"],
                    "action": log["action"],
                    "confidence": log["confidence"],
                    "executionTimeMs": log["execution_time_ms"],
                    "raiFlags": log.get("rai_flags", [])
                }
                for log in state.get("agent_logs", [])
            ],
            "manipulationIndicators": state.get("manipulation_indicators", []),
            "fairnessFlags": state.get("fairness_flags", []),
            "governanceAlerts": [
                {
                    "severity": alert["severity"],
                    "principle": alert["principle_violated"],
                    "description": alert["description"],
                    "action": alert["recommended_action"]
                }
                for alert in state.get("governance_alerts", [])
            ],
            "biasMetrics": state.get("bias_metrics", []),
            "explanations": state.get("explanations", []),
            "processingTimeMs": state.get("total_processing_time_ms", 0.0),
            "reportReady": state.get("report_ready", False)
        }


# Singleton instance
_orchestrator = None

def get_orchestrator() -> DeepGuardOrchestrator:
    """Get or create orchestrator instance"""
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = DeepGuardOrchestrator()
    return _orchestrator
