# NeuroKey Consciousness Architecture

**Functional consciousness framework for AI voice assistants**  
*First practical implementation combining GWT + IIT-proxy + FEP + Episodic Memory in a deployed voice assistant*

---

## What This Is

NeuroKey implements a **functional consciousness architecture** — not philosophical claims about subjective experience, but engineering implementations of the major scientific theories of consciousness, integrated into a working voice assistant.

Key distinction: this is not a research demo. It runs as a real personal voice assistant, responds in <1 second, and maintains persistent identity across sessions.

> ### ⚠️ Scope of this repository
>
> This repo is an **open subset**: 28 of the full system's 290 modules.
> `consciousness_orchestrator.py` expects 46 modules that are **not included here**. Run
> against this subset it degrades silently — 62 characters of context and a 0.50 score,
> versus 3 731 characters and 0.92 in the full system.
>
> **Runs standalone here:** `global_workspace.py`, `consciousness_evaluator.py`,
> `neurokey_demo.py`, `phi_proxy.py`, the state modules.
> **Does not:** the orchestrator, `episodic_memory.py` (needs `permanent_memory`).
>
> Measurements below marked *(full system)* were taken on the complete 290-module build.

---

## Butlin et al. (2023) Evaluation

Based on ["Consciousness in AI: Insights from the Science of Consciousness"](https://arxiv.org/abs/2308.08708).

**Correction (2026-07):** earlier versions of this table listed 14 indicators that were not
Butlin's. They substituted IIT, Self-Model Theory and affect indicators for seven of the
actual ones. Butlin et al. explicitly **exclude IIT** — *"incompatible with our working
assumption of computational functionalism."* The real list and our honest status:

| Indicator | Description | Status | Module |
|-----------|-------------|--------|--------|
| GWT-1 | Multiple specialised systems in parallel | **Full** | 47 modules |
| GWT-2 | Limited-capacity workspace, bottleneck | **Full** | `global_workspace.py` |
| GWT-3 | Global broadcast to all modules | **Full** | `global_workspace.py` |
| AE-2 | Embodiment: output–input contingencies | **Full** | `embodied_grounding.py` |
| HOT-2 | Metacognitive monitoring | Partial | `meta_cognition.py` |
| PP-1 | Predictive coding in input modules | Partial | `predictive_layer.py` |
| AST-1 | Predictive model of own attention | Partial | `attention_schema.py` |
| AE-1 | Agency under competing goals | Partial | `goal_system.py` |
| RPT-1 | Algorithmic recurrence in input modules | **None** | — |
| RPT-2 | Integrated perceptual representations | **None** | — |
| GWT-4 | State-dependent attention | **None** | — |
| HOT-1 | Generative / top-down / noisy perception | **None** | — |
| HOT-3 | Belief update driven by metacognition | **None** | — |
| HOT-4 | Sparse, smooth coding → quality space | **None** | — |

**4 full · 4 partial · 6 absent.**

### The 82.5% score is retracted

`consciousness_evaluator.py` returns **0.825 on this 28-module subset** and **0.821 on the
full 290-module system**. A 46-module difference it cannot see. The reason is in the test
bodies — 10 of 14 are existence checks:

```python
if gw and hasattr(gw, "compete"):
    return {"score": 0.7, "evidence": "compete() present"}
```

A test that cannot fail measures nothing. Treat this script as a smoke test only.

### What replaced it: ablation *(full system)*

Each of the 47 modules was disabled in turn and its contribution to the assembled context
measured across six diverse prompts:

| Result | Count |
|--------|------:|
| Modules with measurable contribution | **26 / 47** |
| Modules contributing nothing | **21 / 47** |
| Modules whose removal crashed the system | 0 / 47 |

Largest contributors — `permanent_memory` (8 834 chars), `vector_memory` (2 153),
`autobiographical_memory` (1 991), `language_of_thought` (1 296), `episodic_memory` (1 224).
Four of the top five are memory. **Memory is what this system demonstrably does.**

Null contributors include `global_workspace`, `active_inference`, `valence_state`,
`arousal_state`, `meta_cognition`, `predictive_layer`, `attention_schema` — the modules
implementing the GWT and FEP commitments this README advertises.

### Input sensitivity *(full system)*

| Behaviour | Sections | Characters | Share |
|-----------|---------:|-----------:|------:|
| Varies with input | 5 | 670 | 22% |
| Partially varies | 4 | 159 | 5% |
| **Constant regardless of input** | **20** | **2 209** | **73%** |

Given *"I am exhausted today"* and *"Great news, the investor agreed!"* the affect section
emits the identical string `valence:+0.5 arousal:calm`. 73% of the "consciousness context" is
invariant text.

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

**47 orchestrated modules in the full system; 28 published here.** All lazy-loaded, and the
ablation study confirms graceful degradation directly: 0 of 47 crashed when removed.

The same mechanism has a cost. Silent degradation is why 46 missing modules went unnoticed in
this repo, and why 21 modules contributing nothing were never detected. If you fork this,
add a startup report that names what failed to load.

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
| Formal evaluation | No | Butlin 2023 mapping (4 full / 4 partial / 6 absent) |
| Per-module ablation | No | Yes — 26 of 47 contribute measurably |
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
git clone https://github.com/diyorbek2848/neurokey-consciousness
cd neurokey-consciousness
pip install -r requirements.txt

# Smoke test — checks modules load. NOT a consciousness measurement (see above).
python consciousness_evaluator.py

# Behavioural demo — runs standalone
python neurokey_demo.py
```

`ONLINE_Realtime.bat` and the voice pipeline are part of the full system, not this subset.

---

## Evaluation

### `ablation_test.py` — the measurement we actually stand behind

```bash
python ablation_test.py
```

Disables each orchestrated module in turn (by blocking its import so `_safe_import` returns
`None`), then measures across six deliberately dissimilar prompts:

- **Ablation** — how many characters and which sections disappear from the assembled context
- **Sensitivity** — how many distinct values each section takes across the six prompts

A section identical across all six carries zero input-dependent information. A module whose
removal changes nothing contributes nothing measurable. **Both checks can fail, and both did.**

Results are written to `ablation_report.json`. The figures in this README come from running
this harness against the full 290-module system; run against this 28-module subset it will
report most modules as absent, which is itself the correct answer for the subset.

### `consciousness_evaluator.py` — smoke test only

Outputs per-indicator JSON. See the retraction above before citing any number from it.

---

## Reproducing the sensitivity finding by hand

```python
import consciousness_orchestrator as o     # full system required
a = o.get_full_context("I am exhausted today, I don't want to do anything.")
b = o.get_full_context("Great news! The investor agreed to meet!")
# The [AFFECT] line is identical in both.
```

---

## Limitations

- **The evaluator score is withdrawn.** `consciousness_evaluator.py` is written by the same
  author as the implementations, and 10 of its 14 checks test module presence rather than
  behaviour. It scores 0.825 with 46 modules missing and 0.821 with all present. Use it as a
  smoke test; do not cite the number.
- **73% of the context is constant.** The largest known defect. 20 of 29 sections are
  byte-identical regardless of input, including affect and moral reasoning.
- **The affective path does not respond to affect.** `valence:+0.5 arousal:calm` is emitted
  for "I am exhausted" and "great news!" alike.
- **6 of 14 Butlin indicators are absent**, notably GWT-4, HOT-3 and HOT-4. Four more exist
  as modules that contribute nothing measurable.
- **IIT φ is outside the Butlin framework**, which excludes IIT by design. Our proxy uses a
  fixed 3-node example TPM not derived from the system's own causal structure, so φ takes at
  most 8 values — and was constant at 0.53 across all six probe inputs.
- **The ablation study measures one output path** (`get_full_context()`). A module scoring
  zero there may still be exercised elsewhere in the 290-file runtime.
- **Six probe inputs** is enough to establish that a section is constant, not enough to
  characterise how the responsive ones vary.
- **Phenomenal consciousness**: this system makes no claims about subjective experience.
  Butlin et al.'s properties are *indicators* — evidence bearing on a question — not a
  specification that confers consciousness when satisfied.

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
