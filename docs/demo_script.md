# DeadBase Demo Script

## Objective

Demonstrate how DeadBase performs historical investigations using analytics engineering and multi-agent reasoning.

The demo focuses on one of the most famous performances in Grateful Dead history:

Cornell University — May 8, 1977.

## Demo Question

Why is Cornell 1977 historically significant?

## Main Demonstration

Run:

```bash
python -m scripts.cornell_investigation_demo
```

## Investigation Workflow

The system performs a multi-agent investigation.

### Research Agent

Coordinates the overall investigation.

### Historian Agent

Provides:

- historian rank
- historian percentile
- historical significance score
- archetype classification

### Similarity Agent

Identifies neighboring performances using:

- repertoire overlap
- archive similarity relationships

### Venue Agent

Investigates:

- venue history
- venue rarity
- historical footprint

### Song Agent

Provides context for important songs appearing in the performance.

### Synthesis Agent

Combines all findings into a unified historical interpretation.

## Expected Output

The investigation should produce:

- show location
- historical ranking
- archetype classification
- venue intelligence
- nearest-neighbor performances
- song context
- historical interpretation
- research synthesis

## Example Finding

DeadBase suggests that Cornell's reputation cannot be explained solely through setlist uniqueness.

Instead, the investigation points toward a combination of:

- strong Spring 1977 repertoire
- venue mythology
- tape circulation
- listener consensus
- performance quality
- long-term cultural memory

## Additional Demonstrations

Research Agent:

```bash
python -m scripts.test_research_agent
```

Historian Agent:

```bash
python -m scripts.test_historian_agent
```

Song Evolution Agent:

```bash
python -m scripts.test_song_evolution_agent
```

Similarity Agent:

```bash
python -m scripts.test_show_recommender
```

## Demonstration Goal

The purpose of the demo is to show that DeadBase moves beyond archive retrieval and toward explainable historical investigation.