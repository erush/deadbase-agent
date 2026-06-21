from skill_executors.show_recommender import execute as recommend_shows


class SimilarityAgent:

    def analyze(
        self,
        show_date: str,
        top_n: int = 5
    ):

        result = recommend_shows(
            show_date,
            top_n=top_n
        )

        return {
            "agent": "similarity-agent",
            "input_show": show_date,
            "found": result.get(
                "found",
                False
            ),
            "recommendations": result.get(
                "recommendations",
                []
            ),
            "answer": result.get(
                "answer",
                ""
            )
        }


agent = SimilarityAgent()


def execute(
    show_date: str,
    top_n: int = 5
):

    return agent.analyze(
        show_date,
        top_n=top_n
    )