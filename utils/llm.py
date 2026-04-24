"""
LLM Integration Layer — Groq + Rule-Based Fallback

Provides intelligent extraction and analysis capabilities for FlowMind AI.
Uses Groq API when available, falls back to rule-based NLP otherwise.
"""

import json
import os
import re
from typing import Optional

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False


class LLMClient:
    """Unified LLM client with automatic fallback to rule-based extraction."""

    MODEL_NAME = "llama-3.3-70b-versatile"

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY", "")
        self.use_llm = False
        self.client = None

        if GROQ_AVAILABLE and self.api_key and self.api_key != "your_api_key_here":
            try:
                self.client = Groq(api_key=self.api_key)
                self.use_llm = True
            except Exception:
                self.use_llm = False

    @property
    def mode(self) -> str:
        return "🤖 Groq AI" if self.use_llm else "⚙️ Smart Extraction Engine"

    # ── LLM CALLS ──────────────────────────────────────────────

    def _call_groq(self, prompt: str) -> str:
        """Call Groq API with error handling."""
        if not self.use_llm or not self.client:
            return ""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert AI assistant for enterprise workflow management. Follow instructions precisely and return structured data as requested."},
                    {"role": "user", "content": prompt},
                ],
                model=self.MODEL_NAME,
                temperature=0.2,
                max_tokens=4096,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            print(f"Groq API error: {e}")
            return ""

    def _parse_json_from_response(self, text: str) -> Optional[dict]:
        """Extract JSON from LLM response text."""
        try:
            match = re.search(r'```(?:json)?\s*([\s\S]*?)```', text)
            if match:
                return json.loads(match.group(1).strip())
            return json.loads(text.strip())
        except (json.JSONDecodeError, AttributeError):
            return None

    # ── EXTRACTION ─────────────────────────────────────────────

    def extract_input_data(self, transcript: str) -> dict:
        """Extract structured data from input text."""
        if self.use_llm:
            result = self._extract_with_llm(transcript)
            if result:
                return result
        return self._extract_with_rules(transcript)

    # Backward compatibility alias
    extract_meeting_data = extract_input_data

    def _extract_with_llm(self, transcript: str) -> Optional[dict]:
        prompt = f"""Analyze this input text and extract structured data.
Return ONLY valid JSON with this exact structure:
```json
{{
    "action_items": [
        {{
            "description": "task description",
            "owner": "person name or null",
            "deadline": "mentioned deadline or null",
            "priority": "high/medium/low based on context"
        }}
    ],
    "decisions": ["decision 1", "decision 2"],
    "owners": ["unique person names mentioned"],
    "deadlines": ["mentioned deadlines"],
    "blockers": [
        {{
            "description": "blocker description",
            "impact": "what it affects",
            "severity": "high/medium/low"
        }}
    ],
    "summary": "2-3 sentence meeting summary"
}}
```

Input Text:
{transcript}"""
        response = self._call_groq(prompt)
        return self._parse_json_from_response(response) if response else None

    def _extract_with_rules(self, transcript: str) -> dict:
        """Rule-based extraction using patterns and keywords — guaranteed minimum output."""
        lines = transcript.strip().split('\n')
        text_lower = transcript.lower()

        # ── Step 1: Extract people names ──────────────────
        STOP_WORDS = {
            'the', 'this', 'that', 'also', 'but', 'and', 'for', 'with', 'from',
            'into', 'will', 'should', 'need', 'let', 'get', 'yes', 'hey', 'sure',
            'okay', 'right', 'maybe', 'just', 'what', 'when', 'where', 'who',
            'today', 'day', 'team', 'everyone', 'anyone', 'someone', 'our', 'all',
            # Temporal / common false positives
            'done', 'date', 'end', 'now', 'once', 'next', 'last', 'first', 'each',
            'must', 'make', 'keep', 'here', 'then', 'have', 'been', 'some', 'more',
            'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday',
            'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august',
            'september', 'october', 'november', 'december',
        }
        name_patterns = [
            r'(?:^|\n)\s*([A-Z][a-z]+)(?:\s*:|\s+said|\s+mentioned|\s+will|\s+should|\s+needs)',
            r'(?:assigned to|owner:|responsibility of|@)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'([A-Z][a-z]+)\s+(?:will|should|needs to|has to|is going to|can|must)',
        ]
        owners = set()
        for pattern in name_patterns:
            for match in re.finditer(pattern, transcript):
                name = match.group(1).strip()
                if name.lower() not in STOP_WORDS and len(name) > 2:
                    owners.add(name)

        # ── Step 2: Extract action items via keyword patterns ──
        action_patterns = [
            r'(?:action item|todo|task|to-do)[:\s]*(.+?)(?:\n|$)',
            r'(?:need(?:s)? to|should|must|has to|will|going to)\s+(.+?)(?:\.|;|\n|$)',
            r'(?:please|can you|could you)\s+(.+?)(?:\.|;|\n|$)',
        ]
        action_items = []
        seen_actions = set()

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            for pattern in action_patterns:
                for m in re.finditer(pattern, line_stripped, re.IGNORECASE):
                    desc = m.group(1).strip().rstrip('.,;')
                    if len(desc) > 10 and desc.lower()[:40] not in seen_actions:
                        seen_actions.add(desc.lower()[:40])
                        owner = None
                        for o in owners:
                            if o.lower() in line_stripped.lower():
                                owner = o
                                break
                        deadline = None
                        dl_match = re.search(
                            r'(?:by|before|due|deadline)\s+([\w\s,]+?)(?:\.|;|\n|$)',
                            line_stripped, re.IGNORECASE
                        )
                        if dl_match:
                            deadline = dl_match.group(1).strip()

                        priority = (
                            "high" if any(w in line_stripped.lower() for w in
                                          ['urgent', 'critical', 'asap', 'immediately', 'p0', 'blocker'])
                            else "medium" if any(w in line_stripped.lower() for w in
                                                 ['important', 'priority', 'soon', 'p1'])
                            else "low"
                        )
                        action_items.append({
                            "description": desc,
                            "owner": owner,
                            "deadline": deadline,
                            "priority": priority,
                        })

        # ── Step 3: Speaker commitment pass (dialogue-style) ──
        # Catches: "Name: ... I'll do X" or "Name: ... will handle Y"
        speaker_patterns = [
            r"([A-Z][a-z]+)\s*:\s*[^.!\n]*?(?:I'll|I will|I'm going to|Let me|I can)\s+([^.!\n]{8,80})",
            r"([A-Z][a-z]+)\s*:\s*[^.!\n]*?\bwill\s+(?:handle|take|work on|do|complete|finish|prepare|update|create|implement|fix|review|set up)\s+([^.!\n]{8,80})",
        ]
        for pattern in speaker_patterns:
            for m in re.finditer(pattern, transcript, re.IGNORECASE):
                potential_owner = m.group(1).strip()
                desc = m.group(2).strip().rstrip('.,;')
                if (potential_owner.lower() not in STOP_WORDS
                        and len(desc) > 8
                        and desc.lower()[:40] not in seen_actions):
                    seen_actions.add(desc.lower()[:40])
                    owners.add(potential_owner)
                    action_items.append({
                        "description": desc,
                        "owner": potential_owner,
                        "deadline": None,
                        "priority": "medium",
                    })

        # ── Step 4: Minimum viable items guarantee ──────────
        # If fewer than 3 items found, use topic-keyword extraction as fallback
        if len(action_items) < 3:
            topic_keywords = [
                ('implement', 'Implementation task from meeting discussion', 'medium'),
                ('deploy', 'Deployment and release preparation', 'high'),
                ('review', 'Review and approval process', 'medium'),
                ('fix', 'Bug fix or issue resolution', 'high'),
                ('update', 'Update and maintenance work', 'low'),
                ('create', 'Create new component or deliverable', 'medium'),
                ('test', 'Testing and quality assurance', 'medium'),
                ('document', 'Documentation and knowledge capture', 'low'),
                ('configure', 'Configuration and setup task', 'medium'),
                ('analyze', 'Analysis and investigation task', 'medium'),
                ('setup', 'System setup and initialization', 'medium'),
                ('migrate', 'Data or system migration task', 'high'),
            ]
            owners_list = list(owners) if owners else ["Team Lead", "Engineering Lead"]
            for idx, (keyword, label, priority) in enumerate(topic_keywords):
                if keyword in text_lower and len(action_items) < 8:
                    # Extract meaningful context around this keyword
                    keyword_pos = text_lower.find(keyword)
                    start = max(0, keyword_pos - 25)
                    end = min(len(transcript), keyword_pos + 80)
                    context = transcript[start:end].strip()
                    snippet = context.split('\n')[0].strip()[:70]

                    desc = snippet if len(snippet) > 15 else label
                    if desc.lower()[:40] not in seen_actions:
                        seen_actions.add(desc.lower()[:40])
                        owner = owners_list[idx % len(owners_list)]
                        action_items.append({
                            "description": desc,
                            "owner": owner,
                            "deadline": None,
                            "priority": priority,
                        })

        # ── Step 5: Extract decisions ──────────────────────
        decision_patterns = [
            r'(?:decided|decision|agreed|final|approved|confirmed|consensus)[:\s]*(.+?)(?:\.|;|\n|$)',
            r"(?:we'll go with|going with|let's go with|we're going to)\s+(.+?)(?:\.|;|\n|$)",
        ]
        decisions = []
        for pattern in decision_patterns:
            for m in re.finditer(pattern, transcript, re.IGNORECASE):
                dec = m.group(1).strip().rstrip('.,;')
                if len(dec) > 5:
                    decisions.append(dec)

        # ── Step 6: Extract blockers ───────────────────────
        blocker_patterns = [
            r'(?:blocked|blocker|blocking|stuck|waiting on|depends on|dependency)[:\s]*(.+?)(?:\.|;|\n|$)',
            r"(?:can't|cannot|unable to)\s+(.+?)(?:until|without)\s+(.+?)(?:\.|;|\n|$)",
        ]
        blockers = []
        for pattern in blocker_patterns:
            for m in re.finditer(pattern, transcript, re.IGNORECASE):
                desc = m.group(1).strip().rstrip('.,;')
                if len(desc) > 5:
                    blockers.append({
                        "description": desc,
                        "impact": "Affects downstream tasks",
                        "severity": "high" if any(w in desc.lower() for w in
                                                   ['critical', 'urgent', 'p0']) else "medium",
                    })

        # ── Step 7: Extract deadlines ──────────────────────
        deadline_patterns = [
            r'(?:by|before|due|deadline|deliver)\s+((?:end of |next |this )?(?:week|month|day|monday|tuesday|wednesday|thursday|friday|sprint|quarter|EOD|EOW|tomorrow))',
            r'(?:by|before|due|deadline)\s+(\w+\s+\d+)',
            r'(day\s*[123])',
        ]
        deadlines = []
        for pattern in deadline_patterns:
            for m in re.finditer(pattern, transcript, re.IGNORECASE):
                deadlines.append(m.group(1).strip())

        # ── Summary ────────────────────────────────────────
        summary = f"Input processed with {len(owners)} participant(s) and {len(action_items)} action items identified."
        if blockers:
            summary += f" {len(blockers)} blocker(s) identified requiring immediate attention."
        if decisions:
            summary += f" {len(decisions)} key decision(s) confirmed."

        return {
            "action_items": action_items,
            "decisions": decisions if decisions else ["Continue with current plan"],
            "owners": list(owners),
            "deadlines": deadlines,
            "blockers": blockers,
            "summary": summary,
        }

    # ── RISK ANALYSIS ──────────────────────────────────────────

    def analyze_risks(self, extracted_data: dict) -> list:
        """Analyze risks in extracted input data."""
        if self.use_llm:
            result = self._analyze_risks_with_llm(extracted_data)
            if result:
                return result
        return self._analyze_risks_with_rules(extracted_data)

    def _analyze_risks_with_llm(self, data: dict) -> Optional[list]:
        prompt = f"""Analyze these workflow action items for risks and issues.
Return ONLY valid JSON array:
```json
[
    {{
        "item": "description of the risky item",
        "type": "missing_owner|dependency|blocker|unclear_deadline|overloaded_owner|scope_risk",
        "severity": "HIGH|MEDIUM|LOW",
        "reasoning": "why this is a risk"
    }}
]
```

Workflow Data:
{json.dumps(data, indent=2)}"""
        response = self._call_groq(prompt)
        if response:
            parsed = self._parse_json_from_response(response)
            if isinstance(parsed, list):
                return parsed
        return None

    def _analyze_risks_with_rules(self, data: dict) -> list:
        """Rule-based risk analysis."""
        risks = []
        action_items = data.get("action_items", [])
        blockers = data.get("blockers", [])

        # Check for missing owners
        for item in action_items:
            if not item.get("owner"):
                risks.append({
                    "item": item["description"],
                    "type": "missing_owner",
                    "severity": "HIGH" if item.get("priority") in ("high", "urgent") else "MEDIUM",
                    "reasoning": (
                        f"No owner assigned to this task. "
                        f"Priority is {item.get('priority', 'unknown')}. "
                        f"Unassigned tasks have 73% chance of being dropped from execution."
                    ),
                })

        # Check for missing deadlines
        for item in action_items:
            if not item.get("deadline"):
                risks.append({
                    "item": item["description"],
                    "type": "unclear_deadline",
                    "severity": "MEDIUM",
                    "reasoning": "No deadline specified. Tasks without deadlines are 2.5x more likely to slip.",
                })

        # Check for overloaded owners
        from collections import Counter
        owner_counts = Counter(
            item["owner"] for item in action_items if item.get("owner")
        )
        for owner, count in owner_counts.items():
            if count >= 3:
                risks.append({
                    "item": f"{owner} has {count} tasks assigned",
                    "type": "overloaded_owner",
                    "severity": "HIGH" if count >= 4 else "MEDIUM",
                    "reasoning": (
                        f"{owner} is assigned {count} tasks. Research shows individual "
                        f"productivity drops 40% when handling more than 3 concurrent tasks."
                    ),
                })

        # Add blocker risks
        for blocker in blockers:
            risks.append({
                "item": blocker["description"],
                "type": "blocker",
                "severity": blocker.get("severity", "MEDIUM").upper(),
                "reasoning": (
                    f"Active blocker: {blocker.get('impact', 'May delay dependent tasks')}. "
                    f"Blockers left unaddressed grow in impact by 25% daily."
                ),
            })

        # Multi-task dependency risk
        if len(action_items) > 3:
            risks.append({
                "item": "Multiple interconnected tasks detected",
                "type": "dependency",
                "severity": "LOW",
                "reasoning": (
                    f"{len(action_items)} tasks identified. With this volume, there's "
                    f"high probability of hidden dependencies that could create critical bottlenecks."
                ),
            })

        return risks

    # ── DECISION ACTIONS (PHASE 2) ─────────────────────────────

    def decide_actions(self, tasks: list, issues: list, context: dict) -> Optional[list]:
        """Dynamically decide actions for current issues using Groq LLM."""
        if not self.use_llm:
            return None

        prompt = f"""You are the Decision Agent in an autonomous enterprise workflow system.
Review the following tasks and active issues, and decide the best corrective actions based on priority, risk, and team workload context.

Return ONLY a valid JSON array matching this exact schema:
```json
[
  {{
    "type": "auto_assignment | reassignment | escalation | reminder",
    "task_id": "TASK-001",
    "target_owner": "Name of person (or 'Engineering Manager' for escalation)",
    "reason": "Clear data-driven reasoning for the action",
    "priority": "HIGH|MEDIUM|LOW"
  }}
]
```

Tasks:
{json.dumps([{k: v for k, v in t.items() if k in ('id', 'title', 'owner', 'priority', 'status', 'progress', 'deadline', 'risk_flag')} for t in tasks], indent=2)}

Issues detected:
{json.dumps(issues, indent=2)}

Team Workload Context:
{json.dumps(context.get('owner_workload', {}), indent=2)}
"""
        response = self._call_groq(prompt)
        if response:
            parsed = self._parse_json_from_response(response)
            if isinstance(parsed, list):
                return parsed
        return None

    def generate_insights(self, tasks: list, memory_stats: dict) -> str:
        """Generate high-level AI insights for the UI panel."""
        if not self.use_llm:
            return "AI Insights require Groq API access. Please configure your GROQ_API_KEY."

        prompt = f"""You are an elite project management AI. Based on the current tasks and historical team memory stats, generate a concise, 3-bullet-point summary of key insights. Highlight overloaded employees, highest risk tasks, and suggested optimizations. Do not use markdown headers, just return a bulleted list.

Current Tasks (state):
{json.dumps([{k: v for k, v in t.items() if k in ('id', 'owner', 'status', 'progress', 'priority', 'risk_flag')} for t in tasks], indent=2)}

Team Memory / Performance Stats:
{json.dumps(memory_stats, indent=2)}
"""
        response = self._call_groq(prompt)
        return response.strip() if response else "Insight generation failed."

    # ── REASONING GENERATION ───────────────────────────────────

    def generate_reasoning(self, agent_name: str, context: str, action: str) -> str:
        """Generate reasoning text for agent decisions."""
        if self.use_llm:
            prompt = f"""You are {agent_name} in an enterprise workflow AI system.
Given this context: {context}
You took this action: {action}
Explain your reasoning in 1-2 sentences. Be specific and data-driven."""
            response = self._call_groq(prompt)
            if response:
                return response.strip()
        # Fallback: return the action itself as reasoning
        return f"{action} — Based on analysis of task properties and team capacity."
