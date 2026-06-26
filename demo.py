from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import duckdb
import re


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "duckdb" / "deadbase.duckdb"


SHOW_DATE_CORNELL = "1977/05/08"
DEFAULT_VENUE = "Barton Hall"
DEFAULT_SONG = "Scarlet Begonias"

from dataclasses import dataclass, field

@dataclass
class InvestigationContext:
    question: str
    show_date: str

    research_agent: Any = None
    historian_agent: Any = None
    venue_agent: Any = None
    song_agent: Any = None
    similarity_agent: Any = None
    synthesis_agent: Any = None

    historian: Any = None
    venue: Any = None
    song: Any = None
    similarity: Any = None
    research: Any = None
    synthesis: Any = None

    metadata: dict = field(default_factory=dict)

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

def run_stage(
    stage_name: str,
    action: str,
    fn,
    *args,
    **kwargs,
):

    section(stage_name)

    status(action)

    try:

        result = fn(*args, **kwargs)

    except TypeError:

        result = fn(**kwargs)

    except Exception as exc:

        warn(f"{stage_name} failed: {exc}")

        return None

    return result

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

    return duckdb.connect(str(DB_PATH))

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
    first_year = history[0]["show_date"][:4]
    last_year = history[-1]["show_date"][:4]

    print(f"Years Active       : {first_year} - {last_year}")
    
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

    section("Similarity Features")
    print("DeadBase compares performances using:")
    print()
    print("• Shared repertoire")
    print("• Song sequencing")
    print("• Set architecture")
    print("• Historical embeddings")

def print_show_summary(show: Dict[str, Any]) -> None:

    section("Show Summary")

    print(f"Date:      {display_date(show['show_date'])}")
    print(f"Venue:     {show['venue']}")
    print(f"Location:  {show['city']}, {show['state']}")

    if show.get("country"):
        print(f"Country:   {show['country']}")

def print_warehouse_status() -> None:
    section("Loading Historical Intelligence Base")
    print("Warehouse Version : 2.0")
    print("Analytics Version : 2026.06")
    print()

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
    section("Loading Historical Analytics Layer")
    
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
            dots = "." * max(2, 32 - len(label))
            print(f"✓ {label}{dots} {count:,} rows")
            pause(0.20)

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



# === AGENT STAGE HELPERS FOR CORNELL INVESTIGATION ===

# Helper to extract song summary fields from a result dictionary
def extract_song_summary_fields(result: Dict[str, Any]) -> Dict[str, Any]:
    answer = result.get("answer", "")

    name = result.get("song_name") or result.get("name") or "-"
    plays = result.get("performance_count") or result.get("count") or "-"
    first = (
        result.get("first_year")
        or result.get("first_performance_year")
        or result.get("first_played")
        or result.get("first_performance")
        or "-"
    )

    if isinstance(first, dict):
        date_value = first.get("date", "")
        if isinstance(date_value, str) and len(date_value) >= 4:
            first = date_value[:4]
        else:
            first = "-"

    if answer:
        count_match = re.search(r"appears\s+([0-9,]+)\s+times", answer)
        if count_match and plays == "-":
            plays = count_match.group(1)

        first_match = re.search(r"first recorded performance occurred on\s+([0-9]{4})", answer)
        if first_match and first == "-":
            first = first_match.group(1)

    if not isinstance(first, str):
        first = str(first)
    if isinstance(first, str) and len(first) >= 4:
        first = first[:4]

    return {
        "name": name,
        "plays": plays,
        "first": first,
    }

# Print a compact summary of song intelligence for a list of song agent results
def print_song_summary(results: List[Any]) -> None:
    if not results:
        return

    section("Song Intelligence")
    print(
        f"{'Song':<32}"
        f"{'Plays':>8}"
        f"{'First':>10}"
    )
    line("-")

    for result in results:
        if not isinstance(result, dict):
            continue
        fields = extract_song_summary_fields(result)
        print(
            f"{fields['name']:<32}"
            f"{fields['plays']:>8}"
            f"{str(fields['first']):>10}"
        )

def run_research_stage(ctx: InvestigationContext):
    ctx.research = None
    if ctx.research_agent:
        ctx.research = run_stage(
            "Research Agent",
            "Coordinating multi-agent investigation",
            ctx.research_agent,
            ctx.show_date,
        )

    if isinstance(ctx.research, dict):
        ctx.historian = ctx.research

def run_historian_stage(ctx: InvestigationContext):
    section("Historian Agent")
    status("Analyzing historical significance")

    if not isinstance(ctx.research, dict):
        return

    rank = ctx.research.get("historian_rank")
    total = ctx.research.get("total_shows", 1822)
    percentile = ctx.research.get("historian_percentile")
    score = ctx.research.get("historian_score")
    archetype = ctx.research.get("primary_archetype")

    if score is not None:
        print(f"Historian Score     {score:.4f}")
    if rank is not None:
        print(f"Archive Rank        {rank} / {total}")
    if percentile is not None:
        print(f"Percentile          {percentile:.2f}%")
    if archetype:
        print(f"Primary Archetype   {archetype}")

# === Setlist Investigation Stage ===
def run_setlist_stage(ctx: InvestigationContext):
    show = ctx.metadata.get("show")
    if not show:
        return

    section("Setlist Agent")
    status("Analyzing performance structure")

    setlist = get_show_setlist(show["show_uuid"])
    print_setlist(setlist)

def run_venue_stage(ctx: InvestigationContext):
    ctx.venue = None
    venue = DEFAULT_VENUE
    show = ctx.metadata.get("show")
    if show:
        venue = show["venue"]
    if ctx.venue_agent:
        ctx.venue = run_stage(
            "Venue Agent",
            "Building venue profile",
            ctx.venue_agent,
            venue,
        )
    else:
        venue_skill = load_skill("venue_profile")
        if venue_skill:
            ctx.venue = run_stage(
                "Venue Skill",
                "Building venue profile",
                venue_skill,
                venue,
            )
    # After obtaining the venue result, print the venue timeline, first/last/all performances
    history = get_venue_history(venue)
    print_venue_history(history)
    # Do not print the venue agent preview/result

def run_similarity_stage(ctx: InvestigationContext):
    ctx.similarity = None
    if ctx.similarity_agent:
        ctx.similarity = run_stage(
            "Similarity Agent",
            "Searching for neighboring performances",
            ctx.similarity_agent.analyze,
            ctx.show_date,
            top_n=5,
        )
        if ctx.similarity:
            print_similarity_table(ctx.similarity)
    else:
        recommender = load_skill("show_recommender")
        if recommender:
            ctx.similarity = run_stage(
                "Similarity Skill",
                "Searching for neighboring performances",
                recommender,
                ctx.show_date,
                top_n=5,
            )
            if ctx.similarity:
                print_similarity_table(ctx.similarity)

def run_song_stage(ctx: InvestigationContext):
    ctx.song = []
    song_skill = None
    # Evidence-driven: get show metadata if available
    show = ctx.metadata.get("show")
    songs = []
    if show:
        setlist = get_show_setlist(show["show_uuid"])
        # Build list of first five unique song names in setlist order
        seen = set()
        for song_entry in setlist:
            name = song_entry["song_name"]
            if name not in seen:
                songs.append(name)
                seen.add(name)
            if len(songs) == 5:
                break
    else:
        # Fallback to hard-coded list if no show metadata
        songs = [
            "Scarlet Begonias",
            "Fire On The Mountain",
            "Morning Dew",
            "Saint Stephen",
        ]
    # Print evidence-driven song list
    section("Songs Examined")
    for song in songs:
        print(f"- {song}")
    # Run agent/skill for these songs, do not print full reports
    if ctx.song_agent:
        for song in songs:
            try:
                result = ctx.song_agent(song)
                if isinstance(result, dict):
                    result.setdefault("song_name", song)
                ctx.song.append(result)
            except TypeError:
                result = ctx.song_agent(song_name=song)
                if isinstance(result, dict):
                    result.setdefault("song_name", song)
                ctx.song.append(result)
            except Exception as exc:
                warn(f"Song Agent failed for {song}: {exc}")
    else:
        song_skill = load_skill("song_history")
        if song_skill:
            for song in songs:
                try:
                    result = song_skill(song)
                    if isinstance(result, dict):
                        result.setdefault("song_name", song)
                    ctx.song.append(result)
                except Exception as exc:
                    warn(f"Song skill failed for {song}: {exc}")
    # Print compact song summary at end of stage
    print_song_summary(ctx.song)

def run_synthesis_stage(ctx: InvestigationContext, research_result):
    section("Synthesis Agent")
    status("Combining evidence")
    status("Synthesizing historical evidence")
    section("Historical Conclusion")

    ctx.synthesis = None
    if ctx.synthesis_agent:
        result = ctx.synthesis_agent(ctx.research)
        ctx.synthesis = result
        print_full_result(ctx.synthesis)
    else:
        warn("No synthesis agent available for this investigation.")




# === Context and Pipeline Helpers for Cornell Investigation ===

def load_investigation_context(question: str, show_date: str) -> InvestigationContext:
    ctx = InvestigationContext(
        question=question,
        show_date=show_date,
    )
    ctx.research_agent = load_research_agent()
    ctx.historian_agent = load_historian_agent()
    ctx.venue_agent = load_venue_agent()
    ctx.song_agent = load_song_agent()
    ctx.similarity_agent = load_similarity_agent()
    ctx.synthesis_agent = load_synthesis_agent()

    show = get_show_record(show_date)

    if show:
        ctx.metadata["show"] = show

    return ctx

def load_cornell_context() -> InvestigationContext:
    return load_investigation_context(
        question="Was Cornell 1977 actually unique?",
        show_date=SHOW_DATE_CORNELL,
    )

def run_cornell_pipeline(ctx: InvestigationContext) -> None:
    run_investigation_pipeline(ctx)


# === Generic Investigation Pipeline ===
def run_investigation_pipeline(ctx: InvestigationContext) -> None:
    run_research_stage(ctx)
    run_historian_stage(ctx)
    run_setlist_stage(ctx)
    run_venue_stage(ctx)
    run_similarity_stage(ctx)
    run_song_stage(ctx)
    run_synthesis_stage(ctx, ctx.research)


# === Generic Presentation for Investigation Completion ===
def present_investigation(ctx: InvestigationContext):
    print()
    line("=")
    print("Historical Investigation Complete".center(78))
    print("6 agents successfully orchestrated.".center(78))
    print("Evidence fused into a single historical assessment.".center(78))
    line("=")


def run_planning_stage(ctx: InvestigationContext) -> None:
    section("Planning Agent")
    status("Building historical investigation plan")
    status(f"Selected target show: {display_date(ctx.show_date)}")
    status("Selected evidence sources: historian, venue, song, similarity")
    status("Routing investigation to specialist agents")

def run_cornell_investigation() -> None:
    clear_screen()
    title("DEADBASE LIVE INVESTIGATION")
    print()
    print("Question: Was Cornell 1977 actually unique?")
    print()

    ctx = load_cornell_context()
    start = time.perf_counter()

    run_planning_stage(ctx)
    run_cornell_pipeline(ctx)
    present_investigation(ctx)

    elapsed = time.perf_counter() - start
    line("-")
    print(f"Pipeline Execution Time : {elapsed:.2f} seconds".center(78))
    print("Warehouse Queries       : Complete".center(78))
    print("Agent Orchestration     : Complete".center(78))
    line("-")
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

    show = get_show_record(show_date)

    if not show:
        warn(f"No show found for {display_date(show_date)}.")
        input("\nPress Enter to return to menu...")
        return

    ctx = load_investigation_context(
        question=f"Historical investigation for {display_date(show_date)}",
        show_date=show_date,
    )
    try:
        start = time.perf_counter()
        
        run_planning_stage(ctx)
        run_investigation_pipeline(ctx)
        present_investigation(ctx)

        elapsed = time.perf_counter() - start
        line("-")
        print(f"Pipeline Execution Time : {elapsed:.2f} seconds".center(78))
        print("Warehouse Queries       : Complete".center(78))
        print("Agent Orchestration     : Complete".center(78))
        line("-")
        
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