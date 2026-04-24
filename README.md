# FlowMind AI

**Autonomous Workflow Orchestrator** — Turn unstructured meeting notes, emails, or briefs into tracked tasks, simulated timelines, and autonomous corrective actions across a **five-agent** pipeline.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Streamlit-1.40+-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit" />
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/Groq-LLM-optional-F55036?style=flat-square" alt="Groq" />
</p>

---

## Why FlowMind?

| Pain | FlowMind response |
|------|-------------------|
| Action items buried in text | **Extraction** agent structures owners, deadlines, and priorities |
| Risk blind spots | **Intelligence** agent scores overload, blockers, and dependencies |
| No single task view | **Execution** agent builds a P0/P1/P2 registry |
| “How does Day 3 look?” | **Tracking** agent simulates Day 1 → 3 deterministically |
| Nobody follows up | **Decision** agent auto-assigns, escalates, and reminds (LLM or rules) |

---

## Features

- **Multi-agent pipeline** — Extraction → Intelligence → Execution → Tracking → Decision under one orchestrator
- **Autonomous decisions** — Assignments, reassignments, escalations, reminders with audit-friendly records
- **Groq LLM + rule fallback** — Set `GROQ_API_KEY` for LLM mode; omit it for deterministic **Smart Extraction Engine** behavior
- **Time simulation** — Interactive Day 1–3 replays after a successful run
- **Persistent memory** — JSON-backed owner stats for predictive hints (`data/memory.json`)
- **FastAPI** — `POST /api/v1/orchestrate` for headless runs
- **Streamlit SaaS-style UI** — Dark theme, metrics, task cards, actions panel, exports

### Feature Description

🔍 Intelligent Extraction	
AI-powered parsing of unstructured text into action items, decisions, owners, and deadlines

🧠 Risk Intelligence
Detects missing owners, overloaded team members, blockers, and dependency chains

⚡ Task Automation
Converts raw data into structured tasks with P0/P1/P2 priorities and risk flags

📊 Time Simulation	
Deterministic Day 1→3 progression with bottleneck detection

🤖 Autonomous Decisions	
Auto-assigns unowned tasks, escalates delays, sends reminders, redistributes workload

📜 Full Audit Trail
Every agent action logged with timestamps and reasoning

📎 File Input Support
Upload PDF or TXT files as workflow input

📥 Export Results
Download results as JSON or CSV

💾 Persistent Memory
Historical owner performance tracking for predictive analysis

🔮 Predictive Delays
Forecasts which tasks will be delayed based on historical patterns

---

## Architecture

```
                    ┌─────────────────────────────────────┐
                    │     WorkflowOrchestrator            │
                    │  (state, routing, error handling)   │
                    └─────────────────────────────────────┘
                                        │
    ┌───────────┬───────────┬───────────┼───────────┬───────────┐
    ▼           ▼           ▼           ▼           ▼           │
 Extraction  Intelligence Execution  Tracking   Decision        │
    │           │           │           │           │           │
    └───────────┴───────────┴───────────┴───────────┴───────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
        utils/llm.py        utils/memory.py
     (Groq + fallback)     (JSON persistence)
```

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────┐     ┌──────────────┐     ┌──────────────┐
│  Extraction  │ ──▶ │  Intelligence    │ ──▶ │  Execution    │ ──▶ │  Tracking    │ ──▶ │  Decision    │
│    Agent     │     │     Agent        │     │    Agent      │     │    Agent     │     │    Agent     │
│              │     │                  │     │               │     │              │     │              │
│  🔍 Parse    │      │  🧠 Risks &      │     │ ⚡ Create      │     │  📊 Simulate │     │  🤖 Auto-    │
│  input text  │     │  dependencies    │     │  tasks        │     │  Day 1→3     │     │  assign,     │
│              │     │                  │     │               │     │              │     │  escalate    │
└──────────────┘     └──────────────────┘     └───────────────┘     └──────────────┘     └──────────────┘
```

---

## Tech stack

| Layer | Stack |
|-------|--------|
| UI | Streamlit, Plotly, custom CSS (glass / gradient) |
| Orchestration | Python, central `WorkflowOrchestrator` |
| LLM | Groq (`llama-3.3-70b-versatile`) optional |
| API | FastAPI + Pydantic v2 |
| Persistence | JSON file (`data/memory.json`) |

---

## Repository layout

```
flowmind-ai-agent/
├── agents/              # Five pipeline agents + BaseAgent
├── orchestrator/        # WorkflowOrchestrator
├── utils/               # llm, memory, logger, helpers, integrations
├── components/          # Streamlit UI (dashboard, pipeline, styles, audit)
├── data/                # Sample transcripts, generated memory.json
├── schemas/             # Shared state types
├── api.py               # FastAPI app
├── streamlit_app.py     # Streamlit entrypoint
├── requirements.txt
├── README.md
├── .env.example
├── .streamlit/config.toml
```

---

## Setup

### 1. Clone and install

```bash
git clone <your-repo-url> flowmind-ai
cd flowmind-ai
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment (optional LLM)

```bash
cp .env.example .env
# Edit .env — add GROQ_API_KEY for Groq-powered extraction/decisions
```

Without a key, the app uses the **rule-based** extraction and decision paths (no external LLM calls).

### 3. Run Streamlit (primary)

```bash
streamlit run streamlit_app.py
```

Open the URL shown in the terminal (default `http://localhost:8501`).

### 4. Run FastAPI (optional)

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

---

## API usage

**Orchestrate** (non-empty JSON body required):

```bash
curl -s -X POST "http://localhost:8000/api/v1/orchestrate" \
  -H "Content-Type: application/json" \
  -d '{"input_text":"Alice owns the API integration by Friday. Bob is blocked on auth."}' | jq .
```

Example success shape (abridged):

```json
{
  "status": "success",
  "tasks_generated": 4,
  "intelligence_risks": 3,
  "actions": {
    "auto_assignments": 2,
    "escalations": 0,
    "reminders": 1
  }
}
```

Empty `input_text` returns **422** validation error.

**Memory stats:**

```bash
curl -s "http://localhost:8000/api/v1/memory/stats" | jq .
```

**Health:**

```bash
curl -s "http://localhost:8000/health" | jq .
```

---

## Deploy

### Streamlit Community Cloud

1. Push this repo to GitHub.
2. In [Streamlit Cloud](https://streamlit.io/cloud), **New app** → select repo, main file: `streamlit_app.py`.
3. **Secrets**: add `GROQ_API_KEY` in app secrets if you want LLM mode (optional).
4. Deploy. Set Python version to **3.10+** in `packages.txt` or Cloud settings if needed.

### Local production-ish run

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

Pin your public app URL here after deploy (for example Streamlit Cloud): `https://your-app.streamlit.app`

---

# Deployed Link
https://flowmind-ai-agent-autonomous-workflow-orchestrator.streamlit.app/