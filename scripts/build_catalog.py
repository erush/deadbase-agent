from pathlib import Path
import yaml
import duckdb


DATA_DIR = Path("data/yaml")
DB_PATH = Path("data/duckdb/deadbase.duckdb")


def clean_key(value):
    if value is None:
        return None

    return str(value).lstrip(":").strip()


def normalize_show_record(show_date, show_data):
    return {
        "show_uuid": show_data.get(":uuid") or show_data.get("uuid"),
        "show_date": str(show_date),
        "venue": show_data.get(":venue") or show_data.get("venue"),
        "city": show_data.get(":city") or show_data.get("city"),
        "state": show_data.get(":state") or show_data.get("state"),
        "country": show_data.get(":country") or show_data.get("country"),
        "sets": show_data.get(":sets") or show_data.get("sets") or [],
    }


def load_yaml_files():
    records = []

    for path in DATA_DIR.rglob("*.yaml"):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if data:
            records.append((path, data))

    for path in DATA_DIR.rglob("*.yml"):
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if data:
            records.append((path, data))

    return records


def extract_show_archive(records):
    shows = []
    performances = []
    venues = set()

    for path, data in records:
        if not isinstance(data, dict):
            continue

        for show_date, show_data in data.items():
            if not isinstance(show_data, dict):
                continue

            show = normalize_show_record(show_date, show_data)

            if not show["show_uuid"]:
                continue

            shows.append(
                {
                    "show_uuid": show["show_uuid"],
                    "show_date": show["show_date"],
                    "venue": show["venue"],
                    "city": show["city"],
                    "state": show["state"],
                    "country": show["country"],
                }
            )

            venues.add(
                (
                    show["venue"],
                    show["city"],
                    show["state"],
                    show["country"],
                )
            )

            for set_index, set_data in enumerate(show["sets"], start=1):
                songs = set_data.get(":songs") or set_data.get("songs") or []

                for song_index, song in enumerate(songs, start=1):
                    song_uuid = song.get(":uuid") or song.get("uuid")
                    song_name = song.get(":name") or song.get("name")
                    segued = song.get(":segued") if ":segued" in song else song.get("segued")

                    if not song_name:
                        continue

                    performances.append(
                        {
                            "show_uuid": show["show_uuid"],
                            "song_uuid": song_uuid,
                            "song_name": song_name,
                            "set_number": set_index,
                            "song_position": song_index,
                            "segued": bool(segued),
                        }
                    )

    venue_rows = [
        {
            "venue": venue,
            "city": city,
            "state": state,
            "country": country,
        }
        for venue, city, state, country in sorted(venues)
        if venue
    ]

    return shows, performances, venue_rows


def extract_song_catalog(records):
    songs = {}

    for path, data in records:
        if not isinstance(data, list):
            continue

        for item in data:
            if not isinstance(item, dict):
                continue

            for song_name, song_uuid in item.items():
                if song_name and song_uuid:
                    songs[str(song_uuid)] = str(song_name)

    return [
        {
            "song_uuid": song_uuid,
            "song_name": song_name,
        }
        for song_uuid, song_name in sorted(songs.items(), key=lambda row: row[1])
    ]


def write_duckdb(shows, songs, performances, venues):
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(str(DB_PATH))

    con.execute("DROP TABLE IF EXISTS shows")
    con.execute("DROP TABLE IF EXISTS songs")
    con.execute("DROP TABLE IF EXISTS performances")
    con.execute("DROP TABLE IF EXISTS venues")

    con.execute(
        """
        CREATE TABLE shows (
            show_uuid VARCHAR,
            show_date VARCHAR,
            venue VARCHAR,
            city VARCHAR,
            state VARCHAR,
            country VARCHAR
        )
        """
    )

    con.execute(
        """
        CREATE TABLE songs (
            song_uuid VARCHAR,
            song_name VARCHAR
        )
        """
    )

    con.execute(
        """
        CREATE TABLE performances (
            show_uuid VARCHAR,
            song_uuid VARCHAR,
            song_name VARCHAR,
            set_number INTEGER,
            song_position INTEGER,
            segued BOOLEAN
        )
        """
    )

    con.execute(
        """
        CREATE TABLE venues (
            venue VARCHAR,
            city VARCHAR,
            state VARCHAR,
            country VARCHAR
        )
        """
    )

    if shows:
        con.executemany(
            """
            INSERT INTO shows
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    row["show_uuid"],
                    row["show_date"],
                    row["venue"],
                    row["city"],
                    row["state"],
                    row["country"],
                )
                for row in shows
            ],
        )

    if songs:
        con.executemany(
            """
            INSERT INTO songs
            VALUES (?, ?)
            """,
            [
                (
                    row["song_uuid"],
                    row["song_name"],
                )
                for row in songs
            ],
        )

    if performances:
        con.executemany(
            """
            INSERT INTO performances
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    row["show_uuid"],
                    row["song_uuid"],
                    row["song_name"],
                    row["set_number"],
                    row["song_position"],
                    row["segued"],
                )
                for row in performances
            ],
        )

    if venues:
        con.executemany(
            """
            INSERT INTO venues
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    row["venue"],
                    row["city"],
                    row["state"],
                    row["country"],
                )
                for row in venues
            ],
        )

    con.close()


def main():
    records = load_yaml_files()

    shows, performances, venues = extract_show_archive(records)
    songs = extract_song_catalog(records)

    write_duckdb(shows, songs, performances, venues)

    print(f"records_loaded={len(records)}")
    print(f"shows={len(shows)}")
    print(f"songs={len(songs)}")
    print(f"performances={len(performances)}")
    print(f"venues={len(venues)}")
    print(f"database={DB_PATH}")


if __name__ == "__main__":
    main()