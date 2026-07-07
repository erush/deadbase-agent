# DeadBase: Explainable Multi-Agent Historical Intelligence

## What is DeadBase?

DeadBase is not a chatbot.

It is a specification-driven historical intelligence system that conducts structured investigations over the Grateful Dead archive.

Traditional archive tools retrieve records.

DeadBase plans investigations.

Specialized agents gather structured evidence from an analytical warehouse, synthesize findings, and produce explainable historical reports.

Although demonstrated using the Grateful Dead archive, the architecture is domain independent and designed for any historical intelligence problem.

---

## Why DeadBase?

Most AI applications retrieve documents and generate summaries.

DeadBase demonstrates a different approach.

Every research question becomes a structured historical investigation.

Instead of relying on a single LLM prompt, DeadBase:

- plans an investigation
- dynamically selects specialized skills
- orchestrates multiple research agents
- gathers structured evidence
- synthesizes explainable findings
- evaluates the completed investigation

Every investigation follows the same repeatable engineering workflow:

```text
Specification
      ↓
Planning
      ↓
Skill Selection
      ↓
Agent Orchestration
      ↓
Evidence Collection
      ↓
Historical Synthesis
      ↓
Evaluation
```

The result is a transparent, reproducible historical intelligence system rather than a traditional retrieval-based chatbot.

---

# Kaggle AI Agents Capstone

DeadBase was developed as a submission for the Kaggle AI Agents Capstone.

The project demonstrates an end-to-end AI agent architecture featuring:

- Planning Agent
- Investigation Session
- Dynamic Skill Planning
- Multi-Agent Orchestration
- MCP Tool Integration
- Evidence Collection
- Research Synthesis
- Automated Evaluation

The repository follows a specification-driven development approach in which every investigation is planned before execution, dynamically orchestrated through specialized agents, and evaluated upon completion rather than relying on hard-coded workflows.

---

## AI Agents Intensive Course Alignment

DeadBase was intentionally designed to demonstrate the core engineering principles taught throughout the Google/Kaggle 5-Day AI Agents Intensive.

Rather than showcasing isolated AI capabilities, the project integrates modern agent engineering concepts into a complete end-to-end historical intelligence platform.

| Google/Kaggle AI Agents Intensive | DeadBase Implementation |
|-----------------------------------|-------------------------|
| **Planning Before Execution** | Planning Agent creates an investigation plan before any research begins |
| **Multi-Agent Systems** | Specialized Research, Historian, Venue, Song, Similarity, Evolution, and Synthesis agents collaborate to solve complex investigations |
| **Dynamic Skills** | Skills are selected and dispatched dynamically based on the investigation objective rather than following hard-coded workflows |
| **Tool Use & Interoperability** | Model Context Protocol (MCP) exposes analytical capabilities as reusable agent tools |
| **Context Engineering** | Structured Investigation Sessions preserve execution state, evidence, and reasoning throughout the research lifecycle |
| **Explainability** | Every investigation records evidence, execution traces, intermediate findings, and synthesized conclusions |
| **Evaluation** | Completed investigations automatically validate planned skills, executed skills, tool usage, execution traces, evidence objects, and overall pipeline success |
| **Production-Oriented AI Engineering** | DuckDB analytics warehouse, specification-driven architecture, modular agents, and deterministic analytical pipelines support reproducible investigations |

DeadBase demonstrates how the concepts introduced throughout the AI Agents Intensive can be combined into a reusable architecture for explainable, evidence-driven AI systems rather than isolated demonstrations of individual techniques.

---

# Problem

The Grateful Dead archive contains:

- 2,308 performances
- 35,000+ song performances
- 446 songs
- 592 venues

Although the archive contains decades of information, historical investigation still relies heavily on manual research and community knowledge.

Most archive tools answer:

> What happened?

DeadBase attempts to answer:

> Why did it matter?

---

# System Architecture

```text
User Question
        │
        ▼
Planning Agent
        │
        ▼
Investigation Session
        │
        ▼
Dynamic Skill Planning
        │
        ▼
Research Agents
        │
        ▼
Evidence Collection
        │
        ▼
Synthesis Agent
        │
        ▼
Evaluation
```

Every investigation follows this architecture regardless of the research question.

---
# Performance & Execution

DeadBase executes entirely against a local DuckDB warehouse and locally generated analytical feature sets. The Planning Agent orchestrates deterministic Python skills and analytical queries rather than relying on multiple sequential calls to external LLM APIs.

As a result, a complete multi-agent historical investigation executes in approximately 2–3 seconds on local hardware.

The demonstration video reflects actual runtime execution. Agent orchestration, evidence collection, synthesis, and evaluation are performed live during the investigation.

---

# Investigation Pipeline

Each investigation proceeds through seven stages.

## 1. Planning

The Planning Agent analyzes the user's question and determines:

- investigation intent
- required skills
- entities
- MCP tools
- execution plan

Example

Question:

> Was Cornell 1977 actually unique?

The planner produces:

- show-lookup
- show-intelligence
- venue-analysis
- setlist-similarity
- song-history
- synthesis

before any research agent executes.

---

## 2. Investigation Session

Each investigation creates a structured session object that records the complete lifecycle of the research process.

The session stores:

- question
- intent
- selected skills
- tool calls
- execution trace
- evidence
- stage evaluation
- synthesized report

This provides complete observability throughout the investigation.

---

## 3. Dynamic Skill Dispatch

The execution pipeline is not hard coded for a single investigation.

Instead, the Planning Agent selects skills dynamically and the pipeline dispatches the appropriate research agents.

Example workflow:

```text
Planning Agent

↓

show-lookup

↓

Research Agent

↓

venue-analysis

↓

Venue Agent

↓

song-history

↓

Song Agent
```

This architecture allows different questions to execute different research pipelines.

---

## 4. Research Agents

DeadBase contains specialized historical research agents.

### Research Agent

Coordinates historical archive investigation.

### Historian Agent

Measures historical significance using archive analytics.

### Venue Agent

Builds historical venue profiles.

### Song Agent

Analyzes historical song information.

### Similarity Agent

Finds historically similar performances.

### Song Evolution Agent

Models song careers across the archive.

### Synthesis Agent

Combines evidence from multiple agents into a single explainable historical report.

---

## 5. Evidence Collection

Rather than returning isolated answers, every investigation records evidence.

Evidence includes:

- historical rankings
- similarity analysis
- venue intelligence
- song intelligence
- synthesis output

The evidence collection layer makes every investigation explainable and reproducible.

---

## 6. Evaluation

Each completed investigation automatically evaluates:

- planned skills
- executed skills
- tool calls
- execution trace
- evidence objects
- overall pipeline success

## Current Evaluation Coverage

- Planning validation
- Skill selection validation
- Tool execution validation
- Evidence validation
- Pipeline validation
- Overall investigation success

Every completed investigation concludes with an automated evaluation summary that verifies successful execution of the complete investigation pipeline.

---

# Analytics Layer

DeadBase transforms raw archive data into analytical intelligence.

Generated datasets include:

## show_dna

Structural characteristics for every performance.

## song_profile

Historical lifecycle statistics for every song.

## song_evolution

Song career modeling.

## venue_profile

Historical venue intelligence.

## venue_rankings

Venue importance rankings.

## show_embeddings

Feature vectors used for similarity analysis.

## show_historical_significance

Historical scoring model for every performance.

Produces:

- historian score
- archive rank
- percentile

## show_archetypes

Automatically classifies performances into historical categories.

Examples include:

- Complex Set Structure
- Marathon Show
- Rare Song Show
- Venue Landmark Show

## show_clusters

Machine-learning grouping of historically similar performances.

---

# Example Investigation

Question:

> Was Cornell 1977 actually unique?

The Planning Agent selected:

- show-lookup
- show-intelligence
- venue-analysis
- setlist-similarity
- song-history
- synthesis

The investigation then produced:

- historical ranking
- archetype classification
- venue analysis
- neighboring performances
- song intelligence
- evidence-based historical synthesis

Final conclusion:

Cornell is historically significant, but its reputation cannot be explained by setlist uniqueness alone. The investigation shows that cultural reputation extends beyond measurable archive signals, incorporating performance quality, listener consensus, tape circulation, and historical memory.

---

# Repository Structure

```text
agents/
analytics/
docs/
evals/
mcp_server/
scripts/
session/
specs/
tests/
tools/
demo.py
```

---

# Data Boundary

The public repository intentionally excludes:

- raw archive files
- generated warehouse
- DuckDB database

Only the analytics framework and agent architecture are published.

---

# Results

Current archive modeled:

- 1,822 performances
- 35,000+ song performances
- 445 songs
- 434 venues

Analytics generated:

- show_dna
- show_embeddings
- show_historical_significance
- show_archetypes
- show_clusters
- song_profile
- song_evolution
- venue_profile
- venue_rankings

The platform performs complete multi-agent investigations with planning, orchestration, evidence collection, synthesis, and evaluation.

---

# Why Not Traditional RAG?

| Traditional RAG | DeadBase |
|-----------------|----------|
| Retrieve documents | Plan investigations |
| Generic prompts | Specification-driven planning |
| Single assistant | Specialized research agents |
| Text retrieval | Structured analytics |
| Opaque reasoning | Explainable evidence |
| One response | Complete investigation lifecycle |

---

# Technology

- Python
- DuckDB
- Pandas
- Scikit-Learn
- MCP
- Multi-Agent Systems
- Analytics Engineering
- Specification-Driven Development

---

# Documentation

Additional documentation is available in:

- docs/architecture.md
- docs/demo_script.md
- docs/deployment.md
- docs/evaluation.md
- specs/
- evals/

---

# Future Work

The architecture was intentionally designed to be domain independent.

The same investigation framework can be applied to:

- Negro League Baseball
- MLB Historical Intelligence
- NASCAR Analytics
- AEW Match Intelligence
- WNBA Historical Research
- Financial Intelligence Systems

Only the analytics layer and research agents change while the planning, orchestration, investigation session, evidence collection, and evaluation architecture remain the same.

---

# Conclusion

DeadBase demonstrates a reusable architecture for explainable AI research systems.

Instead of building agents that simply retrieve information, DeadBase plans investigations, dynamically orchestrates specialized agents, records evidence, synthesizes findings, and evaluates the entire execution pipeline.

The result is a transparent historical intelligence system capable of answering complex research questions while exposing every step of its reasoning process.