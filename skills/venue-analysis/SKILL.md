---
name: venue-analysis
description: |
  Analyze Grateful Dead venue history.

  Use when the user asks:
  - venue statistics
  - venue history
  - venue trends
  - venue performance patterns

  Do NOT use for:
  - song history
  - tour summaries
  - specific show lookup
---

# Purpose

Analyze venue-level historical performance information.

# MCP Tools

- find_venue

# Procedure

1. Identify venue.
2. Call find_venue.
3. Retrieve venue history.
4. Calculate relevant statistics.
5. Return evidence-supported findings.

# Output Requirements

Return:

- venue
- show count
- years active
- notable trends
- historical context