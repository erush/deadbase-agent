from mcp.server.fastmcp import FastMCP

from skill_executors.show_lookup import execute as execute_show_lookup
from skill_executors.song_history import execute as execute_song_history
from skill_executors.venue_analysis import execute as execute_venue_analysis
from skill_executors.tour_analysis import execute as execute_tour_analysis
from skill_executors.setlist_similarity import execute as execute_setlist_similarity
from skill_executors.song_evolution import execute as execute_song_evolution


mcp = FastMCP("deadbase")


@mcp.tool()
def deadbase_show_lookup(show_date: str):
    """
    Retrieve structured evidence for a specific Grateful Dead show.

    Agent Skill:
    show-lookup
    """
    return execute_show_lookup(show_date)


@mcp.tool()
def deadbase_song_history(song_name: str):
    """
    Retrieve structured evidence about a song's performance history.

    Agent Skill:
    song-history
    """
    return execute_song_history(song_name)


@mcp.tool()
def deadbase_venue_analysis(venue_name: str):
    """
    Retrieve structured evidence about a venue and its DeadBase history.

    Agent Skill:
    venue-analysis
    """
    return execute_venue_analysis(venue_name)


@mcp.tool()
def deadbase_tour_analysis(tour_name: str):
    """
    Retrieve structured evidence about a tour or historical run of shows.

    Agent Skill:
    tour-analysis
    """
    return execute_tour_analysis(tour_name)


@mcp.tool()
def deadbase_setlist_similarity(
    show_date_a: str,
    show_date_b: str
):
    """
    Compare two Grateful Dead shows using setlist similarity evidence.

    Agent Skill:
    setlist-similarity
    """
    return execute_setlist_similarity(
        show_date_a,
        show_date_b
    )


@mcp.tool()
def deadbase_song_evolution(song_name: str):
    """
    Retrieve structured evidence about how a song evolved over time.

    Agent Skill:
    song-evolution
    """
    return execute_song_evolution(song_name)


if __name__ == "__main__":
    mcp.run()