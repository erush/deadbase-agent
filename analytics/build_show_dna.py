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


def determine_era(year):

    if year <= 1969:
        return "60s"

    if year <= 1974:
        return "early_70s"

    if year <= 1979:
        return "late_70s"

    if year <= 1984:
        return "early_80s"

    if year <= 1989:
        return "late_80s"

    return "90s"


def main():

    con = duckdb.connect(str(DB_PATH))

    df = con.execute(
        """
        select
            p.show_uuid,
            s.show_date,
            p.song_name,
            p.set_number,
            p.segued
        from performances p
        join shows s
            on p.show_uuid = s.show_uuid
        """
    ).df()

    df["year"] = (
        df["show_date"]
        .str.slice(0, 4)
        .astype(int)
    )

    rows = []

    for show_uuid, group in df.groupby(
        "show_uuid"
    ):

        first = group.iloc[0]

        year = int(first["year"])

        rows.append(
            {
                "show_uuid": show_uuid,
                "show_date": first["show_date"],
                "year": year,
                "era": determine_era(year),

                "show_length":
                    len(group),

                "song_count":
                    len(group),

                "unique_song_count":
                    group["song_name"].nunique(),

                "set_count":
                    group["set_number"].nunique(),

                "first_set_count":
                    len(
                        group[
                            group["set_number"] == 1
                        ]
                    ),

                "second_set_count":
                    len(
                        group[
                            group["set_number"] == 2
                        ]
                    ),

                "third_set_plus_count":
                    len(
                        group[
                            group["set_number"] >= 3
                        ]
                    ),

                "segued_count":
                    int(
                        group["segued"]
                        .fillna(False)
                        .sum()
                    ),

                "segue_ratio":
                    round(
                        float(
                            group["segued"]
                            .fillna(False)
                            .sum()
                        )
                        / len(group),
                        3
                    )
            }
        )

    show_dna = pd.DataFrame(rows)

    show_dna = show_dna.sort_values(
        [
            "show_length",
            "show_date"
        ],
        ascending=[
            False,
            True
        ]
    )

    con.register(
        "show_dna_df",
        show_dna
    )

    con.execute(
        """
        create or replace table show_dna as
        select *
        from show_dna_df
        """
    )

    print()
    print(
        f"show_dna_rows={len(show_dna)}"
    )
    print()

    print(
        con.execute(
            """
            select
                show_date,
                era,
                show_length,
                unique_song_count,
                set_count,
                third_set_plus_count,
                segued_count,
                segue_ratio
            from show_dna
            order by show_length desc
            limit 20
            """
        ).df()
    )

    print()

    print(
        con.execute(
            """
            select
                era,
                count(*) as shows,
                round(avg(show_length), 2) as avg_show_length,
                round(avg(set_count), 2) as avg_sets,
                round(avg(segue_ratio), 3) as avg_segue_ratio
            from show_dna
            group by era
            order by era
            """
        ).df()
    )

    con.close()


if __name__ == "__main__":
    main()