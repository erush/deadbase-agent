from agents.similarity_agent import execute as similarity_agent
from agents.song_agent import execute as song_agent
from agents.venue_agent import execute as venue_agent

from skill_executors.show_lookup import execute as show_lookup
from skill_executors.show_intelligence import execute as show_intelligence


class HistorianAgent:

    def analyze(self, show_date: str):

        show_result = show_lookup(show_date)

        if not show_result["found"]:
            return {
                "agent": "historian-agent",
                "found": False,
                "answer": f"No show found for {show_date}.",
            }

        intelligence_result = show_intelligence(show_date)
        similarity_result = similarity_agent(show_date)
        venue_result = venue_agent(show_result["venue"])

        song_results = []

        signature_songs = show_result["setlist"][-6:]

        for song in signature_songs:
            try:
                song_results.append(song_agent(song))
            except Exception:
                pass

        lines = []

        lines.append(f"Historical Investigation: {show_date}")
        lines.append("=" * 40)
        lines.append("")

        lines.append(
            f"The Grateful Dead performed at {show_result['venue']} "
            f"in {show_result['city']}, {show_result['state']}."
        )

        lines.append("")

        lines.append("Show Intelligence")
        lines.append("-----------------")

        if intelligence_result.get("found"):
            lines.append(
                f"This profiles as a {intelligence_result['era']} show "
                f"with {intelligence_result['show_length']} songs, "
                f"{intelligence_result['unique_song_count']} unique songs, "
                f"{intelligence_result['set_count']} sets, and a segue ratio "
                f"of {intelligence_result['segue_ratio']}."
            )
            lines.append(
                f"Historian score: {intelligence_result['historian_score']}."
            )

        lines.append("")
        lines.append("Venue Context")
        lines.append("-------------")

        if venue_result.get("found"):
            lines.append(
                f"{venue_result['venue']} hosted {venue_result['show_count']} "
                f"Grateful Dead performances between "
                f"{venue_result['first_show']} and {venue_result['last_show']}."
            )

            if venue_result.get("avg_show_length") is not None:
                lines.append(
                    f"Average show length at this venue: "
                    f"{venue_result['avg_show_length']} songs."
                )

            if venue_result.get("avg_segue_ratio") is not None:
                lines.append(
                    f"Average venue segue ratio: "
                    f"{venue_result['avg_segue_ratio']}."
                )

        lines.append("")
        lines.append("Closest Setlist Neighbors")
        lines.append("-------------------------")

        for rec in similarity_result.get("recommendations", [])[:5]:
            lines.append(
                f"- {rec['show_date']} at {rec['venue']} "
                f"({rec['city']}, {rec['state']}) "
                f"| similarity {rec['similarity']} "
                f"| {rec['shared_song_count']} shared songs"
            )

        lines.append("")
        lines.append("Signature Song Context")
        lines.append("----------------------")

        for song in song_results:
            if song.get("found"):
                lines.append(
                    f"- {song['song']}: {song['performance_count']} "
                    f"archive performances; first played "
                    f"{song['first_performance']['date']}."
                )

        lines.append("")
        lines.append("Interpretation")
        lines.append("--------------")

        lines.append(
            "This show should not be judged only by whether its setlist was unique. "
            "The stronger historical signal comes from the combination of era profile, "
            "venue rarity, repertoire, segue structure, and nearby shows in the archive."
        )

        answer = "\n".join(lines)

        return {
            "agent": "historian-agent",
            "show_date": show_date,
            "answer": answer,
            "evidence": {
                "show": show_result,
                "show_intelligence": intelligence_result,
                "similarity": similarity_result,
                "venue": venue_result,
                "songs": song_results,
            },
        }


agent = HistorianAgent()


def execute(show_date: str):
    return agent.analyze(show_date)