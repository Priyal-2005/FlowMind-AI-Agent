# 🎯 Autonomous Meeting → Action Orchestrator

> **An evolving AI system with memory, predictive intelligence, and autonomous decision-making — simulating a real enterprise command center.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)](https://streamlit.io)
[![Architecture](https://img.shields.io/badge/Architecture-Multi--Agent-purple)]()
[![LLM](https://img.shields.io/badge/LLM-Gemini%202.0%20Flash-green)](https://ai.google.dev)
[![Live Demo](https://img.shields.io/badge/Live%20App-Streamlit-orange)](https://autonomous-meeting-orchestrator.streamlit.app/)

---

## 🎬 Demo Highlight — 10 Second Overview

> **Input:** A raw meeting transcript (pasted or selected from samples)  
> **Output:** A full autonomous enterprise workflow, end-to-end

| Step | What Happens |
|------|-------------|
| 1 | **5 AI agents execute** sequentially in real-time |
| 2 | Tasks are **extracted**, **risk-scored**, and **structured** |
| 3 | **Time simulation** runs: Day 1 → Day 2 → Day 3 |
| 4 | System **detects** delays, blockers, missing owners |
| 5 | System **TAKES ACTIONS** — not suggestions — autonomously |
| 6 | Every decision is **logged** with full reasoning |

Click **"⚡ Auto Demo"** in the sidebar for a one-click full walkthrough.

---

## 🏆 Why This Project Wins

| Traditional AI Tools | This System |
|---|---|
| Extract info from meetings | ✅ Extracts **AND executes** workflows |
| Give insights and suggestions | ✅ Takes **autonomous corrective actions** |
| Static snapshots | ✅ **Time-aware simulation** (Day 1 → 3) |
| React after problems happen | ✅ **Predicts delays before they occur** |
| One-shot analysis | ✅ **Persistent memory** across runs |
| Single model | ✅ **Multi-agent orchestration** with specialised roles |

This is not a chatbot. This is not an analytics dashboard.  
**This is a full agentic workflow engine that acts like an autonomous project manager.**

---

## 🚀 Quick Start

```bash
# 1. Clone and install
pip install -r requirements.txt

# 2. Optional: Add Gemini API key for AI-powered decisions
cp .env.example .env
# Add your GEMINI_API_KEY to .env — works fully without it too

# 3. Run
streamlit run app.py
```

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Intelligent Extraction** | Rule-based NLP + Gemini parses dialogue-style transcripts with speaker recognition |
| 🧠 **Risk Intelligence** | Detects missing owners, overloaded team members, blockers, and dependency chains |
| ⚡ **Task Automation** | Creates structured P0/P1/P2 tasks with deadlines, risk flags, and ownership |
| 📊 **Time Simulation** | Deterministic Day 1→3 simulation with realistic status progression |
| 🤖 **Autonomous Actions (LLM-powered)** | Auto-assigns owners, escalates P0s, redistributes overloaded tasks, sends reminders |
| 🔮 **Predictive AI** | Anticipates delays before they occur using heuristics + historical memory |
| 💾 **Persistent Memory** | Tracks owner performance and task history across runs |
| 🔔 **Mock Integrations** | Simulated Slack notifications and Email escalations |
| 📜 **Full Audit Trail** | Chronological log of every agent decision with reasoning |
| 🎯 **Works Offline** | Full functionality without any API key via Smart Extraction Engine |

---

## ⚡ Autonomous Execution Engine (Not Just AI Insights)

This is the core differentiator. The **Decision Agent** does not generate suggestions — it **executes real corrective actions** automatically:

- 👤 **Auto-assigns** unowned tasks to the least-loaded available team member
- 🔄 **Reassigns** tasks when an owner is overloaded (≥3 concurrent tasks)
- 🚨 **Escalates** P0/P1 blockers to the Engineering Manager via mock Email
- 🔔 **Sends reminders** to task owners on delay or stall detection
- 🧠 **Uses Gemini AI** to reason about optimal actions contextually (fallback to deterministic rules if no API key)

Every action is logged in the Audit Trail with its full reasoning chain.

---

## 🧠 Advanced Capabilities (Phase 2)

| Capability | Description |
|---|---|
| **Persistent Memory System** | Stores tasks across runs; tracks owner delay rate and completion rate via `data/memory.json` |
| **Predictive Risk Intelligence** | Scores tasks with delay probability scores before Day 3 based on priority, assignment, stall detection, and historical performance |
| **LLM Decision Engine** | Gemini `decide_actions()` generates contextual JSON decisions; deterministic fallback if no API key |
| **Real-World Integrations (Mocked)** | `send_slack_message` + `send_email` emit to Audit Trail + `st.toast` pop-ups; demonstrates production readiness |
| **Adaptive Learning** | `Intelligence Agent` adjusts bottleneck thresholds using each owner's historical delay rate from Memory |

---

## 🏗️ Architecture

### 1 Orchestrator + 5 Specialised Agents

```
┌─────────────────────────────────────────────────────────────┐
│            🎯 ORCHESTRATOR (Central Brain)                   │
│  Routes data, manages global state, handles errors           │
└─────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────┐   ┌──────────────────┐   ┌──────────────────┐
│ 🔍           │ → │ 🧠               │ → │ ⚡               │
│  Extraction  │   │  Intelligence    │   │  Execution       │
│  Agent       │   │  Agent           │   │  Agent           │
└──────────────┘   └──────────────────┘   └──────────────────┘
  Parse transcript   Risk & gap analysis    Create P0/P1/P2
  Extract owners,    Missing owners,        task objects with
  tasks, blockers    dependencies, scores   metadata
         │
         ▼
┌──────────────┐   ┌────────────────────────────────────────────┐
│ 📊           │ → │ 🤖                                         │
│  Tracking    │   │  Decision Agent                             │
│  Agent       │   │  (Autonomous Action Engine)                 │
└──────────────┘   └────────────────────────────────────────────┘
  Time simulation    Takes corrective actions — assigns, escalates,
  Day 1 → 3         redistributes, reminds. Powered by Gemini AI.
         │
         ▼
┌──────────────────────────────────────────────────────────────┐
│  📜 Audit Logger — Full decision trail with reasoning        │
│  💾 Memory Layer — Persists tasks + owner metrics to JSON    │
└──────────────────────────────────────────────────────────────┘
```

### Agent Roles

| Agent | Role | Input | Output |
|---|---|---|---|
| **🎯 Orchestrator** | Central brain + state manager | Transcript | Coordinates all agents |
| **🔍 Extraction** | Parses raw transcript | Raw text | Action items, owners, deadlines, blockers |
| **🧠 Intelligence** | Risk + gap analysis | Extracted data | Risk scores, missing owners, dependency chains |
| **⚡ Execution** | Task structuring | Extracted + intelligence data | Structured P0/P1/P2 task objects |
| **📊 Tracking** | Time simulation engine | Tasks + target day | Updated tasks: progress, delays, blocked states |
| **🤖 Decision** | Autonomous action engine | Tasks + issues | Actions, escalations, reminders, reassignments |

### Data Flow

```
Transcript  →  [Extraction]   →  ActionItems, Owners, Blockers, Deadlines
            →  [Intelligence] →  Risks, MissingOwners, Overloads, Dependencies
            →  [Execution]    →  StructuredTasks[id, priority, status, risk_flag]
            →  [Tracking]     →  UpdatedTasks[progress, delays, predicted_risk]
            →  [Decision]     →  Actions[auto-assign, escalate, remind, redistribute]
            →  [Audit + Mem]  →  Full transparency log + persistent JSON store
```

### LLM Strategy — Dual Mode

| Mode | Behaviour |
|---|---|
| **With Gemini API Key** | Uses `gemini-2.0-flash` for extraction, risk analysis, action decisions, and AI insights |
| **Without API Key (default)** | Smart Extraction Engine: multi-pass regex + speaker commitment detection. Decision Agent falls back to deterministic heuristics. Full functionality guaranteed. |

---

## 🧠 Persistent Memory Layer

Built at `utils/memory.py`, backed by `data/memory.json`:

- **Saves** all tasks and actions from every pipeline run
- **Tracks** per-owner metrics: `delay_rate`, `completion_rate`, `total_tasks`
- **Feeds** the Intelligence Agent for smarter bottleneck detection
- **Powers** the Tracking Agent's predictive delay scoring
- **Reset** anytime with the "🗑️ Wipe Database" button in the sidebar

---

## 🎬 Demo Flow

**1. Select a Transcript**
- Choose from 3 realistic enterprise scenarios in the sidebar
- Use **"Crisis Response — Missing Owners"** for maximum autonomous action

**2. Run the Pipeline**
- Click **"🚀 Run Autonomous Workflow"**
- Watch 5 agents execute sequentially with a live status bar

**3. Explore the Dashboard**
- **📋 Task Registry** — Tasks with status, priority, risk, predicted delay badges, and AI-decision tags
- **📊 Analytics** — Status distribution, priority breakdown, owner workload charts
- **🤖 Autonomous Actions** — Every action taken by the Decision Agent with reasoning
- **📜 Audit Trail** — Full chronological log of every agent decision

**4. Simulate Time**
- Click **Day 1 → Day 2 → Day 3**
- Watch delays emerge, escalations trigger, and auto-reassignments happen

**5. AI Insights Panel**
- Live Gemini-generated summary of team health, bottlenecks, and suggested optimisations

---

## 📁 Project Structure

```
autonomous-meeting-orchestrator/
├── app.py                    # Main Streamlit application + Phase 2 UI panels
├── orchestrator.py           # Central orchestrator controller
├── api.py                    # FastAPI endpoints (/orchestrate, /memory/stats)
├── requirements.txt
├── .env.example
│
├── agents/
│   ├── base.py               # Abstract BaseAgent class
│   ├── extraction.py         # Extraction Agent
│   ├── intelligence.py       # Intelligence Agent (memory-aware)
│   ├── execution.py          # Execution Agent
│   ├── tracking.py           # Tracking Agent (time sim + predictive risk)
│   └── decision.py           # Decision Agent (LLM-powered autonomous actions)
│
├── components/
│   ├── styles.py             # CSS glassmorphism dark theme
│   ├── pipeline.py           # Pipeline visualisation component
│   ├── dashboard.py          # Task registry, metrics, charts, actions panel
│   └── audit.py              # Audit trail component
│
├── data/
│   ├── transcripts.py        # 3 sample meeting transcripts
│   └── memory.json           # Persistent memory store (auto-generated)
│
└── utils/
    ├── llm.py                # LLM client: Gemini + decide_actions + generate_insights
    ├── memory.py             # Persistent memory: save_run, get_owner_stats
    ├── integrations.py       # Mock Slack + Email integrations
    └── logger.py             # Audit logger (AuditEntry, AuditLogger)
```

---

## 🎭 Sample Transcripts

| Transcript | Complexity | Best For |
|---|---|---|
| **Sprint Planning** | Simple | Clean workflow, all tasks assigned |
| **Q4 Product Review** | Medium | Blocker detection, dependency chains |
| **Crisis Response** | 🔥 High | Max autonomous actions, missing owners, escalations |

---

## 📊 Business Impact

For a 100-person engineering team:

| Metric | Value |
|---|---|
| Time saved per employee | ⏱️ 2.5 hrs/week |
| Total team hours recovered | 📊 250 hrs/week |
| Value recovered | 💰 ₹5 lakh/week |
| Projected annual savings | 🚀 ₹2.6 Cr/year |

---

## 🏢 Enterprise Readiness

- ✅ **Modular multi-agent architecture** — each agent independently testable and replaceable
- ✅ **Offline-first** — full functionality with zero API dependency
- ✅ **Audit trail** — every decision logged with reasoning for compliance
- ✅ **Persistent memory** — cross-session intelligence, not just one-shot processing
- ✅ **Integration-ready** — Slack, Email, and REST API (`api.py`) scaffolded
- ✅ **Deterministic simulation** — reproducible Day 1→3 for consistent demos

---

## 🔧 Configuration

```env
# .env
GEMINI_API_KEY=your_key_here  # Optional — full functionality works without it
```

---

## 📦 Requirements

```
streamlit>=1.32.0
plotly>=5.18.0
python-dotenv>=1.0.0
google-generativeai>=0.5.0   # Optional — for Gemini AI mode
fastapi                       # Optional — for REST API mode
uvicorn                       # Optional — for REST API mode
```

---

## 🔭 Future Scope

- **Real Slack/Email webhooks** — swap mocks for live API calls with minimal changes
- **Calendar integration** — auto-schedule follow-up meetings based on blocked tasks
- **Multi-meeting memory** — track project health across sprints, not just single meetings
- **Role-based access** — per-owner dashboards and notification preferences
- **Advanced LLM routing** — use different models per agent based on cost/accuracy tradeoffs

---

## 🤝 Architecture Principles

1. **Modularity** — Each agent is independently testable and replaceable
2. **Graceful Degradation** — Every agent has a deterministic fallback (no API required)
3. **Auditability** — Every decision is logged with full reasoning and timestamp
4. **Determinism** — Time simulation produces consistent results for demo reliability
5. **Autonomy** — Decision agent always acts — never passive, always adds value
6. **Memory** — System learns and improves with each run

---

## 🌐 Live Demo

**[https://autonomous-meeting-orchestrator.streamlit.app/](https://autonomous-meeting-orchestrator.streamlit.app/)**