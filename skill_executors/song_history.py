from mcp_server.tools import find_song


def execute(song_name: str):

    performances = find_song(song_name)

    if not performances:
        return {
            "skill": "song-history",
            "song": song_name,
            "found": False,
            "answer": f"No performance history found for {song_name}."
        }

    first = performances[0]
    last = performances[-1]

    answer = (
        f"{song_name} appears {len(performances)} times in the archive. "
        f"The first recorded performance occurred on {first[1]} at "
        f"{first[2]} in {first[3]}, {first[4]}. "
        f"The most recent recorded performance occurred on {last[1]} at "
        f"{last[2]} in {last[3]}, {last[4]}."
    )

    return {
        "skill": "song-history",
        "song": song_name,
        "found": True,
        "performance_count": len(performances),
        "first_performance": {
            "date": first[1],
            "venue": first[2],
            "city": first[3],
            "state": first[4],
        },
        "last_performance": {
            "date": last[1],
            "venue": last[2],
            "city": last[3],
            "state": last[4],
        },
        "answer": answer,
    }