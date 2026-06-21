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


def main():

    con = duckdb.connect(str(DB_PATH))

    performances = con.execute(
        """
        select
            p.song_uuid,
            p.song_name,
            s.show_date
        from performances p
        join shows s
            on p.show_uuid = s.show_uuid
        """
    ).df()

    performances["year"] = (
        performances["show_date"]
        .str.slice(0, 4)
        .astype(int)
    )

    profiles = []

    for song_name, group in performances.groupby("song_name"):

        group = group.sort_values("show_date")

        song_uuid = (
            group["song_uuid"]
            .mode()
            .iloc[0]
        )

        yearly = (
            group.groupby("year")
            .size()
            .reset_index(name="count")
        )

        peak_row = yearly.sort_values(
            ["count", "year"],
            ascending=[False, True]
        ).iloc[0]

        first_date = group["show_date"].min()
        last_date = group["show_date"].max()

        first_year = int(str(first_date)[:4])
        last_year = int(str(last_date)[:4])

        profiles.append(
            {
                "song_uuid": song_uuid,
                "song_name": song_name,
                "performance_count": len(group),
                "first_performance": first_date,
                "last_performance": last_date,
                "first_year": first_year,
                "last_year": last_year,
                "active_years": (
                    last_year - first_year + 1
                ),
                "peak_year": int(
                    peak_row["year"]
                ),
                "peak_year_count": int(
                    peak_row["count"]
                ),
            }
        )

    profile_df = pd.DataFrame(profiles)

    profile_df = profile_df.sort_values(
        [
            "performance_count",
            "song_name"
        ],
        ascending=[
            False,
            True
        ]
    )

    con.register(
        "profile_df",
        profile_df
    )

    con.execute(
        """
        create or replace table song_profile as
        select *
        from profile_df
        """
    )

    count = con.execute(
        """
        select count(*)
        from song_profile
        """
    ).fetchone()[0]

    print()
    print(f"song_profiles={count}")
    print()

    print(
        con.execute(
            """
            select
                song_name,
                performance_count,
                first_performance,
                last_performance,
                peak_year,
                peak_year_count
            from song_profile
            order by performance_count desc
            limit 20
            """
        ).df()
    )

    con.close()


if __name__ == "__main__":
    main()