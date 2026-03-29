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
import random
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
        # Fixed seed for deterministic demo behavior
        self._rng = random.Random(42)

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

        logger.log(
            self.name,
            f"Day {day} simulation complete — {completed} done, {delayed} delayed, {len(issues)} issues",
            f"Progress: {completed}/{len(current_tasks)} tasks completed. "
            f"{delayed} tasks are delayed. {len(issues)} issues require attention. "
            f"Velocity: {'on track' if delayed == 0 else 'at risk' if delayed <= 2 else 'critical'}.",
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
        """Simulate progress for a single day."""
        self._rng = random.Random(42 + day)  # Deterministic per day

        for task in tasks:
            prev_status = task["status"]
            task = self._update_task_for_day(task, day)

            if task["status"] != prev_status:
                status_icon = {
                    "completed": "✅",
                    "in-progress": "🔄",
                    "delayed": "⚠️",
                    "blocked": "🚫",
                    "pending": "⏳",
                }.get(task["status"], "📋")

                self.add_log(
                    f"  {status_icon} Day {day}: {task['id']} ({task['title'][:35]}...) "
                    f"→ {task['status'].upper()}"
                )

                if task["status"] in ("delayed", "blocked"):
                    logger.log(
                        self.name,
                        f"Day {day}: {task['id']} is now {task['status'].upper()}",
                        f"Task '{task['title'][:50]}' owned by {task['owner']} "
                        f"has moved to {task['status']} status. "
                        f"Priority: {task['priority']}. Due: {task['deadline']}.",
                        severity="WARNING",
                    )

        return tasks

    def _update_task_for_day(self, task: dict, day: int) -> dict:
        """Deterministic task state update based on properties."""
        priority = task["priority"]
        risk = task["risk_flag"]
        owner = task["owner"]
        deadline = task["deadline"]
        status = task["status"]

        # Already completed tasks stay completed
        if status == "completed":
            return task

        # Unassigned tasks never progress
        if owner == "UNASSIGNED":
            if day >= 2:
                task["status"] = "delayed"
                task["delay_reason"] = "No owner assigned — task cannot progress"
            return task

        # Day 1 simulation
        if day == 1:
            if priority == "P0":
                # P0 tasks start immediately
                if risk != "HIGH":
                    task["status"] = "in-progress"
                    task["progress"] = 40
                else:
                    task["status"] = "in-progress"
                    task["progress"] = 20
            elif priority == "P1":
                # P1 tasks may start
                if self._rng.random() > 0.4:
                    task["status"] = "in-progress"
                    task["progress"] = 15
            # P2 tasks stay pending on Day 1

        # Day 2 simulation
        elif day == 2:
            if priority == "P0":
                if risk == "HIGH":
                    # High risk P0 tasks get delayed
                    task["status"] = "delayed"
                    task["delay_reason"] = "High risk factors slowing progress"
                    task["progress"] = 35
                elif deadline == "Day 1":
                    # Overdue P0 task
                    task["status"] = "delayed"
                    task["delay_reason"] = "Missed Day 1 deadline"
                    task["progress"] = 60
                else:
                    task["status"] = "in-progress"
                    task["progress"] = 75
            elif priority == "P1":
                if status == "in-progress":
                    if self._rng.random() > 0.3:
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
                if self._rng.random() > 0.5:
                    task["status"] = "in-progress"
                    task["progress"] = 10

        # Day 3 simulation
        elif day == 3:
            if priority == "P0":
                if status == "delayed":
                    task["progress"] = min(task.get("progress", 50) + 20, 70)
                    # Still delayed but progressing
                else:
                    task["status"] = "completed"
                    task["progress"] = 100
            elif priority == "P1":
                if status == "delayed":
                    task["progress"] = min(task.get("progress", 30) + 15, 60)
                elif status == "in-progress":
                    if task.get("progress", 0) >= 50:
                        task["status"] = "completed"
                        task["progress"] = 100
                    else:
                        task["progress"] = min(task.get("progress", 0) + 30, 80)
                else:
                    task["status"] = "in-progress"
                    task["progress"] = 25
            elif priority == "P2":
                if status == "in-progress":
                    task["progress"] = min(task.get("progress", 0) + 20, 50)
                elif deadline == "Day 3":
                    task["status"] = "delayed"
                    task["delay_reason"] = "Day 3 deadline approaching, not started"
                    task["progress"] = 0

        # Blocked task check (if has unmet dependencies)
        if task.get("dependencies"):
            task["status"] = "blocked"
            task["delay_reason"] = f"Blocked by dependencies: {', '.join(task['dependencies'])}"

        return task

    def _detect_issues(self, tasks: list, day: int, logger) -> list:
        """Detect issues requiring autonomous action."""
        issues = []

        for task in tasks:
            # Overdue tasks
            deadline_day = int(task["deadline"].replace("Day ", "")) if "Day" in task.get("deadline", "") else 3
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
                    f"Priority: {task['priority']}. Current status: {task['status']}.",
                    severity="WARNING",
                )

            # Unassigned tasks
            if task["owner"] == "UNASSIGNED" and task["status"] != "completed":
                issue = {
                    "type": "unassigned",
                    "task_id": task["id"],
                    "task_title": task["title"],
                    "priority": task["priority"],
                    "detail": f"Still unassigned on Day {day}",
                    "severity": "HIGH",
                }
                issues.append(issue)

            # Stalled tasks (in-progress but low progress)
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
                    "owner": task["owner"],
                    "priority": task["priority"],
                    "detail": task.get("delay_reason", "Unknown delay"),
                    "severity": "HIGH" if task["priority"] == "P0" else "MEDIUM",
                }
                issues.append(issue)

        return issues
