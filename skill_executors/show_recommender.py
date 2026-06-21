from mcp_server.tools import find_show
from mcp_server.tools import get_connection


def execute(show_date: str, top_n: int = 10):

    source_result = find_show(show_date)

    if not source_result["show"]:
        return {
            "skill": "show-recommender",
            "show_date": show_date,
            "found": False,
            "answer": f"No show found for {show_date}."
        }

    source_songs = {
        row[0]
        for row in source_result["performances"]
    }

    con = get_connection()

    shows = con.execute(
        """
        select
            show_uuid,
            show_date,
            venue,
            city,
            state
        from shows
        where show_date <> ?
        order by show_date
        """,
        [show_date]
    ).fetchall()

    recommendations = []

    for show_uuid, other_date, venue, city, state in shows:

        songs = con.execute(
            """
            select distinct song_name
            from performances
            where show_uuid = ?
            """,
            [show_uuid]
        ).fetchall()

        other_songs = {
            row[0]
            for row in songs
        }

        union = source_songs | other_songs

        if not union:
            continue

        similarity = round(
            len(source_songs & other_songs)
            / len(union),
            3
        )

        recommendations.append({
            "show_date": other_date,
            "venue": venue,
            "city": city,
            "state": state,
            "similarity": similarity,
            "shared_song_count": len(
                source_songs & other_songs
            )
        })

    con.close()

    recommendations.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    recommendations = recommendations[:top_n]

    answer = (
        f"Found {len(recommendations)} shows similar to "
        f"{show_date}. "
        f"The most similar show is "
        f"{recommendations[0]['show_date']} "
        f"with a similarity score of "
        f"{recommendations[0]['similarity']}."
        if recommendations
        else f"No similar shows found for {show_date}."
    )

    return {
        "skill": "show-recommender",
        "show_date": show_date,
        "found": True,
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
        "answer": answer
    }