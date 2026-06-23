# DeadBase: A Multi-Agent Historical Intelligence Platform

## Overview

DeadBase is a multi-agent historical intelligence system built on top of the Grateful Dead performance archive.

Traditional archive tools focus on retrieval:

- Find a show
- Find a song
- Find a venue
- Find a date

DeadBase explores a different question:

Can analytical models and AI agents investigate historical performances and explain why they matter?

The project combines analytics engineering, feature generation, historical modeling, and agent orchestration to transform archive records into explainable historical investigations.

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

## Solution

DeadBase converts raw archive records into a layered intelligence system.

Archive data is transformed into analytical models describing:

- Song evolution
- Venue history
- Show structure
- Historical significance
- Similarity relationships
- Performance archetypes
- Performance clusters

Specialized agents then use these analytical models to perform historical investigations.

---

## Architecture

Archive Data

→ DuckDB Warehouse

→ Analytics Layer

→ Skill Layer

→ Agent Layer

→ Research Synthesis

---

## Analytics Layer

The analytics layer transforms archive records into structured historical signals.

### Song Profiles

Captures:

- Performance count
- First appearance
- Final appearance
- Peak year
- Active years

### Song Evolution

Models song careers using:

- Historical tiers
- Career patterns
- Longevity scores
- Peak concentration

### Show DNA

Captures structural characteristics including:

- Show length
- Set count
- Segue ratio
- Repertoire structure

### Venue Profiles

Models venue history using:

- Show count
- Active years
- Average show length
- Average segue ratio

### Venue Rankings

Ranks venues by:

- Historical importance
- Rarity
- Archive footprint

### Show Embeddings

Transforms performances into analytical feature vectors.

Features include:

- Era
- Show length
- Set complexity
- Segue behavior
- Venue importance
- Historical significance

### Historical Significance Rankings

Ranks every performance in the archive using measurable historical signals.

Outputs include:

- Historian score
- Historian rank
- Historian percentile

### Show Archetypes

Classifies performances into categories such as:

- Marathon Show
- High Segue Show
- Venue Landmark Show
- Rare Song Show
- Complex Set Structure

### Show Clusters

Groups performances into families based on shared characteristics and historical patterns.

---

## Agent Architecture

DeadBase uses specialized agents that investigate different aspects of the archive.

### Song Agent

Provides historical context for songs including frequency, lifecycle, and repertoire evolution.

### Venue Agent

Investigates venue history, rarity, and historical significance.

### Similarity Agent

Identifies neighboring performances using repertoire overlap and analytical embeddings.

### Song Evolution Agent

Explains how songs changed throughout the band's history.

### Historian Agent

Evaluates performances using historical rankings, archetypes, and archive signals.

### Research Agent

Coordinates multiple agents and synthesizes findings into a unified historical investigation.

The Research Agent represents the primary intelligence layer of the system.

---

## Cornell Investigation Example

To demonstrate the system, I selected one of the most famous performances in Grateful Dead history:

Cornell University — May 8, 1977.

Rather than asking whether the show is famous, DeadBase asks why.

The investigation combined:

- Historian Agent
- Similarity Agent
- Venue Agent
- Song Agent

The Historian Agent determined that Cornell ranks in the 79th percentile of archive performances and belongs to the Complex Set Structure archetype.

The Similarity Agent identified several Spring 1977 performances with highly overlapping repertoires.

The Venue Agent revealed that Barton Hall hosted only three Grateful Dead performances.

The Song Agent examined the historical context of key repertoire selections including Estimated Prophet, Saint Stephen, Morning Dew, and Not Fade Away.

The resulting synthesis suggested that Cornell's historical reputation is not fully explained by setlist uniqueness.

Instead, the evidence points toward a combination of:

- Spring 1977 repertoire strength
- Venue mythology
- Tape circulation
- Listener consensus
- Performance quality
- Long-term cultural memory

This investigation demonstrates how analytical modeling and agent orchestration can be combined to produce explainable historical research.

---

## Lessons Learned

The most important insight from this project was that analytics and agents become significantly more useful when combined.

Analytical models create structured historical signals.

Agents provide investigation, interpretation, and synthesis.

Together they enable explainable historical reasoning rather than simple retrieval.

Another key lesson was the importance of separating measurable archive evidence from cultural reputation.

DeadBase intentionally distinguishes between what the data supports and what historical memory preserves.

---

## Future Work

Potential future extensions include:

- Archive review intelligence
- Fan sentiment modeling
- Era transition detection
- Tour-level intelligence
- Community narrative extraction
- Historical recommendation systems
- Interactive research interfaces
- Cross-domain applications to sports intelligence systems

---

## Conclusion

DeadBase demonstrates how analytics engineering and multi-agent reasoning can transform a large cultural archive into an explorable historical intelligence system.

Instead of asking:

"Find me a show."

DeadBase attempts to answer:

"Help me understand why this show mattered."