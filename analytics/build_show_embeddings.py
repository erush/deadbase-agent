from pathlib import Path
import duckdb
import pandas as pd


DB_PATH = Path(__file__).parent.parent / "data" / "duckdb" / "deadbase.duckdb"


def main():
    con = duckdb.connect(str(DB_PATH))

    df = con.execute(
        """
        select
            d.show_uuid,
            d.show_date,
            d.year,
            d.era,
            d.show_length,
            d.unique_song_count,
            d.set_count,
            d.segued_count,
            d.segue_ratio,
            s.venue,
            coalesce(v.venue_rank, 9999) as venue_rank,
            coalesce(v.importance_score, 0) as venue_importance_score,
            coalesce(v.rarity_score, 0) as venue_rarity_score
        from show_dna d
        join shows s
            on d.show_uuid = s.show_uuid
        left join venue_rankings v
            on s.venue = v.venue
        """
    ).df()

    era_map = {
        "60s": 0.1,
        "early_70s": 0.3,
        "late_70s": 0.5,
        "early_80s": 0.7,
        "late_80s": 0.85,
        "90s": 1.0,
    }

    df["era_score"] = df["era"].map(era_map).fillna(0)

    df["length_score"] = (
        df["show_length"] / df["show_length"].max()
    ).round(4)

    df["unique_song_score"] = (
        df["unique_song_count"] / df["unique_song_count"].max()
    ).round(4)

    df["set_count_score"] = (
        df["set_count"] / df["set_count"].max()
    ).round(4)

    df["segue_score"] = df["segue_ratio"].round(4)

    df["historian_score"] = (
        df["length_score"] * 0.25
        + df["unique_song_score"] * 0.20
        + df["set_count_score"] * 0.15
        + df["segue_score"] * 0.20
        + df["venue_importance_score"] * 0.10
        + df["venue_rarity_score"] * 0.10
    ).round(4)

    con.register("show_embeddings_df", df)

    con.execute(
        """
        create or replace table show_embeddings as
        select *
        from show_embeddings_df
        """
    )

    print()
    print(f"show_embeddings={len(df)}")
    print()

    print(
        con.execute(
            """
            select
                show_date,
                venue,
                era,
                show_length,
                set_count,
                segue_ratio,
                historian_score
            from show_embeddings
            order by historian_score desc
            limit 20
            """
        ).df()
    )

    con.close()


if __name__ == "__main__":
    main()