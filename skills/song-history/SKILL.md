---
name: song-history
description: |
  Analyze historical Grateful Dead song performance history.

  Use when the user asks:
  - first performance
  - last performance
  - song frequency
  - performance gaps
  - song statistics

  Do NOT use for:
  - venue questions
  - tour summaries
  - show lookup
---

# Purpose

Research and analyze historical song performance patterns.

# MCP Tools

- find_song

# Procedure

1. Identify song name.
2. Call find_song.
3. Retrieve performance history.
4. Analyze timeline.
5. Generate evidence-based summary.

# Output Requirements

Return:

- song
- first performance
- last performance
- performance count
- historical context

Never fabricate performances.