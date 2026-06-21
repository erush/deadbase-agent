from pathlib import Path

import duckdb
import pandas as pd


DB_PATH = (
    Path(__file__)
    .parent.parent
    / "data"
    / "duckdb"
    / "deadbase.duckdb"
)


def percentile(series, pct):

    return series.quantile(pct)


def assign_primary(row, thresholds):

    if row["segue_score"] >= thresholds["segue"]:
        return "High Segue Show"

    if row["show_length_score"] >= thresholds["length"]:
        return "Marathon Show"

    if row["song_rarity_score"] >= thresholds["rarity"]:
        return "Rare Song Show"

    if row["venue_importance_score"] >= thresholds["venue"]:
        return "Venue Landmark Show"

    if row["set_complexity_score"] >= thresholds["sets"]:
        return "Complex Set Structure"

    if row["historian_score"] >= thresholds["historian"]:
        return "Canonical Repertoire Show"

    return "Standard Performance"


def assign_secondary(row, primary, thresholds):

    candidates = []

    if (
        row["venue_importance_score"]
        >= thresholds["venue"]
        and primary != "Venue Landmark Show"
    ):
        candidates.append("Venue Landmark Show")

    if (
        row["song_rarity_score"]
        >= thresholds["rarity"]
        and primary != "Rare Song Show"
    ):
        candidates.append("Rare Song Show")

    if (
        row["show_length_score"]
        >= thresholds["length"]
        and primary != "Marathon Show"
    ):
        candidates.append("Marathon Show")

    if (
        row["segue_score"]
        >= thresholds["segue"]
        and primary != "High Segue Show"
    ):
        candidates.append("High Segue Show")

    if (
        row["historian_score"]
        >= thresholds["historian"]
        and primary != "Canonical Repertoire Show"
    ):
        candidates.append("Canonical Repertoire Show")

    if candidates:
        return candidates[0]

    return None


def main():

    con = duckdb.connect(str(DB_PATH))

    df = con.execute(
        """
        select *
        from show_historical_significance
        """
    ).df()

    thresholds = {
        "segue": percentile(
            df["segue_score"],
            0.90
        ),
        "length": percentile(
            df["show_length_score"],
            0.90
        ),
        "rarity": percentile(
            df["song_rarity_score"],
            0.90
        ),
        "venue": percentile(
            df["venue_importance_score"],
            0.90
        ),
        "sets": percentile(
            df["set_complexity_score"],
            0.90
        ),
        "historian": percentile(
            df["historian_score"],
            0.90
        ),
    }

    archetypes = []

    for _, row in df.iterrows():

        primary = assign_primary(
            row,
            thresholds
        )

        secondary = assign_secondary(
            row,
            primary,
            thresholds
        )

        archetypes.append(
            {
                "show_uuid": row["show_uuid"],
                "show_date": row["show_date"],
                "primary_archetype": primary,
                "secondary_archetype": secondary,
                "historian_score": row[
                    "historian_score"
                ],
            }
        )

    archetypes_df = pd.DataFrame(
        archetypes
    )

    con.execute(
        """
        create or replace table
        show_archetypes as
        select *
        from archetypes_df
        """
    )

    count = con.execute(
        """
        select count(*)
        from show_archetypes
        """
    ).fetchone()[0]

    print()
    print(
        f"show_archetypes={count}"
    )
    print()

    print(
        con.execute(
            """
            select
                primary_archetype,
                count(*) as shows
            from show_archetypes
            group by 1
            order by 2 desc
            """
        ).df()
    )

    print()

    print(
        con.execute(
            """
            select
                show_date,
                primary_archetype,
                secondary_archetype,
                round(
                    historian_score,
                    4
                ) as historian_score
            from show_archetypes
            order by historian_score desc
            limit 20
            """
        ).df()
    )

    con.close()


if __name__ == "__main__":
    main()