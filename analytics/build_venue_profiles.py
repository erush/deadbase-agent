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

    df = con.execute(
        """
        select
            s.venue,
            s.city,
            s.state,
            s.show_date,
            d.show_length,
            d.set_count,
            d.segue_ratio
        from show_dna d
        join shows s
            on d.show_uuid = s.show_uuid
        """
    ).df()

    rows = []

    for venue, group in df.groupby("venue"):

        first = group.iloc[0]

        first_show = group["show_date"].min()
        last_show = group["show_date"].max()

        first_year = int(first_show[:4])
        last_year = int(last_show[:4])

        rows.append(
            {
                "venue": venue,
                "city": first["city"],
                "state": first["state"],
                "show_count": len(group),
                "first_show": first_show,
                "last_show": last_show,
                "active_years":
                    last_year - first_year + 1,
                "avg_show_length":
                    round(
                        group["show_length"].mean(),
                        2
                    ),
                "avg_set_count":
                    round(
                        group["set_count"].mean(),
                        2
                    ),
                "avg_segue_ratio":
                    round(
                        group["segue_ratio"].mean(),
                        3
                    )
            }
        )

    venue_profile = pd.DataFrame(rows)

    con.register(
        "venue_profile_df",
        venue_profile
    )

    con.execute(
        """
        create or replace table venue_profile as
        select *
        from venue_profile_df
        """
    )

    print()
    print(
        f"venue_profiles={len(venue_profile)}"
    )
    print()

    print(
        con.execute(
            """
            select
                venue,
                city,
                state,
                show_count,
                avg_show_length,
                avg_segue_ratio
            from venue_profile
            order by show_count desc
            limit 20
            """
        ).df()
    )

    con.close()


if __name__ == "__main__":
    main()