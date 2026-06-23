# DeadBase: Multi-Agent Historical Intelligence for the Grateful Dead Archive

## Overview

DeadBase is a multi-agent historical intelligence platform built on top of the Grateful Dead performance archive.

Traditional archive tools focus on retrieval:

- Find a show
- Find a song
- Find a venue
- Find a date

DeadBase takes a different approach.

The system attempts to discover historical structure within the archive through analytics engineering, feature generation, and agent-based investigation.

Rather than simply retrieving information, DeadBase attempts to answer questions such as:

- Why is a show historically important?
- What family of shows does it belong to?
- Which songs defined an era?
- How unique was a performance?
- What explains the reputation of a legendary show?

---

## Kaggle AI Agents Capstone

DeadBase was developed as a submission for the Kaggle Vibe Coding Agents Capstone.

The project demonstrates how analytics engineering, feature generation, and multi-agent reasoning can be combined to investigate large historical archives.

Rather than functioning as a traditional search tool, DeadBase uses specialized agents to perform explainable historical investigations.

---

## Problem

The Grateful Dead archive contains:

- 1,822 unique performances
- 35,000+ song performances
- 445 unique songs
- 434 venues

While the archive is rich with information, historical investigation remains difficult.

Researchers often rely on:

- Manual searches
- Community reputation
- Anecdotal evidence
- Personal knowledge

Most archive tools answer:

"What happened?"

DeadBase attempts to answer:

"Why did it matter?"

---

## Quick Start

Run the primary demonstration:

```bash
python -m scripts.cornell_investigation_demo
```

This performs a complete multi-agent investigation of the Grateful Dead's legendary Cornell University performance on May 8, 1977.

The investigation combines:

- Historian Agent
- Venue Agent
- Song Agent
- Similarity Agent
- Research Agent
- Synthesis Agent

to generate an evidence-based historical assessment.

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

### Data Warehouse

DuckDB powers the archive warehouse.

Core entities:

- shows
- performances
- songs
- venues

The public repository intentionally excludes the raw archive data and generated DuckDB warehouse.

---

### Analytics Layer

DeadBase generates analytical datasets that transform raw archive records into historical intelligence.

#### song_profile

Song lifecycle information.

Metrics include:

- performance count
- first appearance
- final appearance
- peak year
- active years

#### song_evolution

Models song careers.

Metrics include:

- historical tier
- career pattern
- longevity score
- peak concentration

Examples:

- Cornerstone Songs
- Core Repertoire
- Important Rotation
- Rare Songs

#### show_dna

Structural characteristics of every performance.

Metrics include:

- show length
- set count
- segue ratio
- repertoire structure

#### venue_profile

Historical venue intelligence.

Metrics include:

- show count
- active years
- average show length
- average segue ratio

#### venue_rankings

Ranks venues by:

- importance
- rarity
- historical footprint

#### show_embeddings

Transforms shows into analytical feature vectors.

Features include:

- era
- show length
- set complexity
- segue behavior
- venue importance
- historical significance

#### show_historical_significance

Ranks every show in the archive.

Produces:

- historian score
- historian rank
- historian percentile

#### show_archetypes

Classifies performances into historical categories.

Examples:

- Marathon Show
- High Segue Show
- Venue Landmark Show
- Rare Song Show
- Complex Set Structure

#### show_clusters

Groups performances into broader analytical families using machine learning and shared historical characteristics.

---

## Agent Layer

### Similarity Agent

Identifies neighboring performances based on repertoire overlap and analytical similarity.

Example:

"What shows are most similar to Cornell 1977?"

### Venue Agent

Investigates venue history and historical significance.

Example:

"What role did Barton Hall play in Grateful Dead history?"

### Song Agent

Provides song-level archive intelligence.

Example:

"When did Saint Stephen first appear?"

### Song Evolution Agent

Models song lifecycles across the archive.

Example:

"How did Dark Star evolve across the band's career?"

### Historian Agent

Combines multiple analytical signals into a historical profile.

Example:

"Why was Cornell 1977 important?"

### Research Agent

Performs multi-agent investigations.

Combines:

- historian analysis
- venue intelligence
- song intelligence
- similarity analysis
- analytical rankings
- research synthesis

to generate evidence-based historical narratives.

---

## Example Investigation

### Cornell — 1977/05/08

DeadBase investigated Cornell using:

- Historical significance rankings
- Show archetypes
- Venue analysis
- Song evolution
- Similarity analysis

Findings:

- Cornell ranks in the 79th percentile of archive performances.
- The show belongs to the Complex Set Structure archetype.
- Barton Hall hosted only three Grateful Dead performances.
- Several Spring 1977 shows display highly similar repertoire.
- The archive does not support the claim that Cornell's significance is driven solely by setlist uniqueness.

DeadBase suggests that Cornell's reputation emerges from a combination of:

- strong Spring 1977 repertoire
- venue mythology
- tape circulation
- listener consensus
- performance quality
- long-term cultural memory

---

## Results

DeadBase currently models:

- 1,822 performances
- 35,000+ song performances
- 445 songs
- 434 venues

Generated analytical datasets include:

- song_profile
- song_evolution
- show_dna
- venue_profile
- venue_rankings
- show_embeddings
- show_historical_significance
- show_archetypes
- show_clusters

The platform successfully performs multi-agent investigations that combine historical rankings, venue intelligence, repertoire analysis, archetype classification, and similarity modeling into explainable research outputs.

---

## Repository Structure

```text
agents/            Specialized research agents
analytics/         Analytics builders and feature generation
docs/              Documentation and submission materials
evals/             Evaluation datasets
mcp_server/        MCP server implementation
scripts/           Demos and test scripts
skill_executors/   Skill execution layer
skills/            Skill definitions
specs/             Project specifications
tests/             Test suite
tools/             Archive query tools
```

---

## Data Boundary

The public repository intentionally excludes:

- raw YAML archive files
- processed archive assets
- DuckDB warehouse files

The repository publishes the analytics and agent framework while protecting the underlying archive assets.

---

## Key Insight

DeadBase separates:

### Cultural Reputation

What fans believe is historically important.

### Archive Evidence

What measurable historical signals support.

This distinction allows researchers to investigate where the archive supports the legend and where the legend extends beyond measurable structure.

---

## Future Work

Potential future research directions include:

- Archive.org review analysis
- Fan sentiment modeling
- Tape circulation intelligence
- Era transition detection
- Song sequence modeling
- Advanced clustering
- Venue lineage analysis
- Community narrative extraction
- Historical recommendation systems
- Interactive research interfaces
- Cross-domain applications to sports intelligence systems

---

## Technology

- Python
- DuckDB
- Pandas
- Scikit-Learn
- Multi-Agent Architecture
- Historical Analytics
- Agent Orchestration
- Research Synthesis

---

## Documentation

Additional project documentation:

- docs/architecture.md
- docs/demo_script.md
- docs/deployment.md
- docs/evaluation.md
- docs/kaggle_submission.md
- docs/rubric_checklist.md

---

## Conclusion

DeadBase demonstrates how analytics engineering and agent-based reasoning can transform a large cultural archive into an explorable historical intelligence system.

Instead of asking:

"Find me a show."

DeadBase attempts to answer:

"Help me understand why this show mattered."