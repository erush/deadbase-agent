# Agent Orchestration Specification

## Purpose

The Agent Orchestration layer coordinates the complete execution lifecycle of a DeadBase historical investigation.

It transforms a user's research question into a deterministic, evidence-based historical report using the Planning Agent, Investigation Session, Agent Skills, MCP tools, and Synthesis Agent.

The orchestration layer is responsible for execution.

Historical reasoning belongs to specialist Agent Skills.

---

# Objectives

The orchestration layer shall:

- receive research questions
- create an Investigation Session
- invoke the Planning Agent
- select the appropriate Agent Skills
- coordinate MCP tool execution
- collect structured evidence
- invoke the Synthesis Agent
- return a fully explainable historical report

---

# Runtime Architecture

Every investigation follows the same execution pipeline.

```text
User Question
        ↓
Planning Agent
        ↓
Investigation Session
        ↓
Agent Skill Selection
        ↓
MCP Tool Invocation
        ↓
Evidence Collection
        ↓
Synthesis Agent
        ↓
Historical Investigation Report
```

---

# Component Responsibilities

## Planning Agent

Responsible for:

- understanding user intent
- selecting Agent Skills
- initiating investigations
- managing execution flow

The Planning Agent never performs historical analysis.

---

## Investigation Session

Responsible for:

- shared execution context
- execution trace
- selected skills
- tool invocations
- collected evidence
- final report

Exactly one Investigation Session exists per investigation.

---

## Agent Skills

Each Agent Skill performs one specialized historical task.

Current Agent Skills include:

- show-lookup
- show-intelligence
- song-history
- song-evolution
- venue-analysis
- tour-analysis
- setlist-similarity

Agent Skills never route investigations.

Agent Skills never synthesize reports.

---

## MCP Tool Layer

Agent Skills access historical data exclusively through MCP tools.

Example tools include:

- deadbase_show_lookup
- deadbase_song_history
- deadbase_song_evolution
- deadbase_venue_analysis
- deadbase_setlist_similarity
- deadbase_tour_analysis

MCP tools return structured historical evidence.

---

## Knowledge Layer

MCP tools retrieve information from the analytical warehouse.

The warehouse consists of:

- canonical archive tables
- analytical feature tables
- derived historical intelligence

The orchestration layer never queries DuckDB directly.

---

## Synthesis Agent

The Synthesis Agent receives structured evidence collected during the investigation.

Responsibilities include:

- integrating evidence
- resolving findings
- generating the final historical narrative

The Synthesis Agent never performs additional database queries.

---

# Skill Selection

The Planning Agent determines which Agent Skills should execute.

Only required skills participate in an investigation.

Example:

Question:

Why is Cornell 5/8/77 considered legendary?

Selected Agent Skills:

- show-lookup
- show-intelligence
- venue-analysis
- setlist-similarity
- song-history
- song-evolution

Not every investigation requires every Agent Skill.

---

# Investigation Flow

Each investigation proceeds through these stages.

## Stage 1

Receive research question.

## Stage 2

Create Investigation Session.

## Stage 3

Determine investigation intent.

## Stage 4

Select Agent Skills.

## Stage 5

Invoke MCP tools.

## Stage 6

Collect structured evidence.

## Stage 7

Launch Synthesis Agent.

## Stage 8

Generate Historical Investigation Report.

---

# Observability

Every investigation records:

- original question
- selected Agent Skills
- MCP tool invocations
- execution trace
- evidence collected
- investigation duration
- final report

This information supports debugging, evaluation, and explainability.

---

# Determinism

The orchestration layer is deterministic.

The same question executed against the same warehouse should produce:

- identical Agent Skill selection
- identical MCP tool usage
- identical execution trace
- identical evidence
- identical synthesized report

---

# Security

The orchestration layer never:

- modifies archival data
- executes arbitrary code
- bypasses MCP tools
- accesses source YAML directly

Historical investigations are strictly read-only.

---

# Evaluation

Successful orchestration demonstrates:

- correct Planning Agent decisions
- correct Agent Skill selection
- correct MCP tool usage
- complete evidence collection
- successful synthesis
- reproducible execution

---

# Relationship to the DeadBase Architecture

The orchestration layer connects every major subsystem.

```text
Project Specification
        ↓
Planning Agent
        ↓
Investigation Session
        ↓
Agent Orchestration
        ↓
Agent Skills
        ↓
MCP Tool Layer
        ↓
Knowledge Layer
        ↓
Analytical Warehouse
        ↓
Historical Archive
```

The orchestration layer is the runtime backbone of the DeadBase historical intelligence platform.