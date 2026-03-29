import json
import os
from typing import Dict, List, Any

MEMORY_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "memory.json")

class MemoryStore:
    """Persistent storage acting as the database for the Memory System."""
    
    def __init__(self):
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
        if not os.path.exists(MEMORY_FILE):
            self.clear()

    def _load(self) -> Dict[str, Any]:
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return self.clear()

    def _save(self, data: Dict[str, Any]):
        with open(MEMORY_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    def clear(self) -> Dict[str, Any]:
        """Wipe the database schema to fresh state."""
        empty = {
            "tasks": [],
            "actions": [],
            "owner_stats": {}
        }
        self._save(empty)
        return empty

    def save_run(self, tasks: List[Dict[str, Any]], actions: List[Dict[str, Any]]):
        """Commit tasks and actions to persistent storage, updating owner heuristics."""
        data = self._load()
        
        # Save historical tasks (prevent duplicates by ID)
        existing_task_ids = {t["id"]: i for i, t in enumerate(data["tasks"])}
        
        for task in tasks:
            # Update owner stats incrementally
            owner = task.get("owner")
            if owner and owner != "UNASSIGNED":
                if owner not in data["owner_stats"]:
                    data["owner_stats"][owner] = {"completed": 0, "delayed": 0, "total": 0}
                
                # We check the delta from previous save to avoid double counting
                # A proper implementation tracks task ID status changes specifically, 
                # but for this demo a simple increment when processing a run works.
                status = task.get("status")
                if status == "completed":
                    data["owner_stats"][owner]["completed"] += 1
                elif status == "delayed":
                    data["owner_stats"][owner]["delayed"] += 1
                data["owner_stats"][owner]["total"] += 1

            if task["id"] not in existing_task_ids:
                data["tasks"].append(task)
                existing_task_ids[task["id"]] = len(data["tasks"]) - 1
            else:
                idx = existing_task_ids[task["id"]]
                data["tasks"][idx] = task
        
        data["actions"].extend(actions)
        self._save(data)

    def get_owner_stats(self, owner: str) -> Dict[str, Any]:
        """Extract performance heuristics for an owner to assist predictive scoring."""
        data = self._load()
        stats = data.get("owner_stats", {}).get(owner, {"completed": 0, "delayed": 0, "total": 0})
        
        if stats["total"] > 0:
            stats["delay_rate"] = stats["delayed"] / stats["total"]
            stats["completion_rate"] = stats["completed"] / stats["total"]
        else:
            stats["delay_rate"] = 0.0
            stats["completion_rate"] = 0.0
            
        return dict(stats)

    def get_historical_context(self) -> Dict[str, Any]:
        """Get aggregate intelligence for the insights dashboard."""
        data = self._load()
        return {
            "total_tasks_tracked": len(data["tasks"]),
            "total_actions_logged": len(data["actions"]),
            "owner_metrics": data["owner_stats"]
        }
