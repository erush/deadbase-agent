from skill_executors.song_history import execute as song_history


class SongAgent:

    def analyze(
        self,
        song_name: str
    ):

        result = song_history(song_name)

        return {
            "agent": "song-agent",
            **result
        }


agent = SongAgent()


def execute(
    song_name: str
):

    return agent.analyze(
        song_name
    )