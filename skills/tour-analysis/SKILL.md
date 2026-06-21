---
name: tour-analysis
description: |
  Analyze Grateful Dead tours and historical eras.

  Use when the user asks:
  - tour summaries
  - tour statistics
  - era analysis
  - historical tour comparisons

  Do NOT use for:
  - venue profiles
  - individual songs
  - single show lookup
---

# Purpose

Provide tour-level historical analysis.

# MCP Tools

- find_tour

# Procedure

1. Identify tour.
2. Call find_tour.
3. Retrieve tour metadata.
4. Analyze tour characteristics.
5. Generate summary.

# Output Requirements

Return:

- tour
- date range
- show count
- locations
- historical significance