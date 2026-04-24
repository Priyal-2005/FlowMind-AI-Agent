"""
Intelligence Agent — Risk & Dependency Analyzer

Analyzes extracted input data to detect:
- Missing owners (unassigned tasks)
- Task dependencies
- Active blockers and their impact
- Risk scores with reasoning
- Overloaded team members
"""

from typing import Any
from agents.base import BaseAgent
from utils.helpers import demo_sleep


class IntelligenceAgent(BaseAgent):
    """Analyzes extracted data for risks, dependencies, and missing assignments."""

    def __init__(self):
        super().__init__(
            name="Intelligence Agent",
            icon="🧠",
            description="Detects missing owners, dependencies, blockers, and assigns risk scores with reasoning",
        )

    def process(self, input_data: Any, context: dict) -> dict:
        extracted = input_data
        llm = context["llm"]
        logger = context["logger"]

        logger.log(
            self.name,
            "Starting risk & dependency analysis",
            f"Analyzing {len(extracted.get('action_items', []))} action items for risks and gaps",
        )
        self.add_log("🧠 Initiating intelligent analysis...")
        demo_sleep(context, 0.3)

        action_items = extracted.get("action_items", [])
        owners = extracted.get("owners", [])
        blockers = extracted.get("blockers", [])

        # Perform risk analysis
        self.add_log("🔎 Scanning for missing owners...")
        demo_sleep(context, 0.3)
        missing_owners = [item for item in action_items if not item.get("owner")]
        if missing_owners:
            self.add_log(f"⚠️ {len(missing_owners)} tasks have NO owner assigned!")
            for item in missing_owners:
                logger.log(
                    self.name,
                    f"Missing owner detected: '{(item.get('description') or '')[:60]}...'",
                    f"This is a {item.get('priority', 'medium')} priority task with no owner. "
                    f"Unassigned tasks have a 73% probability of being dropped. Flagging for auto-assignment.",
                    severity="WARNING",
                )
        else:
            self.add_log("✅ All tasks have owners assigned")

        # Check for overloaded owners and historical bottlenecks
        self.add_log("📊 Analyzing team workload distribution & history...")
        demo_sleep(context, 0.3)
        from collections import Counter
        from utils.memory import MemoryStore
        memory = MemoryStore()
        
        owner_load = Counter(item["owner"] for item in action_items if item.get("owner"))
        overloaded = {}
        
        for owner, count in owner_load.items():
            stats = memory.get_owner_stats(owner)
            # Mark overloaded if >= 3 tasks OR (>= 2 tasks AND historical delay rate >= 40%)
            if count >= 3 or (count >= 2 and stats.get("delay_rate", 0.0) >= 0.4):
                overloaded[owner] = count
                
        if overloaded:
            for owner, count in overloaded.items():
                stats = memory.get_owner_stats(owner)
                delay_rate = int(stats.get("delay_rate", 0.0) * 100)
                
                self.add_log(f"🔴 {owner} flagged as bottleneck ({count} tasks, {delay_rate}% past delay rate)")
                logger.log(
                    self.name,
                    f"Bottleneck risk: {owner} ({count} tasks, {delay_rate}% historical delay rate)",
                    f"Research shows productivity drops significantly when handling multiple concurrent tasks, especially with historical delay precursors. "
                    f"Recommending redistribution to maintain team velocity.",
                    severity="WARNING",
                )
        else:
            self.add_log("✅ Workload distribution is balanced")

        # Analyze dependencies
        self.add_log("🔗 Detecting task dependencies...")
        demo_sleep(context, 0.3)
        dependencies = self._detect_dependencies(action_items)
        if dependencies:
            self.add_log(f"🔗 Found {len(dependencies)} dependency chains")
            for dep in dependencies:
                logger.log(
                    self.name,
                    f"Dependency: '{dep['from'][:40]}' → '{dep['to'][:40]}'",
                    f"Task sequencing detected. Blocking task must complete first to unblock dependent work.",
                )

        # Blocker analysis
        self.add_log("🚧 Analyzing blockers and impact...")
        demo_sleep(context, 0.3)
        if blockers:
            self.add_log(f"🚨 {len(blockers)} active blockers detected!")
            for b in blockers:
                logger.log(
                    self.name,
                    f"Active blocker: {b['description'][:60]}",
                    f"Severity: {b.get('severity', 'medium')}. {b.get('impact', 'May affect timeline')}. "
                    f"Blockers grow in impact by 25% daily if unaddressed.",
                    severity="WARNING",
                )

        # Get full risk assessment
        risks = llm.analyze_risks(extracted)
        self.add_log(f"📋 Generated {len(risks)} risk assessments")

        # Calculate overall risk score
        high_risks = sum(1 for r in risks if r.get("severity") == "HIGH")
        med_risks = sum(1 for r in risks if r.get("severity") == "MEDIUM")
        overall_risk = "HIGH" if high_risks >= 2 else "MEDIUM" if (high_risks >= 1 or med_risks >= 2) else "LOW"

        self.add_log(f"{'🔴' if overall_risk == 'HIGH' else '🟡' if overall_risk == 'MEDIUM' else '🟢'} "
                     f"Overall risk level: {overall_risk}")

        logger.log(
            self.name,
            f"Analysis complete — Overall risk: {overall_risk} "
            f"({high_risks} high, {med_risks} medium risks)",
            f"Identified {len(missing_owners)} unassigned tasks, {len(overloaded)} overloaded members, "
            f"{len(blockers)} blockers, {len(dependencies)} dependencies. "
            f"Overall project risk assessed as {overall_risk}.",
        )

        demo_sleep(context, 0.2)

        return {
            "risks": risks,
            "missing_owners": missing_owners,
            "overloaded_owners": dict(overloaded),
            "dependencies": dependencies,
            "blocker_analysis": blockers,
            "overall_risk": overall_risk,
            "owner_workload": dict(owner_load),
        }

    def _detect_dependencies(self, action_items: list) -> list:
        """Detect dependencies between tasks using keyword analysis."""
        dependencies = []
        dep_keywords = ["after", "once", "when", "depends on", "requires", "blocked by",
                        "waiting for", "following", "prerequisite"]

        for i, item in enumerate(action_items):
            desc = item.get("description", "").lower()
            for j, other in enumerate(action_items):
                if i == j:
                    continue
                other_desc = other.get("description", "").lower()
                # Check if this item references the other
                for kw in dep_keywords:
                    if kw in desc:
                        # Simple heuristic: check for word overlap
                        item_words = set(desc.split())
                        other_words = set(other_desc.split())
                        overlap = item_words & other_words - {"the", "a", "to", "and", "or", "is", "in", "on", "for"}
                        if len(overlap) >= 2:
                            dependencies.append({
                                "from": other["description"],
                                "to": item["description"],
                                "type": "sequential",
                            })
                            break

        return dependencies
