# AGENTS.md

# DeadBase Agent Project Instructions

## Project Identity

DeadBase is a spec-driven historical research system for exploring Grateful Dead concert history.

The system is built using:

- Spec-Driven Development (SDD)
- Agent Skills
- MCP
- Evaluation-Driven Development (EDD)

The specification is the source of truth.

All implementation must conform to:

```text
specs/project_spec.md
```

If implementation and specification conflict:

THE SPECIFICATION WINS.

---

# Mission

Build an evidence-based historical research agent capable of answering questions about:

- Shows
- Songs
- Venues
- Tours
- Eras
- Setlists

The system must prioritize:

- Historical accuracy
- Traceability
- Evidence
- Reproducibility

The system must never invent historical facts.

---

# Development Philosophy

Follow Spec-Driven Development.

Workflow:

```text
Specification
→ Evaluation
→ Skill
→ MCP Tool
→ Agent
→ UI
```

Never skip directly from idea to implementation.

Every feature must begin with a specification.

Every feature must have evaluation coverage.

---

# Architectural Principles

## Single Agent

DeadBase uses:

```text
One Agent
Many Skills
```

Do not create multiple autonomous agents unless explicitly required.

Skills are preferred over agent proliferation.

---

## Read Only Architecture

The system is a historical archive.

The system must never:

- Modify source YAML files
- Delete records
- Update records
- Write to archival datasets

All archive access is read-only.

---

## Evidence First

Responses must be grounded in source data.

Preferred response format:

1. Answer
2. Supporting Evidence
3. Historical Context

Historical claims should be explainable.

---

# Skills

Current skill catalog:

- show-lookup
- song-history
- venue-analysis
- tour-analysis
- setlist-similarity
- song-evolution

When implementing new functionality:

1. Determine if an existing skill should be extended.
2. Only create a new skill when behavior is fundamentally different.

Avoid skill duplication.

---

# MCP Guidelines

MCP provides access to archive data.

Current MCP tools:

- find_show
- find_song
- find_venue
- find_tour
- compare_setlists

MCP tools should:

- be deterministic
- be read-only
- return structured output

MCP tools should not generate narratives.

Narrative generation belongs to the agent layer.

---

# Data Guidelines

Primary source:

```text
data/yaml/
```

Source YAML files are authoritative.

Processed assets may be generated under:

```text
data/processed/
```

Generated assets must never overwrite source data.

---

# Evaluation Requirements

Every skill requires evaluation cases.

Evaluation files belong in:

```text
evals/
```

Minimum requirements:

- positive case
- negative case
- edge case

No feature is complete without evaluation coverage.

---

# Testing Requirements

All code must be testable.

Tests belong in:

```text
tests/
```

New functionality should include:

- unit tests
- tool tests
- skill tests where applicable

---

# Logging

The system should log:

- selected skill
- tool usage
- execution time
- evaluation results

Logging should aid debugging and observability.

---

# Security

The system must:

- remain read-only
- avoid arbitrary code execution
- avoid unrestricted filesystem access
- avoid hardcoded secrets

No credentials should be committed.

Use:

```text
.env
```

for local configuration.

---

# Documentation

Documentation is part of the product.

Whenever architecture changes:

Update:

```text
docs/architecture.md
```

Whenever functionality changes:

Update:

```text
README.md
```

Whenever behavior changes:

Update relevant specifications.

---

# Code Style

Priorities:

1. Correctness
2. Clarity
3. Maintainability

Avoid:

- premature optimization
- unnecessary abstractions
- hidden side effects

Prefer explicit code over clever code.

---

# Definition of Done

A feature is complete only when:

- specification exists
- evaluations exist
- tests pass
- documentation updated
- implementation complete

Incomplete features must not be marked complete.

---

# DeadBase Principles

DeadBase is a historical research system.

DeadBase is not a chatbot.

DeadBase is not a content generator.

DeadBase is not a recommendation engine.

DeadBase is an evidence-based archival research agent.

Historical accuracy is more important than creativity.