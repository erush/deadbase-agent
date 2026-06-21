# DeadBase Agent

## Subtitle

A Spec-Driven Historical Research Agent for Exploring Grateful Dead Concert History

---

# 1. Problem Statement

The Grateful Dead produced one of the most extensively documented live music archives in history.

However, historical information remains fragmented across:

- Setlists
- Show archives
- Fan websites
- Tour summaries
- Venue records
- Song histories
- Discussion forums

Answering historical questions often requires manually searching multiple sources and synthesizing information.

Examples:

- When was Dark Star last played before Cornell 1977?
- How did Scarlet Begonias evolve during the 1970s?
- Which venues hosted the most Grateful Dead performances?
- What songs disappeared after 1974?
- What shows most closely resemble Cornell 1977?

The objective of DeadBase is to provide a historical research agent capable of answering these questions using structured archival data.

---

# 2. Project Goals

DeadBase will:

1. Answer historical Grateful Dead research questions.
2. Use structured archival data as the source of truth.
3. Provide evidence-based responses.
4. Demonstrate Spec-Driven Development.
5. Demonstrate Agent Skills.
6. Demonstrate MCP integration.
7. Demonstrate evaluation-driven development.
8. Demonstrate deployable AI agent architecture.

---

# 3. Non-Goals

DeadBase will not:

- Generate fictional history.
- Provide concert recordings.
- Provide copyrighted media.
- Modify archival records.
- Perform financial transactions.
- Perform user account management.

All interactions are read-only.

---

# 4. Users

## Primary Users

- Grateful Dead fans
- Music historians
- Researchers
- Writers
- Podcasters
- Archivists

## Secondary Users

- Data scientists
- Agent developers
- Kaggle judges

---

# 5. Data Sources

## Source Data

Primary data originates from:

- YAML show files
- Setlist archives
- Tour metadata
- Venue metadata

## Data Characteristics

Contains:

- Show dates
- Venues
- Locations
- Setlists
- Songs
- Tours
- Performance order

---

# 6. System Architecture

User

↓

DeadBase Agent

↓

Skill Router

↓

Agent Skills

↓

MCP Tools

↓

YAML Knowledge Base

---

# 7. Core Agent Responsibilities

The DeadBase Agent acts as:

- Research assistant
- Historical archivist
- Query planner
- Evidence synthesizer

The agent must:

- Determine user intent
- Select the correct skill
- Call required tools
- Collect evidence
- Generate final response

---

# 8. MCP Server Responsibilities

The MCP Server exposes archival data through tools.

The MCP Server must provide:

- find_show
- find_song
- find_venue
- find_tour
- compare_setlists

The MCP Server must be read-only.

The MCP Server must never alter source data.

---

# 9. Agent Skills

## Skill: Show Lookup

Purpose:

Retrieve information for a specific show.

Examples:

- What was played on 1977-05-08?
- Show me the setlist from Veneta 1972.

Outputs:

- Date
- Venue
- Location
- Setlist

---

## Skill: Song History

Purpose:

Analyze performance history of a song.

Examples:

- First performance
- Last performance
- Frequency by year
- Performance gaps

Outputs:

- Timeline
- Counts
- Historical narrative

---

## Skill: Venue Analysis

Purpose:

Analyze venue history.

Examples:

- Most frequently played venues
- Venue-specific trends

Outputs:

- Venue statistics
- Historical context

---

## Skill: Tour Analysis

Purpose:

Analyze tours and tour eras.

Examples:

- Europe 72
- Spring 77

Outputs:

- Tour summary
- Statistics
- Key performances

---

## Skill: Setlist Similarity

Purpose:

Compare shows and setlists.

Examples:

- Similar shows to Cornell 1977
- Similarity between tours

Outputs:

- Similarity score
- Shared songs
- Comparative analysis

---

## Skill: Song Evolution

Purpose:

Track evolution of songs through time.

Examples:

- Scarlet Begonias evolution
- Dark Star evolution

Outputs:

- Timeline
- Historical narrative
- Significant transitions

---

# 10. Evaluation Requirements

Each skill requires evaluation cases.

Evaluation files must define:

- User input
- Expected skill
- Expected tools
- Expected output structure

Evaluation must occur before deployment.

---

# 11. Behavior Driven Specifications

## Scenario

Show Lookup

Given:

A valid show date exists

When:

A user requests information about the show

Then:

The correct show is retrieved

And:

The setlist is returned

And:

The source show is cited

---

## Scenario

Song History

Given:

A song exists

When:

The user requests historical analysis

Then:

All matching performances are identified

And:

Historical patterns are summarized

And:

Evidence is returned

---

## Scenario

Tour Analysis

Given:

A valid tour exists

When:

The user requests a tour summary

Then:

Relevant shows are retrieved

And:

Tour statistics are calculated

And:

A narrative summary is generated

---

# 12. Security Requirements

The system is read-only.

The system must:

- Prevent data modification
- Prevent arbitrary code execution
- Prevent unrestricted file access
- Prevent write operations through MCP

No credentials may be stored in source code.

---

# 13. Observability Requirements

The system must log:

- Skill selected
- MCP tools used
- Query execution time
- Evaluation results

---

# 14. Deployment Requirements

DeadBase must run locally.

Optional deployment targets:

- Cloud Run
- Render
- Railway

Deployment must use the same MCP interface and skills library.

---

# 15. Success Criteria

A successful DeadBase release can answer:

1. When was Dark Star last played before Cornell 1977?
2. What songs disappeared after 1974?
3. Which venues hosted the most shows?
4. Summarize Europe 72.
5. Find shows similar to Cornell 1977.

Using:

- Agent Skills
- MCP Tools
- Structured Data
- Evidence-Based Responses

Without manual intervention.

# 16. Agent Skill Catalog

The DeadBase Agent shall support the following skill catalog.

| Skill | Purpose |
|---------|---------|
| show-lookup | Retrieve information about a specific show |
| song-history | Analyze performance history of songs |
| venue-analysis | Analyze venue history and trends |
| tour-analysis | Analyze tours and eras |
| setlist-similarity | Compare shows and setlists |
| song-evolution | Track evolution of songs over time |

Skills shall load dynamically based on user intent.

Only the skill required for the current task should be loaded.

---

# 17. MCP Tool Definitions

The MCP Server shall expose the following tools.

## find_show

Input:

- date
- venue

Output:

- show metadata
- setlist
- venue information

---

## find_song

Input:

- song_name

Output:

- performance history
- first performance
- last performance
- performance count

---

## find_venue

Input:

- venue_name

Output:

- venue profile
- show count
- performance history

---

## find_tour

Input:

- tour_name

Output:

- tour metadata
- associated shows
- summary statistics

---

## compare_setlists

Input:

- show_a
- show_b

Output:

- similarity score
- shared songs
- unique songs

---

# 18. Evaluation Dataset

The project shall contain evaluation cases covering:

- show lookup
- song history
- venue analysis
- tour analysis
- setlist similarity

Each evaluation shall contain:

- user input
- expected skill
- expected MCP tool usage
- expected response structure

Minimum evaluation count:

25 total cases.

---

# 19. Kaggle Demonstration Scenarios

The final demonstration video shall showcase:

Scenario 1

Question:

When was Dark Star last played before Cornell 1977?

Expected Skill:

song-history

Expected Tool:

find_song

---

Scenario 2

Question:

Which venues hosted the most Grateful Dead shows?

Expected Skill:

venue-analysis

Expected Tool:

find_venue

---

Scenario 3

Question:

Summarize Europe 72.

Expected Skill:

tour-analysis

Expected Tool:

find_tour

---

Scenario 4

Question:

Find shows most similar to Cornell 1977.

Expected Skill:

setlist-similarity

Expected Tool:

compare_setlists

---

Scenario 5

Question:

How did Scarlet Begonias evolve during the 1970s?

Expected Skill:

song-evolution

Expected Tool:

find_song

---

# 20. Future Expansion

Future versions may support:

- Jerry Garcia Band
- Dead & Company
- Further
- RatDog
- Phil & Friends
- Interactive timeline visualizations
- Geographic tour visualizations
- Audio archive integrations
- Multi-artist historical archive support