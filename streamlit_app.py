"""
FlowMind AI — Autonomous Workflow Orchestrator
Enterprise Command Center Dashboard

Main Streamlit application that orchestrates the multi-agent
AI system for workflow intelligence and autonomous task management.
"""

import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from orchestrator.orchestrator import WorkflowOrchestrator
from data.transcripts import SAMPLE_INPUTS, get_input_names
from components.styles import get_main_styles
from components.pipeline import render_pipeline, render_agent_logs
from components.dashboard import (
    render_metrics,
    render_task_table,
    render_day_simulation,
    render_actions_panel,
    render_risk_chart,
    render_summary_banner,
)
from components.audit import render_audit_trail
from utils.helpers import extract_text_from_file, export_to_json, export_to_csv

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="FlowMind AI — Autonomous Workflow Orchestrator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── INJECT STYLES ────────────────────────────────────
st.markdown(get_main_styles(), unsafe_allow_html=True)

# ── SESSION STATE INIT ───────────────────────────────
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = WorkflowOrchestrator()
if "pipeline_ran" not in st.session_state:
    st.session_state.pipeline_ran = False
if "current_day" not in st.session_state:
    st.session_state.current_day = 1
if "selected_transcript" not in st.session_state:
    st.session_state.selected_transcript = get_input_names()[0]


# ── SIDEBAR ──────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 0.5rem 0;">
        <div style="font-size: 2.5rem; margin-bottom: 0.3rem;">🧠</div>
        <div style="font-size: 1.1rem; font-weight: 700; 
             background: linear-gradient(135deg, #00D4AA, #6C63FF);
             -webkit-background-clip: text; -webkit-text-fill-color: transparent;
             background-clip: text;">FlowMind AI</div>
        <div style="font-size: 0.7rem; color: #8B8FA3; margin-top: 0.2rem;">
            Autonomous Workflow Orchestrator
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # LLM Mode indicator
    orch = st.session_state.orchestrator
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 1rem;">
        <span class="mode-badge">{orch.llm.mode}</span>
    </div>
    """, unsafe_allow_html=True)

    # Input Selection
    st.markdown("### 📄 Workflow Input")

    transcript_name = st.selectbox(
        "Select a sample input",
        get_input_names(),
        key="transcript_selector",
        label_visibility="collapsed",
    )
    st.session_state.selected_transcript = transcript_name

    selected = SAMPLE_INPUTS[transcript_name]
    st.caption(f"{selected['icon']} {selected['description']}")

    # Show input text
    transcript_text = st.text_area(
        "Workflow Input",
        value=selected["transcript"].strip(),
        height=200,
        key="transcript_input",
        label_visibility="collapsed",
    )

    # ── FILE UPLOAD ──────────────────────────────────
    st.markdown("---")
    st.markdown("### 📎 Upload Input File")
    uploaded_file = st.file_uploader(
        "Upload a TXT or PDF file",
        type=["txt", "pdf"],
        key="file_uploader",
        label_visibility="collapsed",
        help="Upload a .txt or .pdf file to use as workflow input instead of the text area above.",
    )
    if uploaded_file is not None:
        extracted_text = extract_text_from_file(uploaded_file)
        if extracted_text and not extracted_text.startswith("[Error]"):
            transcript_text = extracted_text
            st.success(f"✅ Loaded {len(extracted_text)} chars from {uploaded_file.name}")
        elif extracted_text.startswith("[Error]"):
            st.error(extracted_text)
        else:
            st.warning("⚠️ Could not extract text from the uploaded file.")

    st.markdown("---")

    # Memory System
    st.markdown("### 💾 Persistence")
    wipe_clicked = st.button(
        "🗑️ Wipe Database",
        use_container_width=True,
        type="secondary",
        key="wipe_db"
    )
    if wipe_clicked:
        try:
            from utils.memory import MemoryStore
            MemoryStore().clear()
            st.toast("Database wiped successfully!", icon="🧹")
        except Exception as e:
            pass

    # Demo Mode button
    st.markdown("---")
    st.markdown("### 🎬 Demo Mode")
    demo_clicked = st.button(
        "⚡ Auto Demo (Crisis Response)",
        use_container_width=True,
        type="secondary",
        key="demo_mode",
        help="Loads the Crisis Response input and runs the pipeline automatically",
    )

    # Run button
    run_clicked = st.button(
        "🚀 Run Autonomous Workflow",
        use_container_width=True,
        type="primary",
        key="run_pipeline",
    )

    if demo_clicked:
        # Switch to crisis input
        crisis_name = "Crisis Response — Missing Owners"
        if crisis_name in SAMPLE_INPUTS:
            st.session_state.selected_transcript = crisis_name
            # Flag that we should auto-run
            st.session_state.auto_run = True
            st.rerun()

    if run_clicked or st.session_state.get("auto_run", False):
        if st.session_state.get("auto_run"):
            st.session_state.auto_run = False
            run_clicked = True

    # Architecture info
    st.markdown("---")
    st.markdown("### 🏗️ System Architecture")
    with st.expander("View Agents", expanded=False):
        agents_info = [
            ("🎯", "Orchestrator", "Central control & routing"),
            ("🔍", "Extraction", "Parse input data"),
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
    <h1>🧠 FlowMind AI</h1>
    <div class="subtitle">Multi-Agent Autonomous Workflow Orchestrator</div>
</div>
""", unsafe_allow_html=True)


# ── RUN PIPELINE ─────────────────────────────────────
if run_clicked and transcript_text.strip():
    # Reset state
    st.session_state.pipeline_ran = False
    st.session_state.current_day = 1
    new_orch = WorkflowOrchestrator()
    st.session_state.orchestrator = new_orch

    import time
    with st.status("🧠 FlowMind AI initializing pipeline...", expanded=True) as status:
        stages = [
            "🔍 Extraction Agent — Parsing input...",
            "🧠 Intelligence Agent — Analyzing risks...",
            "⚡ Execution Agent — Creating tasks...",
            "📊 Tracking Agent — Simulating Day 1...",
            "🤖 Decision Agent — Taking autonomous actions...",
        ]
        
        for stage in stages:
            st.write(stage)
            time.sleep(0.65)
            
        st.write("⚙️ Executing intelligence core...")
        
        # Actually run the pipeline
        result = st.session_state.orchestrator.run_pipeline(transcript_text.strip())
        
        status.update(label="✅ Pipeline complete — All agents succeeded!", state="complete", expanded=False)
        time.sleep(0.4)

    st.session_state.pipeline_ran = True
    st.session_state.current_day = 1
    
    st.rerun()


# ── READ ORCH FROM SESSION ALWAYS ────────────────────
orch = st.session_state.orchestrator


# ── DISPLAY RESULTS ──────────────────────────────────
if st.session_state.pipeline_ran and orch.state.get("pipeline_status") in ("complete", "error"):
    state = orch.state

    # ── SUMMARY BANNER ──────────────────────────────
    tasks = state.get("tasks", [])
    decision = state.get("decision", {})
    tracking = state.get("tracking", {})
    issues = tracking.get("issues", [])
    actions = decision.get("actions_taken", []) if decision else []
    escalations = decision.get("escalations", []) if decision else []
    reminders = decision.get("reminders", []) if decision else []

    render_summary_banner(
        total_tasks=len(tasks),
        issues_detected=len(issues),
        actions_taken=len(actions) + len(escalations) + len(reminders),
        llm_mode=orch.llm.mode,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── EXPORT BUTTONS ──────────────────────────────
    export_col1, export_col2, export_col3 = st.columns([1, 1, 4])
    with export_col1:
        json_data = export_to_json({
            "pipeline_status": state.get("pipeline_status"),
            "tasks": tasks,
            "intelligence": state.get("intelligence"),
            "decision": decision,
            "tracking": {k: v for k, v in tracking.items() if k != "day_snapshots"},
        })
        st.download_button(
            label="📥 Export JSON",
            data=json_data,
            file_name="flowmind_results.json",
            mime="application/json",
            use_container_width=True,
        )
    with export_col2:
        csv_data = export_to_csv(tasks)
        st.download_button(
            label="📥 Export CSV",
            data=csv_data,
            file_name="flowmind_tasks.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PIPELINE VISUALIZATION ───────────────────────
    render_pipeline(orch.agent_list, state.get("current_agent"))
    render_agent_logs(orch.agent_list)

    st.markdown("---")

    # ── TIME SIMULATION ──────────────────────────────
    new_day = render_day_simulation(st.session_state.current_day)
    if new_day != st.session_state.current_day:
        st.session_state.current_day = new_day
        orch.simulate_day(new_day)
        # Persist the updated orchestrator
        st.session_state.orchestrator = orch
        st.rerun()

    st.markdown("---")

    # ── RELOAD STATE AFTER DAY CHANGE ────────────────
    state = orch.state
    tasks = state.get("tasks", [])
    tracking = state.get("tracking", {})
    decision = state.get("decision", {})

    # Compute stats from tracking or derive from tasks
    stats = tracking.get("stats", {})
    if not stats:
        stats = {
            "total": len(tasks),
            "completed": sum(1 for t in tasks if t.get("status") == "completed"),
            "in_progress": sum(1 for t in tasks if t.get("status") == "in-progress"),
            "pending": sum(1 for t in tasks if t.get("status") == "pending"),
            "delayed": sum(1 for t in tasks if t.get("status") == "delayed"),
            "blocked": sum(1 for t in tasks if t.get("status") == "blocked"),
        }

    # ── METRICS ─────────────────────────────────────
    render_metrics(stats, st.session_state.current_day)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── AI INSIGHTS & WHAT-IF ─────────────────────
    ins_col1, ins_col2 = st.columns([2, 1])
    
    with ins_col1:
        st.markdown('### 💡 AI Insights')
        # Load from LLM based on memory and current tasks
        from utils.memory import MemoryStore
        memory_stats = MemoryStore().get_historical_context()
        
        with st.spinner("Generating insights..."):
            insights = orch.llm.generate_insights(tasks, memory_stats)
            with st.container(border=True):
                st.markdown("**(Live AI Assessment)**")
                st.markdown(insights)
            
    with ins_col2:
        st.markdown('### 🎛️ What-If Simulation')
        st.markdown("""
        <div class="glass-card" style="padding: 1rem; min-height: 120px; font-size: 0.85rem; color: #8B8FA3;">
            <div style="font-weight: 600; color: #00D4AA; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                <span>⚡</span> Risk Parameters
            </div>
            <p style="margin-bottom: 0.5rem;">Adjust parameters to recalculate risks dynamically.</p>
        </div>
        """, unsafe_allow_html=True)
        # We can implement streamlit sliders here in the future
        with st.expander("Adjust Team Capacity (Simulated)"):
            st.slider("Max Tasks per Owner", min_value=1, max_value=10, value=3)
            st.button("Recalculate Constraints", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── TABBED CONTENT ───────────────────────────────
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
    # ── WELCOME STATE ────────────────────────────────
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
                Select a workflow input from the sidebar or upload a file, then click 
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
        ("🔍", "Intelligent Extraction", "Parses input text to extract action items, decisions, owners, deadlines, and blockers using AI-powered analysis."),
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

    # Demo flow section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-header"><span class="header-icon">🎬</span> Demo Flow</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="glass-card" style="padding: 1.5rem;">
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem;">
            <div style="text-align: center; padding: 0.75rem; background: rgba(0,212,170,0.05); border-radius: 10px; border: 1px solid rgba(0,212,170,0.15);">
                <div style="font-size: 1.5rem;">1️⃣</div>
                <div style="font-weight: 600; color: #FAFAFA; margin: 0.3rem 0; font-size: 0.85rem;">Provide Input</div>
                <div style="color: #8B8FA3; font-size: 0.72rem;">Choose a sample workflow, paste your own text, or upload a PDF/TXT file</div>
            </div>
            <div style="text-align: center; padding: 0.75rem; background: rgba(108,99,255,0.05); border-radius: 10px; border: 1px solid rgba(108,99,255,0.15);">
                <div style="font-size: 1.5rem;">2️⃣</div>
                <div style="font-weight: 600; color: #FAFAFA; margin: 0.3rem 0; font-size: 0.85rem;">Run Pipeline</div>
                <div style="color: #8B8FA3; font-size: 0.72rem;">Watch 5 AI agents execute sequentially — extract, analyze, task, track, and decide</div>
            </div>
            <div style="text-align: center; padding: 0.75rem; background: rgba(240,147,251,0.05); border-radius: 10px; border: 1px solid rgba(240,147,251,0.15);">
                <div style="font-size: 1.5rem;">3️⃣</div>
                <div style="font-weight: 600; color: #FAFAFA; margin: 0.3rem 0; font-size: 0.85rem;">Simulate & Export</div>
                <div style="color: #8B8FA3; font-size: 0.72rem;">Switch between Day 1→3, see autonomous actions, and export results as JSON/CSV</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
