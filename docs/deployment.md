# DeadBase Deployment

## Overview

DeadBase is currently deployed as a local Python and DuckDB historical intelligence platform.

The system was built as a demonstration of analytics engineering, agent orchestration, and historical investigation workflows.

Rather than functioning as a traditional archive search tool, DeadBase combines analytical models and specialized agents to produce explainable historical investigations.

---

## Environment

Development Environment:

- Python 3.x
- DuckDB
- Pandas
- Scikit-Learn

Primary Components:

- Analytics Layer
- Skill Executors
- Agent Layer
- Research Synthesis Layer

---

## Installation

Clone the repository:

```bash
git clone https://github.com/erush/deadbase-agent.git

cd deadbase-agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running Demonstrations

### Cornell Historical Investigation

Primary end-to-end demonstration:

```bash
python -m scripts.cornell_investigation_demo
```

This executes a complete multi-agent investigation of Cornell University on May 8, 1977.

---

### Research Agent

```bash
python -m scripts.test_research_agent
```

Demonstrates orchestration across multiple analytical perspectives.

---

### Historian Agent

```bash
python -m scripts.test_historian_agent
```

Demonstrates historical ranking and significance analysis.

---

### Song Evolution Agent

```bash
python -m scripts.test_song_evolution_agent
```

Demonstrates lifecycle analysis of songs across the archive.

---

## Analytics Pipeline

DeadBase transforms archive records into analytical intelligence layers.

Current build pipeline:

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

---

## Data Boundary

The public repository intentionally excludes all archive assets.

Excluded content:

```text
data/yaml/
data/processed/
data/duckdb/
```

This includes:

- raw Grateful Dead archive records
- transformed datasets
- DuckDB warehouse files

The repository publishes the intelligence framework while protecting local archive assets.

---

## Repository Contents

The public repository includes:

- analytics builders
- agents
- skill executors
- tests
- evaluation assets
- documentation
- demo scripts

The repository is intended to demonstrate architecture, analytics engineering, and agent design rather than distribute archive data.

---

## Future Deployment Options

Potential future deployment targets include:

- FastAPI APIs
- MCP Servers
- Streamlit Applications
- React Research Interfaces
- Hosted Investigation Platforms

---

## Long-Term Vision

DeadBase serves as a reference implementation for a reusable intelligence architecture.

The same pattern can be applied to additional domains:

```text
Raw Data
    ↓
Warehouse
    ↓
Analytics
    ↓
Skills
    ↓
Agents
    ↓
Research Synthesis
```

Potential future applications include:

- WNBA Historical Intelligence
- MLB Historical Intelligence
- NASCAR Race Intelligence
- AEW Historical Intelligence
- Negro Leagues Historical Intelligence

DeadBase demonstrates the architecture using Grateful Dead performance history, but the framework is domain-independent.