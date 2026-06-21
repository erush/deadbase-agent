from pathlib import Path

import duckdb


DB_PATH = (
    Path(__file__)
    .parent.parent
    / "data"
    / "duckdb"
    / "deadbase.duckdb"
)


def execute(song_name: str):

    con = duckdb.connect(str(DB_PATH))

    row = con.execute(
        """
        select
            song_name,
            performance_count,
            first_year,
            peak_year,
            last_year,
            active_years,
            peak_year_count,
            peak_share,
            longevity_score,
            historical_tier,
            career_pattern
        from song_evolution
        where lower(song_name) = lower(?)
        """,
        [song_name]
    ).fetchone()

    con.close()

    if not row:

        return {
            "found": False,
            "answer": f"No song found for {song_name}."
        }

    return {
        "found": True,
        "song_name": row[0],
        "performance_count": row[1],
        "first_year": row[2],
        "peak_year": row[3],
        "last_year": row[4],
        "active_years": row[5],
        "peak_year_count": row[6],
        "peak_share": row[7],
        "longevity_score": row[8],
        "historical_tier": row[9],
        "career_pattern": row[10],
        "answer": (
            f"{row[0]} is classified as {row[9]}.\n\n"
            f"First Year: {row[2]}\n"
            f"Peak Year: {row[3]}\n"
            f"Last Year: {row[4]}\n"
            f"Performance Count: {row[1]}\n"
            f"Active Years: {row[5]}\n"
            f"Peak Share: {row[7]}\n"
            f"Career Pattern: {row[10]}"
        )
    }