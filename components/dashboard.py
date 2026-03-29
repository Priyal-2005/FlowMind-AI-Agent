"""
Dashboard Component — Task Command Center

Renders:
- KPI metric tiles (summary stats)
- Task table with status badges
- Escalation and action panels
- Time simulation controls
- Summary banner (post-run)
"""

import html as _html
import streamlit as st
import plotly.graph_objects as go


def h(text: str) -> str:
    """HTML-escape user-provided content to prevent raw HTML rendering."""
    return _html.escape(str(text))


def render_summary_banner(total_tasks: int, issues_detected: int, actions_taken: int, llm_mode: str):
    """Render a prominent summary banner after pipeline execution."""
    st.markdown(f"""
    <div class="summary-banner">
        <div class="summary-banner-inner">
            <div class="summary-stat">
                <div class="summary-stat-icon">📋</div>
                <div class="summary-stat-value">{total_tasks}</div>
                <div class="summary-stat-label">Tasks Created</div>
            </div>
            <div class="summary-divider"></div>
            <div class="summary-stat">
                <div class="summary-stat-icon">🚨</div>
                <div class="summary-stat-value" style="color: {'#FF4B4B' if issues_detected > 3 else '#FFB800' if issues_detected > 0 else '#00D4AA'};">{issues_detected}</div>
                <div class="summary-stat-label">Issues Detected</div>
            </div>
            <div class="summary-divider"></div>
            <div class="summary-stat">
                <div class="summary-stat-icon">🤖</div>
                <div class="summary-stat-value" style="color: #00D4AA;">{actions_taken}</div>
                <div class="summary-stat-label">Actions Taken</div>
            </div>
            <div class="summary-divider"></div>
            <div class="summary-stat">
                <div class="summary-stat-icon">⚙️</div>
                <div class="summary-stat-value" style="font-size: 0.9rem; color: #6C63FF;">LIVE</div>
                <div class="summary-stat-label">{llm_mode}</div>
            </div>
        </div>
        <div class="summary-banner-label">✅ Pipeline Executed Successfully — 5 Agents Completed</div>
    </div>
    """, unsafe_allow_html=True)


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
        status_icon = {"completed": "✅", "in-progress": "🔄", "pending": "⏳", "delayed": "⚠️", "blocked": "🚫"}.get(status, "")
        status_badge = f'<span class="badge badge-{status}">{status_icon} {status.upper()}</span>'

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
            owner_display = f'<span style="color: #00D4AA;" title="Auto-assigned by AI">{owner} 🤖</span>'
        elif task.get("reassigned"):
            owner_display = f'<span style="color: #F093FB;" title="Reassigned by AI">{owner} 🔄</span>'
        elif task.get("redistributed"):
            owner_display = f'<span style="color: #FFB800;" title="Redistributed by AI">{owner} ⚖️</span>'

        # Progress bar
        progress = task.get("progress", 0)
        if status == "completed":
            progress = 100
        elif status == "pending" and progress == 0:
            progress = 0
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

        # Row highlight class for delayed/blocked
        row_class = ""
        if status == "delayed":
            row_class = "row-delayed"
        elif status == "blocked":
            row_class = "row-blocked"
        elif status == "completed":
            row_class = "row-completed"

        table_html += f'''
        <tr class="{row_class}">
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
        '<span class="header-badge">INTERACTIVE</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Day descriptions with rich context
    day_info = {
        1: {
            "label": "Day 1 — Kickoff",
            "emoji": "🟢",
            "desc": "**Day 1 — Kickoff**: Tasks are initiated. P0 items start immediately. Team begins execution. 1st-day setup and alignment.",
            "color": "#00D4AA",
        },
        2: {
            "label": "Day 2 — Mid Sprint",
            "emoji": "🟡",
            "desc": "**Day 2 — Mid Sprint**: Progress check-in. Early delays emerge. Bottlenecks become visible. Decision agent intervenes.",
            "color": "#FFB800",
        },
        3: {
            "label": "Day 3 — Deadline",
            "emoji": "🔴",
            "desc": "**Day 3 — Deadline**: Critical pressure. Stalled tasks escalated. Autonomous reassignments triggered. Final stretch.",
            "color": "#FF4B4B",
        },
    }

    # Render day selector as cards
    cols = st.columns(3)
    selected_day = current_day

    for i, col in enumerate(cols, 1):
        info = day_info[i]
        is_active = i == current_day
        with col:
            if st.button(
                f"{info['emoji']} {info['label']}",
                key=f"day_btn_{i}",
                use_container_width=True,
                type="primary" if is_active else "secondary",
                help=f"Simulate task progress on Day {i}",
            ):
                selected_day = i

    # Show description for current day
    info = day_info[current_day]
    st.markdown(
        f'<div class="day-description" style="border-left-color: {info["color"]};">'
        f'{info["desc"]}'
        f'</div>',
        unsafe_allow_html=True,
    )

    return selected_day


def render_actions_panel(decision_data: dict):
    """Render the escalation and autonomous actions panel."""
    if not decision_data:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 2rem; color: #8B8FA3;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🤖</div>
            <div style="font-weight: 600; color: #FAFAFA; margin-bottom: 0.3rem;">No Decision Data</div>
            <div style="font-size: 0.8rem;">Run the pipeline to see autonomous actions taken by the Decision Agent.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    actions = decision_data.get("actions_taken", [])
    escalations = decision_data.get("escalations", [])
    reminders = decision_data.get("reminders", [])

    total = len(actions) + len(escalations) + len(reminders)

    st.markdown(
        '<div class="section-header">'
        '<span class="header-icon">🤖</span> Autonomous Actions Panel'
        f'<span class="header-badge">{total} TOTAL ACTIONS</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    if not total:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 1.5rem;">
            <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">✅</div>
            <div style="color: #00D4AA; font-weight: 600; margin-bottom: 0.2rem;">All Systems Nominal</div>
            <div style="color: #8B8FA3; font-size: 0.8rem;">No critical issues detected. Switch to Day 2 or Day 3 to see autonomous actions.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    # Quick stats row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="action-stat-card action-stat-blue">
            <div class="action-stat-value">{len(actions)}</div>
            <div class="action-stat-label">⚡ Corrective Actions</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="action-stat-card action-stat-red">
            <div class="action-stat-value">{len(escalations)}</div>
            <div class="action-stat-label">🚨 Escalations</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="action-stat-card action-stat-yellow">
            <div class="action-stat-value">{len(reminders)}</div>
            <div class="action-stat-label">🔔 Reminders Sent</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

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

                # Determine what changed
                prev_owner = action.get("previous_owner", "")
                new_owner = action.get("new_owner", "")
                owner_change_html = ""
                if prev_owner and new_owner:
                    owner_change_html = f'<div class="owner-change"><span class="owner-from">{prev_owner}</span> → <span class="owner-to">{new_owner}</span></div>'

                safe_title = h(action.get("task_title", ""))[:70]
                if len(action.get("task_title", "")) > 70:
                    safe_title += "..."
                safe_action_text = h(action.get("action", ""))
                safe_reasoning = h(action.get("reasoning", ""))

                card_html = (
                    f'<div class="action-card {card_class} animate-slide-in">'
                    f'<div class="action-header">'
                    f'<span class="action-type-badge">{icon} {action_type}</span>'
                    f'<span class="action-task-id">{action.get("task_id", "")}</span>'
                    f'</div>'
                    f'<div class="action-title">{safe_title}</div>'
                    f'<div class="action-detail">{safe_action_text}</div>'
                    f'{owner_change_html}'
                    f'<div class="action-reasoning">💭 {safe_reasoning}</div>'
                    f'</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1.5rem; color: #8B8FA3;">
                <div style="font-size: 1.2rem;">✅</div>
                <div style="font-size: 0.85rem; margin-top: 0.3rem;">No corrective actions needed.</div>
                <div style="font-size: 0.75rem; margin-top: 0.2rem;">Try Day 2 or Day 3 for more action.</div>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        if escalations:
            for esc in escalations:
                safe_title = h(esc.get("task_title", ""))[:70]
                safe_action_text = h(esc.get("action", ""))
                safe_reason = h(esc.get("reason", ""))
                target = h(esc.get("target", "Engineering Manager"))
                card_html = (
                    '<div class="action-card escalation-card animate-slide-in">'
                    '<div class="action-header">'
                    '<span class="action-type-badge" style="color: #FF4B4B;">🚨 ESCALATION</span>'
                    f'<span class="action-task-id">{esc.get("task_id", "")}</span>'
                    '</div>'
                    f'<div class="action-title">{safe_title}</div>'
                    f'<div class="action-detail">{safe_action_text}</div>'
                    f'<div class="action-reasoning">🎯 Target: <b>{target}</b> | Reason: {safe_reason}</div>'
                    f'<div class="escalation-badge">⚡ Priority: {esc.get("priority", "P0")}</div>'
                    '</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1.5rem; color: #8B8FA3;">
                <div style="font-size: 1.2rem;">✅</div>
                <div style="font-size: 0.85rem; margin-top: 0.3rem;">No escalations triggered on this day.</div>
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        if reminders:
            for rem in reminders:
                safe_title = h(rem.get("task_title", ""))[:70]
                safe_action_text = h(rem.get("action", ""))
                safe_reason = h(rem.get("reason", ""))
                card_html = (
                    '<div class="action-card reminder-card animate-slide-in">'
                    '<div class="action-header">'
                    '<span class="action-type-badge" style="color: #FFB800;">🔔 REMINDER</span>'
                    f'<span class="action-task-id">{rem.get("task_id", "")}</span>'
                    '</div>'
                    f'<div class="action-title">{safe_title}</div>'
                    f'<div class="action-detail">{safe_action_text}</div>'
                    f'<div class="action-reasoning">📋 Reason: {safe_reason}</div>'
                    '</div>'
                )
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1.5rem; color: #8B8FA3;">
                <div style="font-size: 1.2rem;">✅</div>
                <div style="font-size: 0.85rem; margin-top: 0.3rem;">No reminders sent on this day.</div>
            </div>
            """, unsafe_allow_html=True)


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

    col1, col2, col3 = st.columns(3)

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

    with col3:
        # Progress histogram
        progress_vals = [t.get("progress", 0) for t in tasks]
        owners = list(set(t.get("owner", "UNASSIGNED") for t in tasks if t.get("owner") != "UNASSIGNED"))

        # Owner workload chart
        owner_counts = {}
        for t in tasks:
            o = t.get("owner", "UNASSIGNED")
            owner_counts[o] = owner_counts.get(o, 0) + 1

        sorted_owners = sorted(owner_counts.items(), key=lambda x: x[1], reverse=True)[:6]
        owner_labels = [x[0] for x in sorted_owners]
        owner_values = [x[1] for x in sorted_owners]
        bar_colors = ["#FF4B4B" if v >= 3 else "#FFB800" if v >= 2 else "#00D4AA" for v in owner_values]

        fig3 = go.Figure(data=[go.Bar(
            x=owner_labels,
            y=owner_values,
            marker_color=bar_colors,
            text=owner_values,
            textposition="outside",
            textfont=dict(size=11, family="Inter", color="#FAFAFA"),
        )])
        fig3.update_layout(
            title=dict(text="Owner Workload", font=dict(size=13, color="#FAFAFA", family="Inter")),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#8B8FA3"),
            height=280,
            margin=dict(t=40, b=20, l=20, r=20),
            xaxis=dict(showgrid=False, tickangle=-20),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)"),
        )
        st.plotly_chart(fig3, use_container_width=True)
