from __future__ import annotations

import copy
import re
from datetime import datetime
from typing import Any


class DeadBaseAgent:
    """
    DeadBase planning agent.

    This file is not the Kaggle terminal demo.
    This file owns intent detection, workflow planning, and entity extraction.

    demo.py remains the live presentation layer.
    """

    SHOW_INVESTIGATION = {
        "intent": "historical_show_investigation",
        "skills": [
            "show-lookup",
            "show-intelligence",
            "venue-analysis",
            "setlist-similarity",
            "song-history",
            "synthesis",
        ],
        "mcp_tools": [
            "deadbase_find_show",
            "deadbase_find_venue",
        ],
    }

    SONG_HISTORY = {
        "intent": "song_history",
        "skills": [
            "song-history",
        ],
        "mcp_tools": [
            "deadbase_find_song",
        ],
    }

    VENUE_ANALYSIS = {
        "intent": "venue_analysis",
        "skills": [
            "venue-analysis",
        ],
        "mcp_tools": [
            "deadbase_find_venue",
        ],
    }

    SONG_CANDIDATES = [
        "Dark Star",
        "Scarlet Begonias",
        "Althea",
        "Fire On The Mountain",
        "Morning Dew",
        "Bird Song",
        "Jack Straw",
        "Loser",
        "Bertha",
        "Stagger Lee",
        "New Minglewood Blues",
        "They Love Each Other",
        "Alabama Getaway",
        "Greatest Story Ever Told",
    ]

    VENUE_CANDIDATES = [
        "Winterland",
        "Barton Hall",
        "Fillmore",
        "Frost Amphitheatre",
        "Manor Downs",
        "Greek Theatre",
        "Madison Square Garden",
        "Veneta",
        "Saratoga Performing Arts Center",
    ]

    SHOW_ALIASES = {
        "cornell": {
            "show_date": "1977/05/08",
            "venue": "Barton Hall",
        },
        "barton hall": {
            "show_date": "1977/05/08",
            "venue": "Barton Hall",
        },
        "veneta": {
            "show_date": "1972/08/27",
            "venue": "Old Renaissance Faire Grounds",
        },
    }

    def plan(self, query: str) -> dict[str, Any]:
        query_lower = query.lower()
        entities = self.extract_entities(query)

        if self.is_song_history_query(query_lower, entities):
            return self.build_plan(
                self.SONG_HISTORY,
                entities,
            )

        if self.is_venue_query(query_lower, entities):
            return self.build_plan(
                self.VENUE_ANALYSIS,
                entities,
            )

        if self.is_show_investigation_query(query_lower, entities):
            return self.build_plan(
                self.SHOW_INVESTIGATION,
                entities,
            )

        return {
            "intent": "unknown",
            "skills": [],
            "mcp_tools": [],
            "entities": entities,
        }

    def build_plan(
        self,
        workflow: dict[str, Any],
        entities: dict[str, Any],
    ) -> dict[str, Any]:
        plan = copy.deepcopy(workflow)
        plan["entities"] = entities
        return plan

    def extract_entities(self, query: str) -> dict[str, Any]:
        query_lower = query.lower()
        entities: dict[str, Any] = {}

        date = self.extract_date(query)
        if date:
            entities["show_date"] = date

        year_match = re.search(r"\b(19[6-9][0-9])\b", query)
        if year_match:
            entities["year"] = year_match.group(1)

        for alias, alias_entities in self.SHOW_ALIASES.items():
            if alias in query_lower:
                entities.update(alias_entities)

        for song in self.SONG_CANDIDATES:
            if song.lower() in query_lower:
                entities["song"] = song
                break

        for venue in self.VENUE_CANDIDATES:
            if venue.lower() in query_lower:
                entities["venue"] = venue
                break

        if "second set" in query_lower:
            entities["set_number"] = 2
        elif "first set" in query_lower:
            entities["set_number"] = 1
        elif "third set" in query_lower:
            entities["set_number"] = 3

        return entities

    def extract_date(self, query: str) -> str | None:
        match = re.search(
            r"\d{4}/\d{1,2}/\d{1,2}|\d{4}-\d{1,2}-\d{1,2}|\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}-\d{1,2}-\d{2,4}",
            query,
        )

        if not match:
            return None

        raw = match.group(0)

        formats = [
            "%Y/%m/%d",
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%m-%d-%Y",
            "%m/%d/%y",
            "%m-%d-%y",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(raw, fmt).strftime("%Y/%m/%d")
            except ValueError:
                continue

        return None

    def is_song_history_query(
        self,
        query_lower: str,
        entities: dict[str, Any],
    ) -> bool:
        if "song" in entities and any(
            phrase in query_lower
            for phrase in [
                "first played",
                "first performance",
                "last played",
                "last performance",
                "how often",
                "how many times",
                "played in",
                "song history",
            ]
        ):
            return True

        return any(
            phrase in query_lower
            for phrase in [
                "when was dark star",
                "when was scarlet begonias",
                "when was althea",
                "when was morning dew",
            ]
        )

    def is_venue_query(
        self,
        query_lower: str,
        entities: dict[str, Any],
    ) -> bool:
        if "venue" in query_lower:
            return True

        if "venue" in entities and any(
            phrase in query_lower
            for phrase in [
                "tell me about",
                "hosted the most",
                "most commonly played",
                "songs were most commonly played",
                "profile",
            ]
        ):
            return True

        return False

    def is_show_investigation_query(
        self,
        query_lower: str,
        entities: dict[str, Any],
    ) -> bool:
        if "show_date" in entities:
            return True

        return any(
            phrase in query_lower
            for phrase in [
                "cornell",
                "veneta",
                "setlist",
                "unique",
                "historical investigation",
                "investigate",
                "compare",
                "similar",
                "what was played",
                "what songs were played",
            ]
        )

    def execute(self, query: str) -> dict[str, Any]:
        """Compatibility wrapper around the planner."""

        plan = self.plan(query)

        return {
            "found": bool(plan["skills"]),
            "question": query,
            "intent": plan["intent"],
            "skills": plan["skills"],
            "mcp_tools": plan["mcp_tools"],
            "entities": plan.get("entities", {}),
            "plan": plan,
        }

    def investigate(self, question: str) -> dict[str, Any]:
        """
        Future orchestration entrypoint.

        For the Kaggle submission this method owns planning and returns a
        canonical investigation object. Execution continues inside demo.py
        until the orchestration layer is migrated.
        """

        plan = self.plan(question)

        if not plan["skills"]:
            raise RuntimeError(
                f"Planning Agent could not determine a workflow for: {question}"
            )

        return {
            "question": question,
            "intent": plan["intent"],
            "skills": plan["skills"],
            "mcp_tools": plan["mcp_tools"],
            "entities": plan.get("entities", {}),
            "plan": plan,
        }