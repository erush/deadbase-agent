from mcp_server.tools import find_song_before_date


def execute(song_name: str, before_date: str):

    performances = find_song_before_date(
        song_name,
        before_date
    )

    if not performances:
        return {
            "skill": "song-evolution",
            "found": False
        }

    last = performances[-1]

    return {
        "skill": "song-evolution",
        "song": song_name,
        "before_date": before_date,
        "last_performance_before_date": {
            "date": last[1],
            "venue": last[2],
            "city": last[3],
            "state": last[4]
        },
        "answer": (
            f"The last recorded performance of "
            f"{song_name} before {before_date} "
            f"occurred on {last[1]} at "
            f"{last[2]} in {last[3]}, {last[4]}."
        )
    }