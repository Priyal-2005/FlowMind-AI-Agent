"""
Extraction Agent — Input Data Parser

Takes raw input text and extracts structured data:
- Action items with owners and deadlines
- Decisions identified in the input
- Participants/owners mentioned
- Deadlines and timeframes
- Blockers and impediments
"""

import time
from typing import Any
from agents.base import BaseAgent


class ExtractionAgent(BaseAgent):
    """Parses input text into structured actionable data."""

    def __init__(self):
        super().__init__(
            name="Extraction Agent",
            icon="🔍",
            description="Parses input text to extract action items, decisions, owners, deadlines, and blockers",
        )

    def process(self, input_data: Any, context: dict) -> dict:
        transcript = input_data
        llm = context["llm"]
        logger = context["logger"]

        logger.log(
            self.name,
            "Starting input analysis",
            f"Processing {len(transcript)} characters of input text using {llm.mode}",
        )
        self.add_log(f"📄 Received input ({len(transcript)} chars)")
        time.sleep(0.3)  # Visual delay for demo

        # Extract structured data from input
        self.add_log(f"🔬 Analyzing with {llm.mode}...")
        time.sleep(0.5)
        extracted = llm.extract_input_data(transcript)

        action_items = extracted.get("action_items", [])
        decisions = extracted.get("decisions", [])
        owners = extracted.get("owners", [])
        deadlines = extracted.get("deadlines", [])
        blockers = extracted.get("blockers", [])
        summary = extracted.get("summary", "")

        self.add_log(f"✅ Found {len(action_items)} action items")
        self.add_log(f"📋 Found {len(decisions)} decisions")
        self.add_log(f"👥 Identified {len(owners)} team members: {', '.join(owners)}")
        self.add_log(f"⏰ Found {len(deadlines)} deadlines")
        self.add_log(f"🚧 Found {len(blockers)} blockers")

        logger.log(
            self.name,
            f"Extraction complete: {len(action_items)} action items, {len(decisions)} decisions, "
            f"{len(blockers)} blockers from {len(owners)} participants",
            f"Used {llm.mode} to parse transcript. "
            f"Identified key participants: {', '.join(owners)}. "
            f"Summary: {summary}",
        )

        time.sleep(0.2)

        return {
            "action_items": action_items,
            "decisions": decisions,
            "owners": owners,
            "deadlines": deadlines,
            "blockers": blockers,
            "summary": summary,
            "raw_transcript": transcript,
        }
