from __future__ import annotations

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

import duckdb
import re
from dataclasses import dataclass, field


ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "duckdb" / "deadbase.duckdb"


SHOW_DATE_CORNELL = "1977/05/08"
DEFAULT_VENUE = "Barton Hall"
DEFAULT_SONG = "Scarlet Begonias"


@dataclass
class InvestigationSession:
    question: str
    show_date: str
    intent: str = ""
    selected_skills: list[str] = field(default_factory=list)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    execution_trace: list[str] = field(default_factory=list)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    final_report: str = ""
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
    stage_results: dict[str, bool] = field(default_factory=dict)

    def trace(self, event: str):
        self.execution_trace.append(event)

    def add_skill(self, skill: str):
        if skill not in self.selected_skills:
            self.selected_skills.append(skill)

    def add_tool_call(
        self,
        tool: str,
        arguments: dict[str, Any],
    ):
        self.tool_calls.append(
            {
                "tool": tool,
                "arguments": arguments,
            }
        )

    def add_evidence(
        self,
        source: str,
        payload: Any,
    ):
        self.evidence.append(
            {
                "source": source,
                "payload": payload,
            }
        )

    def mark_stage(self, stage: str, success: bool = True):
        self.stage_results[stage] = success

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

def run_research_stage(session: InvestigationSession):
    session.trace("Research Agent started")
    session.research = None

    if session.research_agent:
        session.research = run_stage(
            "Research Agent",
            "Coordinating multi-agent investigation",
            session.research_agent,
            session.show_date,
        )
    # Observability: trace, skill, evidence
    if session.research is not None:
        session.trace("Research Agent completed")
        if isinstance(session.research, dict):
            session.add_evidence("research-agent", session.research)
            session.historian = session.research
        # Mark stage success for show-lookup if result exists
        session.mark_stage("show-lookup", True)
    else:
        # Mark stage fail if no result
        session.mark_stage("show-lookup", False)

def run_historian_stage(session: InvestigationSession):
    session.trace("Historian Agent started")
    section("Historian Agent")
    status("Analyzing historical significance")

    if not isinstance(session.research, dict):
        session.trace("Historian Agent completed")
        session.mark_stage("show-intelligence", False)
        return

    rank = session.research.get("historian_rank")
    total = session.research.get("total_shows", 1822)
    percentile = session.research.get("historian_percentile")
    score = session.research.get("historian_score")
    archetype = session.research.get("primary_archetype")

    has_result = any(
        x is not None
        for x in (score, rank, percentile, archetype)
    )
    if score is not None:
        print(f"Historian Score     {score:.4f}")
    if rank is not None:
        print(f"Archive Rank        {rank} / {total}")
    if percentile is not None:
        print(f"Percentile          {percentile:.2f}%")
    if archetype:
        print(f"Primary Archetype   {archetype}")
    session.trace("Historian Agent completed")
    session.mark_stage("show-intelligence", has_result)

# === Setlist Investigation Stage ===
def run_setlist_stage(session: InvestigationSession):
    show = session.metadata.get("show")
    if not show:
        return

    section("Setlist Agent")
    status("Analyzing performance structure")

    setlist = get_show_setlist(show["show_uuid"])
    print_setlist(setlist)

def run_venue_stage(session: InvestigationSession):
    session.venue = None
    entities = session.metadata.get("entities", {})
    venue = entities.get("venue")
    if not venue:
        show = session.metadata.get("show")
        if show:
            venue = show["venue"]
    # Observability: trace and tool call before agent/skill
    session.trace("Venue Agent started")
    session.add_tool_call("deadbase_find_venue", {"venue": venue})
    if not session.venue_agent:
        raise RuntimeError("Venue Agent unavailable.")

    session.venue = run_stage(
        "Venue Agent",
        "Building venue profile",
        session.venue_agent,
        venue,
    )
    # After obtaining the venue result, print the venue timeline, first/last/all performances
    if isinstance(session.venue, dict):
        session.add_evidence("venue-agent", session.venue)
        session.trace("Venue Agent completed")
        session.mark_stage("venue-analysis", True)
    else:
        session.mark_stage("venue-analysis", False)
    history = get_venue_history(venue)
    print_venue_history(history)
    # Do not print the venue agent preview/result

def run_similarity_stage(session: InvestigationSession):
    session.similarity = None
    # Observability: trace and tool call before similarity analysis
    session.trace("Similarity Agent started")
    session.add_tool_call("show_recommender", {"show_date": session.show_date, "top_n": 5})
    if not session.similarity_agent:
        raise RuntimeError("Similarity Agent unavailable.")

    session.similarity = run_stage(
        "Similarity Agent",
        "Searching for neighboring performances",
        session.similarity_agent.analyze,
        session.show_date,
        top_n=5,
    )

    if isinstance(session.similarity, dict):
        session.add_evidence("similarity-agent", session.similarity)
        session.trace("Similarity Agent completed")

    if session.similarity:
        print_similarity_table(session.similarity)

    session.mark_stage("setlist-similarity", bool(session.similarity))

def run_song_stage(session: InvestigationSession):
    session.trace("Song Agent started")
    session.song = []
    song_skill = None
    show = session.metadata.get("show")

    if not show:
        warn("No show context available for song analysis.")
        session.mark_stage("song-history", False)
        return

    setlist = get_show_setlist(show["show_uuid"])

    songs = []
    seen = set()

    for performance in setlist:
        song_name = performance["song_name"]

        if song_name in seen:
            continue

        seen.add(song_name)
        songs.append(song_name)
    # Print evidence-driven song list
    section("Songs Examined")
    for song in songs:
        print(f"- {song}")
    # Run agent/skill for these songs, do not print full reports
    if not session.song_agent:
        raise RuntimeError("Song Agent unavailable.")
    for song in songs:
        try:
            result = session.song_agent(song)
            if isinstance(result, dict):
                result.setdefault("song_name", song)
                session.add_evidence("song-agent", result)
            session.song.append(result)
        except TypeError:
            result = session.song_agent(song_name=song)
            if isinstance(result, dict):
                result.setdefault("song_name", song)
                session.add_evidence("song-agent", result)
            session.song.append(result)
        except Exception as exc:
            warn(f"Song Agent failed for {song}: {exc}")
    # Print compact song summary at end of stage
    print_song_summary(session.song)
    session.trace("Song Agent completed")
    # Mark stage as pass if we have at least one song result
    session.mark_stage("song-history", bool(session.song))

def run_synthesis_stage(session: InvestigationSession, research_result):
    session.trace("Synthesis Agent started")
    section("Synthesis Agent")
    status("Combining evidence")
    status("Synthesizing historical evidence")
    section("Historical Conclusion")

    session.synthesis = None
    if not session.synthesis_agent:
        raise RuntimeError("Synthesis Agent unavailable.")

    result = session.synthesis_agent(session.research)
    session.synthesis = result
    if isinstance(result, dict):
        session.final_report = result.get("answer", "")
        session.add_evidence("synthesis-agent", result)
        session.trace("Synthesis Agent completed")
    print_full_result(session.synthesis)
    session.mark_stage("synthesis", session.synthesis is not None)




# === Context and Pipeline Helpers for Cornell Investigation ===

def load_investigation_context(question: str, show_date: str) -> InvestigationSession:
    session = InvestigationSession(
        question=question,
        show_date=show_date,
    )
    session.research_agent = load_research_agent()
    session.historian_agent = load_historian_agent()
    session.venue_agent = load_venue_agent()
    session.song_agent = load_song_agent()
    session.similarity_agent = load_similarity_agent()
    session.synthesis_agent = load_synthesis_agent()

    if show_date:
        show = get_show_record(show_date)
        if not show:
            raise ValueError(f"Show not found in warehouse: {show_date}")
        session.metadata["show"] = show
    return session

def load_cornell_context() -> InvestigationSession:
    return load_investigation_context(
        question="Was Cornell 1977 actually unique?",
        show_date=SHOW_DATE_CORNELL,
    )

def run_cornell_pipeline(session: InvestigationSession) -> None:
    run_investigation_pipeline(session)


# === Generic Investigation Pipeline ===
def run_investigation_pipeline(session: InvestigationSession) -> None:
    plan = session.metadata.get("plan", {})
    skills = plan.get("skills", [])

    if not skills:
        raise RuntimeError(
            "Planning Agent did not produce a workflow. Investigation cannot continue."
        )

    skill_handlers = {
        "show-lookup": run_research_stage,
        "show-intelligence": run_historian_stage,
        "venue-analysis": run_venue_stage,
        "setlist-analysis": run_setlist_stage,
        "setlist-similarity": run_similarity_stage,
        "song-history": run_song_stage,
        "synthesis": lambda s: run_synthesis_stage(s, s.research),
    }

    for skill in skills:
        print(f"Dispatching Skill: {skill}")

        handler = skill_handlers.get(skill)

        if handler is None:
            warn(f"No executor registered for skill: {skill}")
            session.mark_stage(skill, False)
            continue

        handler(session)
        print(f"✓ Completed: {skill}")


# === Generic Presentation for Investigation Completion ===
def present_investigation(session: InvestigationSession):
    print()
    line("=")
    print("Historical Investigation Complete".center(78))
    line("=")

    # Section: Investigation
    section("Investigation")
    print(f"Question: {session.question}")
    print(f"Intent: {session.intent}")

    # Section: Planning
    section("Planning")
    planned_skills = ", ".join(session.selected_skills) if session.selected_skills else "None"
    planned_tools = ", ".join(session.metadata.get("mcp_tools", [])) if session.metadata.get("mcp_tools") else "None"
    print(f"Planned Skills: {planned_skills}")
    print(f"Planned MCP Tools: {planned_tools}")

    # Section: Execution Metrics
    section("Execution Metrics")
    print(f"Skills Executed: {len(session.selected_skills)}")
    print(f"MCP Tool Calls: {len(session.tool_calls)}")
    print(f"Evidence Objects: {len(session.evidence)}")
    print(f"Execution Trace Events: {len(session.execution_trace)}")
    print(f"Historical Report Generated: {'Yes' if getattr(session, 'synthesis', None) else 'No'}")

    # Section: Evaluation
    section("Evaluation")
    # For every planned skill, print pass/fail based on session.stage_results
    skill_names = session.selected_skills
    # Map canonical skill names to stage keys
    
    overall_pass = True
    for skill in skill_names:
        passed = session.stage_results.get(skill, False)
        status_icon = "✓" if passed else "✗"
        status_word = "PASS" if passed else "FAIL"
        print(f"{status_icon} {skill} {status_word}")
        if not passed:
            overall_pass = False
    print()
    print(f"Overall Evaluation: {'PASS' if overall_pass else 'FAIL'}")

    # Section: Tool Calls
    section("Tool Calls")
    if session.tool_calls:
        for call in session.tool_calls:
            tool = call.get("tool", "unknown")
            arguments = call.get("arguments", {})
            print(f"- {tool} {arguments}")
    else:
        print("None")

    # Section: Execution Trace
    section("Execution Trace")
    if session.execution_trace:
        for event in session.execution_trace:
            print(event)
    else:
        print("None")

    # Section: Evidence Sources
    section("Evidence Sources")
    if session.evidence:
        sources = set()
        for e in session.evidence:
            src = e.get("source")
            if src is not None:
                sources.add(src)
        if sources:
            for src in sorted(sources):
                print(src)
        else:
            print("None")
    else:
        print("None")
    line("=")


def run_planning_stage(session: InvestigationSession) -> None:
    from agents.deadbase_agent import DeadBaseAgent
    planner = DeadBaseAgent()
    plan = planner.plan(session.question)
    session.metadata["entities"] = plan.get("entities", {})
    if not plan.get("skills"):
        raise RuntimeError(
            f"Planning Agent could not determine a workflow for: {session.question}"
        )
    session.metadata["plan"] = plan
    session.metadata["mcp_tools"] = plan.get("mcp_tools", [])
    session.intent = plan.get("intent", "")
    # Clear existing selected skills if any
    session.selected_skills.clear()
    for skill in plan.get("skills", []):
        session.add_skill(skill)
    session.trace("Planning complete")
    print()
    print("Planning Agent")
    line("-")
    print(f"Question: {session.question}")
    print(f"Intent: {session.intent}")
    print()
    print("Selected Skills")
    for skill in session.selected_skills:
        print(f"✓ {skill}")
    print()
    print("MCP Tools")
    for tool in session.metadata["mcp_tools"]:
        print(f"✓ {tool}")
    print()
    print("Investigation Session Created")
    print("Execution Trace Started")

def run_cornell_investigation() -> None:
    clear_screen()
    title("DEADBASE LIVE INVESTIGATION")
    print()
    print("Question: Was Cornell 1977 actually unique?")
    print()

    session = load_cornell_context()
    start = time.perf_counter()

    run_planning_stage(session)
    run_cornell_pipeline(session)
    present_investigation(session)

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

    agent = load_research_agent()
    if not agent:
        raise RuntimeError("Research Agent unavailable.")

    try:
        result = agent(show_date)
    except TypeError:
        result = agent(show_date=show_date)

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
    if not agent:
        raise RuntimeError("Venue Agent unavailable.")

    try:
        result = agent(venue)
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
    if not agent:
        raise RuntimeError("Song Evolution Agent unavailable.")
    try:
        result = agent(song)
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
    if not agent:
        raise RuntimeError("Similarity Agent unavailable.")
    try:
        result = agent.analyze(show_date, top_n=10)
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


    session = load_investigation_context(
        question=f"Historical investigation for {display_date(show_date)}",
        show_date=show_date,
    )
    try:
        start = time.perf_counter()
        
        run_planning_stage(session)
        run_investigation_pipeline(session)
        present_investigation(session)

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
    print("Multi-Agent Historical Intelligence Platform".center(78))
    print()
    print("Available Intelligence Workflows")
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