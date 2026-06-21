from skill_executors.venue_profile import execute as venue_profile


class VenueAgent:

    def analyze(
        self,
        venue_name: str
    ):

        result = venue_profile(
            venue_name
        )

        return {
            "agent": "venue-agent",
            **result
        }


agent = VenueAgent()


def execute(
    venue_name: str
):

    return agent.analyze(
        venue_name
    )