"""
Shared Workflow State — FlowMind AI

Defines the core data structure that flows through the entire
multi-agent pipeline. Each agent reads from and writes to this
shared state, ensuring a consistent contract across all stages:

    Extraction → Intelligence → Execution → Tracking → Decision
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class WorkflowState:
    """
    Central state container for the FlowMind AI pipeline.

    Attributes:
        input_text:         Raw text input (from user or uploaded file).
        extracted:          Structured data from the Extraction Agent
                            (action items, decisions, owners, deadlines, blockers).
        intelligence:       Risk and dependency analysis from the Intelligence Agent
                            (risks, missing owners, overloaded owners, dependencies).
        execution_results:  Structured task objects from the Execution Agent
                            (task list with IDs, priorities, risk flags).
        tracking_data:      Time simulation results from the Tracking Agent
                            (day snapshots, issues, status stats).
        decisions:          Autonomous actions from the Decision Agent
                            (auto-assignments, escalations, reminders).
        tasks:              The current canonical task list (updated by each agent).
        current_day:        The current simulation day (1–3).
        pipeline_status:    Pipeline lifecycle state (idle | running | complete | error).
        current_agent:      Name of the currently executing agent (or None).
    """

    # ── Input ────────────────────────────────────────
    input_text: Optional[str] = None

    # ── Agent Outputs ────────────────────────────────
    extracted: Optional[dict] = None
    intelligence: Optional[dict] = None
    execution_results: Optional[dict] = None
    tracking_data: Optional[dict] = None
    decisions: Optional[dict] = None

    # ── Canonical Task List ──────────────────────────
    tasks: list = field(default_factory=list)

    # ── Pipeline Metadata ────────────────────────────
    current_day: int = 1
    pipeline_status: str = "idle"       # idle | running | complete | error
    current_agent: Optional[str] = None

    def to_dict(self) -> dict:
        """Serialize state to a plain dictionary (for JSON export / session storage)."""
        return {
            "input_text": self.input_text,
            "extracted": self.extracted,
            "intelligence": self.intelligence,
            "execution_results": self.execution_results,
            "tracking_data": self.tracking_data,
            "decisions": self.decisions,
            "tasks": self.tasks,
            "current_day": self.current_day,
            "pipeline_status": self.pipeline_status,
            "current_agent": self.current_agent,
        }

    def reset(self):
        """Reset all fields to initial state."""
        self.input_text = None
        self.extracted = None
        self.intelligence = None
        self.execution_results = None
        self.tracking_data = None
        self.decisions = None
        self.tasks = []
        self.current_day = 1
        self.pipeline_status = "idle"
        self.current_agent = None
