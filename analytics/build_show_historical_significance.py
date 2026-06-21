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


def normalize(series):

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series([0.0] * len(series))

    return (
        series - minimum
    ) / (
        maximum - minimum
    )


def main():

    con = duckdb.connect(str(DB_PATH))

    show_df = con.execute(
        """
        select
            show_uuid,
            show_date,
            show_length,
            set_count,
            segue_ratio
        from show_dna
        """
    ).df()

    venue_df = con.execute(
        """
        select
            venue,
            importance_score,
            rarity_score
        from venue_rankings
        """
    ).df()

    venue_lookup = con.execute(
        """
        select
            show_uuid,
            venue
        from shows
        """
    ).df()

    song_profile = con.execute(
        """
        select
            song_name,
            performance_count
        from song_profile
        """
    ).df()

    performances = con.execute(
        """
        select
            p.show_uuid,
            p.song_name
        from performances p
        """
    ).df()

    max_song_count = (
        song_profile["performance_count"]
        .max()
    )

    song_profile["rarity"] = (
        1
        - (
            song_profile["performance_count"]
            / max_song_count
        )
    )

    rarity_lookup = dict(
        zip(
            song_profile["song_name"],
            song_profile["rarity"]
        )
    )

    song_rarity_rows = []

    for show_uuid, group in performances.groupby(
        "show_uuid"
    ):

        rarities = [
            rarity_lookup.get(song, 0)
            for song in group["song_name"]
        ]

        avg_rarity = (
            sum(rarities)
            / len(rarities)
            if rarities
            else 0
        )

        song_rarity_rows.append(
            {
                "show_uuid": show_uuid,
                "song_rarity_score": avg_rarity
            }
        )

    song_rarity_df = pd.DataFrame(
        song_rarity_rows
    )

    df = (
        show_df
        .merge(
            venue_lookup,
            on="show_uuid",
            how="left"
        )
        .merge(
            venue_df,
            on="venue",
            how="left"
        )
        .merge(
            song_rarity_df,
            on="show_uuid",
            how="left"
        )
    )

    df["show_length_score"] = normalize(
        df["show_length"]
    )

    df["set_complexity_score"] = normalize(
        df["set_count"]
    )

    df["segue_score"] = normalize(
        df["segue_ratio"]
    )

    df["venue_importance_score"] = normalize(
        df["importance_score"]
    )

    df["venue_rarity_score"] = normalize(
        df["rarity_score"]
    )

    df["song_rarity_score"] = normalize(
        df["song_rarity_score"]
    )

    df["historian_score"] = (
        df["show_length_score"] * 0.10
        + df["set_complexity_score"] * 0.15
        + df["segue_score"] * 0.20
        + df["venue_importance_score"] * 0.20
        + df["venue_rarity_score"] * 0.15
        + df["song_rarity_score"] * 0.20
    )

    df = df.sort_values(
        "historian_score",
        ascending=False
    )

    df["historian_rank"] = (
        range(
            1,
            len(df) + 1
        )
    )

    df["historian_percentile"] = (
        (
            len(df)
            - df["historian_rank"]
            + 1
        )
        / len(df)
    ) * 100

    output = df[
        [
            "show_uuid",
            "show_date",
            "show_length_score",
            "set_complexity_score",
            "segue_score",
            "venue_importance_score",
            "venue_rarity_score",
            "song_rarity_score",
            "historian_score",
            "historian_rank",
            "historian_percentile"
        ]
    ]

    con.execute(
        """
        create or replace table
        show_historical_significance
        as
        select *
        from output
        """
    )

    count = con.execute(
        """
        select count(*)
        from show_historical_significance
        """
    ).fetchone()[0]

    print()
    print(
        f"show_historical_significance={count}"
    )
    print()

    print(
        con.execute(
            """
            select
                show_date,
                historian_score,
                historian_rank,
                round(
                    historian_percentile,
                    2
                ) as percentile
            from show_historical_significance
            order by historian_score desc
            limit 20
            """
        ).df()
    )

    con.close()


if __name__ == "__main__":
    main()