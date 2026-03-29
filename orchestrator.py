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
            # Safe read: execution result may be None or missing "tasks" if the agent
            # failed/returned partial data. Fall back to the existing task list.
            self.state["tasks"] = (
                self.state["execution"].get("tasks")
                if isinstance(self.state.get("execution"), dict)
                else None
            ) or self.state["tasks"]

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
            # Safe read: tracking result may be None or missing "tasks".
            # Fall back to the task list produced by the execution agent.
            self.state["tasks"] = (
                self.state["tracking"].get("tasks")
                if isinstance(self.state.get("tracking"), dict)
                else None
            ) or self.state["tasks"]
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
            # Safe read (three-level fallback):
            #   1. decision["tasks"]   — preferred: decision agent applied corrections
            #   2. tracking["tasks"]   — fallback: pre-decision task state
            #   3. state["tasks"]      — last resort: whatever we had before this step
            decision_result = self.state.get("decision")
            tracking_result = self.state.get("tracking")
            self.state["tasks"] = (
                (decision_result.get("tasks") if isinstance(decision_result, dict) else None)
                or (tracking_result.get("tasks") if isinstance(tracking_result, dict) else None)
                or self.state["tasks"]
            )

            # Complete
            self.state["pipeline_status"] = "complete"
            self.state["current_agent"] = None

            self.audit_logger.log(
                "Orchestrator",
                "Pipeline complete — All agents executed successfully",
                f"Processed {len(self.state['tasks'])} tasks. "
                f"Day 1 simulation complete. "
                f"{len((self.state.get('decision') or {}).get('actions_taken', []))} autonomous actions taken. "
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
        """Run time simulation for a specific day.

        Safe by design: never assumes that any prior agent result exists or
        contains the expected keys. Falls back gracefully at every step so
        the app never crashes when the user jumps between days or triggers
        simulation before the full pipeline has finished.
        """
        # Guard: pipeline must have at least produced an execution result
        # (tasks to re-simulate). Without it there is nothing to work with.
        execution_result = self.state.get("execution")
        if not isinstance(execution_result, dict):
            # Pipeline hasn't run far enough — return current state unchanged.
            return self.state

        ctx = self.get_context()

        # Safely pull the baseline task list produced by the execution agent.
        # Fall back to the current state tasks if the key is absent.
        original_tasks = deepcopy(
            execution_result.get("tasks") or self.state.get("tasks") or []
        )

        self.audit_logger.log(
            "Orchestrator",
            f"Time simulation: Advancing to Day {day}",
            f"Re-running tracking and decision agents for Day {day} scenario.",
        )

        # Reset tracking and decision agents for a clean simulation run
        self.agents["tracking"].reset()
        self.agents["decision"].reset()

        # --- Tracking agent ---
        self.state["current_agent"] = "tracking"
        tracking_result = self.agents["tracking"].execute(
            {"tasks": original_tasks, "day": day},
            ctx,
        )
        self.state["tracking"] = tracking_result

        # Safe read: tracking may return None or omit "tasks" on failure.
        # Keep original tasks as the fallback so the UI always has data.
        tracking_tasks = (
            tracking_result.get("tasks")
            if isinstance(tracking_result, dict)
            else None
        )
        self.state["tasks"] = tracking_tasks or original_tasks

        # --- Decision agent ---
        self.state["current_agent"] = "decision"
        decision_result = self.agents["decision"].execute(
            {
                "tasks": self.state["tasks"],
                # Safe read: "issues" may be absent from tracking result
                "issues": (tracking_result or {}).get("issues", []),
                "intelligence": self.state.get("intelligence"),
                "day": day,
            },
            ctx,
        )
        self.state["decision"] = decision_result

        # Three-level fallback for tasks after the decision agent:
        #   1. decision["tasks"]   — preferred: corrective actions applied
        #   2. tracking["tasks"]   — fallback: pre-decision task state
        #   3. state["tasks"]      — last resort: whatever existed before this call
        decision_tasks = (
            decision_result.get("tasks")
            if isinstance(decision_result, dict)
            else None
        )
        self.state["tasks"] = (
            decision_tasks
            or tracking_tasks
            or self.state["tasks"]
        )

        self.state["current_day"] = day
        self.state["current_agent"] = None

        # Safe reads for audit log counters — default to 0 if keys are missing
        issue_count = len((tracking_result or {}).get("issues", []))
        action_count = len((decision_result or {}).get("actions_taken", []))
        self.audit_logger.log(
            "Orchestrator",
            f"Day {day} simulation complete",
            f"Tasks updated. Issues: {issue_count}. Actions: {action_count}.",
        )

        return self.state
