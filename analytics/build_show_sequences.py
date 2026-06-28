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


def determine_era(year: int) -> str:
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


def determine_season(month: int) -> str:
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Spring"
    if month in (6, 7, 8):
        return "Summer"
    return "Fall"


def main():
    con = duckdb.connect(str(DB_PATH))

    shows = con.execute(
        """
        select
            show_uuid,
            show_date,
            venue,
            city,
            state,
            country
        from shows
        """
    ).df()

    performance_shows = con.execute(
        """
        select distinct show_uuid
        from performances
        """
    ).df()

    performance_show_ids = set(performance_shows["show_uuid"].tolist())

    shows["parsed_date"] = pd.to_datetime(
        shows["show_date"],
        format="%Y/%m/%d",
        errors="coerce"
    )

    shows["year"] = shows["parsed_date"].dt.year
    shows["month"] = shows["parsed_date"].dt.month
    shows["day"] = shows["parsed_date"].dt.day
    shows["weekday"] = shows["parsed_date"].dt.day_name()

    shows["era"] = shows["year"].apply(lambda x: determine_era(int(x)) if pd.notna(x) else None)
    shows["season"] = shows["month"].apply(lambda x: determine_season(int(x)) if pd.notna(x) else None)

    shows["has_performance_data"] = shows["show_uuid"].isin(performance_show_ids)

    show_profile = shows[
        [
            "show_uuid",
            "show_date",
            "year",
            "month",
            "day",
            "weekday",
            "era",
            "season",
            "venue",
            "city",
            "state",
            "country",
            "has_performance_data",
        ]
    ].sort_values("show_date")

    con.register("show_profile_df", show_profile)

    con.execute(
        """
        create or replace table show_profile as
        select *
        from show_profile_df
        """
    )

    total_rows = con.execute("select count(*) from show_profile").fetchone()[0]
    with_perf = con.execute(
        """
        select count(*)
        from show_profile
        where has_performance_data = true
        """
    ).fetchone()[0]
    without_perf = con.execute(
        """
        select count(*)
        from show_profile
        where has_performance_data = false
        """
    ).fetchone()[0]

    print()
    print(f"show_profile_rows={total_rows}")
    print(f"shows_with_performance_data={with_perf}")
    print(f"shows_without_performance_data={without_perf}")
    print()

    print(
        con.execute(
            """
            select
                era,
                count(*) as shows,
                sum(case when has_performance_data then 1 else 0 end) as shows_with_performances,
                sum(case when not has_performance_data then 1 else 0 end) as shows_without_performances
            from show_profile
            group by era
            order by era
            """
        ).df()
    )

    con.close()


if __name__ == "__main__":
    main()