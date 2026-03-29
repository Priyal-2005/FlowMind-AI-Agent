"""
Autonomous Meeting → Action Orchestrator
Enterprise Command Center Dashboard

Main Streamlit application that orchestrates the multi-agent
AI system for meeting intelligence and autonomous workflow management.
"""

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from orchestrator import MeetingOrchestrator
from data.transcripts import TRANSCRIPTS, get_transcript_names
from components.styles import get_main_styles
from components.pipeline import render_pipeline, render_agent_logs
from components.dashboard import (
    render_metrics,
    render_task_table,
    render_day_simulation,
    render_actions_panel,
    render_risk_chart,
)
from components.audit import render_audit_trail

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="Meeting Orchestrator — AI Command Center",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── INJECT STYLES ────────────────────────────────────
st.markdown(get_main_styles(), unsafe_allow_html=True)

# ── SESSION STATE INIT ───────────────────────────────
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = MeetingOrchestrator()
if "pipeline_ran" not in st.session_state:
    st.session_state.pipeline_ran = False
if "current_day" not in st.session_state:
    st.session_state.current_day = 1
if "selected_transcript" not in st.session_state:
    st.session_state.selected_transcript = get_transcript_names()[0]

orch = st.session_state.orchestrator


# ── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">🎯</div>
        <div style="font-size: 1.1rem; font-weight: 700; 
             background: linear-gradient(135deg, #00D4AA, #6C63FF);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             background-clip: text;">Meeting Orchestrator</div>
        <div style="font-size: 0.7rem; color: #8B8FA3; margin-top: 0.2rem;">
            Autonomous AI Command Center
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # LLM Mode indicator
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span class="mode-badge">{orch.llm.mode}</span>
    </div>
    """, unsafe_allow_html=True)

    # Transcript Selection
    st.markdown("### 📄 Meeting Transcript")

    transcript_name = st.selectbox(
        "Select a sample transcript",
        get_transcript_names(),
        key="transcript_selector",
        label_visibility="collapsed",
    )
    st.session_state.selected_transcript = transcript_name

    selected = TRANSCRIPTS[transcript_name]
    st.caption(f"{selected['icon']} {selected['description']}")

    # Show transcript
    transcript_text = st.text_area(
        "Meeting Transcript",
        value=selected["transcript"].strip(),
        height=250,
        key="transcript_input",
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Run button
    run_clicked = st.button(
        "🚀 Run Autonomous Workflow",
        use_container_width=True,
        type="primary",
        key="run_pipeline",
    )

    if run_clicked:
        st.session_state.pipeline_ran = False
        st.session_state.current_day = 1
        # Reset orchestrator
        orch.reset()
        st.session_state.orchestrator = MeetingOrchestrator()
        orch = st.session_state.orchestrator

    # Architecture info
    st.markdown("---")
    st.markdown("### 🏗️ System Architecture")
    with st.expander("View Agents", expanded=False):
        agents_info = [
            ("🎯", "Orchestrator", "Central control & routing"),
            ("🔍", "Extraction", "Parse transcript data"),
            ("🧠", "Intelligence", "Risk & gap analysis"),
            ("⚡", "Execution", "Task structuring"),
            ("📊", "Tracking", "Time simulation"),
            ("🤖", "Decision", "Autonomous actions"),
            ("📜", "Audit Logger", "Full trail recording"),
        ]
        for icon, name, desc in agents_info:
            st.markdown(f"**{icon} {name}**  \n{desc}")

    # Impact metrics
    st.markdown("---")
    st.markdown("### 💰 Business Impact")
    st.markdown("""
    <div class="glass-card" style="font-size: 0.75rem; padding: 0.75rem;">
        <div style="color: #00D4AA; font-weight: 700; font-size: 0.85rem; margin-bottom: 0.3rem;">
            ROI Calculator (100-person team)
        </div>
        <div style="margin-bottom: 0.2rem;">⏱️ <b>2.5 hrs/week</b> saved per employee</div>
        <div style="margin-bottom: 0.2rem;">📊 <b>250 hrs/week</b> total saved</div>
        <div style="margin-bottom: 0.2rem;">💰 <b>₹5 lakh/week</b> value recovered</div>
        <div style="color: #FFB800; font-weight: 700; margin-top: 0.3rem; font-size: 0.9rem;">
            = ₹2.6 Cr/year savings
        </div>
    </div>
    """, unsafe_allow_html=True)


# ── MAIN CONTENT ─────────────────────────────────────

# Header
st.markdown("""
<div class="main-header">
    <h1>🎯 Autonomous Meeting Orchestrator</h1>
    <div class="subtitle">Multi-Agent AI Command Center for Enterprise Workflow Intelligence</div>
</div>
""", unsafe_allow_html=True)


# ── RUN PIPELINE ─────────────────────────────────────
if run_clicked and transcript_text.strip():
    with st.spinner(""):
        # Create progress container
        progress_placeholder = st.empty()
        pipeline_placeholder = st.empty()

        stages = [
            ("🔍 Extraction Agent — Parsing transcript...", 0.17),
            ("🧠 Intelligence Agent — Analyzing risks...", 0.34),
            ("⚡ Execution Agent — Creating tasks...", 0.51),
            ("📊 Tracking Agent — Simulating Day 1...", 0.68),
            ("🤖 Decision Agent — Taking actions...", 0.85),
            ("✅ Pipeline complete!", 1.0),
        ]

        # Show progress bar
        progress_bar = st.progress(0, text="🎯 Orchestrator initializing pipeline...")

        import time
        for stage_text, stage_progress in stages:
            progress_bar.progress(stage_progress, text=stage_text)
            time.sleep(0.3)

        # Actually run the pipeline
        result = orch.run_pipeline(transcript_text.strip())
        st.session_state.pipeline_ran = True
        st.session_state.current_day = 1

        progress_bar.progress(1.0, text="✅ All agents executed successfully!")
        time.sleep(0.5)
        progress_bar.empty()

    st.rerun()


# ── DISPLAY RESULTS ──────────────────────────────────
if st.session_state.pipeline_ran and orch.state.get("pipeline_status") in ("complete", "error"):
    state = orch.state

    # Agent Pipeline Visualization
    render_pipeline(orch.agent_list, state.get("current_agent"))
    render_agent_logs(orch.agent_list)

    st.markdown("---")

    # Time Simulation
    new_day = render_day_simulation(st.session_state.current_day)
    if new_day != st.session_state.current_day:
        st.session_state.current_day = new_day
        orch.simulate_day(new_day)
        st.rerun()

    st.markdown("---")

    # Get current stats
    tracking = state.get("tracking", {})
    stats = tracking.get("stats", {})
    if not stats:
        # Compute from tasks
        tasks = state.get("tasks", [])
        stats = {
            "total": len(tasks),
            "completed": sum(1 for t in tasks if t.get("status") == "completed"),
            "in_progress": sum(1 for t in tasks if t.get("status") == "in-progress"),
            "pending": sum(1 for t in tasks if t.get("status") == "pending"),
            "delayed": sum(1 for t in tasks if t.get("status") == "delayed"),
            "blocked": sum(1 for t in tasks if t.get("status") == "blocked"),
        }

    # Metrics
    render_metrics(stats, st.session_state.current_day)

    st.markdown("<br>", unsafe_allow_html=True)

    # Main content area — Task Table + Charts
    tab_tasks, tab_charts, tab_actions, tab_audit = st.tabs([
        "📋 Task Registry",
        "📊 Analytics",
        "🤖 Autonomous Actions",
        "📜 Audit Trail",
    ])

    with tab_tasks:
        render_task_table(state.get("tasks", []))

    with tab_charts:
        render_risk_chart(state.get("tasks", []))

    with tab_actions:
        render_actions_panel(state.get("decision"))

    with tab_audit:
        render_audit_trail(orch.audit_logger)

else:
    # Welcome state — show instructions
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="glass-card-accent" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🚀</div>
            <div style="font-size: 1.2rem; font-weight: 700; color: #FAFAFA; margin-bottom: 0.5rem;">
                Ready to Orchestrate
            </div>
            <div style="color: #8B8FA3; font-size: 0.9rem; margin-bottom: 1rem;">
                Select a meeting transcript from the sidebar and click 
                <span style="color: #00D4AA; font-weight: 600;">"Run Autonomous Workflow"</span>
                to activate the multi-agent pipeline.
            </div>
            <div style="color: #5A5E73; font-size: 0.75rem;">
                The system will extract action items, detect risks, create tasks,<br>
                simulate time progression, and take autonomous corrective actions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    st.markdown('<div class="section-header"><span class="header-icon">✨</span> System Capabilities</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    features = [
        ("🔍", "Intelligent Extraction", "Parses meeting transcripts to extract action items, decisions, owners, deadlines, and blockers using AI-powered analysis."),
        ("🧠", "Risk Intelligence", "Detects missing owners, dependencies, blockers, and overloaded team members with severity-scored risk assessment."),
        ("⚡", "Task Automation", "Converts extracted data into structured executable tasks with priorities, deadlines, and risk flags."),
        ("📊", "Time Simulation", "Simulates task progression across Day 1 → Day 3 with realistic status updates and bottleneck detection."),
        ("🤖", "Autonomous Actions", "Takes corrective actions automatically — assigns owners, escalates delays, sends reminders, redistributes workload."),
        ("📜", "Full Audit Trail", "Maintains chronological logs of every agent decision with reasoning for complete transparency and compliance."),
    ]

    for i, (icon, title, desc) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f'''
            <div class="glass-card" style="margin-bottom: 0.75rem; min-height: 140px;">
                <div style="font-size: 1.5rem; margin-bottom: 0.3rem;">{icon}</div>
                <div style="font-weight: 600; color: #FAFAFA; margin-bottom: 0.3rem; font-size: 0.9rem;">{title}</div>
                <div style="color: #8B8FA3; font-size: 0.75rem; line-height: 1.4;">{desc}</div>
            </div>
            ''', unsafe_allow_html=True)
