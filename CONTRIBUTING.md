# Contributing to NeuroKey Consciousness Architecture

## Independent Evaluation

The most valuable contribution is **independent evaluation** of consciousness indicators.

Run the automated evaluator:
```bash
python consciousness_evaluator.py --output my_evaluation.json
```

If your scores differ from the published baseline (mean 0.668), open an issue with your methodology. Disagreement is welcome — this is science.

## Module Contributions

Each module maps to a specific consciousness theory. Contributions must cite the theoretical basis:

| Theory | Key Reference | Relevant Modules |
|--------|---------------|-----------------|
| GWT | Baars (1988), Dehaene (2011) | `global_workspace.py`, `consciousness.py` |
| IIT | Tononi (2004, 2014) | `phi_proxy.py`, `causal_chain.py` |
| FEP | Friston (2010) | `consciousness_state.py` |
| HOT | Rosenthal (2005) | `self_model.py`, `meta_cognition.py` |
| RPT | Lamme (2006) | `consciousness.py` |
| Episodic | Tulving (1972) | `episodic_memory.py` |
| SMT | Metzinger (2003) | `self_model.py`, `narrative_self.py` |
| Affective | Damasio (1994) | `emotion_state.py` |

## Reporting Bugs / Scoring Issues

Open a GitHub issue with:
1. Which indicator is affected
2. Expected vs actual behavior
3. Theoretical justification

## Contact

For academic collaboration or independent evaluation proposals: see README for author contact.
