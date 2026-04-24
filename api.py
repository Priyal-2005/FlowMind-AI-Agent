"""
FlowMind AI — API Endpoints

Enterprise REST API for programmatic access to the
multi-agent workflow orchestration pipeline.
"""

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from orchestrator.orchestrator import WorkflowOrchestrator
from utils.memory import MemoryStore

app = FastAPI(
    title="FlowMind AI — Autonomous Workflow Orchestrator API",
    description="Enterprise endpoints for extracting, tracking, and actioning workflow items autonomously.",
    version="2.0.0"
)

class WorkflowInput(BaseModel):
    input_text: str

    @field_validator("input_text")
    @classmethod
    def strip_non_empty(cls, v: str) -> str:
        if v is None or not str(v).strip():
            raise ValueError("input_text must be a non-empty string")
        return str(v).strip()

@app.post("/api/v1/orchestrate", tags=["Core Pipeline"])
def run_orchestrator(input_data: WorkflowInput):
    """
    Execute the entire 5-stage multi-agent pipeline immediately:
    Extraction -> Intelligence -> Execution -> Tracking -> Decision.
    """
    try:
        orch = WorkflowOrchestrator()
        state = orch.run_pipeline(input_data.input_text)
        
        if state.get("pipeline_status") == "error":
            raise HTTPException(status_code=500, detail="Agent pipeline encountered an error.")
            
        decision = state.get("decision", {})
        
        return {
            "status": "success",
            "tasks_generated": len(state.get("tasks", [])),
            "intelligence_risks": len(state.get("intelligence", {}).get("risks", [])),
            "actions": {
                "auto_assignments": len(decision.get("actions_taken", [])),
                "escalations": len(decision.get("escalations", [])),
                "reminders": len(decision.get("reminders", []))
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/memory/stats", tags=["Intelligence"])
def get_system_intelligence():
    """
    Retrieve historical AI context covering tracked tasks, total actions, 
    and employee overload/delay heuristics.
    """
    try:
        memory = MemoryStore()
        return memory.get_historical_context()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", tags=["System"])
def health_check():
    """Verify backend and database states."""
    try:
        # Check if memory store works
        MemoryStore()._load()
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return {"status": "degraded", "database": "unavailable"}
