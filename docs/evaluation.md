# DeadBase Evaluation

## Evaluation Objective

DeadBase is evaluated as a historical intelligence system rather than a simple archive lookup tool.

The central question is:

Can analytics and agents combine multiple sources of evidence into meaningful historical investigations?

## Evaluation Assets

Evaluation files are located in:

```text
evals/
```

Current evaluation assets include:

- show_lookup.json
- song_history.json
- venue_profile.json
- tour_analysis.json
- setlist_similarity.json

## Test Coverage

Test files are located in:

```text
tests/
```

Current tests include:

- show lookup
- song history
- venue profile
- tour analysis

## Demo Evaluation

Primary evaluation script:

```bash
python -m scripts.cornell_investigation_demo
```

The demo verifies that the system can:

- identify a performance
- retrieve venue intelligence
- retrieve song intelligence
- discover similar performances
- apply historical rankings
- generate research synthesis

## Qualitative Evaluation Criteria

A successful investigation should:

- combine multiple analytical signals
- provide evidence-based reasoning
- distinguish reputation from measurable evidence
- explain why a performance matters
- synthesize information across multiple agents

## Current Capabilities

DeadBase currently supports:

- archive lookup
- song history
- song evolution
- venue analysis
- similarity analysis
- historical significance ranking
- archetype classification
- performance clustering
- research synthesis

## Success Criteria

DeadBase succeeds when it moves beyond simple retrieval and provides explainable historical interpretation supported by measurable archive signals.

This distinction between retrieval and investigation is the primary goal of the project.

## Current Status

The repository currently includes:

- analytics engineering pipeline
- multi-agent architecture
- historical investigation workflow
- evaluation assets
- public GitHub repository
- documentation
- demonstration scripts

The project is considered submission-ready for Kaggle AI Agents Capstone evaluation.