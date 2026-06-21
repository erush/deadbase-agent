from mcp_server.tools import find_venue


def execute(venue_name: str):

    shows = find_venue(venue_name)

    if not shows:
        return {
            "skill": "venue-analysis",
            "venue": venue_name,
            "found": False,
            "answer": f"No venue information found for {venue_name}."
        }

    first_show = shows[0]
    last_show = shows[-1]

    answer = (
        f"{venue_name} hosted {len(shows)} Grateful Dead performances "
        f"between {first_show[1]} and {last_show[1]}. "
        f"The venue is located in {first_show[3]}, {first_show[4]}."
    )

    return {
        "skill": "venue-analysis",
        "venue": venue_name,
        "found": True,
        "show_count": len(shows),
        "first_show": first_show[1],
        "last_show": last_show[1],
        "city": first_show[3],
        "state": first_show[4],
        "answer": answer,
    }