"""
Tracking Agent — Time Simulation Engine

Simulates task progression across Day 1 → Day 2 → Day 3.
Uses deterministic simulation logic based on task properties
(priority, risk, owner) for consistent demo behavior.

Detects:
- Overdue tasks
- Stalled tasks
- Unassigned tasks still pending
- Bottlenecks
"""

import time
from typing import Any
from copy import deepcopy
from agents.base import BaseAgent


class TrackingAgent(BaseAgent):
    """Simulates task progression over time and detects issues."""

    def __init__(self):
        super().__init__(
            name="Tracking Agent",
            icon="📊",
            description="Simulates Day 1→Day 3 progression, detects delays, overdue tasks, and bottlenecks",
        )

    def process(self, input_data: Any, context: dict) -> dict:
        tasks = deepcopy(input_data["tasks"])
        day = input_data.get("day", 1)
        logger = context["logger"]

        logger.log(
            self.name,
            f"Starting Day {day} simulation",
            f"Simulating progress for {len(tasks)} tasks on Day {day}. "
            f"Applying realistic progression patterns based on priority, risk, and ownership.",
        )
        self.add_log(f"📊 Simulating Day {day} progress for {len(tasks)} tasks...")
        time.sleep(0.3)

        # Ensure all tasks have required fields initialized
        for task in tasks:
            if "progress" not in task:
                task["progress"] = 0
            if "status" not in task:
                task["status"] = "pending"

        # Apply simulation for each day up to the requested day
        day_snapshots = {}
        current_tasks = deepcopy(tasks)

        for d in range(1, day + 1):
            current_tasks = self._simulate_day(current_tasks, d, logger)
            day_snapshots[f"day_{d}"] = deepcopy(current_tasks)
            time.sleep(0.2)

        # Analyze current state
        issues = self._detect_issues(current_tasks, day, logger)

        # Summary stats
        completed = sum(1 for t in current_tasks if t["status"] == "completed")
        in_progress = sum(1 for t in current_tasks if t["status"] == "in-progress")
        delayed = sum(1 for t in current_tasks if t["status"] == "delayed")
        pending = sum(1 for t in current_tasks if t["status"] == "pending")
        blocked = sum(1 for t in current_tasks if t["status"] == "blocked")

        self.add_log(f"\n📈 Day {day} Status Report:")
        self.add_log(f"   ✅ Completed: {completed}")
        self.add_log(f"   🔄 In Progress: {in_progress}")
        self.add_log(f"   ⏳ Pending: {pending}")
        self.add_log(f"   ⚠️ Delayed: {delayed}")
        self.add_log(f"   🚫 Blocked: {blocked}")
        self.add_log(f"   🚨 Issues Detected: {len(issues)}")

        velocity = "on track" if delayed == 0 else "at risk" if delayed <= 2 else "critical"

        logger.log(
            self.name,
            f"Day {day} simulation complete — {completed} done, {delayed} delayed, {len(issues)} issues",
            f"Progress: {completed}/{len(current_tasks)} tasks completed. "
            f"{delayed} tasks are delayed. {len(issues)} issues require autonomous action. "
            f"Velocity: {velocity}. Routing to Decision Agent for corrective actions.",
        )

        return {
            "tasks": current_tasks,
            "day": day,
            "day_snapshots": day_snapshots,
            "issues": issues,
            "stats": {
                "completed": completed,
                "in_progress": in_progress,
                "delayed": delayed,
                "pending": pending,
                "blocked": blocked,
                "total": len(current_tasks),
            },
        }

    def _simulate_day(self, tasks: list, day: int, logger) -> list:
        """Simulate progress for a single day — fully deterministic."""
        # Use a deterministic mapping based on task index and day
        for idx, task in enumerate(tasks):
            prev_status = task["status"]
            prev_progress = task.get("progress", 0)
            task = self._update_task_for_day(task, day, idx)

            if task["status"] != prev_status or task.get("progress", 0) != prev_progress:
                status_icon = {
                    "completed": "✅",
                    "in-progress": "🔄",
                    "delayed": "⚠️",
                    "blocked": "🚫",
                    "pending": "⏳",
                }.get(task["status"], "📋")

                title_short = task['title'][:35]
                if len(task['title']) > 35:
                    title_short += "..."

                self.add_log(
                    f"  {status_icon} Day {day}: {task['id']} ({title_short}) "
                    f"→ {task['status'].upper()} [{task.get('progress', 0)}%]"
                )

                if task["status"] in ("delayed", "blocked"):
                    logger.log(
                        self.name,
                        f"Day {day}: {task['id']} is now {task['status'].upper()}",
                        f"Task '{task['title'][:50]}' owned by {task['owner']} "
                        f"has moved to {task['status']} status. "
                        f"Priority: {task['priority']}. Due: {task['deadline']}. "
                        f"Reason: {task.get('delay_reason', 'Unknown')}",
                        severity="WARNING",
                    )

        return tasks

    def _update_task_for_day(self, task: dict, day: int, task_idx: int = 0) -> dict:
        """Deterministic task state update based on properties and task index."""
        priority = task["priority"]
        risk = task["risk_flag"]
        owner = task["owner"]
        deadline = task["deadline"]
        status = task["status"]

        # Already completed tasks stay completed
        if status == "completed":
            task["progress"] = 100
            return task

        # Unassigned tasks never progress
        if owner == "UNASSIGNED":
            if day >= 2:
                task["status"] = "delayed"
                task["delay_reason"] = "No owner assigned — task cannot progress"
                task["progress"] = 0
            return task

        # Use task_idx as a deterministic offset (0-based)
        # odd-indexed tasks slightly behind, even-indexed slightly ahead
        idx_factor = task_idx % 2  # 0 or 1

        # ── DAY 1 ──────────────────────────────────
        if day == 1:
            if priority == "P0":
                task["status"] = "in-progress"
                task["progress"] = 35 if risk == "HIGH" else (45 - idx_factor * 5)
            elif priority == "P1":
                # All P1s start on Day 1 (deterministic)
                if idx_factor == 0:
                    task["status"] = "in-progress"
                    task["progress"] = 20
                else:
                    task["status"] = "in-progress"
                    task["progress"] = 15
            # P2 tasks stay pending on Day 1

        # ── DAY 2 ──────────────────────────────────
        elif day == 2:
            if priority == "P0":
                if risk == "HIGH":
                    task["status"] = "delayed"
                    task["delay_reason"] = "High risk factors slowing progress"
                    task["progress"] = 40
                elif deadline == "Day 1":
                    task["status"] = "delayed"
                    task["delay_reason"] = "Missed Day 1 deadline"
                    task["progress"] = 60
                else:
                    task["status"] = "in-progress"
                    task["progress"] = 75 - idx_factor * 10
            elif priority == "P1":
                if status == "in-progress":
                    # Deterministic: even tasks progress, odd tasks get delayed
                    if idx_factor == 0:
                        task["status"] = "in-progress"
                        task["progress"] = 55
                    else:
                        task["status"] = "delayed"
                        task["delay_reason"] = "Dependencies or resource constraints"
                        task["progress"] = 30
                else:
                    task["status"] = "in-progress"
                    task["progress"] = 20
            elif priority == "P2":
                if idx_factor == 0:
                    task["status"] = "in-progress"
                    task["progress"] = 10

        # ── DAY 3 ──────────────────────────────────
        elif day == 3:
            if priority == "P0":
                if status == "delayed":
                    task["progress"] = min(task.get("progress", 50) + 20, 75)
                    # Still delayed but progressing toward resolution
                else:
                    task["status"] = "completed"
                    task["progress"] = 100
            elif priority == "P1":
                if status == "delayed":
                    task["progress"] = min(task.get("progress", 30) + 15, 65)
                elif status == "in-progress":
                    if task.get("progress", 0) >= 50:
                        task["status"] = "completed"
                        task["progress"] = 100
                    else:
                        task["progress"] = min(task.get("progress", 0) + 30, 85)
                else:
                    task["status"] = "in-progress"
                    task["progress"] = 25
            elif priority == "P2":
                if status == "in-progress":
                    task["progress"] = min(task.get("progress", 0) + 25, 55)
                elif deadline == "Day 3" and status == "pending":
                    task["status"] = "delayed"
                    task["delay_reason"] = "Day 3 deadline reached, task not started"
                    task["progress"] = 0

        # Blocked task check (if has unmet dependencies)
        if task.get("dependencies") and status != "completed":
            task["status"] = "blocked"
            task["delay_reason"] = f"Blocked by: {', '.join(task['dependencies'])}"

        return task

    def _detect_issues(self, tasks: list, day: int, logger) -> list:
        """Detect issues requiring autonomous action."""
        issues = []

        for task in tasks:
            deadline_str = task.get("deadline", "Day 3")
            try:
                deadline_day = int(deadline_str.replace("Day ", "").strip())
            except (ValueError, AttributeError):
                deadline_day = 3

            # Overdue tasks
            if day >= deadline_day and task["status"] not in ("completed",):
                issue = {
                    "type": "overdue",
                    "task_id": task["id"],
                    "task_title": task["title"],
                    "owner": task["owner"],
                    "priority": task["priority"],
                    "detail": f"Due on {task['deadline']} but status is {task['status']} on Day {day}",
                    "severity": "HIGH" if task["priority"] == "P0" else "MEDIUM",
                }
                issues.append(issue)
                logger.log(
                    self.name,
                    f"⏰ OVERDUE: {task['id']} was due {task['deadline']}, now Day {day}",
                    f"Task '{task['title'][:50]}' owned by {task['owner']} is overdue. "
                    f"Priority: {task['priority']}. Current status: {task['status']}. "
                    f"Progress: {task.get('progress', 0)}%.",
                    severity="WARNING",
                )

            # Unassigned tasks
            if task["owner"] == "UNASSIGNED" and task["status"] != "completed":
                issue = {
                    "type": "unassigned",
                    "task_id": task["id"],
                    "task_title": task["title"],
                    "priority": task["priority"],
                    "owner": "UNASSIGNED",
                    "detail": f"Still unassigned on Day {day}",
                    "severity": "HIGH",
                }
                issues.append(issue)

            # Stalled tasks (in-progress but very low progress on Day 2+)
            if task["status"] == "in-progress" and task.get("progress", 0) < 20 and day >= 2:
                issue = {
                    "type": "stalled",
                    "task_id": task["id"],
                    "task_title": task["title"],
                    "owner": task["owner"],
                    "priority": task["priority"],
                    "detail": f"Only {task.get('progress', 0)}% progress after {day} days",
                    "severity": "MEDIUM",
                }
                issues.append(issue)

            # Delayed tasks
            if task["status"] == "delayed":
                issue = {
                    "type": "delayed",
                    "task_id": task["id"],
                    "task_title": task["title"],
                    "owner": task.get("owner", "UNASSIGNED"),
                    "priority": task["priority"],
                    "detail": task.get("delay_reason", "Unknown delay"),
                    "severity": "HIGH" if task["priority"] == "P0" else "MEDIUM",
                }
                issues.append(issue)

        return issues
