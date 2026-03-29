"""
Dashboard Component — Task Command Center

Renders:
- KPI metric tiles (summary stats)
- Task table with status badges
- Escalation and action panels
- Time simulation controls
"""

import streamlit as st
import plotly.graph_objects as go


def render_metrics(stats: dict, day: int):
    """Render KPI metric tiles."""
    st.markdown(
        '<div class="section-header">'
        '<span class="header-icon">📊</span> Command Center Overview'
        f'<span class="header-badge">DAY {day}</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(6)

    metrics = [
        ("Total Tasks", stats.get("total", 0), "purple", "📋"),
        ("Completed", stats.get("completed", 0), "green", "✅"),
        ("In Progress", stats.get("in_progress", 0), "blue", "🔄"),
        ("Pending", stats.get("pending", 0), "yellow", "⏳"),
        ("Delayed", stats.get("delayed", 0), "red", "⚠️"),
        ("Blocked", stats.get("blocked", 0), "red", "🚫"),
    ]

    for col, (label, value, color, icon) in zip(cols, metrics):
        with col:
            st.markdown(f'''
            <div class="metric-tile metric-{color}">
                <div style="font-size: 1.2rem; margin-bottom: 0.2rem;">{icon}</div>
                <p class="metric-value">{value}</p>
                <p class="metric-label">{label}</p>
            </div>
            ''', unsafe_allow_html=True)


def render_task_table(tasks: list):
    """Render the task command center table."""
    st.markdown(
        '<div class="section-header">'
        '<span class="header-icon">⚡</span> Task Registry'
        f'<span class="header-badge">{len(tasks)} TASKS</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not tasks:
        st.info("No tasks created yet. Run the workflow to generate tasks.")
        return

    # Build table HTML
    table_html = '''
    <table class="task-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Task</th>
                <th>Owner</th>
                <th>Status</th>
                <th>Priority</th>
                <th>Risk</th>
                <th>Deadline</th>
                <th>Progress</th>
            </tr>
        </thead>
        <tbody>
    '''

    for task in tasks:
        # Status badge
        status = task.get("status", "pending")
        status_badge = f'<span class="badge badge-{status}">{status.upper()}</span>'

        # Priority badge
        priority = task.get("priority", "P2")
        priority_badge = f'<span class="badge badge-{priority.lower()}">{priority}</span>'

        # Risk badge
        risk = task.get("risk_flag", "LOW")
        risk_badge = f'<span class="badge badge-{risk.lower()}">{risk}</span>'

        # Owner
        owner = task.get("owner", "UNASSIGNED")
        owner_display = owner
        if owner == "UNASSIGNED":
            owner_display = '<span style="color: #FF4B4B; font-weight: 600;">⚠️ UNASSIGNED</span>'
        elif task.get("auto_assigned"):
            owner_display = f'<span style="color: #00D4AA;">{owner} 🤖</span>'
        elif task.get("reassigned"):
            owner_display = f'<span style="color: #F093FB;">{owner} 🔄</span>'

        # Progress bar
        progress = task.get("progress", 0)
        if status == "completed":
            progress = 100
        progress_color = "green" if progress >= 75 else "blue" if progress >= 40 else "yellow" if progress > 0 else "red"
        progress_html = f'''
        <div class="progress-bar-container">
            <div class="progress-bar-fill progress-{progress_color}" style="width: {progress}%;"></div>
        </div>
        <span style="font-size: 0.65rem; color: #8B8FA3; font-family: 'JetBrains Mono', monospace;">{progress}%</span>
        '''

        # Title (truncate if needed)
        title = task.get("title", "")
        title_display = title[:55] + "..." if len(title) > 55 else title

        table_html += f'''
        <tr>
            <td><span class="task-id">{task.get("id", "")}</span></td>
            <td>{title_display}</td>
            <td>{owner_display}</td>
            <td>{status_badge}</td>
            <td>{priority_badge}</td>
            <td>{risk_badge}</td>
            <td><span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem;">{task.get("deadline", "—")}</span></td>
            <td style="min-width: 80px;">{progress_html}</td>
        </tr>
        '''

    table_html += '</tbody></table>'
    st.markdown(table_html, unsafe_allow_html=True)


def render_day_simulation(current_day: int):
    """Render day simulation selector. Returns selected day."""
    st.markdown(
        '<div class="section-header">'
        '<span class="header-icon">⏱️</span> Time Simulation Engine'
        '</div>',
        unsafe_allow_html=True,
    )

    cols = st.columns([1, 1, 1, 2])
    selected_day = current_day

    for i, col in enumerate(cols[:3], 1):
        with col:
            day_label = f"Day {i}"
            if i == 1:
                day_label += " — Start"
            elif i == 2:
                day_label += " — Mid"
            elif i == 3:
                day_label += " — Deadline"

            if st.button(
                day_label,
                key=f"day_btn_{i}",
                use_container_width=True,
                type="primary" if i == current_day else "secondary",
            ):
                selected_day = i

    with cols[3]:
        day_descriptions = {
            1: "🟢 **Day 1**: Tasks kick off. P0 items start immediately. Team begins execution.",
            2: "🟡 **Day 2**: Progress check. Delays emerge. Bottlenecks become visible.",
            3: "🔴 **Day 3**: Deadline pressure. Stalled tasks escalated. Autonomous actions triggered.",
        }
        st.markdown(day_descriptions.get(current_day, ""), unsafe_allow_html=True)

    return selected_day


def render_actions_panel(decision_data: dict):
    """Render the escalation and autonomous actions panel."""
    if not decision_data:
        return

    actions = decision_data.get("actions_taken", [])
    escalations = decision_data.get("escalations", [])
    reminders = decision_data.get("reminders", [])

    total = len(actions) + len(escalations) + len(reminders)

    st.markdown(
        '<div class="section-header">'
        '<span class="header-icon">🤖</span> Autonomous Actions'
        f'<span class="header-badge">{total} ACTIONS</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not total:
        st.success("✅ No issues detected — all systems nominal.")
        return

    tab1, tab2, tab3 = st.tabs([
        f"⚡ Actions ({len(actions)})",
        f"🚨 Escalations ({len(escalations)})",
        f"🔔 Reminders ({len(reminders)})",
    ])

    with tab1:
        if actions:
            for action in actions:
                icon = action.get("icon", "⚡")
                action_type = action.get("type", "").replace("_", " ").title()
                card_class = "assignment-card" if "assign" in action.get("type", "") else "action-card"
                st.markdown(f'''
                <div class="action-card {card_class} animate-slide-in">
                    <div class="action-type" style="color: var(--accent-primary);">{icon} {action_type}</div>
                    <div class="action-detail">{action.get("action", "")}</div>
                    <div class="action-reasoning">{action.get("reasoning", "")}</div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No corrective actions needed.")

    with tab2:
        if escalations:
            for esc in escalations:
                st.markdown(f'''
                <div class="action-card escalation-card animate-slide-in">
                    <div class="action-type" style="color: var(--accent-error);">🚨 ESCALATION</div>
                    <div class="action-detail">{esc.get("action", "")}</div>
                    <div class="action-reasoning">Target: {esc.get("target", "Management")} | Reason: {esc.get("reason", "")}</div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No escalations triggered.")

    with tab3:
        if reminders:
            for rem in reminders:
                st.markdown(f'''
                <div class="action-card reminder-card animate-slide-in">
                    <div class="action-type" style="color: var(--accent-warning);">🔔 REMINDER</div>
                    <div class="action-detail">{rem.get("action", "")}</div>
                    <div class="action-reasoning">Task: {rem.get("task_id", "")} — {rem.get("reason", "")}</div>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("No reminders sent.")


def render_risk_chart(tasks: list):
    """Render task distribution charts using Plotly."""
    if not tasks:
        return

    # Status distribution
    status_counts = {}
    for t in tasks:
        s = t.get("status", "pending")
        status_counts[s] = status_counts.get(s, 0) + 1

    status_colors = {
        "completed": "#00D4AA",
        "in-progress": "#45B7D1",
        "pending": "#8B8FA3",
        "delayed": "#FFB800",
        "blocked": "#FF4B4B",
    }

    col1, col2 = st.columns(2)

    with col1:
        fig = go.Figure(data=[go.Pie(
            labels=list(status_counts.keys()),
            values=list(status_counts.values()),
            marker_colors=[status_colors.get(s, "#8B8FA3") for s in status_counts.keys()],
            hole=0.55,
            textinfo="label+value",
            textfont=dict(size=11, family="Inter"),
        )])
        fig.update_layout(
            title=dict(text="Task Status Distribution", font=dict(size=13, color="#FAFAFA", family="Inter")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8B8FA3"),
            height=280,
            margin=dict(t=40, b=20, l=20, r=20),
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Priority distribution
        priority_counts = {}
        for t in tasks:
            p = t.get("priority", "P2")
            priority_counts[p] = priority_counts.get(p, 0) + 1

        priority_colors = {"P0": "#FF4B4B", "P1": "#FFB800", "P2": "#45B7D1"}

        fig2 = go.Figure(data=[go.Bar(
            x=list(priority_counts.keys()),
            y=list(priority_counts.values()),
            marker_color=[priority_colors.get(p, "#8B8FA3") for p in priority_counts.keys()],
            text=list(priority_counts.values()),
            textposition="outside",
            textfont=dict(size=12, family="Inter", color="#FAFAFA"),
        )])
        fig2.update_layout(
            title=dict(text="Priority Distribution", font=dict(size=13, color="#FAFAFA", family="Inter")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8B8FA3"),
            height=280,
            margin=dict(t=40, b=20, l=20, r=20),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig2, use_container_width=True)
