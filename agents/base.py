"""
Base Agent — Abstract interface for all agents in the system.

Every agent follows a consistent lifecycle:
  IDLE → RUNNING → COMPLETE (or ERROR)

Each agent receives input, processes it, logs its actions,
and returns structured output for the next agent in the pipeline.
"""

import time
from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, name: str, icon: str, description: str):
        self.name = name
        self.icon = icon
        self.description = description
        self.status = "idle"  # idle | running | complete | error
        self.execution_time = 0.0
        self.result = None
        self.error = None
        self._logs = []

    @abstractmethod
    def process(self, input_data: Any, context: dict) -> dict:
        """Core processing logic. Must be implemented by each agent."""
        pass

    def execute(self, input_data: Any, context: dict) -> dict:
        """Execute the agent with timing and status tracking."""
        self.status = "running"
        self._logs = []
        self.error = None
        start = time.time()

        try:
            self.result = self.process(input_data, context)
            self.status = "complete"
        except Exception as e:
            self.status = "error"
            self.error = str(e)
            self.result = {"error": str(e)}
        finally:
            self.execution_time = round(time.time() - start, 2)

        return self.result

    def add_log(self, message: str):
        """Add a processing log entry."""
        self._logs.append(message)

    @property
    def logs(self) -> list[str]:
        return self._logs.copy()

    def reset(self):
        """Reset agent to idle state."""
        self.status = "idle"
        self.execution_time = 0.0
        self.result = None
        self.error = None
        self._logs = []

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "icon": self.icon,
            "description": self.description,
            "status": self.status,
            "execution_time": self.execution_time,
            "logs": self._logs,
            "error": self.error,
        }
