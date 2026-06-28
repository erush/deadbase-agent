# Investigation Session Specification

## Purpose

The Investigation Session represents the complete execution state of a single historical investigation.

It provides shared context between the Planning Agent, Agent Skills, MCP tools, and the Synthesis Agent.

Every user investigation creates exactly one Investigation Session.

---

# Objectives

The Investigation Session is responsible for:

- preserving execution context
- recording planning decisions
- tracking MCP tool usage
- storing collected evidence
- maintaining execution trace logs
- preserving the final historical report

The Investigation Session never performs reasoning.

Reasoning belongs to the Planning Agent and specialist Agent Skills.

---

# Lifecycle

An Investigation Session exists only for the duration of a single investigation.

```text
User Question
        ↓
Create Investigation Session
        ↓
Planning Agent
        ↓
Agent Skill Execution
        ↓
Evidence Collection
        ↓
Synthesis Agent
        ↓
Historical Report
        ↓
Session Complete
```

Once the investigation finishes, the session becomes immutable.

---

# Session Contents

Every Investigation Session stores:

- research question
- investigation timestamp
- selected Agent Skills
- MCP tool invocations
- structured evidence
- execution trace
- metadata
- synthesized report

---

# Context Management

The Investigation Session serves as the shared context passed between every component of the system.

Context includes:

- current investigation
- accumulated evidence
- completed tool calls
- execution metadata

No Agent Skill maintains independent investigation state.

---

# Agent Responsibilities

## Planning Agent

Responsible for:

- creating the Investigation Session
- selecting Agent Skills
- recording planning decisions

---

## Agent Skills

Responsible for:

- executing specialized historical analysis
- collecting structured evidence
- updating the Investigation Session

Agent Skills never modify historical archives.

---

## MCP Tools

Responsible for:

- retrieving structured historical data
- returning deterministic results

MCP tools record every invocation within the Investigation Session.

---

## Synthesis Agent

Responsible for:

- consuming collected evidence
- generating the final historical narrative

The Synthesis Agent writes the completed report back into the Investigation Session.

---

# Execution Trace

The Investigation Session maintains an execution trace.

Example:

```text
Investigation started

Planning complete

Selected Skills

show-lookup

venue-analysis

song-history

Calling MCP Tool

deadbase_show_lookup

Evidence collected

Calling MCP Tool

deadbase_song_history

Evidence collected

Launching Synthesis Agent

Historical report generated

Investigation complete
```

The execution trace supports observability and debugging.

---

# Evidence Model

Evidence is stored as structured objects.

Each evidence item includes:

- originating Agent Skill
- supporting data
- execution metadata

Evidence remains immutable once recorded.

---

# Determinism

The Investigation Session must preserve deterministic execution.

The same investigation executed against the same warehouse should produce:

- identical Agent Skill selection
- identical MCP tool invocations
- identical execution trace
- identical historical report

---

# Security

The Investigation Session never modifies:

- source YAML
- DuckDB warehouse
- generated analytical assets

All investigations are read-only.

---

# Success Criteria

A valid Investigation Session:

- is created by the Planning Agent
- persists throughout execution
- records Agent Skill selection
- records MCP tool invocations
- stores structured evidence
- maintains execution trace
- stores the synthesized historical report

The Investigation Session is the authoritative execution record for every historical investigation.