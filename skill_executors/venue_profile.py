from pathlib import Path

import duckdb


DB_PATH = (
    Path(__file__)
    .parent.parent
    / "data"
    / "duckdb"
    / "deadbase.duckdb"
)


def execute(
    venue_name: str
):

    con = duckdb.connect(
        str(DB_PATH)
    )

    row = con.execute(
        """
        select
            venue,
            city,
            state,
            show_count,
            first_show,
            last_show,
            active_years,
            avg_show_length,
            avg_set_count,
            avg_segue_ratio
        from venue_profile
        where lower(venue)
        like lower(?)
        limit 1
        """,
        [f"%{venue_name}%"]
    ).fetchone()

    con.close()

    if row is None:

        return {
            "found": False,
            "venue": venue_name,
            "answer":
                f"No venue found matching "
                f"{venue_name}."
        }

    return {
        "found": True,
        "venue": row[0],
        "city": row[1],
        "state": row[2],
        "show_count": row[3],
        "first_show": row[4],
        "last_show": row[5],
        "active_years": row[6],
        "avg_show_length": row[7],
        "avg_set_count": row[8],
        "avg_segue_ratio": row[9],
        "answer":
            f"{row[0]} hosted "
            f"{row[3]} Grateful Dead shows."
    }