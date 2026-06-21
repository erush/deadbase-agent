import re

from skill_executors.song_history import execute as song_history_execute
from skill_executors.show_lookup import execute as show_lookup_execute
from skill_executors.venue_analysis import execute as venue_analysis_execute


class DeadBaseAgent:

    def route(self, query: str):

        query_lower = query.lower()

        if re.search(r"\d{4}/\d{2}/\d{2}", query):
            return "show-lookup"

        if any(
            phrase in query_lower
            for phrase in [
                "first played",
                "last played",
                "how many times",
                "song history",
                "dark star",
                "scarlet",
                "althea",
                "morning dew",
                "fire on the mountain",
            ]
        ):
            return "song-history"

        if any(
            phrase in query_lower
            for phrase in [
                "venue",
                "winterland",
                "barton hall",
                "fillmore",
            ]
        ):
            return "venue-analysis"

        return "unknown"

    def execute(self, query: str):

        skill = self.route(query)

        if skill == "show-lookup":

            match = re.search(
                r"\d{4}/\d{2}/\d{2}",
                query
            )

            if not match:
                return {
                    "skill": skill,
                    "error": "show date not found"
                }

            show_date = match.group()

            return show_lookup_execute(show_date)

        if skill == "song-history":

            song_candidates = [
                "Dark Star",
                "Scarlet Begonias",
                "Althea",
                "Fire On The Mountain",
                "Morning Dew",
            ]

            song_name = None

            for candidate in song_candidates:

                if candidate.lower() in query.lower():

                    song_name = candidate
                    break

            if not song_name:
                return {
                    "skill": skill,
                    "error": "song not identified"
                }

            return song_history_execute(song_name)

        if skill == "venue-analysis":

            venue_candidates = [
                "Winterland",
                "Barton Hall",
                "Fillmore",
            ]

            venue_name = None

            for candidate in venue_candidates:

                if candidate.lower() in query.lower():

                    venue_name = candidate
                    break

            if not venue_name:
                return {
                    "skill": skill,
                    "error": "venue not identified"
                }

            return venue_analysis_execute(venue_name)

        return {
            "skill": "unknown",
            "error": "unable to route query"
        }