# Agent Orchestration Specification

## Purpose

The DeadBase Agent serves as the orchestration layer between users, skills, and MCP tools.

The agent is responsible for:

- understanding user intent
- selecting the correct skill
- invoking MCP tools
- generating evidence-based responses

The agent does not directly access YAML files.

The agent does not directly query DuckDB.

All data access occurs through MCP tools.

---

# Architecture

User

↓

DeadBase Agent

↓

Skill Selection

↓

MCP Tool

↓

DuckDB Archive

↓

Response

---

# Agent Responsibilities

The agent must:

1. Receive user query
2. Determine intent
3. Select skill
4. Execute MCP tool
5. Format response
6. Return evidence

The agent must never fabricate historical information.

---

# Skill Routing

## Show Lookup

Questions:

- What was played on 1977/05/08?
- Show me Cornell 1977.
- What was the setlist at Veneta?

Selected Skill:

show-lookup

MCP Tool:

find_show

---

## Song History

Questions:

- When was Dark Star first played?
- When was Dark Star last played?
- How many times was Althea played?

Selected Skill:

song-history

MCP Tool:

find_song

---

## Venue Analysis

Questions:

- Tell me about Winterland.
- Which venue hosted the most shows?

Selected Skill:

venue-analysis

MCP Tool:

find_venue

---

## Tour Analysis

Questions:

- Summarize Europe 72.
- Tell me about Spring 1977.

Selected Skill:

tour-analysis

MCP Tool:

find_tour

---

## Setlist Similarity

Questions:

- Find shows similar to Cornell.
- Compare Cornell and Veneta.

Selected Skill:

setlist-similarity

MCP Tool:

compare_setlists

---

# Response Structure

All responses should contain:

1. Answer
2. Supporting Evidence
3. Historical Context

Example:

Question:

When was Dark Star last played before Cornell 1977?

Answer:

1974/10/18

Supporting Evidence:

Venue
Location
Show Date

Historical Context:

Dark Star entered a performance hiatus following this period.

---

# Error Handling

If no matching data exists:

Return:

- skill selected
- reason no data was found

Do not hallucinate results.

---

# Observability

The agent should log:

- user query
- selected skill
- selected MCP tool
- execution time

---

# Success Criteria

The orchestration layer is complete when:

- show-lookup routes correctly
- song-history routes correctly
- venue-analysis routes correctly
- tour-analysis routes correctly
- setlist-similarity routes correctly

and all responses are generated using MCP tools only.