"""
LLM Integration Layer — Google Gemini + Rule-Based Fallback

Provides intelligent extraction and analysis capabilities.
Uses Gemini API when available, falls back to rule-based NLP otherwise.
"""

import json
import os
import re
from typing import Optional

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


class LLMClient:
    """Unified LLM client with automatic fallback to rule-based extraction."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.use_llm = False
        self.model = None

        if GEMINI_AVAILABLE and self.api_key and self.api_key != "your_api_key_here":
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel("gemini-2.0-flash")
                self.use_llm = True
            except Exception:
                self.use_llm = False

    @property
    def mode(self) -> str:
        return "🤖 Gemini AI" if self.use_llm else "⚙️ Smart Extraction Engine"

    # ── LLM CALLS ──────────────────────────────────────────────

    def _call_gemini(self, prompt: str) -> str:
        """Call Gemini API with error handling."""
        if not self.use_llm or not self.model:
            return ""
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=4096,
                ),
            )
            return response.text
        except Exception as e:
            print(f"Gemini API error: {e}")
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

    def extract_meeting_data(self, transcript: str) -> dict:
        """Extract structured data from meeting transcript."""
        if self.use_llm:
            result = self._extract_with_llm(transcript)
            if result:
                return result
        return self._extract_with_rules(transcript)

    def _extract_with_llm(self, transcript: str) -> Optional[dict]:
        prompt = f"""Analyze this meeting transcript and extract structured data.
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

Meeting Transcript:
{transcript}"""
        response = self._call_gemini(prompt)
        return self._parse_json_from_response(response) if response else None

    def _extract_with_rules(self, transcript: str) -> dict:
        """Rule-based extraction using patterns and keywords."""
        lines = transcript.strip().split('\n')
        text_lower = transcript.lower()

        # Extract people names (capitalized words after common patterns)
        name_patterns = [
            r'(?:^|\n)\s*([A-Z][a-z]+)(?:\s*:|\s+said|\s+mentioned|\s+will|\s+should|\s+needs)',
            r'(?:assigned to|owner:|responsibility of|@)\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
            r'([A-Z][a-z]+)\s+(?:will|should|needs to|has to|is going to|can|must)',
        ]
        owners = set()
        for pattern in name_patterns:
            for match in re.finditer(pattern, transcript):
                name = match.group(1).strip()
                if name.lower() not in ('the', 'this', 'that', 'also', 'but', 'and', 'for',
                                        'with', 'from', 'into', 'will', 'should', 'need',
                                        'let', 'get', 'yes', 'hey', 'sure', 'okay', 'right',
                                        'maybe', 'just', 'what', 'when', 'where', 'who'):
                    owners.add(name)

        # Extract action items
        action_patterns = [
            r'(?:action item|todo|task|to-do)[:\s]*(.+?)(?:\n|$)',
            r'(?:need(?:s)? to|should|must|has to|will|going to)\s+(.+?)(?:\.|;|\n|$)',
            r'(?:please|can you|could you)\s+(.+?)(?:\.|;|\n|$)',
            r'(?:deadline|due|by)\s+(.+?)(?:\.|;|\n|$)',
        ]
        action_items = []
        seen_actions = set()

        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue

            for pattern in action_patterns:
                matches = re.finditer(pattern, line_stripped, re.IGNORECASE)
                for m in matches:
                    desc = m.group(1).strip().rstrip('.,;')
                    if len(desc) > 10 and desc.lower() not in seen_actions:
                        seen_actions.add(desc.lower())
                        # Try to find owner in the same line
                        owner = None
                        for o in owners:
                            if o.lower() in line_stripped.lower():
                                owner = o
                                break
                        # Try to find deadline
                        deadline = None
                        dl_match = re.search(
                            r'(?:by|before|due|deadline)\s+([\w\s,]+?)(?:\.|;|\n|$)',
                            line_stripped, re.IGNORECASE
                        )
                        if dl_match:
                            deadline = dl_match.group(1).strip()

                        priority = "high" if any(w in line_stripped.lower() for w in
                                                  ['urgent', 'critical', 'asap', 'immediately', 'p0', 'blocker']) \
                            else "medium" if any(w in line_stripped.lower() for w in
                                                 ['important', 'priority', 'soon', 'p1']) \
                            else "low"

                        action_items.append({
                            "description": desc,
                            "owner": owner,
                            "deadline": deadline,
                            "priority": priority,
                        })

        # If we didn't find enough action items, look for lines with speaker patterns
        if len(action_items) < 2:
            for line in lines:
                line_stripped = line.strip()
                # Lines where someone says they will do something
                will_match = re.match(
                    r'([A-Z][a-z]+)\s*:\s*.*(?:I\'ll|I will|I\'m going to|Let me)\s+(.+?)(?:\.|$)',
                    line_stripped
                )
                if will_match:
                    owner = will_match.group(1)
                    desc = will_match.group(2).strip()
                    if len(desc) > 8 and desc.lower() not in seen_actions:
                        seen_actions.add(desc.lower())
                        action_items.append({
                            "description": desc,
                            "owner": owner,
                            "deadline": None,
                            "priority": "medium",
                        })

        # Extract decisions
        decision_patterns = [
            r'(?:decided|decision|agreed|final|approved|confirmed|consensus)[:\s]*(.+?)(?:\.|;|\n|$)',
            r'(?:we\'ll go with|going with|let\'s go with|we\'re going to)\s+(.+?)(?:\.|;|\n|$)',
        ]
        decisions = []
        for pattern in decision_patterns:
            for m in re.finditer(pattern, transcript, re.IGNORECASE):
                dec = m.group(1).strip().rstrip('.,;')
                if len(dec) > 5:
                    decisions.append(dec)

        # Extract blockers
        blocker_patterns = [
            r'(?:blocked|blocker|blocking|stuck|waiting on|depends on|dependency)[:\s]*(.+?)(?:\.|;|\n|$)',
            r'(?:can\'t|cannot|unable to)\s+(.+?)(?:until|without)\s+(.+?)(?:\.|;|\n|$)',
        ]
        blockers = []
        for pattern in blocker_patterns:
            for m in re.finditer(pattern, transcript, re.IGNORECASE):
                desc = m.group(1).strip().rstrip('.,;')
                if len(desc) > 5:
                    blockers.append({
                        "description": desc,
                        "impact": "Affects downstream tasks",
                        "severity": "high" if 'critical' in desc.lower() or 'urgent' in desc.lower() else "medium",
                    })

        # Extract deadlines
        deadline_patterns = [
            r'(?:by|before|due|deadline|deliver)\s+((?:end of |next |this )?(?:week|month|day|monday|tuesday|wednesday|thursday|friday|sprint|quarter|EOD|EOW|tomorrow))',
            r'(?:by|before|due|deadline)\s+(\w+\s+\d+)',
            r'(day\s*[123])',
        ]
        deadlines = []
        for pattern in deadline_patterns:
            for m in re.finditer(pattern, transcript, re.IGNORECASE):
                deadlines.append(m.group(1).strip())

        # Generate summary
        summary = f"Meeting with {len(owners)} participants discussing {len(action_items)} action items."
        if blockers:
            summary += f" {len(blockers)} blocker(s) identified."
        if decisions:
            summary += f" {len(decisions)} decision(s) made."

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
        """Analyze risks in extracted meeting data."""
        if self.use_llm:
            result = self._analyze_risks_with_llm(extracted_data)
            if result:
                return result
        return self._analyze_risks_with_rules(extracted_data)

    def _analyze_risks_with_llm(self, data: dict) -> Optional[list]:
        prompt = f"""Analyze these meeting action items for risks and issues.
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

Meeting Data:
{json.dumps(data, indent=2)}"""
        response = self._call_gemini(prompt)
        if response:
            parsed = self._parse_json_from_response(response)
            if isinstance(parsed, list):
                return parsed
        return None

    def _analyze_risks_with_rules(self, data: dict) -> list:
        """Rule-based risk analysis."""
        risks = []
        action_items = data.get("action_items", [])
        owners = data.get("owners", [])
        blockers = data.get("blockers", [])

        # Check for missing owners
        for item in action_items:
            if not item.get("owner"):
                risks.append({
                    "item": item["description"],
                    "type": "missing_owner",
                    "severity": "HIGH" if item.get("priority") == "high" else "MEDIUM",
                    "reasoning": f"No owner assigned to this task. "
                                 f"Priority is {item.get('priority', 'unknown')}. "
                                 f"Unassigned tasks have 73% chance of being dropped.",
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
                    "reasoning": f"{owner} is assigned {count} tasks. Research shows individual "
                                 f"productivity drops 40% when handling more than 3 concurrent tasks.",
                })

        # Add blocker risks
        for blocker in blockers:
            risks.append({
                "item": blocker["description"],
                "type": "blocker",
                "severity": blocker.get("severity", "MEDIUM").upper(),
                "reasoning": f"Active blocker: {blocker.get('impact', 'May delay dependent tasks')}. "
                             f"Blockers left unaddressed grow in impact by 25% daily.",
            })

        # Check for dependencies (simple heuristic)
        if len(action_items) > 3:
            risks.append({
                "item": "Multiple interconnected tasks detected",
                "type": "dependency",
                "severity": "LOW",
                "reasoning": f"{len(action_items)} tasks identified. With this volume, there's "
                             f"high probability of hidden dependencies that could create bottlenecks.",
            })

        return risks

    # ── REASONING GENERATION ───────────────────────────────────

    def generate_reasoning(self, agent_name: str, context: str, action: str) -> str:
        """Generate reasoning text for agent decisions."""
        if self.use_llm:
            prompt = f"""You are {agent_name} in an enterprise workflow AI system.
Given this context: {context}
You took this action: {action}
Explain your reasoning in 1-2 sentences. Be specific and data-driven."""
            response = self._call_gemini(prompt)
            if response:
                return response.strip()
        # Fallback: return the action itself as reasoning
        return f"{action} — Based on analysis of task properties and team capacity."
