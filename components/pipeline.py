"""
Pipeline Visualization Component

Renders the horizontal agent pipeline with status indicators,
animated transitions, and real-time execution logs.
"""

import streamlit as st
from utils.logger import AuditLogger


def render_pipeline(agents: list, current_agent: str = None):
    """Render the horizontal agent pipeline visualization."""

    st.markdown('<div class="section-header"><span class="header-icon">🔄</span> Agent Pipeline <span class="header-badge">LIVE</span></div>', unsafe_allow_html=True)

    # Build pipeline HTML
    cards_html = '<div class="pipeline-container">'

    for i, agent in enumerate(agents):
        status = agent.status
        status_class = status if status in ("idle", "running", "complete", "error") else "idle"

        # If this is the current running agent
        if current_agent and agent.name.lower().replace(" ", "_").replace("_agent", "") in current_agent:
            status_class = "running"

        status_labels = {
            "idle": "WAITING",
            "running": "RUNNING",
            "complete": "DONE",
            "error": "ERROR",
        }

        time_display = f"{agent.execution_time}s" if agent.execution_time > 0 else "—"

        cards_html += (
            f'<div class="agent-card {status_class}">'
            f'<div class="agent-icon">{agent.icon}</div>'
            f'<div class="agent-name">{agent.name}</div>'
            f'<span class="agent-status status-{status_class}">{status_labels.get(status_class, "WAITING")}</span>'
            f'<div class="agent-time">{time_display}</div>'
            f'</div>'
        )

        # Add arrow between agents (not after last)
        if i < len(agents) - 1:
            arrow_class = "active" if agent.status == "complete" else ""
            cards_html += f'<div class="pipeline-arrow {arrow_class}">→</div>'

    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)


def render_agent_logs(agents: list):
    """Render processing logs from each completed agent."""

    completed_agents = [a for a in agents if a.status in ("complete", "error")]
    if not completed_agents:
        return

    st.markdown('<div class="section-header"><span class="header-icon">📝</span> Agent Processing Logs</div>', unsafe_allow_html=True)

    for agent in completed_agents:
        if agent.logs:
            with st.expander(f"{agent.icon} {agent.name} — {len(agent.logs)} entries ({agent.execution_time}s)", expanded=False):
                for line in agent.logs:
                    # Semantic icons based on log content
                    icon = "🔹"
                    line_lower = line.lower()
                    if any(x in line_lower for x in ["success", "completed", "assigned", "done"]):
                        icon = "✅"
                    elif any(x in line_lower for x in ["error", "failed", "issue", "delayed", "warning", "missing"]):
                        icon = "⚠️"
                    elif any(x in line_lower for x in ["starting", "running", "executing", "triggered"]):
                        icon = "🚀"
                    elif any(x in line_lower for x in ["found", "extracted", "detected", "analyzing"]):
                        icon = "🔍"
                    elif any(x in line_lower for x in ["created", "generated"]):
                        icon = "✨"
                    
                    st.markdown(f"{icon} {line}")
