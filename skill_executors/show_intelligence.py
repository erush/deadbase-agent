from pathlib import Path

import duckdb


DB_PATH = (
    Path(__file__)
    .parent.parent
    / "data"
    / "duckdb"
    / "deadbase.duckdb"
)


def execute(show_date: str):

    con = duckdb.connect(str(DB_PATH))

    row = con.execute(
        """
        select
            show_date,
            venue,
            era,
            show_length,
            unique_song_count,
            set_count,
            segue_ratio,
            venue_rank,
            venue_importance_score,
            venue_rarity_score,
            historian_score
        from show_embeddings
        where show_date = ?
        limit 1
        """,
        [show_date],
    ).fetchone()

    con.close()

    if row is None:
        return {
            "skill": "show-intelligence",
            "show_date": show_date,
            "found": False,
            "answer": f"No show intelligence profile found for {show_date}.",
        }

    return {
        "skill": "show-intelligence",
        "show_date": row[0],
        "venue": row[1],
        "era": row[2],
        "show_length": row[3],
        "unique_song_count": row[4],
        "set_count": row[5],
        "segue_ratio": row[6],
        "venue_rank": row[7],
        "venue_importance_score": row[8],
        "venue_rarity_score": row[9],
        "historian_score": row[10],
        "found": True,
        "answer": (
            f"{row[0]} profiles as a {row[2]} show with "
            f"{row[3]} songs, {row[4]} unique songs, "
            f"{row[5]} sets, a segue ratio of {row[6]}, "
            f"and a historian score of {row[10]}."
        ),
    }