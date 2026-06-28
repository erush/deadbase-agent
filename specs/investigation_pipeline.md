# Planning Agent Specification

## Purpose

The Planning Agent is the primary orchestrator of the DeadBase historical intelligence platform.

It is responsible for transforming a user's research question into a deterministic, explainable historical investigation.

The Planning Agent does not perform historical analysis.

Its responsibility is orchestration.

---

# Responsibilities

The Planning Agent shall:

- receive the user question
- create an Investigation Session
- determine the investigation intent
- select the appropriate Agent Skills
- invoke MCP tools
- collect structured evidence
- launch the Synthesis Agent
- return the final historical report

---

# Investigation Lifecycle

Every investigation follows the same execution pipeline.

```
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

# Inputs

The Planning Agent accepts:

- Natural language questions

Examples:

- Why is Cornell 5/8/77 legendary?
- Tell me about Europe '72.
- How many times was Scarlet Begonias played?
- What happened on 1977/05/08?

---

# Investigation Session

Every investigation creates exactly one Investigation Session.

The Investigation Session records:

- original question
- selected Agent Skills
- MCP tool invocations
- collected evidence
- execution trace
- final synthesized report

The Investigation Session is immutable with respect to archival data.

---

# Skill Selection

The Planning Agent selects Agent Skills using the Skill Registry.

Current skills include:

- show-lookup
- show-intelligence
- song-history
- song-evolution
- venue-analysis
- tour-analysis
- setlist-similarity

Only the required skills should execute.

---

# MCP Integration

The Planning Agent never queries DuckDB directly.

Instead it invokes MCP tools.

Examples:

- deadbase_show_lookup
- deadbase_song_history
- deadbase_venue_analysis
- deadbase_tour_analysis
- deadbase_setlist_similarity
- deadbase_song_evolution

---

# Evidence Collection

Each Agent Skill returns structured evidence.

Evidence must include:

- originating skill
- supporting data
- historical findings

Evidence is accumulated inside the Investigation Session.

---

# Synthesis

Once all evidence has been collected, the Planning Agent invokes the Synthesis Agent.

The Synthesis Agent receives only structured evidence.

It produces:

- final narrative
- historical interpretation
- evidence-backed conclusions

---

# Observability

The Planning Agent records an execution trace.

Example:

```
Investigation started

Planning complete

Selected Skills

show-lookup

venue-analysis

song-history

Calling MCP Tool

deadbase_show_lookup

Evidence received

Calling MCP Tool

deadbase_song_history

Evidence received

Launching synthesis

Historical report complete
```

---

# Determinism

The Planning Agent must produce deterministic investigations.

The same question against the same warehouse should produce the same investigation workflow.

---

# Security

The Planning Agent never modifies historical records.

All archive access is read-only.

Only MCP tools may access the warehouse.

---

# Evaluation

Evaluation verifies:

- correct skill selection
- correct MCP tool invocation
- successful evidence collection
- successful synthesis
- reproducible execution trace