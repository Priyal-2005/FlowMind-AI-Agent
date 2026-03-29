"""
Decision Agent — Autonomous Action Engine

When issues are detected, this agent TAKES ACTIONS (not suggestions):
- Auto-assigns unassigned tasks to available team members
- Sends escalation notices for delayed P0 tasks
- Flags blockers for immediate attention
- Reassigns tasks from overloaded owners
- Triggers reminder notifications

Every action is logged with full reasoning.
"""

import time
from typing import Any
from copy import deepcopy
from agents.base import BaseAgent


class DecisionAgent(BaseAgent):
    """Takes autonomous corrective actions based on detected issues."""

    def __init__(self):
        super().__init__(
            name="Decision Agent",
            icon="🤖",
            description="Autonomously assigns owners, escalates delays, flags blockers, and redistributes workload",
        )

    def process(self, input_data: Any, context: dict) -> dict:
        tasks = deepcopy(input_data["tasks"])
        issues = input_data.get("issues", [])
        intelligence = input_data.get("intelligence", {})
        day = input_data.get("day", 1)
        logger = context["logger"]

        logger.log(
            self.name,
            f"Autonomous Decision Engine activated — {len(issues)} issues to resolve",
            f"Day {day}: Analyzing {len(issues)} detected issues. "
            f"Will take autonomous corrective actions based on priority, workload, and risk assessment.",
        )
        self.add_log(f"🤖 Decision Engine activated — {len(issues)} issues detected")
        time.sleep(0.3)

        actions_taken = []
        escalations = []
        reminders = []

        # Build team workload map
        owner_workload = intelligence.get("owner_workload", {})
        all_owners = list(set(
            t["owner"] for t in tasks
            if t["owner"] != "UNASSIGNED"
        ))

        # Process each issue
        for issue in issues:
            issue_type = issue["type"]
            task_id = issue["task_id"]
            task = next((t for t in tasks if t["id"] == task_id), None)
            if not task:
                continue

            if issue_type == "unassigned":
                action = self._auto_assign(task, all_owners, owner_workload, logger)
                if action:
                    actions_taken.append(action)

            elif issue_type == "overdue":
                action = self._handle_overdue(task, day, logger)
                actions_taken.append(action)
                if task["priority"] == "P0":
                    esc = self._escalate(task, "P0 task overdue", logger)
                    escalations.append(esc)

            elif issue_type == "delayed":
                action = self._handle_delay(task, day, all_owners, owner_workload, logger)
                actions_taken.append(action)
                reminder = self._send_reminder(task, "Task is delayed", logger)
                reminders.append(reminder)

            elif issue_type == "stalled":
                reminder = self._send_reminder(task, "Task progress stalled", logger)
                reminders.append(reminder)
                if task["priority"] in ("P0", "P1"):
                    esc = self._escalate(task, "High-priority task stalled", logger)
                    escalations.append(esc)

            time.sleep(0.15)

        # Check for overloaded owners and redistribute
        for owner, count in owner_workload.items():
            if count >= 3:
                redistributed = self._redistribute_workload(
                    owner, tasks, all_owners, owner_workload, logger
                )
                actions_taken.extend(redistributed)

        # Summary
        self.add_log(f"\n🤖 Autonomous Actions Summary:")
        self.add_log(f"   ⚡ Actions Taken: {len(actions_taken)}")
        self.add_log(f"   🚨 Escalations: {len(escalations)}")
        self.add_log(f"   🔔 Reminders Sent: {len(reminders)}")

        logger.log(
            self.name,
            f"Decision cycle complete: {len(actions_taken)} actions, "
            f"{len(escalations)} escalations, {len(reminders)} reminders",
            f"Autonomous decision engine resolved {len(actions_taken)} issues. "
            f"Sent {len(escalations)} escalation notices and {len(reminders)} reminders. "
            f"All actions logged with full reasoning for audit compliance.",
        )

        return {
            "tasks": tasks,
            "actions_taken": actions_taken,
            "escalations": escalations,
            "reminders": reminders,
            "summary": {
                "total_actions": len(actions_taken),
                "total_escalations": len(escalations),
                "total_reminders": len(reminders),
            },
        }

    def _auto_assign(self, task: dict, owners: list, workload: dict, logger) -> dict:
        """Auto-assign unassigned task to team member with lowest workload."""
        if not owners:
            # No known owners, create a placeholder
            assigned_to = "Team Lead"
            reasoning = "No team members identified from meeting. Escalating to Team Lead for assignment."
        else:
            # Find owner with lowest workload
            sorted_owners = sorted(owners, key=lambda o: workload.get(o, 0))
            assigned_to = sorted_owners[0]
            their_load = workload.get(assigned_to, 0)
            reasoning = (
                f"Auto-assigned to {assigned_to} (current load: {their_load} tasks). "
                f"Selected because they have the lowest workload among "
                f"{len(owners)} team members. Task priority: {task['priority']}."
            )

        task["owner"] = assigned_to
        task["auto_assigned"] = True

        # Update workload tracking
        workload[assigned_to] = workload.get(assigned_to, 0) + 1

        action = {
            "type": "auto_assignment",
            "task_id": task["id"],
            "task_title": task["title"],
            "action": f"Auto-assigned to {assigned_to}",
            "previous_owner": "UNASSIGNED",
            "new_owner": assigned_to,
            "reasoning": reasoning,
            "icon": "👤",
        }

        self.add_log(f"  👤 AUTO-ASSIGN: {task['id']} → {assigned_to} (lowest workload)")

        logger.log(
            self.name,
            f"AUTO-ASSIGNED {task['id']} to {assigned_to}",
            reasoning,
            severity="ACTION",
        )

        return action

    def _handle_overdue(self, task: dict, day: int, logger) -> dict:
        """Handle overdue tasks with priority-based response."""
        if task["priority"] == "P0":
            action_text = f"CRITICAL: {task['id']} is overdue. Marked as urgent. Escalating to management."
            task["escalated"] = True
        else:
            action_text = f"{task['id']} is past deadline. Sending reminder to {task['owner']}."

        action = {
            "type": "overdue_response",
            "task_id": task["id"],
            "task_title": task["title"],
            "action": action_text,
            "owner": task["owner"],
            "reasoning": (
                f"Task was due on {task['deadline']} but is still '{task['status']}' on Day {day}. "
                f"Priority: {task['priority']}. "
                f"Every day of delay costs approximately 2.5 productive hours across the team."
            ),
            "icon": "⏰",
        }

        self.add_log(f"  ⏰ OVERDUE: {task['id']} — {action_text[:60]}")

        logger.log(
            self.name,
            f"OVERDUE ACTION: {action_text[:80]}",
            action["reasoning"],
            severity="ACTION",
        )

        return action

    def _handle_delay(self, task: dict, day: int, owners: list, workload: dict, logger) -> dict:
        """Handle delayed tasks — may reassign if persistent."""
        delay_reason = task.get("delay_reason", "Unknown")

        # If delayed for more than expected, consider reassignment
        if day >= 3 and task["status"] == "delayed" and task.get("progress", 0) < 50:
            # Reassign to less loaded team member
            if owners:
                sorted_owners = sorted(owners, key=lambda o: workload.get(o, 0))
                new_owner = sorted_owners[0]
                if new_owner != task["owner"]:
                    old_owner = task["owner"]
                    task["owner"] = new_owner
                    task["reassigned"] = True

                    action = {
                        "type": "reassignment",
                        "task_id": task["id"],
                        "task_title": task["title"],
                        "action": f"Reassigned from {old_owner} to {new_owner}",
                        "previous_owner": old_owner,
                        "new_owner": new_owner,
                        "reasoning": (
                            f"Task has been delayed for {day} days with only "
                            f"{task.get('progress', 0)}% progress. "
                            f"Reassigning from {old_owner} to {new_owner} "
                            f"(workload: {workload.get(new_owner, 0)} tasks) to unblock progress."
                        ),
                        "icon": "🔄",
                    }

                    self.add_log(f"  🔄 REASSIGN: {task['id']} {old_owner} → {new_owner}")

                    logger.log(
                        self.name,
                        f"REASSIGNED {task['id']} from {old_owner} to {new_owner}",
                        action["reasoning"],
                        severity="ACTION",
                    )

                    return action

        action = {
            "type": "delay_response",
            "task_id": task["id"],
            "task_title": task["title"],
            "action": f"Acknowledged delay on {task['id']}. Monitoring closely.",
            "owner": task["owner"],
            "reasoning": f"Delay reason: {delay_reason}. Day {day}. Priority: {task['priority']}.",
            "icon": "⚠️",
        }

        self.add_log(f"  ⚠️ DELAY: {task['id']} — {delay_reason[:50]}")

        logger.log(
            self.name,
            f"DELAY MONITORED: {task['id']} — {delay_reason[:60]}",
            action["reasoning"],
            severity="ACTION",
        )

        return action

    def _escalate(self, task: dict, reason: str, logger) -> dict:
        """Create escalation notice."""
        escalation = {
            "type": "escalation",
            "task_id": task["id"],
            "task_title": task["title"],
            "owner": task["owner"],
            "priority": task["priority"],
            "reason": reason,
            "action": f"Escalated to management: {reason}",
            "target": "Engineering Manager",
            "icon": "🚨",
        }

        self.add_log(f"  🚨 ESCALATION: {task['id']} → Management ({reason})")

        logger.log(
            self.name,
            f"ESCALATED: {task['id']} to Engineering Manager",
            f"Reason: {reason}. Task: '{task['title'][:50]}'. "
            f"Owner: {task['owner']}. Priority: {task['priority']}. "
            f"Auto-escalation triggered by autonomous decision engine.",
            severity="ESCALATION",
        )

        return escalation

    def _send_reminder(self, task: dict, reason: str, logger) -> dict:
        """Send reminder notification."""
        reminder = {
            "type": "reminder",
            "task_id": task["id"],
            "task_title": task["title"],
            "owner": task["owner"],
            "reason": reason,
            "action": f"Reminder sent to {task['owner']}: {reason}",
            "icon": "🔔",
        }

        self.add_log(f"  🔔 REMINDER: {task['owner']} — {reason} ({task['id']})")

        logger.log(
            self.name,
            f"REMINDER sent to {task['owner']}: {reason}",
            f"Automated reminder for {task['id']}: '{task['title'][:50]}'. "
            f"Current status: {task['status']}.",
            severity="ACTION",
        )

        return reminder

    def _redistribute_workload(self, overloaded_owner: str, tasks: list,
                                owners: list, workload: dict, logger) -> list:
        """Redistribute tasks from overloaded owner."""
        actions = []
        their_tasks = [t for t in tasks if t["owner"] == overloaded_owner and t["status"] == "pending"]

        if len(their_tasks) <= 1 or len(owners) <= 1:
            return actions

        # Move lowest priority tasks to less loaded owners
        sorted_tasks = sorted(their_tasks, key=lambda t: {"P0": 0, "P1": 1, "P2": 2}.get(t["priority"], 3))

        # Keep P0 tasks, redistribute others
        for task in sorted_tasks:
            if task["priority"] == "P0":
                continue

            available = [o for o in owners if o != overloaded_owner and workload.get(o, 0) < 2]
            if not available:
                break

            new_owner = available[0]
            old_owner = task["owner"]
            task["owner"] = new_owner
            task["redistributed"] = True
            workload[new_owner] = workload.get(new_owner, 0) + 1
            workload[overloaded_owner] -= 1

            action = {
                "type": "redistribution",
                "task_id": task["id"],
                "task_title": task["title"],
                "action": f"Redistributed from {old_owner} to {new_owner}",
                "previous_owner": old_owner,
                "new_owner": new_owner,
                "reasoning": (
                    f"{old_owner} was overloaded with {workload.get(old_owner, 0) + 1} tasks. "
                    f"Moved '{task['title'][:40]}' ({task['priority']}) to {new_owner} "
                    f"who has capacity ({workload.get(new_owner, 0)} tasks)."
                ),
                "icon": "⚖️",
            }

            self.add_log(f"  ⚖️ REDISTRIBUTE: {task['id']} {old_owner} → {new_owner}")

            logger.log(
                self.name,
                f"REDISTRIBUTED {task['id']} from {old_owner} to {new_owner}",
                action["reasoning"],
                severity="ACTION",
            )

            actions.append(action)

        return actions
