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

    profile = con.execute(
        """
        select
            show_uuid,
            show_date,
            year,
            era,
            venue,
            city,
            state,
            country,
            has_performance_data
        from show_profile
        order by show_date
        """
    ).df()

    performances = con.execute(
        """
        select
            show_uuid,
            song_name,
            set_number,
            segued
        from performances
        """
    ).df()

    rows = []

    for _, show in profile.iterrows():
        show_uuid = show["show_uuid"]

        group = performances[
            performances["show_uuid"] == show_uuid
        ]

        has_perf = len(group) > 0

        if has_perf:
            segued_count = int(
                group["segued"]
                .fillna(False)
                .sum()
            )

            song_count = int(len(group))

            segue_ratio = round(
                float(segued_count) / song_count,
                3
            ) if song_count > 0 else None

            row = {
                "show_uuid": show_uuid,
                "show_date": show["show_date"],
                "year": int(show["year"]) if pd.notna(show["year"]) else None,
                "era": show["era"],
                "venue": show["venue"],
                "city": show["city"],
                "state": show["state"],
                "country": show["country"],

                "has_performance_data": True,
                "dna_complete": True,
                "processing_status": "COMPLETE",

                "show_length": song_count,
                "song_count": song_count,
                "unique_song_count": int(group["song_name"].nunique()),
                "set_count": int(group["set_number"].nunique()),

                "first_set_count": int(len(group[group["set_number"] == 1])),
                "second_set_count": int(len(group[group["set_number"] == 2])),
                "third_set_plus_count": int(len(group[group["set_number"] >= 3])),

                "segued_count": segued_count,
                "segue_ratio": segue_ratio,
            }

        else:
            row = {
                "show_uuid": show_uuid,
                "show_date": show["show_date"],
                "year": int(show["year"]) if pd.notna(show["year"]) else None,
                "era": show["era"],
                "venue": show["venue"],
                "city": show["city"],
                "state": show["state"],
                "country": show["country"],

                "has_performance_data": False,
                "dna_complete": False,
                "processing_status": "INSUFFICIENT_DATA",

                "show_length": 0,
                "song_count": 0,
                "unique_song_count": 0,
                "set_count": 0,

                "first_set_count": 0,
                "second_set_count": 0,
                "third_set_plus_count": 0,

                "segued_count": 0,
                "segue_ratio": None,
            }

        rows.append(row)

    show_dna = pd.DataFrame(rows)

    show_dna = show_dna.sort_values(
        [
            "has_performance_data",
            "show_length",
            "show_date",
        ],
        ascending=[
            False,
            False,
            True,
        ],
    )

    con.register("show_dna_df", show_dna)

    con.execute(
        """
        create or replace table show_dna as
        select *
        from show_dna_df
        """
    )

    total_rows = con.execute("select count(*) from show_dna").fetchone()[0]
    complete_rows = con.execute(
        """
        select count(*)
        from show_dna
        where dna_complete = true
        """
    ).fetchone()[0]
    metadata_only_rows = con.execute(
        """
        select count(*)
        from show_dna
        where dna_complete = false
        """
    ).fetchone()[0]

    print()
    print(f"show_dna_rows={total_rows}")
    print(f"dna_complete_rows={complete_rows}")
    print(f"metadata_only_rows={metadata_only_rows}")
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
                segue_ratio,
                dna_complete
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
                sum(case when dna_complete then 1 else 0 end) as complete_dna,
                sum(case when not dna_complete then 1 else 0 end) as metadata_only,
                round(avg(nullif(show_length, 0)), 2) as avg_show_length,
                round(avg(nullif(set_count, 0)), 2) as avg_sets,
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