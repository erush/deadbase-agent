---
name: setlist-similarity
description: |
  Compare Grateful Dead shows and setlists.

  Use when the user asks:
  - similar shows
  - setlist comparisons
  - comparable performances
  - shared song analysis

  Do NOT use for:
  - venue history
  - tour summaries
  - song evolution
---

# Purpose

Measure similarity between shows and setlists.

# MCP Tools

- compare_setlists

# Procedure

1. Identify comparison targets.
2. Call compare_setlists.
3. Retrieve similarity metrics.
4. Identify common songs.
5. Summarize results.

# Output Requirements

Return:

- compared shows
- similarity score
- shared songs
- differences