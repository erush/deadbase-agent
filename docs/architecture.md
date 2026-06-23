# DeadBase Architecture

DeadBase is organized as a layered historical intelligence system.

## System Flow

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

## Warehouse Layer

Core entities:

- shows
- performances
- songs
- venues

The warehouse is local and excluded from the public repository.

## Analytics Layer

The analytics layer transforms archive records into reusable historical signals.

Analytics builders:

- analytics/build_song_profiles.py
- analytics/build_song_evolution.py
- analytics/build_show_dna.py
- analytics/build_show_embeddings.py
- analytics/build_show_historical_significance.py
- analytics/build_show_archetypes.py
- analytics/build_show_clusters.py
- analytics/build_venue_profiles.py
- analytics/build_venue_rankings.py

Generated analytical datasets:

- song_profile
- song_evolution
- show_dna
- venue_profile
- venue_rankings
- show_embeddings
- show_historical_significance
- show_archetypes
- show_clusters

## Skill Layer

Skill executors expose focused capabilities:

- show lookup
- song history
- song evolution
- venue profile
- setlist similarity
- show recommender
- show intelligence

## Agent Layer

DeadBase uses specialized agents that investigate different aspects of the archive.

Agents include:

- Song Agent
- Song Evolution Agent
- Venue Agent
- Similarity Agent
- Historian Agent
- Research Agent
- Synthesis Agent

## Research Layer

The Research Agent coordinates multiple analytical perspectives into a single historical investigation.

Example workflow:

```text
Cornell 1977
    ↓
Venue Analysis
    ↓
Song Context
    ↓
Similarity Analysis
    ↓
Historical Ranking
    ↓
Synthesis
```

## Data Boundary

The public repository contains:

- analytics code
- agent code
- skill executors
- documentation
- evaluation assets
- test scripts

The repository does not contain:

- raw YAML archive files
- processed archive assets
- DuckDB warehouse files

These assets remain local and are intentionally excluded from source control.
```
:::

### `docs/demo_script.md`

:::writing{variant="document" id="58124"}
# DeadBase Demo Script

## Objective

Demonstrate how DeadBase performs historical investigations using analytical models and multiple specialized agents.

## Main Demonstration

Run:

```bash
python -m scripts.cornell_investigation_demo
```

## Investigation Question

Why is Cornell University on May 8, 1977 considered historically significant?

## Workflow

The demo executes:

1. Research Agent
2. Historian Agent
3. Similarity Agent
4. Venue Agent
5. Song Agent
6. Synthesis Agent

## Analytical Evidence

The investigation uses:

- Historical significance rankings
- Show archetypes
- Venue intelligence
- Song evolution
- Similarity relationships

## Expected Output

The system generates a report containing:

- Location
- Historian Rank
- Historian Percentile
- Historian Score
- Archetype Classification
- Venue Context
- Similar Shows
- Song Context
- Historical Interpretation
- Research Synthesis

## Key Finding

Cornell 1977 is culturally legendary, but the archive suggests that its reputation cannot be explained by setlist uniqueness alone.

DeadBase separates:

- Cultural reputation
- Measurable archive evidence

and investigates where those perspectives overlap.

## Additional Demos

Research Agent:

```bash
python -m scripts.test_research_agent
```

Historian Agent:

```bash
python -m scripts.test_historian_agent
```

Song Evolution Agent:

```bash
python -m scripts.test_song_evolution_agent
```

Similarity Agent:

```bash
python -m scripts.test_show_recommender
```
```
:::

### `docs/deployment.md`

:::writing{variant="document" id="58125"}
# DeadBase Deployment

## Current Deployment Model

DeadBase currently operates as a local Python and DuckDB research platform.

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Primary Demo

Run:

```bash
python -m scripts.cornell_investigation_demo
```

## Supporting Demos

```bash
python -m scripts.test_research_agent

python -m scripts.test_historian_agent

python -m scripts.test_song_evolution_agent
```

## Data Requirements

The public repository intentionally excludes:

```text
data/yaml/
data/processed/
data/duckdb/
```

These assets contain archive source material and locally generated warehouse files.

The repository publishes the intelligence engine rather than the underlying archive assets.

## Analytics Rebuild Pipeline

When archive data is available locally, rebuild the analytics layer:

```bash
python analytics/build_song_profiles.py

python analytics/build_song_evolution.py

python analytics/build_show_dna.py

python analytics/build_venue_profiles.py

python analytics/build_venue_rankings.py

python analytics/build_show_embeddings.py

python analytics/build_show_historical_significance.py

python analytics/build_show_archetypes.py

python analytics/build_show_clusters.py
```

## Future Deployment Targets

Potential future deployment options include:

- FastAPI APIs
- React frontends
- Streamlit applications
- MCP servers
- Hosted research interfaces
- Multi-domain intelligence platforms

## Long-Term Vision

DeadBase serves as a reference implementation for a reusable historical intelligence architecture that can later be applied to:

- WNBA
- MLB
- NASCAR
- AEW
- Negro Leagues
- Additional historical archives
```
:::

### `docs/evaluation.md`

:::writing{variant="document" id="58126"}
# DeadBase Evaluation

## Evaluation Goal

DeadBase is evaluated as a historical intelligence system rather than a simple archive lookup tool.

The primary question is:

Can analytical models and agents combine multiple sources of evidence into useful historical investigations?

## Evaluation Assets

Evaluation files are located in:

```text
evals/
```

Current evaluation assets:

- show_lookup.json
- song_history.json
- venue_profile.json
- tour_analysis.json
- setlist_similarity.json

## Functional Testing

Test files are located in:

```text
tests/
```

Current tests include:

- show lookup
- song history
- venue profile
- tour analysis

## Demo Evaluation

Primary evaluation script:

```bash
python -m scripts.cornell_investigation_demo
```

The demonstration verifies that the system can:

- identify a show
- retrieve venue intelligence
- retrieve song intelligence
- discover similar performances
- apply historical rankings
- generate research synthesis

## Qualitative Evaluation Criteria

A strong investigation should:

- combine multiple analytical signals
- provide evidence-based reasoning
- distinguish reputation from evidence
- explain why a performance matters
- synthesize information across agents

## Current System Capabilities

DeadBase currently supports:

- archive lookup
- song history
- song evolution
- venue analysis
- similarity analysis
- historical significance ranking
- archetype classification
- performance clustering
- research synthesis

## Success Criteria

A successful output should move beyond retrieval and provide historical interpretation supported by measurable archive signals.

This distinction between retrieval and investigation is the central objective of the project.
```
:::