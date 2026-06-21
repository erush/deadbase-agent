import duckdb

con = duckdb.connect(
    "data/duckdb/deadbase.duckdb"
)

print("\nSHOWS\n")
print(
    con.execute(
        "describe shows"
    ).fetchdf()
)

print("\nPERFORMANCES\n")
print(
    con.execute(
        "describe performances"
    ).fetchdf()
)

print("\nSONGS\n")
print(
    con.execute(
        "describe songs"
    ).fetchdf()
)

print("\nVENUES\n")
print(
    con.execute(
        "describe venues"
    ).fetchdf()
)

con.close()