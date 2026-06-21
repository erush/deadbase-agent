from mcp_server.database import get_connection


def find_show(show_date: str):

    con = get_connection()

    show = con.execute(
        """
        select *
        from shows
        where show_date = ?
        """,
        [show_date]
    ).fetchall()

    performances = con.execute(
        """
        select
            song_name,
            set_number,
            song_position,
            segued
        from performances p
        join shows s
            on p.show_uuid = s.show_uuid
        where s.show_date = ?
        order by
            set_number,
            song_position
        """,
        [show_date]
    ).fetchall()

    con.close()

    return {
        "show": show,
        "performances": performances
    }


def find_song(song_name: str):

    con = get_connection()

    results = con.execute(
        """
        select
            p.song_name,
            s.show_date,
            s.venue,
            s.city,
            s.state
        from performances p
        join shows s
            on p.show_uuid = s.show_uuid
        where lower(p.song_name) = lower(?)
        order by s.show_date
        """,
        [song_name]
    ).fetchall()

    con.close()

    return results


def find_venue(venue_name: str):

    con = get_connection()

    results = con.execute(
        """
        select *
        from shows
        where lower(venue) like lower(?)
        order by show_date
        """,
        [f"%{venue_name}%"]
    ).fetchall()

    con.close()

    return results

def find_song_before_date(
    song_name: str,
    before_date: str
):

    con = get_connection()

    results = con.execute(
        """
        select
            p.song_name,
            s.show_date,
            s.venue,
            s.city,
            s.state
        from performances p
        join shows s
            on p.show_uuid = s.show_uuid
        where lower(p.song_name) = lower(?)
          and s.show_date < ?
        order by s.show_date
        """,
        [song_name, before_date]
    ).fetchall()

    con.close()

    return results

def compare_setlists(
    show_date_a: str,
    show_date_b: str
):

    con = get_connection()

    songs_a = con.execute(
        """
        select distinct p.song_name
        from performances p
        join shows s
            on p.show_uuid = s.show_uuid
        where s.show_date = ?
        """,
        [show_date_a]
    ).fetchall()

    songs_b = con.execute(
        """
        select distinct p.song_name
        from performances p
        join shows s
            on p.show_uuid = s.show_uuid
        where s.show_date = ?
        """,
        [show_date_b]
    ).fetchall()

    con.close()

    set_a = {row[0] for row in songs_a}
    set_b = {row[0] for row in songs_b}

    shared = sorted(list(set_a & set_b))

    only_a = sorted(list(set_a - set_b))

    only_b = sorted(list(set_b - set_a))

    similarity = 0

    if len(set_a | set_b) > 0:
        similarity = round(
            len(set_a & set_b)
            / len(set_a | set_b),
            3
        )

    return {
        "show_a": show_date_a,
        "show_b": show_date_b,
        "shared_songs": shared,
        "only_a": only_a,
        "only_b": only_b,
        "similarity": similarity
    }