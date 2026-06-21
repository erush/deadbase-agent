import duckdb

con = duckdb.connect("data/duckdb/deadbase.duckdb")

tables = [
    "shows",
    "songs",
    "performances",
    "venues"
]

for table in tables:
    count = con.execute(
        f"select count(*) from {table}"
    ).fetchone()[0]

    print(f"{table}: {count:,}")

print()

print(
    con.execute(
        """
        select *
        from songs
        order by song_name
        limit 10
        """
    ).fetchdf()
)

print()

print(
    con.execute(
        """
        select *
        from shows
        limit 5
        """
    ).fetchdf()
)

con.close()