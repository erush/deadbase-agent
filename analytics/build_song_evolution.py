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


def classify_tier(performance_count):

    if performance_count >= 500:
        return "Cornerstone"

    if performance_count >= 250:
        return "Core Repertoire"

    if performance_count >= 100:
        return "Important Rotation"

    if performance_count >= 25:
        return "Occasional"

    return "Rare"


def classify_career_pattern(first_year, peak_year, last_year):

    if last_year <= 1974:
        return "Early Era Song"

    if first_year >= 1980:
        return "Late Era Song"

    if peak_year <= 1974 and last_year >= 1989:
        return "Revived Legacy Song"

    if peak_year <= 1974:
        return "Early Peak Song"

    if peak_year >= 1980:
        return "Late Peak Song"

    return "Long-Term Repertoire Song"


def main():

    con = duckdb.connect(str(DB_PATH))

    df = con.execute(
        """
        select
            sp.song_uuid,
            sp.song_name,
            sp.performance_count,
            sp.first_year,
            sp.last_year,
            sp.active_years,
            sp.peak_year,
            sp.peak_year_count
        from song_profile sp
        """
    ).df()

    df["peak_share"] = (
        df["peak_year_count"]
        / df["performance_count"]
    ).round(4)

    df["longevity_score"] = (
        df["active_years"]
        / df["active_years"].max()
    ).round(4)

    df["historical_tier"] = df[
        "performance_count"
    ].apply(classify_tier)

    df["career_pattern"] = df.apply(
        lambda row: classify_career_pattern(
            row["first_year"],
            row["peak_year"],
            row["last_year"],
        ),
        axis=1,
    )

    df = df[
        [
            "song_uuid",
            "song_name",
            "performance_count",
            "first_year",
            "peak_year",
            "last_year",
            "active_years",
            "peak_year_count",
            "peak_share",
            "longevity_score",
            "historical_tier",
            "career_pattern",
        ]
    ]

    con.register(
        "song_evolution_df",
        df
    )

    con.execute(
        """
        create or replace table song_evolution as
        select *
        from song_evolution_df
        """
    )

    print()
    print(
        f"song_evolution={len(df)}"
    )
    print()

    print(
        con.execute(
            """
            select
                song_name,
                performance_count,
                first_year,
                peak_year,
                last_year,
                historical_tier,
                career_pattern
            from song_evolution
            order by performance_count desc
            limit 20
            """
        ).df()
    )

    con.close()


if __name__ == "__main__":
    main()