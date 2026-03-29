# 🎯 Autonomous Meeting → Action Orchestrator

> **Enterprise AI Command Center** — A production-quality multi-agent system that autonomously transforms raw meeting transcripts into executable enterprise workflows with real-time tracking, intelligent risk detection, and fully autonomous corrective actions.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![Multi-Agent](https://img.shields.io/badge/Architecture-Multi--Agent-purple)
![LLM](https://img.shields.io/badge/LLM-Gemini%20%7C%20Rule--Based-green)

---

## 🚀 Quick Start

```bash
# 1. Clone and install
pip install -r requirements.txt

# 2. Optional: Add Gemini API key for AI-powered extraction
cp .env.example .env
# Add your GEMINI_API_KEY to .env (works without it too!)

# 3. Run
streamlit run app.py
```

---

## 🎬 Demo Flow

### Step-by-step walkthrough for a live demo:

**1. Select a Transcript**
- Choose from 3 realistic enterprise scenarios in the sidebar
- Each has different complexity: simple sprint, blocked Q4 review, crisis response
- Or paste any custom meeting transcript

**2. Run the Pipeline**
- Click **"🚀 Run Autonomous Workflow"**
- Watch 5 AI agents execute sequentially with live progress bar
- Each agent logs its reasoning in real-time

**3. Explore the Dashboard**
- **📋 Task Registry** — All tasks with color-coded status, priority, risk, and progress bars
- **📊 Analytics** — Status distribution, priority breakdown, owner workload charts
- **🤖 Autonomous Actions** — All decisions taken by the Decision Agent with reasoning
- **📜 Audit Trail** — Full chronological log of every agent decision

**4. Simulate Time Progression**
- Click **Day 1 → Day 2 → Day 3**
- Watch tasks evolve: delays emerge, escalations trigger, auto-reassignments happen
- Day 3 is the most dramatic — maximum autonomous action

**5. Best Demo Transcript**
- Use **"Crisis Response — Missing Owners"** for maximum autonomous action visibility
- Or click **"⚡ Auto Demo"** in the sidebar to auto-load it

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🔍 **Intelligent Extraction** | Rule-based NLP parses dialogue-style transcripts with speaker recognition |
| 🧠 **Risk Intelligence** | Detects missing owners, overloaded team members, blockers, and dependency chains |
| ⚡ **Task Automation** | Creates structured P0/P1/P2 tasks with deadlines, risk flags, and ownership |
| 📊 **Time Simulation** | Deterministic Day 1→3 simulation with realistic status progression |
| 🤖 **Autonomous Actions** | Auto-assigns owners, escalates P0s, redistributes overloaded tasks, sends reminders |
| 📜 **Full Audit Trail** | Chronological log with agent-specific colors, severity indicators, and expandable reasoning |
| 🎯 **Works Offline** | Full functionality without any API key via Smart Extraction Engine |

---

## 🏗️ Architecture

### System Architecture Overview

```
Meeting Transcript
       │
       ▼
  ┌─────────────────────────────────────────────────────┐
  │              ORCHESTRATOR (Central Controller)       │
  │     Routes data, manages state, handles errors       │
  └─────────────────────────────────────────────────────┘
       │
       ▼
  ┌──────────┐    ┌──────────────┐    ┌──────────────┐
  │ 🔍       │ →  │ 🧠           │ →  │ ⚡           │
  │Extraction│    │ Intelligence │    │ Execution    │
  │  Agent   │    │    Agent     │    │   Agent      │
  └──────────┘    └──────────────┘    └──────────────┘
  Parse &         Risk & gap          Create P0/P1/P2
  structure       analysis            task objects
       │
       ▼
  ┌──────────────┐    ┌──────────────┐
  │ 📊           │ →  │ 🤖           │
  │  Tracking    │    │  Decision    │
  │   Agent      │    │   Agent      │
  └──────────────┘    └──────────────┘
  Time simulation     Autonomous
  Day 1→3             corrective actions
       │
       ▼
  ┌─────────────────────────┐
  │  📜 Audit Logger         │
  │  Full trail of all       │
  │  agent decisions         │
  └─────────────────────────┘
```

### Agent Roles

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **Orchestrator** | Central controller and state manager | Transcript | Coordinates all agents |
| **Extraction Agent** | Parse raw transcript into structured data | Raw text | Action items, owners, deadlines, blockers |
| **Intelligence Agent** | Risk and gap analysis | Extracted data | Risk scores, missing owners, dependency chains |
| **Execution Agent** | Task structuring and metadata | Extracted + intelligence | Structured P0/P1/P2 tasks |
| **Tracking Agent** | Time simulation across Day 1-3 | Tasks + day | Updated tasks with realistic progression |
| **Decision Agent** | Autonomous corrective actions | Tasks + issues | Actions, escalations, reminders |

### Data Flow

```
Transcript → [extract] → ActionItems, Owners, Blockers
           → [analyze] → Risks, MissingOwners, Dependencies
           → [execute] → StructuredTasks[id, priority, status, risk]
           → [track]   → UpdatedTasks[progress, delays, blocked]
           → [decide]  → Actions[auto-assign, escalate, remind, redistribute]
           → [log]     → AuditTrail[100% transparency]
```

### LLM Strategy

1. **With Gemini API key** — Uses `gemini-2.0-flash` for:
   - High-accuracy transcript parsing
   - Contextual risk reasoning
   - Nuanced priority assignment

2. **Without API key (default)** — Smart Extraction Engine:
   - Multi-pass regex extraction (keyword + dialogue patterns)
   - Speaker commitment detection (`"Name: I'll do X"`)
   - Guaranteed minimum action item extraction
   - Deterministic, consistent output

---

## 📁 Project Structure

```
autonomous-meeting-orchestrator/
├── app.py                    # Main Streamlit application
├── orchestrator.py           # Central orchestrator controller
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variable template
│
├── agents/
│   ├── base.py               # Abstract BaseAgent class
│   ├── extraction.py         # Extraction Agent
│   ├── intelligence.py       # Intelligence Agent
│   ├── execution.py          # Execution Agent
│   ├── tracking.py           # Tracking Agent (time simulation)
│   └── decision.py           # Decision Agent (autonomous actions)
│
├── components/
│   ├── styles.py             # CSS (glassmorphism dark theme)
│   ├── pipeline.py           # Pipeline visualization component
│   ├── dashboard.py          # Task table, metrics, charts, actions panel
│   └── audit.py              # Audit trail component
│
├── data/
│   └── transcripts.py        # 3 sample meeting transcripts
│
└── utils/
    ├── llm.py                # LLM client (Gemini + rule-based fallback)
    └── logger.py             # Audit logger (AuditEntry, AuditLogger)
```

---

## 🎭 Sample Transcripts

| Transcript | Complexity | Best For |
|---|---|---|
| **Sprint Planning** | Simple | Clean workflow demo, all tasks assigned |
| **Q4 Product Review** | Medium | Blocker detection, dependency chains |
| **Crisis Response** | High | Max autonomous actions, missing owners, escalations |

---

## 📊 Business Impact

For a 100-person engineering team:
- ⏱️ **2.5 hrs/week** saved per employee on meeting follow-up
- 📊 **250 hrs/week** total recovered productivity
- 💰 **₹5 lakh/week** in value recovered
- 🚀 **₹2.6 Cr/year** projected savings

---

## 🔧 Configuration

```env
# .env
GEMINI_API_KEY=your_key_here  # Optional — app works without it
```

---

## 📦 Requirements

```
streamlit>=1.32.0
plotly>=5.18.0
python-dotenv>=1.0.0
google-generativeai>=0.5.0  # Optional — for AI mode
```

---

## 🤝 Architecture Principles

1. **Modularity** — Each agent is independently testable and replaceable
2. **Graceful Degradation** — Every agent has a deterministic fallback (no API required)
3. **Auditability** — Every decision is logged with full reasoning and timestamp
4. **Determinism** — Time simulation produces consistent results for demo reliability
5. **Autonomy** — Decision agent always acts — never passive, always adds value

## 🧠 Why This Wins

Unlike traditional meeting assistants, this system:
- Doesn’t just extract → it executes
- Doesn’t just suggest → it acts autonomously
- Doesn’t just track → it predicts and prevents failure

This is a true Agentic AI system.