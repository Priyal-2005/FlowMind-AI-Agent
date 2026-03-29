"""
Audit Trail Component

Renders chronological agent decision logs with:
- Color-coded entries by agent
- Severity indicators
- Expandable reasoning
- Agent filtering
"""

import streamlit as st
from utils.logger import AuditLogger, AuditEntry


def render_audit_trail(audit_logger: AuditLogger):
    """Render the full audit trail panel."""
    entries = audit_logger.get_entries()

    st.markdown(
        '<div class="section-header">'
        '<span class="header-icon">📜</span> Audit Trail'
        f'<span class="header-badge">{len(entries)} ENTRIES</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not entries:
        st.info("Audit trail will populate as agents execute.")
        return

    # Filter controls
    col1, col2 = st.columns([2, 1])
    with col1:
        agent_names = ["All"] + list(AuditLogger.AGENT_COLORS.keys())
        selected_agent = st.selectbox(
            "Filter by Agent",
            agent_names,
            key="audit_agent_filter",
            label_visibility="collapsed",
        )
    with col2:
        severity_filter = st.selectbox(
            "Filter by Severity",
            ["All", "INFO", "WARNING", "ACTION", "ESCALATION"],
            key="audit_severity_filter",
            label_visibility="collapsed",
        )

    # Filter entries
    filtered = entries
    if selected_agent != "All":
        filtered = [e for e in filtered if e.agent_name == selected_agent]
    if severity_filter != "All":
        filtered = [e for e in filtered if e.severity == severity_filter]

    # Render entries
    if not filtered:
        st.caption("No entries match the selected filters.")
        return

    # Build entries HTML for performance
    entries_html = ""
    for entry in filtered:
        agent_class = _get_agent_class(entry.agent_name)
        color = AuditLogger.AGENT_COLORS.get(entry.agent_name, "#8B8FA3")
        icon = AuditLogger.AGENT_ICONS.get(entry.agent_name, "📋")

        severity_indicator = ""
        if entry.severity == "WARNING":
            severity_indicator = '<span style="color: #FFB800; margin-left: 0.3rem;">⚠️</span>'
        elif entry.severity == "ACTION":
            severity_indicator = '<span style="color: #00D4AA; margin-left: 0.3rem;">⚡</span>'
        elif entry.severity == "ESCALATION":
            severity_indicator = '<span style="color: #FF4B4B; margin-left: 0.3rem;">🚨</span>'

        reasoning_html = ""
        if entry.reasoning:
            reasoning_html = f'<div class="reasoning-text">💭 {entry.reasoning}</div>'

        entries_html += f'''
        <div class="audit-entry {agent_class} animate-slide-in">
            <span class="timestamp">[{entry.timestamp}]</span>
            <span class="agent-tag" style="color: {color};"> {icon} [{entry.agent_name}]</span>
            {severity_indicator}
            <div class="action-text">{entry.action}</div>
            {reasoning_html}
        </div>
        '''

    st.markdown(entries_html, unsafe_allow_html=True)


def render_audit_summary(audit_logger: AuditLogger):
    """Render a compact audit summary with key stats."""
    entries = audit_logger.get_entries()
    if not entries:
        return

    actions = audit_logger.get_autonomous_actions()
    escalations = audit_logger.get_escalations()
    warnings = audit_logger.get_actions_by_severity("WARNING")

    cols = st.columns(4)
    with cols[0]:
        st.metric("Total Logs", len(entries))
    with cols[1]:
        st.metric("Actions Taken", len(actions))
    with cols[2]:
        st.metric("Escalations", len(escalations))
    with cols[3]:
        st.metric("Warnings", len(warnings))


def _get_agent_class(agent_name: str) -> str:
    """Map agent name to CSS class."""
    mapping = {
        "Orchestrator": "audit-orchestrator",
        "Extraction Agent": "audit-extraction",
        "Intelligence Agent": "audit-intelligence",
        "Execution Agent": "audit-execution",
        "Tracking Agent": "audit-tracking",
        "Decision Agent": "audit-decision",
    }
    return mapping.get(agent_name, "")
