# FlowMind AI — Autonomous Workflow Orchestrator

<p align="center">
  <strong>🧠 A multi-agent AI system that transforms unstructured text into a fully managed, autonomous workflow</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/Groq-LLaMA_3.3_70B-F55036?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Agents-5_Stage_Pipeline-00D4AA?style=for-the-badge" />
</p>

---

## Problem

Manual workflow management is **inefficient** and requires constant human coordination. Teams waste hours:
- Tracking action items across meetings and documents
- Identifying risks and dependencies manually
- Following up on overdue tasks
- Reassigning work when bottlenecks emerge

## Solution

FlowMind AI uses a **5-agent autonomous pipeline** to:
1. **Extract** structured tasks from any text input
2. **Analyze** priorities, risks, and dependencies
3. **Execute** structured workflow task creation
4. **Track** progress with time simulation (Day 1→3)
5. **Decide** autonomous corrective actions (assign, escalate, remind)

All with **zero human intervention** once initiated.

---

## Architecture

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────┐     ┌──────────────┐     ┌──────────────┐
│  Extraction  │ ──▶ │  Intelligence    │ ──▶ │  Execution    │ ──▶ │  Tracking    │ ──▶ │  Decision    │
│    Agent     │     │     Agent        │     │    Agent      │     │    Agent     │     │    Agent     │
│              │     │                  │     │               │     │              │     │              │
│  🔍 Parse    │     │  🧠 Risks &     │     │  ⚡ Create    │     │  📊 Simulate │     │  🤖 Auto-    │
│  input text  │     │  dependencies   │     │  tasks        │     │  Day 1→3     │     │  assign,     │
│              │     │                  │     │               │     │              │     │  escalate    │
└──────────────┘     └──────────────────┘     └───────────────┘     └──────────────┘     └──────────────┘
```

---

## Features

| Feature | Description |
|---------|-------------|
| 🔍 **Intelligent Extraction** | AI-powered parsing of unstructured text into action items, decisions, owners, and deadlines |
| 🧠 **Risk Intelligence** | Detects missing owners, overloaded team members, blockers, and dependency chains |
| ⚡ **Task Automation** | Converts raw data into structured tasks with P0/P1/P2 priorities and risk flags |
| 📊 **Time Simulation** | Deterministic Day 1→3 progression with bottleneck detection |
| 🤖 **Autonomous Decisions** | Auto-assigns unowned tasks, escalates delays, sends reminders, redistributes workload |
| 📜 **Full Audit Trail** | Every agent action logged with timestamps and reasoning |
| 📎 **File Input Support** | Upload PDF or TXT files as workflow input |
| 📥 **Export Results** | Download results as JSON or CSV |
| 💾 **Persistent Memory** | Historical owner performance tracking for predictive analysis |
| 🔮 **Predictive Delays** | Forecasts which tasks will be delayed based on historical patterns |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit (dark theme, glassmorphism UI) |
| **LLM** | Groq — LLaMA 3.3 70B Versatile (with rule-based fallback) |
| **Charts** | Plotly |
| **Persistence** | JSON file store |
| **Language** | Python 3.10+ |

---

## Project Structure

```
flowmind-ai/
├── streamlit_app.py          # UI entry point
├── orchestrator/
│   └── orchestrator.py       # Central pipeline controller
├── agents/
│   ├── base.py               # Abstract base agent
│   ├── extraction.py         # Stage 1: Input parsing
│   ├── intelligence.py       # Stage 2: Risk analysis
│   ├── execution.py          # Stage 3: Task structuring
│   ├── tracking.py           # Stage 4: Time simulation
│   └── decision.py           # Stage 5: Autonomous actions
├── schemas/
│   └── state.py              # Shared WorkflowState dataclass
├── utils/
│   ├── llm.py                # Groq client + fallback engine
│   ├── memory.py             # Persistent memory store
│   ├── logger.py             # Audit trail logger
│   ├── helpers.py            # File upload + export utilities
│   └── integrations.py       # Mock Slack/Email integrations
├── components/               # Streamlit UI components
├── data/
│   ├── sample_inputs.txt     # Sample workflow inputs
│   └── memory.json           # Auto-generated memory store
├── notebooks/
│   └── explanation.md        # Architecture documentation
├── README.md
├── requirements.txt
└── .env.example
```

---

## How to Run

### 1. Clone & Setup
```bash
git clone https://github.com/your-username/FlowMind-AI-Agent
cd flowmind-ai
pip install -r requirements.txt
```

### 2. Configure Environment (Optional)
```bash
cp .env.example .env
# Edit .env and add your Groq API key
# The system works without it using a rule-based fallback engine
```

### 3. Run
```bash
streamlit run streamlit_app.py
```

### 4. Demo Flow
1. **Select input** — Choose a sample workflow or upload your own file
2. **Run pipeline** — Watch 5 AI agents execute sequentially
3. **Simulate days** — Switch between Day 1→3 to see task progression
4. **Export results** — Download as JSON or CSV

---

## API Access (Optional)

```bash
uvicorn api:app --reload
```

Endpoints:
- `POST /api/v1/orchestrate` — Run the full pipeline
- `GET /api/v1/memory/stats` — Historical intelligence
- `GET /health` — System health check

---

## Key Design Decisions

1. **LLM + Fallback**: Every Groq call has a deterministic rule-based fallback, ensuring the system works offline
2. **Deterministic Simulation**: Tracking Agent uses index-based logic (not random) for consistent demo behavior
3. **Zero-Config**: System runs out of the box without any API keys
4. **Explainable AI**: Every autonomous decision includes full reasoning in the audit trail


---

# Deployed Link

https://flowmind-ai.streamlit.app/