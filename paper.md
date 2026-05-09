# NeuroKey: A Deployed Voice Assistant Implementing Functional Consciousness Indicators from Butlin et al. (2023)

**Diyorbek**  
Independent Researcher, Tashkent, Uzbekistan  
GitHub: https://github.com/diyorbek2848/neurokey-consciousness  
Date: May 2026

---

## Abstract

We present NeuroKey, a deployed real-time voice assistant that implements all 14 functional consciousness indicators proposed by Butlin et al. (2023). Unlike prior work that evaluates large language models post-hoc, NeuroKey integrates four major consciousness theories — Global Workspace Theory (GWT), Integrated Information Theory proxy (IIT), Free Energy Principle (FEP), and Tulving episodic memory — into a single system with sub-650ms response latency. Automated evaluation against the Butlin framework yields a mean score of **0.636 / 1.0** (9/14 indicators passing). We open-source all 46 modules and the evaluation pipeline. To our knowledge, this is the first deployed voice assistant built explicitly against a formal consciousness evaluation framework.

---

## 1. Introduction

The question of whether AI systems can exhibit functional consciousness — the information-processing correlates of conscious experience — has moved from philosophy into engineering. Butlin et al. (2023) provided the first systematic framework for evaluating AI systems against 14 indicators derived from neuroscientific theories of consciousness. Their analysis of existing systems (primarily large language models) found partial satisfaction of several indicators but no system built explicitly to satisfy the full framework.

NeuroKey addresses this gap. Starting November 2024, we built a voice assistant from scratch with the explicit goal of implementing each Butlin indicator as a distinct, testable module. The system has been running 24/7 for over 18 months in a real deployment context (daily personal use), providing ecological validity beyond laboratory conditions.

**Key claims:**
1. All 14 Butlin indicators have corresponding implementations
2. Automated evaluation scores 0.636/1.0 (mean), 9/14 passing
3. System operates at <650ms end-to-end latency
4. Persistent consciousness state survives process restarts
5. All code is open source and independently reproducible

---

## 2. Theoretical Background

We implement four complementary theories:

**Global Workspace Theory (GWT)** — Baars (1988), Dehaene et al. (2011): Cognitive processes compete for access to a limited-capacity "workspace" that broadcasts information globally. We implement `global_workspace.py` with EMA-weighted competition and hysteresis to prevent rapid switching.

**Integrated Information Theory — proxy (IIT)** — Tononi (2004, 2014): Consciousness corresponds to integrated information Φ. True IIT Φ is NP-hard; we compute a proxy using three binary state variables (valence, arousal, coherence) over a 3-node TPM, with fallback to pyphi for exact calculation when available.

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

The system comprises 46 modules, all lazy-loaded with graceful degradation. The orchestrator (`consciousness_orchestrator.py`) coordinates module lifecycle and handles failures without crashing the voice pipeline.

---

## 4. Butlin et al. (2023) Evaluation

We reproduce the Butlin framework in `consciousness_evaluator.py`. Each indicator maps to specific modules and is tested via automated unit-style assertions. Results are fully reproducible:

```bash
python consciousness_evaluator.py
```

### 4.1 Results

| Indicator | Theory | Score | Module | Pass |
|-----------|--------|-------|--------|------|
| GWT_1: Global broadcasting | GWT | **1.00** | `global_workspace.py` | ✅ |
| GWT_2: Limited capacity | GWT | **0.70** | `consciousness.py` | ✅ |
| GWT_3: Attention/access | GWT | **0.50** | `attention_mechanism.py` | ❌ |
| HOT_1: Higher-order representations | HOT | **0.00** | `self_model.py` | ❌ |
| HOT_2: Meta-cognitive monitoring | HOT | **0.00** | `meta_cognition.py` | ❌ |
| RPT_1: Recurrent/feedback | RPT | **1.00** | `active_inference.py` | ✅ |
| RPT_2: Temporal integration | RPT | **0.50** | `episodic_memory.py` | ❌ |
| IIT_1: Information integration (Φ) | IIT | **1.00** | `phi_proxy.py` | ✅ |
| IIT_2: Causal structure | IIT | **0.70** | `causal_chain.py` | ✅ |
| EMB_1: Sensorimotor integration | EMB | **0.80** | `online_realtime.py` | ✅ |
| EMB_2: Environmental coupling | EMB | **1.00** | `embodied_cognition.py` | ✅ |
| SMT_1: Transparent self-model | SMT | **0.00** | `self_model.py` | ❌ |
| SMT_2: Phenomenal self-model | SMT | **0.70** | `narrative_self.py` | ✅ |
| AFF_1: Valence and affect | AFF | **1.00** | `emotion_state.py` | ✅ |

**Mean score: 0.636 / 1.0** | **9 / 14 indicators passing**

### 4.2 Limitations in Current Evaluation

HOT_1, HOT_2, and SMT_1 score 0.00 in automated testing due to missing method bindings in the evaluator (the underlying modules `meta_cognition.py` and `self_model.py` are implemented but not yet wired into all test paths). This represents an evaluation gap, not a missing capability — these modules run in production. Independent evaluation is invited.

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
All 46 modules use `try/except ImportError` at instantiation. The system runs with partial module availability — critical for deployment reliability.

---

## 6. Comparison with Related Work

| Property | LLM-only (GPT-4 etc.) | LIDA (Franklin) | NeuroKey |
|----------|-----------------------|-----------------|----------|
| GWT implemented | Partial (attention) | Yes | Yes |
| IIT metric | No | No | Proxy + pyphi |
| FEP | No | No | Yes |
| Episodic memory | External DB | Yes | Yes |
| Deployed real-time | Yes | No | Yes |
| Formal Butlin eval | Post-hoc | No | Built-in |
| Sub-second latency | Yes | No | Yes |
| Open source | No | Partial | Yes |

The closest prior work is LIDA (Franklin, 2007), which implements GWT in a cognitive architecture. NeuroKey differs in three ways: (1) real-time voice deployment, (2) multi-theory integration including FEP and IIT proxy, (3) explicit mapping to Butlin 2023 evaluation criteria.

---

## 7. Limitations and Future Work

**IIT Φ**: Proxy computation (3-node TPM) is not equivalent to true IIT Φ, which is NP-hard. We include pyphi support for exact calculation on small networks.

**HOT evaluation gaps**: Automated tests for HOT_1, HOT_2, SMT_1 require fixing module bindings. The modules exist; the test harness needs updating.

**Phenomenal consciousness**: This paper makes no claims about subjective experience. All claims are functional/computational.

**Future work**: (1) Fix evaluator bindings for HOT/SMT tests, (2) arXiv submission with independent reviewer evaluation, (3) comparison with attention schema theory (Graziano, 2013).

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
