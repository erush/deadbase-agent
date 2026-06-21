# Indexing Pipeline Specification

## Objective

Transform raw Grateful Dead YAML archives into a normalized research catalog that can be accessed through MCP tools.

The indexing pipeline is the foundation of DeadBase.

All research, retrieval, analysis, and agent behavior depend on this catalog.

---

# Inputs

## Show Archive

Source:

data/yaml/

Structure:

YYYY/MM/DD
→ show metadata
→ venue metadata
→ set information
→ song performances

Example fields:

- uuid
- venue
- city
- state
- country
- sets

---

## Song Catalog

Source:

data/yaml/

Structure:

Song Name
→ Song UUID

Example:

Dark Star
→ 0ead60da-6abf-4589-98dd-e56faca0c767

This dataset represents the authoritative song dimension.

---

# Output

Target:

data/duckdb/deadbase.duckdb

The database must be fully rebuildable from source YAML.

---

# Warehouse Tables

## shows

One row per performance date.

Columns:

- show_uuid
- show_date
- venue
- city
- state
- country

Primary Key:

show_uuid

---

## songs

One row per unique song.

Columns:

- song_uuid
- song_name

Primary Key:

song_uuid

---

## performances

One row per song performance.

Columns:

- show_uuid
- song_uuid
- song_name
- set_number
- song_position
- segued

Relationships:

show_uuid → shows

song_uuid → songs

---

## venues

One row per venue.

Columns:

- venue
- city
- state
- country

---

# Pipeline Stages

## Stage 1

Load all YAML archives.

Validate structure.

Reject malformed records.

---

## Stage 2

Extract show metadata.

Populate:

shows

---

## Stage 3

Extract song catalog.

Populate:

songs

---

## Stage 4

Extract setlists.

Generate performance records.

Populate:

performances

---

## Stage 5

Generate venue dimension.

Populate:

venues

---

# Data Quality Rules

Every show must contain:

- show_uuid
- show_date

Every song must contain:

- song_uuid
- song_name

Performance rows require:

- show_uuid
- song_name

Empty setlists are valid.

Historical records with incomplete metadata should still be indexed.

---

# Rebuild Requirements

The pipeline must be idempotent.

The database must be reproducible from source YAML.

No manual updates are permitted.

All derived tables must be regenerated through the pipeline.

---

# Success Criteria

The pipeline is complete when:

- all YAML files load
- all shows are indexed
- all songs are indexed
- all performances are indexed
- all venues are indexed
- deadbase.duckdb is generated

The resulting catalog must support:

- show lookup
- song history
- venue analysis
- tour analysis
- setlist similarity