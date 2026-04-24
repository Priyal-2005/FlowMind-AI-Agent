"""
Execution Agent — Task Structuring Engine

Takes extracted items and intelligence analysis to create
structured, executable workflow tasks with proper metadata:
- Unique task IDs
- Priority classification (P0/P1/P2)
- Status tracking
- Risk flags
- Dependency mapping
"""

import time
from typing import Any
from agents.base import BaseAgent


class ExecutionAgent(BaseAgent):
    """Converts extracted data into structured executable tasks."""

    def __init__(self):
        super().__init__(
            name="Execution Agent",
            icon="⚡",
            description="Creates structured executable tasks with priorities, risk flags, and dependency tracking",
        )

    def process(self, input_data: Any, context: dict) -> dict:
        extracted = input_data["extracted"]
        intelligence = input_data["intelligence"]
        logger = context["logger"]

        logger.log(
            self.name,
            "Creating structured task objects",
            f"Converting {len(extracted.get('action_items', []))} action items into executable tasks "
            f"with risk flags from intelligence analysis",
        )
        self.add_log("⚡ Initializing task structuring engine...")
        time.sleep(0.3)

        action_items = extracted.get("action_items", [])
        risks = intelligence.get("risks", [])
        missing_owners = intelligence.get("missing_owners", [])
        overall_risk = intelligence.get("overall_risk", "LOW")

        # Build risk lookup
        risk_lookup = {}
        for risk in risks:
            item_desc = risk.get("item", "").lower()
            risk_lookup[item_desc] = risk

        tasks = []
        for idx, item in enumerate(action_items):
            task_id = f"TASK-{idx + 1:03d}"
            desc = item.get("description", "")

            # Determine priority
            raw_priority = item.get("priority", "medium").lower()
            if raw_priority in ("high", "critical", "urgent"):
                priority = "P0"
            elif raw_priority in ("medium", "important"):
                priority = "P1"
            else:
                priority = "P2"

            # Determine risk flag
            risk_flag = "LOW"
            risk_reasoning = ""
            desc_lower = desc.lower()
            for risk_key, risk_data in risk_lookup.items():
                if desc_lower[:30] in risk_key or risk_key[:30] in desc_lower:
                    risk_flag = risk_data.get("severity", "LOW")
                    risk_reasoning = risk_data.get("reasoning", "")
                    break

            # Check if this item is missing an owner
            is_unassigned = not item.get("owner")
            if is_unassigned:
                risk_flag = max(risk_flag, "MEDIUM", key=lambda x: {"LOW": 0, "MEDIUM": 1, "HIGH": 2}.get(x, 0))

            # Determine deadline
            deadline = item.get("deadline")
            if not deadline:
                # Assign default deadline based on priority
                if priority == "P0":
                    deadline = "Day 1"
                elif priority == "P1":
                    deadline = "Day 2"
                else:
                    deadline = "Day 3"

            # Normalize deadline to Day format
            deadline_lower = deadline.lower() if deadline else ""
            if "day 1" in deadline_lower or "today" in deadline_lower or "eod" in deadline_lower or "immediately" in deadline_lower:
                deadline = "Day 1"
            elif "day 2" in deadline_lower or "tomorrow" in deadline_lower:
                deadline = "Day 2"
            elif "day 3" in deadline_lower or "end of week" in deadline_lower or "friday" in deadline_lower:
                deadline = "Day 3"
            elif deadline and "day" not in deadline_lower:
                # Keep as-is but normalize to a day
                if priority == "P0":
                    deadline = "Day 1"
                elif priority == "P1":
                    deadline = "Day 2"
                else:
                    deadline = "Day 3"

            task = {
                "id": task_id,
                "title": desc,
                "owner": item.get("owner") or "UNASSIGNED",
                "deadline": deadline,
                "priority": priority,
                "status": "pending",
                "risk_flag": risk_flag,
                "risk_reasoning": risk_reasoning,
                "dependencies": [],
                "created_by": self.name,
                "original_priority": raw_priority,
            }
            tasks.append(task)

            status_icon = "🔴" if risk_flag == "HIGH" else "🟡" if risk_flag == "MEDIUM" else "🟢"
            owner_display = task["owner"] if task["owner"] != "UNASSIGNED" else "⚠️ UNASSIGNED"
            self.add_log(
                f"{status_icon} {task_id}: {desc[:50]}{'...' if len(desc) > 50 else ''} "
                f"→ {owner_display} | {priority} | Due: {deadline}"
            )

            logger.log(
                self.name,
                f"Created {task_id}: '{desc[:60]}' → {task['owner']} | {priority} | {risk_flag} risk",
                f"Assigned {priority} priority based on '{raw_priority}' classification. "
                f"Deadline set to {deadline}. Risk flag: {risk_flag}. "
                f"{'Owner is unassigned — flagged for auto-assignment.' if is_unassigned else ''}",
            )

            time.sleep(0.15)

        # Map dependencies from intelligence data
        deps = intelligence.get("dependencies", [])
        if deps:
            self.add_log(f"🔗 Mapping {len(deps)} dependency chains...")
            for dep in deps:
                from_task = None
                to_task = None
                for t in tasks:
                    if dep["from"].lower()[:20] in t["title"].lower():
                        from_task = t
                    if dep["to"].lower()[:20] in t["title"].lower():
                        to_task = t
                if from_task and to_task:
                    to_task["dependencies"].append(from_task["id"])
                    self.add_log(f"  🔗 {to_task['id']} depends on {from_task['id']}")

        # Summary
        p0_count = sum(1 for t in tasks if t["priority"] == "P0")
        p1_count = sum(1 for t in tasks if t["priority"] == "P1")
        p2_count = sum(1 for t in tasks if t["priority"] == "P2")
        unassigned = sum(1 for t in tasks if t["owner"] == "UNASSIGNED")
        high_risk = sum(1 for t in tasks if t["risk_flag"] == "HIGH")

        self.add_log(f"\n📊 Task Summary: {len(tasks)} total | P0:{p0_count} P1:{p1_count} P2:{p2_count}")
        self.add_log(f"   ⚠️ Unassigned: {unassigned} | 🔴 High Risk: {high_risk}")

        logger.log(
            self.name,
            f"Task creation complete: {len(tasks)} tasks "
            f"(P0:{p0_count}, P1:{p1_count}, P2:{p2_count}) | "
            f"{unassigned} unassigned | {high_risk} high-risk",
            f"All action items structured into executable tasks. "
            f"Overall project risk: {overall_risk}. "
            f"{'Unassigned tasks require auto-assignment.' if unassigned else 'All tasks assigned.'}",
        )

        time.sleep(0.2)

        return {
            "tasks": tasks,
            "summary": {
                "total": len(tasks),
                "p0": p0_count,
                "p1": p1_count,
                "p2": p2_count,
                "unassigned": unassigned,
                "high_risk": high_risk,
            },
        }
