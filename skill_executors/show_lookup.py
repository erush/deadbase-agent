from mcp_server.tools import find_show


def execute(show_date: str):

    result = find_show(show_date)

    show = result["show"]
    performances = result["performances"]

    if not show:
        return {
            "skill": "show-lookup",
            "show_date": show_date,
            "found": False,
            "answer": f"No show found for {show_date}."
        }

    metadata = show[0]

    venue = metadata[2]
    city = metadata[3]
    state = metadata[4]

    setlist = [song[0] for song in performances]

    answer = (
        f"The Grateful Dead performed on {show_date} at "
        f"{venue} in {city}, {state}. "
        f"The archive contains {len(performances)} songs for this performance."
    )

    return {
        "skill": "show-lookup",
        "show_date": show_date,
        "found": True,
        "venue": venue,
        "city": city,
        "state": state,
        "song_count": len(performances),
        "setlist": setlist,
        "answer": answer,
    }