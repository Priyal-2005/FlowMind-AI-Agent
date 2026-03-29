"""
Orchestrator Agent — Central Workflow Controller

The brain of the multi-agent system. Manages:
- Global state across all agents
- Pipeline routing (Extraction → Intelligence → Execution → Tracking → Decision)
- Step-by-step execution with UI callback support
- Error handling and graceful degradation
- Session state persistence for Streamlit
"""

import time
from typing import Optional, Generator
from copy import deepcopy

from dotenv import load_dotenv
load_dotenv()

from utils.llm import LLMClient
from utils.logger import AuditLogger
from agents.extraction import ExtractionAgent
from agents.intelligence import IntelligenceAgent
from agents.execution import ExecutionAgent
from agents.tracking import TrackingAgent
from agents.decision import DecisionAgent


class MeetingOrchestrator:
    """Central orchestrator for the autonomous meeting workflow system."""

    def __init__(self):
        self.llm = LLMClient()
        self.audit_logger = AuditLogger()

        # Initialize all agents
        self.agents = {
            "extraction": ExtractionAgent(),
            "intelligence": IntelligenceAgent(),
            "execution": ExecutionAgent(),
            "tracking": TrackingAgent(),
            "decision": DecisionAgent(),
        }

        # Pipeline state
        self.state = {
            "transcript": None,
            "extracted": None,
            "intelligence": None,
            "execution": None,
            "tracking": None,
            "decision": None,
            "current_day": 1,
            "pipeline_status": "idle",  # idle | running | complete | error
            "current_agent": None,
            "tasks": [],
        }

    @property
    def agent_list(self) -> list:
        """Return ordered list of agents for pipeline display."""
        return [
            self.agents["extraction"],
            self.agents["intelligence"],
            self.agents["execution"],
            self.agents["tracking"],
            self.agents["decision"],
        ]

    def get_context(self) -> dict:
        """Build shared context for agents."""
        return {
            "llm": self.llm,
            "logger": self.audit_logger,
        }

    def reset(self):
        """Reset all state and agents."""
        self.audit_logger.clear()
        for agent in self.agents.values():
            agent.reset()
        self.state = {
            "transcript": None,
            "extracted": None,
            "intelligence": None,
            "execution": None,
            "tracking": None,
            "decision": None,
            "current_day": 1,
            "pipeline_status": "idle",
            "current_agent": None,
            "tasks": [],
        }

    def run_pipeline(self, transcript: str) -> dict:
        """
        Execute the full agent pipeline synchronously.
        Returns complete state after all agents have executed.
        """
        self.reset()
        self.state["transcript"] = transcript
        self.state["pipeline_status"] = "running"

        ctx = self.get_context()

        self.audit_logger.log(
            "Orchestrator",
            "Pipeline initiated — Processing meeting transcript",
            f"Starting autonomous workflow pipeline with {len(self.agents)} agents. "
            f"LLM mode: {self.llm.mode}. Transcript length: {len(transcript)} chars.",
        )

        try:
            # Step 1: Extraction
            self.state["current_agent"] = "extraction"
            self.audit_logger.log(
                "Orchestrator",
                "Routing to Extraction Agent",
                "First stage: Parse raw transcript into structured data",
            )
            self.state["extracted"] = self.agents["extraction"].execute(transcript, ctx)

            # Step 2: Intelligence
            self.state["current_agent"] = "intelligence"
            self.audit_logger.log(
                "Orchestrator",
                "Routing to Intelligence Agent",
                "Second stage: Analyze extracted data for risks and gaps",
            )
            self.state["intelligence"] = self.agents["intelligence"].execute(
                self.state["extracted"], ctx
            )

            # Step 3: Execution
            self.state["current_agent"] = "execution"
            self.audit_logger.log(
                "Orchestrator",
                "Routing to Execution Agent",
                "Third stage: Create structured executable tasks",
            )
            self.state["execution"] = self.agents["execution"].execute(
                {
                    "extracted": self.state["extracted"],
                    "intelligence": self.state["intelligence"],
                },
                ctx,
            )
            self.state["tasks"] = self.state["execution"]["tasks"]

            # Step 4: Tracking (Day 1 by default)
            self.state["current_agent"] = "tracking"
            self.audit_logger.log(
                "Orchestrator",
                "Routing to Tracking Agent — Day 1 simulation",
                "Fourth stage: Simulate Day 1 task progression",
            )
            self.state["tracking"] = self.agents["tracking"].execute(
                {"tasks": self.state["tasks"], "day": 1},
                ctx,
            )
            self.state["tasks"] = self.state["tracking"]["tasks"]
            self.state["current_day"] = 1

            # Step 5: Decision
            self.state["current_agent"] = "decision"
            self.audit_logger.log(
                "Orchestrator",
                "Routing to Decision Agent — Autonomous action engine",
                "Fifth stage: Take autonomous corrective actions based on detected issues",
            )
            self.state["decision"] = self.agents["decision"].execute(
                {
                    "tasks": self.state["tasks"],
                    "issues": self.state["tracking"].get("issues", []),
                    "intelligence": self.state["intelligence"],
                    "day": self.state["current_day"],
                },
                ctx,
            )
            self.state["tasks"] = self.state["decision"]["tasks"]

            # Complete
            self.state["pipeline_status"] = "complete"
            self.state["current_agent"] = None

            self.audit_logger.log(
                "Orchestrator",
                "Pipeline complete — All agents executed successfully",
                f"Processed {len(self.state['tasks'])} tasks. "
                f"Day 1 simulation complete. "
                f"{len(self.state['decision'].get('actions_taken', []))} autonomous actions taken. "
                f"System ready for time simulation.",
            )

        except Exception as e:
            self.state["pipeline_status"] = "error"
            self.audit_logger.log(
                "Orchestrator",
                f"Pipeline error: {str(e)}",
                "An error occurred during agent execution. Partial results may be available.",
                severity="WARNING",
            )

        return self.state

    def simulate_day(self, day: int) -> dict:
        """Run time simulation for a specific day."""
        if not self.state.get("execution"):
            return self.state

        ctx = self.get_context()

        # Get original tasks from execution (pre-tracking)
        original_tasks = deepcopy(self.state["execution"]["tasks"])

        self.audit_logger.log(
            "Orchestrator",
            f"Time simulation: Advancing to Day {day}",
            f"Re-running tracking and decision agents for Day {day} scenario.",
        )

        # Reset tracking and decision agents
        self.agents["tracking"].reset()
        self.agents["decision"].reset()

        # Re-run tracking for the new day
        self.state["current_agent"] = "tracking"
        self.state["tracking"] = self.agents["tracking"].execute(
            {"tasks": original_tasks, "day": day},
            ctx,
        )
        self.state["tasks"] = self.state["tracking"]["tasks"]

        # Re-run decision agent
        self.state["current_agent"] = "decision"
        self.state["decision"] = self.agents["decision"].execute(
            {
                "tasks": self.state["tasks"],
                "issues": self.state["tracking"].get("issues", []),
                "intelligence": self.state["intelligence"],
                "day": day,
            },
            ctx,
        )
        self.state["tasks"] = self.state["decision"]["tasks"]
        self.state["current_day"] = day
        self.state["current_agent"] = None

        self.audit_logger.log(
            "Orchestrator",
            f"Day {day} simulation complete",
            f"Tasks updated. Issues: {len(self.state['tracking'].get('issues', []))}. "
            f"Actions: {len(self.state['decision'].get('actions_taken', []))}.",
        )

        return self.state
