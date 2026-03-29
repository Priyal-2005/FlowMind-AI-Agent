# 🏗️ System Architecture — Autonomous Meeting Orchestrator

## Overview
A multi-agent AI system that transforms raw meeting transcripts into executable workflows and autonomously manages task execution using predictive intelligence and decision-making.

---

## 🔁 Pipeline Flow

Transcript Input  
→ Extraction Agent  
→ Intelligence Agent  
→ Execution Agent  
→ Tracking Agent  
→ Decision Agent  
→ Autonomous Actions + Audit Logs

---

## 🧠 Agent Responsibilities

### 1. Extraction Agent
- Parses raw transcript
- Extracts:
  - Action items
  - Owners
  - Deadlines
  - Blockers

### 2. Intelligence Agent
- Detects:
  - Missing owners
  - Dependencies
  - Overloaded team members
  - Risk scores

### 3. Execution Agent
- Converts into structured tasks:
  - Task ID
  - Priority (P0/P1/P2)
  - Deadlines
  - Risk flags

### 4. Tracking Agent
- Simulates Day 1 → Day 3
- Tracks:
  - Progress
  - Delays
  - Bottlenecks
- Predicts future delays using heuristics + memory

### 5. Decision Agent
- Takes autonomous actions:
  - Auto-assign tasks
  - Reassign overloaded users
  - Send reminders
  - Escalate blockers

---

## ⚙️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **LLM:** Google Gemini 2.0 Flash
- **State Management:** Custom Orchestrator
- **Memory:** JSON-based persistent storage
- **Visualization:** Plotly

---

## 💾 Memory System

- Stores:
  - Historical tasks
  - Owner performance
- Enables:
  - Delay prediction
  - Adaptive decision making

---

## 🔥 Key Differentiator

Unlike traditional tools:
> This system doesn’t just analyze — it **acts autonomously**.

---

## 📊 Architecture Diagram (Conceptual)

[Transcript]
     ↓
[Extraction]
     ↓
[Intelligence]
     ↓
[Execution]
     ↓
[Tracking]
     ↓
[Decision Engine]
     ↓
[Actions + Notifications + Logs]