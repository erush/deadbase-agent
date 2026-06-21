class SynthesisAgent:

    def assess_show(self, research_result: dict):

        show_date = research_result["show_date"]
        rank = research_result["historian_rank"]
        percentile = research_result["historian_percentile"]
        primary = research_result["primary_archetype"]
        secondary = research_result["secondary_archetype"]

        if percentile >= 95:
            significance_band = "elite historical outlier"
        elif percentile >= 85:
            significance_band = "high-significance archive show"
        elif percentile >= 70:
            significance_band = "notable but not extreme archive show"
        else:
            significance_band = "standard archive show"

        if primary == "Standard Performance":
            archetype_read = (
                "The archetype model does not classify this show as structurally unusual."
            )
        else:
            archetype_read = (
                f"The primary archetype is {primary}, which indicates a measurable "
                f"structural or historical signal in the archive."
            )

        if secondary and secondary != "None":
            archetype_read += f" A secondary signal appears as {secondary}."

        if rank > 250:
            reputation_read = (
                "This creates an important tension: the show is culturally famous, "
                "but the current archive model does not rank it among the most extreme "
                "shows by measurable structure, rarity, venue weight, or song rarity."
            )
        else:
            reputation_read = (
                "The model supports the show's reputation with a high archive ranking."
            )

        answer = f"""
Historical Assessment: {show_date}
==================================

Model Position
--------------
This show ranks #{rank} in the archive, placing it in the {round(percentile, 2)} percentile.

DeadBase classifies it as a {significance_band}.

Archetype Assessment
--------------------
{archetype_read}

Interpretive Finding
--------------------
{reputation_read}

Conclusion
----------
The strongest historical reading is that this show's importance should not be explained by setlist uniqueness alone. DeadBase separates measurable archive signals from cultural reputation, allowing a historian to see where the data supports the legend and where the legend likely comes from listener consensus, tape circulation, performance quality, and later historical memory.
""".strip()

        return {
            "agent": "synthesis-agent",
            "show_date": show_date,
            "answer": answer,
            "significance_band": significance_band,
            "archetype_read": archetype_read,
            "reputation_read": reputation_read,
        }


agent = SynthesisAgent()


def execute(research_result: dict):
    return agent.assess_show(research_result)