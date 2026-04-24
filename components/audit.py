"""
Audit Trail Component

Renders chronological agent decision logs with:
- Color-coded entries by agent
- Severity indicators
- Expandable reasoning
- Agent filtering
"""

import html as _html
import streamlit as st
from utils.logger import AuditLogger, AuditEntry

def h(text: str) -> str:
    """Escape HTML content."""
    return _html.escape(str(text))


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
        # We can still use the color/icon mapping for the UI
        color = AuditLogger.AGENT_COLORS.get(entry.agent_name, "#8B8FA3")
        icon = AuditLogger.AGENT_ICONS.get(entry.agent_name, "📋")

        severity_indicator = ""
        if entry.severity == "WARNING":
            severity_indicator = '<span style="color: #FFB800; margin-left: 0.3rem;">⚠️</span>'
        elif entry.severity == "ACTION":
            severity_indicator = '<span style="color: #00D4AA; margin-left: 0.3rem;">⚡</span>'
        elif entry.severity == "ESCALATION":
            severity_indicator = '<span style="color: #FF4B4B; margin-left: 0.3rem;">🚨</span>'

        with st.container(border=True):
            header_col1, header_col2 = st.columns([1, 4])
            with header_col1:
                st.markdown(f"<span style='font-family: monospace; color: #8B8FA3; font-size: 0.85rem;'>[{entry.timestamp}]</span>", unsafe_allow_html=True)
            with header_col2:
                st.markdown(f"<span style='color: {color}; font-weight: 600; font-size: 0.85rem;'>{icon} [{entry.agent_name}]</span> {severity_indicator}", unsafe_allow_html=True)
            
            st.markdown(f"<div style='font-size: 0.95rem; font-weight: 500; margin-bottom: 0.3rem;'>{h(entry.action)}</div>", unsafe_allow_html=True)
            
            if entry.reasoning:
                st.markdown(f"<div style='background: rgba(255,255,255,0.03); padding: 0.6rem; border-radius: 6px; font-size: 0.85rem; color: #8B8FA3; border-left: 3px solid rgba(255,255,255,0.1); margin-top: 0.4rem;'>💭 {h(entry.reasoning)}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

