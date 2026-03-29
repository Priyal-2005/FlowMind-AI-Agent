from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orchestrator import MeetingOrchestrator
from utils.memory import MemoryStore

app = FastAPI(
    title="Meeting Orchestrator AI Command Center API",
    description="Enterprise endpoints for extracting, tracking, and actioning meeting items autonomously.",
    version="2.0.0"
)

class TranscriptInput(BaseModel):
    transcript: str

@app.post("/api/v1/orchestrate", tags=["Core Pipeline"])
def run_orchestrator(input_data: TranscriptInput):
    """
    Execute the entire 5-stage multi-agent pipeline immediately:
    Extraction -> Intelligence -> Execution -> Tracking -> Decision.
    """
    try:
        orch = MeetingOrchestrator()
        state = orch.run_pipeline(input_data.transcript)
        
        if state["pipeline_status"] == "error":
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
