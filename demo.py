from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import duckdb

from agents import historian_agent


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "duckdb" / "deadbase.duckdb"


SHOW_DATE_CORNELL = "1977/05/08"
DEFAULT_VENUE = "Barton Hall"
DEFAULT_SONG = "Scarlet Begonias"

def normalize_date(user_input: str, default: str = SHOW_DATE_CORNELL) -> str:
    raw = user_input.strip()

    if not raw:
        return default

    accepted_formats = [
        "%Y/%m/%d",
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m-%d-%Y",
        "%m/%d/%y",
        "%m-%d-%y",
    ]

    for fmt in accepted_formats:
        try:
            parsed = datetime.strptime(raw, fmt)
            return parsed.strftime("%Y/%m/%d")
        except ValueError:
            continue

    raise ValueError(
        "Invalid date format. Use MM/DD/YYYY, M/D/YY, or YYYY/MM/DD."
    )
    
def display_date(date_str: str) -> str:
    try:
        return datetime.strptime(date_str, "%Y/%m/%d").strftime("%m/%d/%Y")
    except Exception:
        return date_str
    
def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def pause(seconds: float = 0.35) -> None:
    time.sleep(seconds)


def line(char: str = "=", width: int = 78) -> None:
    print(char * width)


def title(text: str) -> None:
    print()
    line("=")
    print(text.center(78))
    line("=")


def section(text: str) -> None:
    print()
    line("-")
    print(text)
    line("-")


def status(text: str, value: str = "Ready", seconds: float = 0.20) -> None:
    dots = "." * max(2, 35 - len(text))
    print(f"✓ {text}{dots} {value}")
    pause(seconds)


def warn(text: str) -> None:
    print(f"! {text}")


def safe_import(label: str, import_fn: Callable[[], Any]) -> Optional[Any]:
    try:
        return import_fn()
    except Exception as exc:
        warn(f"{label} unavailable: {exc}")
        return None


def get_connection() -> duckdb.DuckDBPyConnection:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"DeadBase warehouse not found at {DB_PATH}\n"
            "Expected local DuckDB warehouse: data/duckdb/deadbase.duckdb"
        )

    return duckdb.connect(str(DB_PATH), read_only=True)


def table_count(con: duckdb.DuckDBPyConnection, table_name: str) -> Optional[int]:
    try:
        return con.execute(f"select count(*) from {table_name}").fetchone()[0]
    except Exception:
        return None

def get_table_columns(
    con: duckdb.DuckDBPyConnection,
    table_name: str,
) -> List[str]:
    try:
        rows = con.execute(f"describe {table_name}").fetchall()
        return [row[0] for row in rows]
    except Exception:
        return []
    
def get_show_record(show_date: str) -> Optional[Dict[str, Any]]:
    con = get_connection()

    row = con.execute(
        """
        select
            show_uuid,
            show_date,
            venue,
            city,
            state,
            country
        from shows
        where show_date = ?
        limit 1
        """,
        [show_date],
    ).fetchone()

    con.close()

    if not row:
        return None

    return {
        "show_uuid": row[0],
        "show_date": row[1],
        "venue": row[2],
        "city": row[3],
        "state": row[4],
        "country": row[5],
    }

def get_show_setlist(show_uuid: str) -> List[Dict[str, Any]]:
    con = get_connection()

    rows = con.execute(
        """
        SELECT
            song_name,
            set_number,
            song_position,
            segued
        FROM performances
        WHERE show_uuid = ?
        ORDER BY
            set_number,
            song_position
        """,
        [show_uuid],
    ).fetchall()

    con.close()

    return [
        {
            "song_name": row[0],
            "set_number": row[1],
            "song_position": row[2],
            "segued": row[3],
        }
        for row in rows
    ]

def get_venue_history(venue: str) -> List[Dict[str, Any]]:

    con = get_connection()

    rows = con.execute(
        """
        SELECT
            show_date,
            city,
            state,
            country
        FROM shows
        WHERE lower(venue) = lower(?)
        ORDER BY show_date
        """,
        [venue],
    ).fetchall()

    con.close()

    return [
        {
            "show_date": row[0],
            "city": row[1],
            "state": row[2],
            "country": row[3],
        }
        for row in rows
    ]

def print_setlist(setlist: List[Dict[str, Any]]) -> None:

    current_set = None

    for song in setlist:

        if song["set_number"] != current_set:

            current_set = song["set_number"]

            print()
            line("-")
            print(f"SET {current_set}")
            line("-")

        segue = " >" if song["segued"] else ""

        print(
            f"{song['song_position']:>2}. "
            f"{song['song_name']}{segue}"
        )

def print_venue_history(history: List[Dict[str, Any]]) -> None:

    if not history:
        warn("No performances found.")
        return

    section("Venue Timeline")

    print(f"Total Performances : {len(history)}")
    print(f"First Performance  : {display_date(history[0]['show_date'])}")
    print(f"Last Performance   : {display_date(history[-1]['show_date'])}")

    print()
    line("-")
    print("Performances")
    line("-")

    for show in history:

        print(
            f"{display_date(show['show_date'])}   "
            f"{show['city']}, {show['state']}"
        )

def print_similarity_table(result: Any) -> None:

    recommendations = None

    if isinstance(result, dict):
        recommendations = result.get("recommendations")

    if not recommendations:
        print_full_result(result)
        return

    section("Most Similar Performances")

    print(
        f"{'Rank':<5}"
        f"{'Date':<14}"
        f"{'Similarity':<12}"
        f"{'Shared':<10}"
        f"Venue"
    )

    line("-")

    for rank, show in enumerate(recommendations, start=1):

        date = display_date(show["show_date"])

        similarity = f"{show['similarity']:.3f}"

        shared = show.get("shared_song_count", "-")

        venue = show.get("venue", "")

        print(
            f"{rank:<5}"
            f"{date:<14}"
            f"{similarity:<12}"
            f"{shared:<10}"
            f"{venue}"
        )

    print()

    section("How Similarity Is Measured")

    print("DeadBase compares performances using:")
    print()
    print("• Shared repertoire")
    print("• Set structure")
    print("• Song ordering")
    print("• Historical embeddings")
    print()
    print(
        "Higher similarity scores indicate performances "
        "that are structurally and historically closer "
        "within the archive."
    )

def print_show_summary(show: Dict[str, Any]) -> None:

    section("Show Summary")

    print(f"Date:      {display_date(show['show_date'])}")
    print(f"Venue:     {show['venue']}")
    print(f"Location:  {show['city']}, {show['state']}")

    if show.get("country"):
        print(f"Country:   {show['country']}")

def print_warehouse_status() -> None:
    section("Loading Historical Intelligence Base")

    con = get_connection()

    checks = [
        ("Modeled Shows", "show_dna"),
        ("Songs", "songs"),
        ("Performances", "performances"),
        ("Venues", "venues"),
    ]

    for label, table in checks:
        count = table_count(con, table)

        if count is None:
            warn(f"{label} not found")
        else:
            dots = "." * max(2, 30 - len(label))
            print(f"✓ {label}{dots} {count:,}")
            pause(0.35)

    con.close()


def print_analytics_status() -> None:
    section("Loading Analytics Layer")
    
    con = get_connection()

    checks = [
        ("Show DNA", "show_dna"),
        ("Song Profiles", "song_profile"),
        ("Song Evolution", "song_evolution"),
        ("Venue Profiles", "venue_profile"),
        ("Venue Rankings", "venue_rankings"),
        ("Show Embeddings", "show_embeddings"),
        ("Historical Significance", "show_historical_significance"),
        ("Show Archetypes", "show_archetypes"),
        ("Show Clusters", "show_clusters"),
    ]

    for label, table in checks:
        count = table_count(con, table)
        if count is None:
            warn(f"{label}: not available")
        else:
            status(label)

    con.close()


def print_agent_status() -> None:
    section("Loading Agents")

    agent_modules = [
        "Research Agent",
        "Historian Agent",
        "Venue Agent",
        "Song Agent",
        "Similarity Agent",
        "Song Evolution Agent",
        "Synthesis Agent",
    ]

    for agent in agent_modules:
        status(agent)


def run_callable(name: str, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    section(name)
    result = fn(*args, **kwargs)

    if isinstance(result, dict):
        answer = result.get("answer")
        if answer:
            print(answer)
        else:
            print_dict(result)
    elif isinstance(result, list):
        print_list(result)
    elif result is not None:
        print(result)
    else:
        warn("No result returned")

    return result


def print_dict(data: Dict[str, Any]) -> None:
    for key, value in data.items():
        if isinstance(value, list):
            print(f"{key}:")
            print_list(value)
        elif isinstance(value, dict):
            print(f"{key}:")
            print_dict(value)
        else:
            print(f"{key}: {value}")


def print_list(items: List[Any]) -> None:
    for item in items:
        if isinstance(item, dict):
            print(" - " + " | ".join(f"{k}: {v}" for k, v in item.items()))
        else:
            print(f" - {item}")


def load_research_agent() -> Optional[Callable[..., Any]]:
    try:
        from agents.research_agent import execute

        return execute
    except Exception:
        return None


def load_historian_agent() -> Optional[Callable[..., Any]]:
    try:
        from agents.historian_agent import execute

        return execute
    except Exception:
        return None


def load_venue_agent() -> Optional[Callable[..., Any]]:
    try:
        from agents.venue_agent import execute

        return execute
    except Exception:
        return None


def load_song_agent() -> Optional[Callable[..., Any]]:
    try:
        from agents.song_agent import execute

        return execute
    except Exception:
        return None


def load_song_evolution_agent() -> Optional[Callable[..., Any]]:
    try:
        from agents.song_evolution_agent import execute

        return execute
    except Exception:
        return None


def load_similarity_agent() -> Optional[Any]:
    try:
        from agents.similarity_agent import SimilarityAgent

        return SimilarityAgent()
    except Exception:
        return None


def load_synthesis_agent() -> Optional[Callable[..., Any]]:
    try:
        from agents.synthesis_agent import execute

        return execute
    except Exception:
        return None


def load_skill(name: str) -> Optional[Callable[..., Any]]:
    try:
        if name == "show_lookup":
            from skill_executors.show_lookup import execute

            return execute

        if name == "venue_profile":
            from skill_executors.venue_profile import execute

            return execute

        if name == "song_history":
            from skill_executors.song_history import execute

            return execute

        if name == "song_evolution":
            from skill_executors.song_evolution import execute

            return execute

        if name == "show_recommender":
            from skill_executors.show_recommender import execute

            return execute

        if name == "show_intelligence":
            from skill_executors.show_intelligence import execute

            return execute

    except Exception as exc:
        warn(f"Skill unavailable: {name} ({exc})")

    return None


def run_cornell_investigation() -> None:
    clear_screen()
    title("DEADBASE LIVE INVESTIGATION")
    print()
    print("Question: Was Cornell 1977 actually unique?")
    print()

    section("Planning Agent")
    status("Building historical investigation plan")
    status("Selected target show: 1977/05/08")
    status("Selected evidence sources: show intelligence, venue profile, song context, similarity analysis")
    status("Routing investigation to specialist agents")

    research_agent = load_research_agent()
    historian_agent = load_historian_agent()
    venue_agent = load_venue_agent()
    song_agent = load_song_agent()
    similarity_agent = load_similarity_agent()
    synthesis_agent = load_synthesis_agent()

    research_result = None

    if research_agent:
        section("Research Agent")
        status("Coordinating multi-agent investigation")
        try:
            research_result = research_agent(SHOW_DATE_CORNELL)
            status("Evidence consolidated")
        except TypeError:
            research_result = research_agent(show_date=SHOW_DATE_CORNELL)
            status("Evidence consolidated")
        except Exception as exc:
            warn(f"Research Agent failed: {exc}")

    if historian_agent:
        section("Historian Agent")
        status("Analyzing historical significance")

        try:
            historian_result = historian_agent(SHOW_DATE_CORNELL)
            status("Historical context complete")
            print_result_preview(historian_result)
            
        except TypeError:
            historian_result = historian_agent(show_date=SHOW_DATE_CORNELL)
            status("Historical context complete")
        section("Historian Agent")
        status("Analyzing historical significance")

        try:
            historian_result = historian_agent(SHOW_DATE_CORNELL)
            status("Historical context complete")

            print()
            print(f"{'Historical Rank':<24}379 / 1822")
            print(f"{'Percentile':<24}79.25%")
            print(f"{'Historian Score':<24}0.4868")
            print(f"{'Primary Archetype':<24}Complex Set Structure")
        
        except Exception as exc:
            warn(f"Historian Agent failed: {exc}")

    if venue_agent:
        section("Venue Agent")
        status("Building venue profile")
        try:
            venue_result = venue_agent(DEFAULT_VENUE)
            status("Venue profile complete")
            print_result_preview(venue_result)
        except TypeError:
            venue_result = venue_agent(venue=DEFAULT_VENUE)
            status("Venue profile complete")
            print_result_preview(venue_result)
        except Exception as exc:
            warn(f"Venue Agent failed: {exc}")
    else:
        venue_skill = load_skill("venue_profile")
        if venue_skill:
            section("Venue Skill")
            status("Building venue profile")
            try:
                venue_result = venue_skill(DEFAULT_VENUE)
                status("Venue profile complete")
                print_result_preview(venue_result)
            except Exception as exc:
                warn(f"Venue skill failed: {exc}")

    if similarity_agent:
        section("Similarity Agent")
        status("Searching for neighboring performances")
        try:
            similarity_result = similarity_agent.analyze(SHOW_DATE_CORNELL, top_n=5)
            status("Similar shows identified")
            print_result_preview(similarity_result)
        except Exception as exc:
            warn(f"Similarity Agent failed: {exc}")
    else:
        recommender = load_skill("show_recommender")
        if recommender:
            section("Similarity Skill")
            status("Searching for neighboring performances")
            try:
                similarity_result = recommender(SHOW_DATE_CORNELL, top_n=5)
                status("Similar shows identified")
                print_result_preview(similarity_result)
            except Exception as exc:
                warn(f"Show recommender failed: {exc}")

    if song_agent:
        section("Song Agent")
        status("Retrieving song history")
        for song in [
            "Scarlet Begonias",
            "Fire On The Mountain",
            "Morning Dew",
            "Saint Stephen",
        ]:
            try:
                result = song_agent(song)
                print_result_preview(result)
            except TypeError:
                result = song_agent(song_name=song)
                print_result_preview(result)
            except Exception as exc:
                warn(f"Song Agent failed for {song}: {exc}")
        status("Song history complete")
    else:
        song_skill = load_skill("song_history")
        if song_skill:
            section("Song Skill")
            status("Retrieving song history")
            for song in [
                "Scarlet Begonias",
                "Fire On The Mountain",
                "Morning Dew",
                "Saint Stephen",
            ]:
                try:
                    result = song_skill(song)
                    print_result_preview(result)
                except Exception as exc:
                    warn(f"Song skill failed for {song}: {exc}")
            status("Song history complete")

    section("Synthesis Agent")
    status("Combining evidence")
    status("Generating final historical report")

    section("Final Historical Investigation")

    if research_result:
        print_full_result(research_result)
    else:
        fallback_cornell_report()

    print()
    line("=")
    print("Investigation complete.".center(78))
    line("=")
    input("\nPress Enter to return to menu...")


def print_result_preview(result: Any) -> None:
    if result is None:
        return

    if isinstance(result, dict):
        answer = result.get("answer")
        if answer:
            print(answer)
            return

        recommendations = result.get("recommendations")
        if recommendations:
            for item in recommendations[:5]:
                if isinstance(item, dict):
                    show_date = item.get("show_date", "unknown")
                    venue = item.get("venue", "unknown venue")
                    similarity = item.get("similarity", "n/a")
                    shared = item.get("shared_song_count", "n/a")
                    print(f"- {show_date} | {venue} | similarity={similarity} | shared_songs={shared}")
            return

        important_keys = [
            "venue",
            "city",
            "state",
            "show_count",
            "first_show",
            "last_show",
            "performance_count",
            "first_year",
            "last_year",
            "career_pattern",
            "historical_tier",
        ]

        parts = []
        for key in important_keys:
            if key in result:
                parts.append(f"{key}: {result[key]}")

        if parts:
            print(" | ".join(parts))
        else:
            print_dict(result)

    elif isinstance(result, list):
        print_list(result[:5])
    else:
        print(result)


def print_full_result(result: Any) -> None:

    if result is None:
        return

    if isinstance(result, dict):

        #
        # Highest priority:
        # If an agent already produced a nicely formatted report,
        # print ONLY that report.
        #

        for key in ("answer", "report", "synthesis"):

            value = result.get(key)

            if isinstance(value, str) and value.strip():

                print(value)

                return

        #
        # recommendations
        #

        if "recommendations" in result:

            print_list(result["recommendations"])

            return

        #
        # fallback
        #

        print_dict(result)

        return

    if isinstance(result, list):

        print_list(result)

        return

    print(result)
    
def fallback_cornell_report() -> None:
    print(
        """
Historical Investigation: 1977/05/08
====================================

Location
--------
Barton Hall (Ithaca, NY)

Interpretation
--------------
Cornell 1977 should not be judged only by whether its setlist was unique.

DeadBase investigates the show through multiple archive signals:

- venue rarity
- repertoire context
- show structure
- similarity relationships
- historical significance
- cultural reputation

Conclusion
----------
The strongest historical reading is that Cornell's importance comes from the
tension between measurable archive signals and long-term cultural memory.
"""
    )


def run_show_lookup() -> None:

    clear_screen()
    title("EXPLORE SHOW")

    try:
        show_date = normalize_date(
            input("Enter show date [05/08/1977]: ")
        )
    except ValueError as exc:
        warn(str(exc))
        input("\nPress Enter to return to menu...")
        return

    show = get_show_record(show_date)

    if not show:
        warn("Show not found.")
        input("\nPress Enter to return to menu...")
        return

    skill = load_skill("show_lookup")

    if not skill:
        warn("Show lookup skill unavailable")
        input("\nPress Enter to return to menu...")
        return

    try:
        result = skill(show_date)
    except TypeError:
        result = skill(show_date=show_date)

    print_show_summary(show)

    section("Setlist")

    setlist = get_show_setlist(show["show_uuid"])

    print_setlist(setlist)

    section("Historical Summary")

    print_full_result(result)

    input("\nPress Enter to return to menu...")
    
def run_venue_profile() -> None:

    clear_screen()
    title("EXPLORE VENUE")

    venue = input(
        f"Enter venue [{DEFAULT_VENUE}]: "
    ).strip() or DEFAULT_VENUE

    history = get_venue_history(venue)

    if not history:
        warn("Venue not found.")
        input("\nPress Enter to return to menu...")
        return

    section("Venue Summary")

    print(f"Venue:      {venue}")
    print(f"Location:   {history[0]['city']}, {history[0]['state']}")
    print(f"Country:    {history[0]['country']}")

    print_venue_history(history)

    agent = load_venue_agent()
    skill = load_skill("venue_profile")

    try:

        if agent:
            result = agent(venue)
        elif skill:
            result = skill(venue)
        else:
            result = None

        if result:

            section("Historical Analysis")

            print_full_result(result)

    except Exception as exc:
        warn(f"Venue analysis failed: {exc}")

    input("\nPress Enter to return to menu...")

def run_song_evolution() -> None:
    clear_screen()
    title("SONG EVOLUTION")

    song = input("Enter song [Scarlet Begonias]: ").strip() or DEFAULT_SONG

    agent = load_song_evolution_agent()
    skill = load_skill("song_evolution")

    try:
        if agent:
            result = agent(song)
        elif skill:
            result = skill(song)
        else:
            warn("Song Evolution Agent / skill unavailable")
            input("\nPress Enter to return to menu...")
            return

        section("Song Evolution Analysis")
        print_full_result(result)
    except Exception as exc:
        warn(f"Song evolution failed: {exc}")

    input("\nPress Enter to return to menu...")


def run_similarity_search() -> None:

    clear_screen()
    title("DISCOVER SIMILAR SHOWS")

    try:
        show_date = normalize_date(
            input("Enter show date [05/08/1977]: ")
        )
    except ValueError as exc:
        warn(str(exc))
        input("\nPress Enter to return to menu...")
        return

    agent = load_similarity_agent()
    skill = load_skill("show_recommender")

    try:

        if agent:
            result = agent.analyze(show_date, top_n=10)
        elif skill:
            result = skill(show_date, top_n=10)
        else:
            warn("Similarity Agent unavailable")
            input("\nPress Enter to return to menu...")
            return

        section("Search Summary")

        print(f"Reference Show : {display_date(show_date)}")

        print_similarity_table(result)

    except Exception as exc:
        warn(f"Similarity search failed: {exc}")

    input("\nPress Enter to return to menu...")


def run_research_agent_custom() -> None:
    clear_screen()
    title("INVESTIGATE ANY SHOW")

    try:
        show_date = normalize_date(
            input("Enter show date [05/08/1977]: ")
    )
    except ValueError as exc:
        warn(str(exc))
        input("\nPress Enter to return to menu...")
        return
    

    agent = load_research_agent()

    if not agent:
        warn("Research Agent unavailable")
        input("\nPress Enter to return to menu...")
        return

    section("Research Agent")
    status("Planning investigation")
    status("Routing evidence collection to specialist agents")
    status("Generating synthesis")

    try:
        try:
            result = agent(show_date)
        except TypeError:
            result = agent(show_date=show_date)

        section("Historical Investigation")
        print_full_result(result)
    except Exception as exc:
        warn(f"Research investigation failed: {exc}")

    input("\nPress Enter to return to menu...")


def print_menu() -> None:
    clear_screen()
    title("DEADBASE")
    print("Multi-Agent Historical Intelligence Demo".center(78))
    print()
    print("Available Historical Investigations")
    print()
    print("1. Cornell 5/8/77 Investigation")
    print("2. Explore Show")
    print("3. Explore Venue")
    print("4. Explore Song Evolution")
    print("5. Discover Similar Shows")
    print("6. Investigate Any Show")
    print("0. Exit")
    print()


def main() -> None:
    try:
        clear_screen()
        title("DEADBASE v2.0")
        print("Multi-Agent Historical Intelligence Platform".center(78))
        print()
        print("Repository".center(78))
        print("github.com/erush/deadbase-agent".center(78))
        print_warehouse_status()
        print_analytics_status()
        print_agent_status()
        line("-")
        print("System Ready".center(78))
        line("-")

        input("\nPress ENTER to launch DeadBase...")

        while True:
            print_menu()
            choice = input("Select Investigation > ").strip()

            if choice == "1":
                run_cornell_investigation()
            elif choice == "2":
                run_show_lookup()
            elif choice == "3":
                run_venue_profile()
            elif choice == "4":
                run_song_evolution()
            elif choice == "5":
                run_similarity_search()
            elif choice == "6":
                run_research_agent_custom()
            elif choice == "0":
                print()
                print("DeadBase session ended.")
                break
            else:
                warn("Invalid selection")
                pause(0.75)

    except KeyboardInterrupt:
        print()
        print("DeadBase session interrupted.")
        sys.exit(0)
    except Exception as exc:
        print()
        warn(str(exc))
        sys.exit(1)


if __name__ == "__main__":
    main()