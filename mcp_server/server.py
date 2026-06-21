from mcp.server.fastmcp import FastMCP

from mcp_server.tools import find_show, find_song, find_venue


mcp = FastMCP("deadbase")


@mcp.tool()
def deadbase_find_show(show_date: str):
    return find_show(show_date)


@mcp.tool()
def deadbase_find_song(song_name: str):
    return find_song(song_name)


@mcp.tool()
def deadbase_find_venue(venue_name: str):
    return find_venue(venue_name)


if __name__ == "__main__":
    mcp.run()