# DeadBase Live Demonstration Walkthrough

## Purpose

This document accompanies the silent live demonstration included with the Kaggle AI Agents Capstone submission.

The demonstration is intentionally a screen capture without narration because the narrated presentation explains the architecture and introduces the demonstration beforehand.

This walkthrough describes exactly what occurs during the live execution.

---

# Demonstration Overview

The demonstration executes a complete historical investigation against a local DuckDB analytics warehouse.

No responses are pre-generated.

No outputs are hard coded.

Every planning decision, analytical query, evidence object, synthesis, and evaluation is executed live.

Total execution time is approximately **2–3 seconds**.

---

# Step 1 — User Question

The investigation begins with the user asking:

> Was Cornell 1977 actually unique?

This question intentionally requires multiple forms of historical evidence rather than a simple record lookup.

---

# Step 2 — Planning Agent

The Planning Agent analyzes the research question.

It determines:

- Investigation intent
- Required specialist skills
- Required analytical datasets
- MCP tool usage
- Investigation execution plan

No historical conclusions are generated during this stage.

The Planning Agent only determines how the investigation should proceed.

---

# Step 3 — Dynamic Skill Selection

The Planning Agent selects the required investigation skills.

Example skills include:

- Show Lookup
- Show Intelligence
- Venue Analysis
- Song History
- Setlist Similarity
- Historical Synthesis

Different research questions produce different execution plans.

The workflow is dynamically generated rather than hard coded.

---

# Step 4 — Research Agent Execution

Specialized research agents execute independently.

Examples include:

- Research Agent
- Historian Agent
- Venue Agent
- Song Agent
- Similarity Agent
- Song Evolution Agent

Each agent contributes structured evidence from the analytical warehouse.

No agent attempts to answer the entire question alone.

---

# Step 5 — Evidence Collection

Evidence objects are collected throughout the investigation.

Examples include:

- Historical rankings
- Venue intelligence
- Song intelligence
- Similarity analysis
- Historical significance metrics

Evidence remains structured throughout the investigation.

---

# Step 6 — Synthesis

The Synthesis Agent combines the evidence gathered by all specialist agents.

The final report integrates multiple historical perspectives into a single explainable investigation.

Rather than summarizing retrieved documents, the report synthesizes structured analytical evidence.

---

# Step 7 — Evaluation

After the investigation completes, DeadBase automatically evaluates the execution.

Evaluation verifies:

- Planned skills
- Executed skills
- Tool execution
- Evidence generation
- Pipeline completion

This confirms that the investigation executed successfully from planning through synthesis.

---

# Demonstration Summary

The live demonstration illustrates the complete DeadBase investigation lifecycle:

User Question

↓

Planning Agent

↓

Dynamic Skill Selection

↓

Specialized Research Agents

↓

Evidence Collection

↓

Historical Synthesis

↓

Automated Evaluation

The demonstration is executed live against a local DuckDB analytical warehouse and reflects the same deterministic investigation workflow used for every historical research question.