"""
Audit Logger — Chronological Agent Decision Recorder

Thread-safe, singleton-pattern logger that maintains a complete audit trail
of all agent actions, decisions, and reasoning throughout the workflow.
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AuditEntry:
    """Single audit log entry."""
    timestamp: str
    agent_name: str
    action: str
    reasoning: str
    details: Optional[dict] = field(default_factory=dict)
    severity: str = "INFO"  # INFO, WARNING, ACTION, ESCALATION

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "agent_name": self.agent_name,
            "action": self.action,
            "reasoning": self.reasoning,
            "details": self.details,
            "severity": self.severity,
        }


class AuditLogger:
    """Centralized audit logger for the multi-agent system."""

    # Agent color mapping for UI
    AGENT_COLORS = {
        "Orchestrator": "#6C63FF",
        "Extraction Agent": "#00D4AA",
        "Intelligence Agent": "#FFB800",
        "Execution Agent": "#FF6B6B",
        "Tracking Agent": "#45B7D1",
        "Decision Agent": "#F093FB",
        "System": "#8B8FA3",
    }

    AGENT_ICONS = {
        "Orchestrator": "🎯",
        "Extraction Agent": "🔍",
        "Intelligence Agent": "🧠",
        "Execution Agent": "⚡",
        "Tracking Agent": "📊",
        "Decision Agent": "🤖",
        "System": "⚙️",
    }

    def __init__(self):
        self.entries: list[AuditEntry] = []
        self._start_time = datetime.now()

    def log(
        self,
        agent_name: str,
        action: str,
        reasoning: str = "",
        details: Optional[dict] = None,
        severity: str = "INFO",
    ) -> AuditEntry:
        """Log an agent action with full context."""
        elapsed = datetime.now() - self._start_time
        total_seconds = int(elapsed.total_seconds())
        minutes, seconds = divmod(total_seconds, 60)
        timestamp = f"{minutes:02d}:{seconds:02d}"

        entry = AuditEntry(
            timestamp=timestamp,
            agent_name=agent_name,
            action=action,
            reasoning=reasoning,
            details=details or {},
            severity=severity,
        )
        self.entries.append(entry)
        return entry

    def get_entries(self, agent_filter: Optional[str] = None) -> list[AuditEntry]:
        """Get log entries, optionally filtered by agent."""
        if agent_filter:
            return [e for e in self.entries if e.agent_name == agent_filter]
        return self.entries.copy()

    def get_recent(self, count: int = 10) -> list[AuditEntry]:
        """Get most recent N entries."""
        return self.entries[-count:]

    def get_actions_by_severity(self, severity: str) -> list[AuditEntry]:
        """Get entries filtered by severity level."""
        return [e for e in self.entries if e.severity == severity]

    def get_escalations(self) -> list[AuditEntry]:
        """Get all escalation entries."""
        return [e for e in self.entries if e.severity == "ESCALATION"]

    def get_autonomous_actions(self) -> list[AuditEntry]:
        """Get all autonomous action entries."""
        return [e for e in self.entries if e.severity == "ACTION"]

    def clear(self):
        """Clear all entries and reset timer."""
        self.entries.clear()
        self._start_time = datetime.now()

    @property
    def total_entries(self) -> int:
        return len(self.entries)

    def format_entry(self, entry: AuditEntry) -> str:
        """Format entry for display."""
        icon = self.AGENT_ICONS.get(entry.agent_name, "📋")
        return f"[{entry.timestamp}] {icon} [{entry.agent_name}] {entry.action}"
