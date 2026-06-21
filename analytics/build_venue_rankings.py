from pathlib import Path
import duckdb
import pandas as pd


DB_PATH = Path(__file__).parent.parent / "data" / "duckdb" / "deadbase.duckdb"


def main():
    con = duckdb.connect(str(DB_PATH))

    df = con.execute(
        """
        select *
        from venue_profile
        """
    ).df()

    df = df.sort_values(
        ["show_count", "avg_show_length", "avg_segue_ratio"],
        ascending=[False, False, False],
    ).reset_index(drop=True)

    df["venue_rank"] = df.index + 1

    max_show_count = df["show_count"].max()

    df["rarity_score"] = (
        1 - (df["show_count"] / max_show_count)
    ).round(3)

    df["importance_score"] = (
        (df["show_count"] / max_show_count * 0.6)
        + (df["avg_show_length"] / df["avg_show_length"].max() * 0.25)
        + (df["avg_segue_ratio"] / df["avg_segue_ratio"].max() * 0.15)
    ).round(3)

    con.register("venue_rankings_df", df)

    con.execute(
        """
        create or replace table venue_rankings as
        select *
        from venue_rankings_df
        """
    )

    print()
    print(f"venue_rankings={len(df)}")
    print()

    print(
        con.execute(
            """
            select
                venue,
                city,
                state,
                show_count,
                venue_rank,
                rarity_score,
                importance_score
            from venue_rankings
            order by venue_rank
            limit 20
            """
        ).df()
    )

    con.close()


if __name__ == "__main__":
    main()