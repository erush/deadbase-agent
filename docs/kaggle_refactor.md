# DeadBase Kaggle Refactor Plan

## Objective

Refactor DeadBase to explicitly align with the Google × Kaggle AI Agents Intensive concepts without changing the underlying historical intelligence architecture.

The goal is **not** to redesign the system.

The goal is to expose existing functionality using the terminology, patterns, and demonstrations taught during the course.

---

# Existing Strengths

DeadBase already contains:

- Multi-agent orchestration
- Specialist agent architecture
- Skill specifications
- MCP server
- DuckDB analytical warehouse
- Explainable historical reports
- Analytics pipeline
- Domain-specific feature engineering
- Structured specifications

These components should be preserved.

---

# Primary Refactor Goals

## 1. Make MCP First-Class

Current

Planner

↓

Skill Executor

↓

DuckDB

Target

Planner

↓

MCP Tool

↓

Skill Executor

↓

DuckDB

The live demo should visibly show MCP tool invocation.

---

## 2. Promote Agent Skills

Current

skill_executors/

Target

Planner selects Agent Skills.

Each skill executes through MCP.

Each skill contributes evidence.

The skills become first-class architectural components rather than implementation details.

---

## 3. Introduce Session State

Create:

sessions/

InvestigationSession

Stores:

- user question
- selected skills
- tool invocations
- evidence
- synthesis
- final report

Purpose

Demonstrate Sessions & Context Management.

---

## 4. Add Evaluation Harness

Current

evals/

Target

evaluation/

goldens/

evaluate.py

Trajectory verification.

Example

Question

↓

Expected Skills

↓

Actual Skills

↓

PASS / FAIL

Purpose

Demonstrate Evaluation.

---

## 5. Improve Observability

Log every stage.

Planning

↓

Selected Skills

↓

MCP Tool Called

↓

Execution Complete

↓

Evidence Added

↓

Session Updated

↓

Synthesis

↓

Report

Purpose

Demonstrate Observability.

---

## 6. README Alignment

Create a section:

## Google AI Agents Intensive Concepts

Map DeadBase architecture to course concepts.

Example

| Course Concept | DeadBase Implementation |
|----------------|-------------------------|
| Multi-Agent Orchestration | Planning + Specialist Agents + Synthesis |
| Agent Skills | skills/ |
| MCP | mcp_server/ |
| Tool Calling | MCP → Skill Executors |
| Sessions | InvestigationSession |
| Context Engineering | Show DNA + Historical Profiles |
| Evaluation | Evaluation Harness |
| Observability | Planner and Tool Execution Logs |

---

## 7. Demo Refactor

Current

Question

↓

Report

Target

Question

↓

Planner

↓

Skill Selection

↓

MCP Tool Calls

↓

Session Updates

↓

Evidence Collection

↓

Evaluation

↓

Historical Report

---

# Explicit Course Concepts

DeadBase should clearly demonstrate:

✓ Multi-Agent Orchestration

✓ Agent Skills

✓ MCP

✓ Tool Calling

✓ Sessions

✓ Context Engineering

✓ Evaluation

✓ Observability

✓ Explainable AI

---
---

# Success Criteria

A Kaggle judge should immediately recognize:

1. Planner
2. Agent Skills
3. MCP Tool Calls
4. Session State
5. Evidence Collection
6. Evaluation
7. Explainable Historical Report

without needing additional explanation.