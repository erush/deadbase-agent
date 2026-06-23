# DeadBase: A Multi-Agent Historical Intelligence Platform

## Overview

DeadBase is a multi-agent historical intelligence system built on top of the Grateful Dead performance archive.

Traditional archive tools focus on retrieval:

- Find a show
- Find a song
- Find a venue
- Find a date

DeadBase explores a different question:

Can analytics and AI agents investigate historical performances and explain why they matter?

The project combines analytics engineering, feature generation, historical modeling, and agent orchestration to transform archive records into explainable historical investigations.

Developed for the Kaggle Vibe Coding Agents Capstone, DeadBase demonstrates how specialized agents can collaborate to investigate a large cultural archive.

---

## Problem

The Grateful Dead archive contains:

- 1,822 performances
- 35,000+ song performances
- 445 songs
- 434 venues

The archive contains an enormous amount of information, but historical investigation remains difficult.

Researchers often rely on:

- manual searching
- community reputation
- anecdotal evidence
- personal expertise

Most archive systems answer:

"What happened?"

DeadBase attempts to answer:

"Why did it matter?"

---

## Solution

DeadBase converts archive records into a layered intelligence system.

Raw archive data is transformed into analytical models describing:

- song evolution
- venue history
- show structure
- historical significance
- similarity relationships
- performance archetypes
- performance clusters

Specialized agents use these analytical models to investigate historical questions and generate explainable research outputs.

---

## Why Agents?

Historical investigation rarely depends on a single signal.

Understanding a performance requires combining:

- venue context
- repertoire context
- historical rankings
- song history
- performance similarity
- structural characteristics

DeadBase uses specialized agents because each analytical domain requires different reasoning and evidence.

The Research Agent coordinates these perspectives into a unified historical assessment.

---

## Architecture

```text
Archive Data
    ↓
DuckDB Warehouse
    ↓
Analytics Layer
    ↓
Skill Executors
    ↓
Agent Layer
    ↓
Research Synthesis
```

---

## Analytics Layer

DeadBase generates reusable intelligence layers from archive data.

### song_profile

Captures:

- performance count
- first appearance
- final appearance
- peak year
- active years

### song_evolution

Models song careers using:

- historical tiers
- career patterns
- longevity scores
- peak concentration

### show_dna

Captures:

- show length
- set count
- segue ratio
- repertoire structure

### venue_profile

Captures:

- show count
- active years
- average show length
- average segue ratio

### venue_rankings

Ranks venues by:

- historical importance
- rarity
- archive footprint

### show_embeddings

Transforms performances into analytical feature vectors.

Features include:

- era
- show length
- set complexity
- segue behavior
- venue importance
- historical significance

### show_historical_significance

Ranks every performance in the archive.

Outputs:

- historian score
- historian rank
- historian percentile

### show_archetypes

Classifies performances into categories such as:

- Marathon Show
- High Segue Show
- Venue Landmark Show
- Rare Song Show
- Complex Set Structure

### show_clusters

Groups performances into broader historical families based on shared characteristics.

---

## Agent Architecture

DeadBase uses specialized agents responsible for distinct historical research tasks.

### Song Agent

Provides song-level archive intelligence.

### Song Evolution Agent

Explains how songs evolved throughout the band's history.

### Venue Agent

Investigates venue history and significance.

### Similarity Agent

Identifies neighboring performances using repertoire overlap and analytical similarity.

### Historian Agent

Evaluates performances using rankings, archetypes, venue context, and historical signals.

### Research Agent

Coordinates multiple agents and synthesizes findings into a single historical investigation.

### Synthesis Agent

Transforms analytical findings into explainable historical narratives.

---

## Demonstration: Cornell 1977

The primary demonstration investigates one of the most famous performances in Grateful Dead history:

Cornell University — May 8, 1977.

The investigation combines:

- Historian Agent
- Similarity Agent
- Venue Agent
- Song Agent
- Research Agent
- Synthesis Agent

Key findings:

- Cornell ranks in the 79th percentile of archive performances.
- The performance belongs to the Complex Set Structure archetype.
- Barton Hall hosted only three Grateful Dead performances.
- Several Spring 1977 performances display highly similar repertoires.
- The archive does not support the claim that Cornell's importance is driven solely by setlist uniqueness.

The resulting synthesis suggests that Cornell's reputation emerges from a combination of:

- Spring 1977 repertoire strength
- venue mythology
- tape circulation
- listener consensus
- performance quality
- long-term cultural memory

This investigation demonstrates how analytical modeling and agent orchestration can be combined to generate explainable historical research.

---

## Results

DeadBase currently models:

- 1,822 performances
- 35,000+ song performances
- 445 songs
- 434 venues

Generated intelligence layers include:

- song_profile
- song_evolution
- show_dna
- venue_profile
- venue_rankings
- show_embeddings
- show_historical_significance
- show_archetypes
- show_clusters

The system successfully performs:

- historical investigations
- venue intelligence
- song evolution analysis
- performance similarity discovery
- research synthesis

---

## Repository Contents

The public repository includes:

- analytics pipelines
- agent implementations
- evaluation assets
- demonstration scripts
- architecture documentation
- deployment documentation
- Kaggle submission materials

The repository intentionally excludes:

- raw YAML archive assets
- processed archive assets
- generated DuckDB warehouses

---

## Lessons Learned

The most important lesson was that analytics and agents become significantly more useful when combined.

Analytics create structured historical signals.

Agents provide interpretation, investigation, comparison, and synthesis.

Together they enable explainable historical reasoning rather than simple retrieval.

Another important lesson was the distinction between cultural reputation and archive evidence.

DeadBase intentionally separates what the archive supports from what historical memory preserves.

---

## Future Work

Potential future extensions include:

- Archive.org review intelligence
- fan sentiment modeling
- era transition detection
- tour-level intelligence
- community narrative extraction
- historical recommendation systems
- interactive research interfaces
- cross-domain applications to sports intelligence systems

---

## Conclusion

DeadBase demonstrates how analytics engineering and multi-agent reasoning can transform a large cultural archive into an explorable historical intelligence system.

Instead of asking:

"Find me a show."

DeadBase attempts to answer:

"Help me understand why this show mattered."