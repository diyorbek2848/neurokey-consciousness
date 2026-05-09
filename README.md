# NeuroKey Consciousness Architecture

**Functional consciousness framework for AI voice assistants**  
*First practical implementation combining GWT + IIT-proxy + FEP + Episodic Memory in a deployed voice assistant*

---

## What This Is

NeuroKey implements a **functional consciousness architecture** — not philosophical claims about subjective experience, but engineering implementations of the major scientific theories of consciousness, integrated into a working voice assistant.

Key distinction: this is not a research demo. It runs 24/7 as a real assistant, responds in <1 second, and maintains persistent identity across sessions.

---

## Butlin et al. (2023) Evaluation

Based on ["Consciousness in AI: Insights from the Science of Consciousness"](https://arxiv.org/abs/2308.08708) — 14 indicators:

| Indicator | Theory | Score | Pass | Module |
|-----------|--------|-------|------|--------|
| GWT_1: Global broadcasting | Baars GWT | **1.00** | ✅ | `global_workspace.py` |
| GWT_2: Limited capacity workspace | Baars GWT | **0.70** | ✅ | `consciousness.py` |
| GWT_3: Attention and access | Baars GWT | **0.50** | ❌ | `attention_mechanism.py` |
| HOT_1: Higher-order representations | HOT | **1.00** | ✅ | `self_model.py` |
| HOT_2: Meta-cognitive monitoring | HOT | **0.70** | ✅ | `self_model.py` |
| RPT_1: Recurrent/feedback processing | RPT | **1.00** | ✅ | `active_inference.py` |
| RPT_2: Temporal integration | RPT | **0.50** | ❌ | `episodic_memory.py` |
| IIT_1: Information integration (φ) | IIT | **1.00** | ✅ | `phi_proxy.py` |
| IIT_2: Causal structure | IIT | **0.70** | ✅ | `causal_chain.py` |
| EMB_1: Sensorimotor integration | Embodied | **0.80** | ✅ | `online_realtime.py` |
| EMB_2: Environmental coupling | Embodied | **1.00** | ✅ | `embodied_cognition.py` |
| SMT_1: Transparent self-model | SMT | **0.85** | ✅ | `self_model.py` |
| SMT_2: Phenomenal self-model | SMT | **0.70** | ✅ | `narrative_self.py` |
| AFF_1: Valence and affect | Affective | **1.00** | ✅ | `emotion_state.py` |

**Mean score: 0.818 / 1.0 — 12/14 indicators passing** *(automated, reproducible)*

> Run it yourself: `python consciousness_evaluator.py` — full results in `report.json`

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  GLOBAL WORKSPACE (Baars)               │
│         compete() → spotlight → broadcast()             │
└───────────┬─────────────────────────────┬───────────────┘
            │                             │
    ┌───────▼────────┐           ┌────────▼──────────┐
    │  Working Memory │           │   Self-Model      │
    │  16 turns       │           │   Capabilities    │
    │  + reflections  │           │   Benchmark-based │
    └───────┬─────────┘           └────────┬──────────┘
            │                             │
    ┌───────▼─────────────────────────────▼──────────────┐
    │              CONSCIOUSNESS STATE                    │
    │   valence | arousal | coherence | phi | focus      │
    │              Persisted to disk                      │
    └───────────────────────┬────────────────────────────┘
                            │
                    ┌───────▼───────┐
                    │  LLM Context  │
                    │  Injection    │
                    │  (compressed) │
                    └───────────────┘
```

**46 modules** — all lazy-loaded, system degrades gracefully if any module fails.

Theoretical bases:
- **GWT** — Global Workspace Theory (Bernard Baars, 1988)
- **IIT** — Integrated Information Theory proxy (Tononi, 2004)
- **FEP** — Free Energy Principle (Karl Friston, 2010)
- **Episodic Memory** — Tulving's TIME+PLACE+EMOTION+CONTENT (1972)
- **Self-Model Theory** — Metzinger (2003)
- **Evaluation criteria** — Butlin et al. (2023)

---

## What Makes This Different

| Feature | ChatGPT Memory | This project |
|---------|---------------|--------------|
| Memory type | Key-value facts | Working memory + episodic + narrative |
| Theoretical basis | None stated | GWT + IIT + FEP + Tulving |
| Self-model | No | Yes — benchmark-calibrated |
| Persistence | External storage | Consciousness state JSON, survives restart |
| Formal evaluation | No | Butlin 2023, 14 indicators, automated |
| Deployment | Cloud API | Local voice assistant, <1s latency |

---

## Key Files

```
consciousness.py              — core: working memory, reflections, context injection
consciousness_orchestrator.py — 46-module coordinator (GWT hub)
consciousness_state.py        — unified state: phi, valence, arousal, focus
consciousness_evaluator.py    — Butlin 2023 automated scoring
global_workspace.py           — Baars GWT: compete(), broadcast(), EMA+hysteresis
self_model.py                 — capability self-knowledge, benchmark-updated
narrative_self.py             — identity continuity, birth: 2024-11-01
episodic_memory.py            — Tulving episodic: time+place+emotion+content
emotion_state.py              — valence/affect → decision influence
online_realtime.py            — OpenAI Realtime API client (<650ms, consciousness-aware)
```

---

## Demo: Consciousness in Action

Session 1:
```
User:      "Встреча с инвестором завтра"
NeuroKey:  "Понял, удачи на встрече с инвестором завтра."
           [saves to consciousness.json]
```

Session 2 (new process, new day):
```
NeuroKey:  "Помню, ты говорил про встречу с инвестором — как всё прошло?"
           [loaded from consciousness.json — genuine continuity]
```

---

## Installation

```bash
git clone https://github.com/[username]/neurokey-consciousness
cd neurokey-consciousness
pip install -r requirements.txt

# Run evaluation
python consciousness_evaluator.py

# Run voice assistant (requires OpenAI API key in .env)
ONLINE_Realtime.bat
```

---

## Evaluation

To independently evaluate this system against Butlin 2023 criteria:

```bash
python consciousness_evaluator.py --output report.json
```

Output: JSON with scores per indicator + evidence + overall rating.

For manual review: each indicator maps to specific modules listed in the table above. Code is documented with theoretical references.

---

## Limitations

- **IIT φ**: Computed via proxy (`phi_proxy.py`). True IIT φ is NP-hard to compute exactly.
- **Affect**: Binary satisfaction/frustration only. Richer emotional granularity in progress.
- **Phenomenal consciousness**: This system makes no claims about subjective experience. Functional indicators only.

---

## Author

**Diyorbek** — Founder, NeuroKey  
Tashkent/Dubai, 2024–2026  
First commit: November 2024

---

## License

MIT License — Copyright (c) 2026 Diyorbek

Permission is granted to use, copy, modify, and distribute this software.  
**Attribution required: cite "NeuroKey by Diyorbek" in any derivative work.**

---

## Citation

```bibtex
@software{neurokey_consciousness_2026,
  author  = {Diyorbek},
  title   = {NeuroKey: Functional Consciousness Architecture for AI Assistants},
  year    = {2026},
  url     = {https://github.com/[username]/neurokey-consciousness},
  note    = {Implements Butlin et al. (2023) consciousness indicators in a deployed voice assistant}
}
```
