# Indexing Pipeline Specification

## Purpose

The Indexing Pipeline transforms raw Grateful Dead archival records into a structured historical knowledge base that powers the DeadBase multi-agent research system.

The pipeline is deterministic, reproducible, and fully rebuildable from source archives.

The warehouse produced by this pipeline serves as the authoritative knowledge layer accessed through MCP tools during historical investigations.

---

# Objectives

The Indexing Pipeline is responsible for:

- Loading historical YAML archives
- Validating archival integrity
- Building the canonical DuckDB warehouse
- Generating analytical features
- Producing agent-ready knowledge assets
- Supporting deterministic historical investigations

The pipeline never generates narratives.

Narrative generation belongs to the Synthesis Agent.

---

# Data Flow

Every historical record follows the same lifecycle.

```text
Historical YAML Archive
            ↓
Archive Validation
            ↓
Canonical Warehouse
            ↓
Analytical Feature Engineering
            ↓
Knowledge Layer
            ↓
MCP Tool Layer
            ↓
Planning Agent
            ↓
Historical Investigation
```

---

# Source Data

Primary archive:

```text
data/yaml/
```

Contents include:

- Shows
- Songs
- Venues
- Performances
- Tours

These files represent the authoritative historical record.

---

# Stage 1 — Archive Validation

Validate every YAML document before loading.

Checks include:

- required fields
- valid identifiers
- valid dates
- structural integrity

Malformed records should be rejected without affecting valid records.

---

# Stage 2 — Canonical Warehouse

Build the normalized DuckDB warehouse.

Primary tables:

- shows
- songs
- performances
- venues

The warehouse is the system of record used throughout DeadBase.

---

# Stage 3 — Analytical Feature Engineering

Generate derived analytical datasets used by Agent Skills.

Examples include:

- show_profiles
- show_embeddings
- show_clusters
- show_archetypes
- show_historical_significance
- venue_profiles
- venue_rankings
- song_profiles
- song_evolution

These datasets are deterministic transformations of the canonical warehouse.

No historical facts are invented during feature generation.

---

# Stage 4 — Knowledge Layer

The analytical datasets form the structured knowledge layer consumed by the DeadBase agent system.

This layer exposes historical intelligence rather than raw database rows.

Agent Skills operate against this knowledge layer.

---

# Stage 5 — MCP Tool Layer

The Planning Agent never queries DuckDB directly.

Instead, historical data is accessed through deterministic MCP tools.

Example tools include:

- deadbase_show_lookup
- deadbase_song_history
- deadbase_song_evolution
- deadbase_venue_analysis
- deadbase_setlist_similarity
- deadbase_tour_analysis

MCP tools provide a standardized interface between the agent system and the warehouse.

---

# Stage 6 — Historical Investigation

During execution:

```text
Planning Agent
        ↓
Investigation Session
        ↓
Agent Skills
        ↓
MCP Tool Calls
        ↓
Evidence Collection
        ↓
Synthesis Agent
        ↓
Historical Investigation Report
```

The Indexing Pipeline supplies the structured evidence used throughout this workflow.

---

# Warehouse Requirements

The warehouse must be:

- deterministic
- reproducible
- read-only during investigations
- fully rebuildable from source YAML

Manual modification of warehouse data is prohibited.

---

# Data Quality

Every investigation depends on warehouse integrity.

Validation requirements include:

- unique show identifiers
- valid song identifiers
- valid relationships
- reproducible analytical features

Derived datasets must remain synchronized with the canonical warehouse.

---

# Security

The Indexing Pipeline:

- never modifies source YAML
- never overwrites archival history
- never accepts user-generated historical content

Source archives remain immutable.

---

# Success Criteria

The pipeline is complete when:

- all YAML archives validate successfully
- the canonical DuckDB warehouse is generated
- analytical feature tables are generated
- the knowledge layer is refreshed
- MCP tools return deterministic results
- Planning Agent investigations execute successfully against the rebuilt warehouse

---

# Relationship to the Agent Architecture

The Indexing Pipeline is responsible only for preparing historical knowledge.

It does not perform reasoning.

Reasoning begins when the Planning Agent creates an Investigation Session and launches a historical investigation using Agent Skills and MCP tools.