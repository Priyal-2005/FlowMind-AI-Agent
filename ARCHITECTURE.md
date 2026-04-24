# FlowMind AI — Architecture Explanation

## Overview

FlowMind AI is a **multi-agent autonomous workflow orchestrator** that processes unstructured text input and transforms it into a fully managed, trackable workflow — complete with risk analysis, task structuring, time simulation, and autonomous decision-making.

## Agent Pipeline

The system runs a **5-stage sequential pipeline**, where each agent builds on the output of the previous one:

```
┌──────────────┐     ┌──────────────────┐     ┌───────────────┐     ┌──────────────┐     ┌──────────────┐
│  Extraction  │ ──▶ │  Intelligence    │ ──▶ │  Execution    │ ──▶ │  Tracking    │ ──▶ │  Decision    │
│    Agent     │     │     Agent        │     │    Agent      │     │    Agent     │     │    Agent     │
├──────────────┤     ├──────────────────┤     ├───────────────┤     ├──────────────┤     ├──────────────┤
│ Parses raw   │     │ Detects risks,   │     │ Creates       │     │ Simulates    │     │ Takes auto   │
│ input into   │     │ missing owners,  │     │ structured    │     │ Day 1→3      │     │ actions:     │
│ action items,│     │ dependencies,    │     │ tasks with    │     │ progression, │     │ assign,      │
│ decisions,   │     │ and overloaded   │     │ priorities,   │     │ detects      │     │ escalate,    │
│ owners       │     │ team members     │     │ risk flags    │     │ issues       │     │ remind       │
└──────────────┘     └──────────────────┘     └───────────────┘     └──────────────┘     └──────────────┘
```

## Agent Details

### 1. Extraction Agent (`agents/extraction.py`)
- **Input**: Raw text (pasted or uploaded)
- **Output**: Structured data — action items, decisions, owners, deadlines, blockers
- **How**: Uses Groq LLM when available, falls back to regex-based NLP extraction

### 2. Intelligence Agent (`agents/intelligence.py`)
- **Input**: Extracted data from Stage 1
- **Output**: Risk assessment — missing owners, overloaded members, dependency chains, risk scores
- **How**: Combines rule-based analysis with historical memory data and LLM risk scoring

### 3. Execution Agent (`agents/execution.py`)
- **Input**: Extracted data + Intelligence analysis
- **Output**: Structured task objects with IDs, priorities (P0/P1/P2), deadlines, risk flags
- **How**: Maps raw action items to executable tasks with proper metadata

### 4. Tracking Agent (`agents/tracking.py`)
- **Input**: Task list + simulation day
- **Output**: Updated tasks with status changes, progress percentages, detected issues
- **How**: Deterministic time simulation (Day 1→3) with predictive delay analysis

### 5. Decision Agent (`agents/decision.py`)
- **Input**: Tasks + detected issues + intelligence context
- **Output**: Autonomous actions — auto-assignments, escalations, reminders, redistributions
- **How**: LLM-driven decision engine with deterministic fallback rules

## Key Design Decisions

1. **LLM + Fallback Architecture**: Every LLM call has a rule-based fallback, so the system works offline or without an API key.

2. **Deterministic Simulation**: The Tracking Agent uses deterministic logic (not random) for consistent demo behavior across runs.

3. **Memory System**: A lightweight JSON-based persistence layer (`data/memory.json`) tracks historical owner performance to improve predictions.

4. **Audit Trail**: Every agent action is logged with timestamps and reasoning for full transparency.

## File Structure

```
flowmind-ai/
├── streamlit_app.py          # Streamlit UI entry point
├── orchestrator/
│   └── orchestrator.py       # Central pipeline controller
├── agents/
│   ├── base.py               # Abstract base agent class
│   ├── extraction.py         # Stage 1: Input parsing
│   ├── intelligence.py       # Stage 2: Risk analysis
│   ├── execution.py          # Stage 3: Task structuring
│   ├── tracking.py           # Stage 4: Time simulation
│   └── decision.py           # Stage 5: Autonomous actions
├── schemas/
│   └── state.py              # WorkflowState dataclass
├── utils/
│   ├── llm.py                # Groq API client + fallback
│   ├── memory.py             # Persistent memory store
│   ├── logger.py             # Audit trail logger
│   ├── helpers.py            # File upload + export utilities
│   └── integrations.py       # Mock Slack/Email integrations
├── components/
│   ├── styles.py             # CSS theme
│   ├── pipeline.py           # Pipeline visualization
│   ├── dashboard.py          # Dashboard components
│   └── audit.py              # Audit trail UI
├── data/
│   ├── sample_inputs.txt     # Sample workflow inputs
│   └── memory.json           # Persistent memory (auto-generated)
├── notebooks/
│   └── explanation.md         # This file
├── README.md
├── requirements.txt
└── .env.example
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| LLM | Groq — LLaMA 3.3 70B Versatile |
| Charts | Plotly |
| Persistence | JSON file store |
| Language | Python 3.10+ |
