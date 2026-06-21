# MCP Tool Specification

## Purpose

Expose DeadBase historical archive data through a stable MCP interface.

The MCP layer serves as the retrieval mechanism between:

Skills

and

DuckDB archival data.

MCP tools must be deterministic.

MCP tools must not generate narratives.

Narrative generation belongs to the agent layer.

---

# Tool: find_show

## Purpose

Retrieve information about a specific Grateful Dead show.

## Inputs

- show_date

Optional:

- venue

## Data Sources

shows

performances

## Outputs

- show metadata
- venue
- location
- setlist
- performance count

---

# Tool: find_song

## Purpose

Retrieve performance history for a song.

## Inputs

- song_name

## Data Sources

songs

performances

shows

## Outputs

- song metadata
- performance count
- first appearance
- last appearance
- performance history

---

# Tool: find_venue

## Purpose

Retrieve venue-level information.

## Inputs

- venue_name

## Data Sources

venues

shows

performances

## Outputs

- venue metadata
- show count
- date range
- song statistics

---

# Tool: find_tour

## Purpose

Retrieve tour-level information.

## Inputs

- tour_name

## Data Sources

shows

performances

## Outputs

- tour summary
- show count
- date range

---

# Tool: compare_setlists

## Purpose

Compare two Grateful Dead performances.

## Inputs

- show_a
- show_b

## Data Sources

performances

## Outputs

- shared songs
- unique songs
- similarity score

---

# Tool Requirements

All tools must:

- be deterministic
- be read-only
- return structured data
- support evaluation testing

Tools must not:

- generate narratives
- modify source data
- modify DuckDB data

---

# Success Criteria

The MCP layer is complete when:

- show-lookup skill can retrieve shows
- song-history skill can retrieve songs
- venue-analysis skill can retrieve venues
- setlist-similarity skill can compare shows

using only MCP tools.