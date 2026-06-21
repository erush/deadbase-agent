---
name: show-lookup
description: |
  Retrieve information about a specific Grateful Dead show.

  Use when the user asks:
  - what was played on a specific date
  - show setlists
  - show details
  - show locations
  - show venues

  Do NOT use for:
  - song history
  - venue analysis
  - tour analysis
---

# Purpose

Retrieve and summarize information about a specific Grateful Dead performance.

# Inputs

- Show date
- Venue name
- Location
- Show identifier

# MCP Tools

- find_show

# Procedure

1. Identify the show being requested.
2. Call find_show.
3. Retrieve show metadata.
4. Retrieve setlist information.
5. Return evidence-based results.

# Output Requirements

Return:

- date
- venue
- city
- state
- setlist
- source citation

Never invent songs or performances.