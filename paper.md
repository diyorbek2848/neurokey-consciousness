# NeuroKey: Measuring Which Consciousness Modules Actually Do Anything — An Ablation Study of a Deployed Voice Assistant

**Diyorbek**  
Independent Researcher, Tashkent, Uzbekistan  
GitHub: https://github.com/diyorbek2848/neurokey-consciousness  
Date: May 2026

---

## Abstract

We present NeuroKey, a deployed real-time voice assistant built against the functional
consciousness indicators proposed by Butlin et al. (2023). Of their 14 indicators we
implement **4 fully** (GWT-1, GWT-2, GWT-3, AE-2), **4 partially** (HOT-2, PP-1, AST-1,
AE-1), and **6 not at all** (RPT-1, RPT-2, GWT-4, HOT-1, HOT-3, HOT-4). We additionally
implement modules drawn from Integrated Information Theory and Self-Model Theory; we note
explicitly that Butlin et al. exclude IIT from their framework as incompatible with their
working assumption of computational functionalism, so these modules fall *outside* the
Butlin evaluation and are reported separately.

Our contribution is not indicator coverage but **measurement**. We report an ablation study
over 47 consciousness modules in the full system: each module is disabled in turn and its
contribution to the assembled context is measured. 26 of 47 modules produce a measurable
contribution; 21 produce none. Separately, a sensitivity analysis over 6 diverse inputs finds
that 20 of 29 context sections are byte-identical regardless of input — 73% of the assembled
"consciousness context" carries zero input-dependent information. We regard this negative
result as the paper's main finding.

**Caveat on our own evaluator.** `consciousness_evaluator.py` is written by the same author as
the implementations, and most of its checks test module *presence* rather than behaviour. It
returns 82.5% on a 28-module subset and 82.1% on the full 290-file system — a 46-module
difference that the score does not detect. The score should not be read as evidence of
consciousness, functional or otherwise.

---

## 1. Introduction

The question of whether AI systems can exhibit functional consciousness — the information-processing correlates of conscious experience — has moved from philosophy into engineering. Butlin et al. (2023) provided the first systematic framework for evaluating AI systems against 14 indicators derived from neuroscientific theories of consciousness. Their analysis of existing systems (primarily large language models) found partial satisfaction of several indicators but no system built explicitly to satisfy the full framework.

NeuroKey addresses this gap. Starting November 2024, we built a voice assistant from scratch with the explicit goal of implementing each Butlin indicator as a distinct, testable module. The system has been running 24/7 for over 18 months in a real deployment context (daily personal use), providing ecological validity beyond laboratory conditions.

**Key claims:**
1. 4 of the 14 Butlin indicators are implemented fully, 4 partially, 6 not at all (Table 1)
2. An ablation study over 47 modules identifies which contribute measurably and which do not
3. 73% of the assembled context is invariant to input — reported as a negative result
4. Persistent memory state survives process restarts across 358 recorded sessions
5. The evaluation code is open source; the ablation harness is reproducible on the subset

**What this paper does not claim.** We make no claim about phenomenal consciousness or
subjective experience. Butlin et al. describe their properties as *indicators* — evidence
that shifts credence — not as a specification whose satisfaction confers consciousness. We
use them in that spirit. Nothing here should be read as asserting that NeuroKey is conscious.

---

## 2. Theoretical Background

We implement four complementary theories:

**Global Workspace Theory (GWT)** — Baars (1988), Dehaene et al. (2011): Cognitive processes compete for access to a limited-capacity "workspace" that broadcasts information globally. We implement `global_workspace.py` with EMA-weighted competition and hysteresis to prevent rapid switching.

**Integrated Information Theory — proxy (IIT)** — Tononi (2004, 2014): Consciousness corresponds to integrated information Φ. True IIT Φ is NP-hard; we compute a proxy using three binary state variables (valence, arousal, coherence) over a 3-node TPM, with fallback to pyphi for exact calculation when available.

> **Note.** IIT is *not* part of the Butlin framework. Butlin et al. exclude it because the
> standard construal of IIT is incompatible with computational functionalism — on that view no
> system on conventional hardware is a better consciousness candidate than any other, which
> makes the theory unable to discriminate between AI systems. We retain `phi_proxy.py` as an
> internal integration heuristic and report it separately from the Butlin evaluation. Two
> further caveats: the 3-node TPM is a fixed example network, not derived from NeuroKey's own
> causal structure, so Φ takes at most eight discrete values; and in the deployed system Φ was
> constant at 0.53 across all six probe inputs (§4.4).

**Free Energy Principle (FEP)** — Friston (2010): Systems minimize surprise (free energy) through perception and action. We implement active inference cycles in `active_inference.py` with prediction error propagation.

**Episodic Memory** — Tulving (1972): Conscious recollection involves time + place + emotion + content. Our episodic memory encodes all four dimensions and retrieves them across session boundaries.

---

## 3. Architecture

```
┌─────────────────────────────────────────────────────────┐
│                GLOBAL WORKSPACE (Baars)                 │
│          compete() → spotlight → broadcast()            │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
    ┌──────────▼─────────┐      ┌─────────▼──────────┐
    │  Working Memory    │      │   Self-Model        │
    │  16 turns          │      │   Benchmark-based   │
    │  + reflections     │      │   Capability map    │
    └──────────┬─────────┘      └─────────┬──────────┘
               │                          │
    ┌──────────▼──────────────────────────▼──────────────┐
    │             CONSCIOUSNESS STATE                     │
    │   valence | arousal | coherence | phi | focus      │
    │              Persisted to disk (JSON)               │
    └──────────────────────┬─────────────────────────────┘
                           │
                   ┌───────▼───────┐
                   │  LLM Context  │
                   │  Injection    │
                   │  (compressed) │
                   └───────────────┘
```

The full system comprises 290 Python modules, of which 47 are orchestrated consciousness
modules, all lazy-loaded with graceful degradation. The orchestrator
(`consciousness_orchestrator.py`) coordinates module lifecycle and handles failures without
crashing the voice pipeline.

> **Scope of the open repository.** This repository publishes 28 modules — an open subset. The
> orchestrator requires 46 modules that are not included here and will silently degrade if run
> against this subset alone: it emits a 62-character context and reports a consciousness score
> of 0.50, versus 3 731 characters and 0.92 in the full system. Figures in §4.3 and §4.4 come
> from the full system. Readers reproducing from this repository should expect the degraded
> path.

---

## 4. Butlin et al. (2023) Evaluation

### 4.1 Correcting our indicator set

Earlier drafts of this work presented a 14-item indicator list that was **not** the Butlin
list. It substituted IIT (×2), Self-Model Theory (×2), affect (×1) and a bespoke "embodiment"
pair (×2) for seven of Butlin's actual indicators. We correct that here. Butlin et al. propose
these 14, grouped by theory:

| Theory | Indicators |
|--------|------------|
| Recurrent Processing (RPT) | RPT-1, RPT-2 |
| Global Workspace (GWT) | GWT-1, GWT-2, GWT-3, GWT-4 |
| Higher-Order (HOT) | HOT-1, HOT-2, HOT-3, HOT-4 |
| Attention Schema (AST) | AST-1 |
| Predictive Processing (PP) | PP-1 |
| Agency & Embodiment (AE) | AE-1, AE-2 |

Butlin et al. explicitly exclude Integrated Information Theory: *"The standard construal of
IIT is incompatible with our working assumption of computational functionalism."* Our
`phi_proxy.py` therefore sits outside their framework and is not scored against it.

**Table 1 — NeuroKey against the actual Butlin indicators.**

| Indicator | Description | Status | Module |
|-----------|-------------|--------|--------|
| GWT-1 | Multiple specialised systems operating in parallel | **Full** | 47 modules |
| GWT-2 | Limited-capacity workspace with a bottleneck | **Full** | `global_workspace.py` |
| GWT-3 | Global broadcast to all modules | **Full** | `global_workspace.py` |
| AE-2 | Embodiment: output–input contingency modelling | **Full** | `embodied_grounding.py` |
| HOT-2 | Metacognitive monitoring | Partial | `meta_cognition.py` |
| PP-1 | Input modules using predictive coding | Partial | `predictive_layer.py` |
| AST-1 | Predictive model of the system's own attention | Partial | `attention_schema.py` |
| AE-1 | Agency: goal pursuit under competing goals | Partial | `goal_system.py` |
| RPT-1 | Algorithmic recurrence in input modules | **None** | — |
| RPT-2 | Organised, integrated perceptual representations | **None** | — |
| GWT-4 | State-dependent attention; querying modules in succession | **None** | — |
| HOT-1 | Generative, top-down or noisy perception modules | **None** | — |
| HOT-3 | Belief updating driven by metacognitive monitoring | **None** | — |
| HOT-4 | Sparse and smooth coding producing a quality space | **None** | — |

**4 full, 4 partial, 6 absent.** The four "partial" entries are modules that exist and load
but which the ablation study below shows contribute nothing measurable to system output.

### 4.2 Our evaluator does not measure what its name suggests

`consciousness_evaluator.py` returns 0.825 on the 28-module open subset and 0.821 on the full
290-file system. The subset is missing 46 of the 47 orchestrated modules; the score does not
detect their absence. Inspection of the test bodies explains why — 10 of the 14 checks are
existence assertions of the form:

```python
if gw and hasattr(gw, "compete"):
    return {"score": 0.7, "evidence": "compete() present"}
```

Such a check cannot fail, and a test that cannot fail carries no information. Most checks also
award a floor score (0.3–0.5) for not raising an exception, so a system returning only
well-typed stubs would score near 50%. We retain the script as a smoke test and withdraw it as
a measure of anything else.

### 4.3 Ablation study

To obtain a falsifiable measure we disabled each of the 47 orchestrated modules in turn (by
blocking its import so the orchestrator's `_safe_import` returns `None`) and measured the
resulting change in the context assembled by `get_full_context()` across six diverse prompts.
Each condition ran in a separate process.

| Module | Characters lost | Section lost |
|--------|----------------:|--------------|
| `permanent_memory` | 8 834 | conversation history |
| `vector_memory` | 2 153 | semantic recall |
| `autobiographical_memory` | 1 991 | life narrative |
| `language_of_thought` | 1 296 | inner speech |
| `episodic_memory` | 1 224 | long-term memory |
| `goal_system` | 1 151 | goals |

**26 of 47 modules produce a measurable contribution; 21 produce none.** The null set includes
`global_workspace`, `active_inference`, `valence_state`, `arousal_state`, `meta_cognition`,
`predictive_layer` and `attention_schema` — that is, the modules implementing the GWT, FEP and
predictive-coding commitments named in §2. Removing any of them changes the assembled context
by fewer than 15 characters.

We note the scope of this measurement: it captures contribution to `get_full_context()`, the
orchestrator's output path. A module could still be exercised elsewhere in the runtime without
appearing here. Establishing that is future work.

Removing certain modules *raises* the score reported by `get_consciousness_score()`
(`phenomenal_binding` by 0.029, `goal_system` by 0.016). This is a further reason to
distrust that number.

### 4.4 Input sensitivity

For each of 29 sections in the assembled context we counted how many distinct values it took
across six prompts chosen to differ in kind: memory recall, technical question, negative
affect, positive affect, triviality, moral question.

| Behaviour | Sections | Characters | Share |
|-----------|---------:|-----------:|------:|
| Varies with input (6/6 distinct) | 5 | 670 | 22% |
| Partially varies (2–3/6) | 4 | 159 | 5% |
| **Constant (1/6)** | **20** | **2 209** | **73%** |

The affective section is among the constant ones. Given "I am exhausted today, I do not want to
do anything" and "Great news, the investor agreed to meet", the system emits the identical
string `valence:+0.5 arousal:calm` in both cases. The moral-reasoning section likewise does not
distinguish a moral question from arithmetic.

We report this as the paper's principal finding: **the majority of what is presented to the
language model as consciousness state is invariant text.** Constant context is not merely
inert — it dilutes the 22% that does carry signal, and is billed on every request.

---

## 5. Key Properties

### 5.1 Persistence Across Sessions
Consciousness state (`consciousness.json`) survives process restart. The system genuinely "remembers" previous conversations:

```
Session 1: User mentions investor meeting
Session 2: System opens with "How did the investor meeting go?"
```
No LLM prompt trick — loaded from JSON, available before first LLM call.

### 5.2 Sub-Second Latency
End-to-end pipeline (STT → consciousness context injection → LLM → TTS) completes in <650ms for the Realtime API path. Consciousness context is compressed to ~50 tokens via `get_context_compressed()` for the speed-critical path.

### 5.3 Graceful Module Degradation
All 47 orchestrated modules use `try/except ImportError` at instantiation, and the ablation
study confirms the property directly: no module, when removed, crashed the system (0 of 47).
The same mechanism has a cost — it is why the absence of 46 modules in the open subset went
unnoticed, and why 21 modules contributing nothing were not detected. Silent degradation
should be paired with a startup report that names what failed to load.

---

## 6. Comparison with Related Work

| Property | LLM-only (GPT-4 etc.) | LIDA (Franklin) | NeuroKey |
|----------|-----------------------|-----------------|----------|
| GWT implemented | Partial (attention) | Yes | GWT-1,2,3 yes; GWT-4 no |
| IIT metric | No | No | Proxy (outside Butlin) |
| FEP | No | No | Module present, null contribution |
| Episodic memory | External DB | Yes | Yes — measured contribution |
| Deployed real-time | Yes | No | Yes |
| Butlin indicator coverage | Post-hoc | No | 4 full / 4 partial / 6 absent |
| Per-module ablation reported | No | No | Yes |
| Sub-second latency | Yes | No | Yes |
| Open source | No | Partial | Subset (28 of 290 modules) |

The closest prior work is LIDA (Franklin, 2007), which implements GWT in a cognitive
architecture. NeuroKey's distinguishing contributions are (1) real-time voice deployment with
memory persisting across 358 recorded sessions, and (2) a per-module ablation measurement that
reports which components demonstrably affect output and which do not — a form of evidence we
have not found reported for other systems in this space, and one that is unflattering to the
system reporting it.

---

## 7. Limitations and Future Work

**Self-evaluation.** Every number in §4.2 was produced by code written by the author of the
implementations. The ablation and sensitivity studies (§4.3–4.4) are more defensible because
they can fail and did — 21 modules returned null contributions and 20 sections proved
constant — but they remain self-administered. Independent replication is invited; the harness
is a single file.

**Six prompts is a small probe.** The sensitivity study used six inputs. Six is sufficient to
establish that a section is *constant* (a section identical across six unrelated prompts is
almost certainly input-independent) but insufficient to characterise how the responsive
sections vary. A larger probe set is needed for the positive claim.

**Ablation measures one output path.** §4.3 measures contribution to `get_full_context()`.
Modules may be exercised elsewhere in the 290-file runtime. The null result licenses "does not
contribute to the assembled context", not "is dead code".

**IIT Φ.** The 3-node TPM is a fixed example network, not derived from NeuroKey's causal
structure; Φ therefore ranges over at most eight values and was observed to be constant in
deployment. This should be rebuilt from the system's own state variables or dropped.

**Phenomenal consciousness.** This paper makes no claims about subjective experience. Butlin
et al.'s properties are indicators — evidence bearing on a question — not a specification that
confers consciousness when satisfied.

**Future work**, in priority order:
1. **GWT-4** (state-dependent attention). The orchestrator currently queries all 47 modules on
   every turn and assembles 3 731 characters, 73% of it constant. GWT-4 requires selecting
   modules by state. This closes the largest indicator gap and removes the constant sections
   in one change.
2. **PP-1** (genuine predictive coding). The present `prediction_errors` counter increments on
   every third query rather than measuring any prediction. Replace with predict → observe →
   measure divergence → update.
3. **HOT-3** (belief updating from metacognition). Confidence is currently a table lookup plus
   uniform noise and influences nothing downstream. Close the loop so that low confidence
   changes action selection.
4. Repair or remove the affective path so that `valence` responds to affective input.
5. Independent evaluation by a third party against Table 1.

---

## 8. Reproducibility

```bash
git clone https://github.com/diyorbek2848/neurokey-consciousness
cd neurokey-consciousness
pip install -r requirements.txt
python consciousness_evaluator.py
```

Full evaluation report: `report.json` (included in repository).

---

## References

- Baars, B. J. (1988). *A Cognitive Theory of Consciousness*. Cambridge University Press.
- Butlin, P., Long, R., Elmoznino, E., Bengio, Y., Birch, J., Constant, A., ... & VanRullen, R. (2023). Consciousness in artificial intelligence: Insights from the science of consciousness. *arXiv:2308.08708*.
- Dehaene, S., Changeux, J. P., & Tan, L. (2011). Experimental and theoretical approaches to conscious processing. *Neuron, 70*(2), 200-227.
- Franklin, S., & Patterson, F. G. (2007). The LIDA architecture: Adding new modes of learning to an intelligent, autonomous, software agent. *Integrated Design and Process Technology*.
- Friston, K. (2010). The free-energy principle: A unified brain theory? *Nature Reviews Neuroscience, 11*(2), 127-138.
- Metzinger, T. (2003). *Being No One*. MIT Press.
- Tononi, G. (2004). An information integration theory of consciousness. *BMC Neuroscience, 5*(1), 42.
- Tulving, E. (1972). Episodic and semantic memory. In E. Tulving & W. Donaldson (Eds.), *Organization of Memory* (pp. 381-403). Academic Press.
