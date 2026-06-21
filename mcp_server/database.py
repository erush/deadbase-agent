import duckdb


DB_PATH = "data/duckdb/deadbase.duckdb"


def get_connection():

    return duckdb.connect(DB_PATH)