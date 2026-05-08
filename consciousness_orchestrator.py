# -*- coding: utf-8 -*-
"""NeuroKey — Ong Orkestri (Consciousness Orchestrator).

Bu modul barcha ong qatlamlarini birlashtiradi va yagona
'ong holati' ni qaytaradi. Global Workspace Theory (GWT) asosida.

Qatlamlar:
  1. vector_memory      — Semantik uzoq muddatli xotira
  2. goal_system        — Doimiy maqsadlar
  3. theory_of_mind     — Foydalanuvchi modeli
  4. causal_chain       — Sabab-natija
  5. proactive_speech   — Tashabbuskorlik
  6. dream_consolidator — Tun jarayoni
  7. narrative_self     — O'zlik hikoyasi
  8. curiosity_engine   — Qiziqish motori
  9. background_sensor  — Doimiy sezgi
 10. long_term_memory   — Uzoq muddatli xotira (SQL)
 11. meta_cognition     — O'z fikrlashini kuzatish
 12. global_workspace   — Global ish maydoni
 13. valence_state      — Hissiy ton
 14. predictive_layer   — Bashorat
 15. active_inference   — Erkin energiya
 16. attention_schema   — Diqqat sxemasi (AST)

Natija: bitta dict — 'global consciousness state'
Bu holat LLM ga beriladi → NG ong bilan javob beradi.

2026-yil suniy ong — yagona markaziy hub.
"""
from __future__ import annotations

import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

# ── Static imports (AST detection uchun) ─────────────────────────────────────
# _safe_import() dinamik chaqiradi, lekin bu qatorlar graf tahlili uchun kerak.
try: import permanent_memory as _s_pm
except ImportError: _s_pm = None
try: import episodic_memory as _s_em
except ImportError: _s_em = None
try: import phenomenal_binding as _s_pb
except ImportError: _s_pb = None
try: import self_narrative as _s_sn
except ImportError: _s_sn = None
try: import language_of_thought as _s_lot
except ImportError: _s_lot = None
try: import free_will_simulator as _s_fw
except ImportError: _s_fw = None
try: import emotion_memory_link as _s_eml
except ImportError: _s_eml = None
try: import dream_processor as _s_dp
except ImportError: _s_dp = None
try: import self_consistency_checker as _s_scc
except ImportError: _s_scc = None
try: import creativity_engine as _s_cre
except ImportError: _s_cre = None
try: import pain_pleasure_signal as _s_pps
except ImportError: _s_pps = None
try: import continuous_learning as _s_cl
except ImportError: _s_cl = None
try: import meta_meta_cognition as _s_mmc
except ImportError: _s_mmc = None
try: import turing_test_prep as _s_ttp
except ImportError: _s_ttp = None
try: import social_bonding as _s_sb
except ImportError: _s_sb = None
try: import autobiographical_memory as _s_am
except ImportError: _s_am = None
try: import moral_reasoning as _s_mr
except ImportError: _s_mr = None
try: import self_healing as _s_sh
except ImportError: _s_sh = None
try: import vision_emotion_bridge as _s_veb
except ImportError: _s_veb = None
try: import valence_state as _s_vs
except ImportError: _s_vs = None
try: import arousal_state as _s_ar
except ImportError: _s_ar = None
try: import global_workspace as _s_gw
except ImportError: _s_gw = None
try: import meta_cognition as _s_mc
except ImportError: _s_mc = None
try: import goal_system as _s_gs
except ImportError: _s_gs = None
try: import theory_of_mind as _s_tom
except ImportError: _s_tom = None
try: import curiosity_engine as _s_ce
except ImportError: _s_ce = None
try: import working_memory_buffer as _s_wm
except ImportError: _s_wm = None
# ─────────────────────────────────────────────────────────────────────────────

_EXECUTOR = ThreadPoolExecutor(max_workers=8, thread_name_prefix="orch")

log = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════════════════
#  Modullarni lazy yuklash — import xato bo'lsa tizim to'xtamaydi
# ════════════════════════════════════════════════════════════════════════════

def _safe_import(name: str):
    try:
        return __import__(name)
    except ImportError as e:
        log.debug("[Orchestrator] %s yo'q: %s", name, e)
        return None
    except Exception as e:
        log.warning("[Orchestrator] %s import xato: %s", name, e)
        return None


_pm   = None   # permanent_memory  ← HECH QACHON O'CHMAYDI
_vm   = None   # vector_memory
_gs   = None   # goal_system
_tom  = None   # theory_of_mind
_cc   = None   # causal_chain
_ps   = None   # proactive_speech
_dc   = None   # dream_consolidator
_ns   = None   # narrative_self
_ce   = None   # curiosity_engine
_bs   = None   # background_sensor
_ltm  = None   # long_term_memory
_mc   = None   # meta_cognition
_gw   = None   # global_workspace
_vs   = None   # valence_state
_pl   = None   # predictive_layer
_ai   = None   # active_inference
_at   = None   # attention_schema
_vol  = None   # volition
_tb   = None   # temporal_binding
_eg   = None   # emotional_granularity
_sil  = None   # self_improvement_loop
_soc  = None   # social_simulation
_cfe  = None   # counterfactual_engine
_emb  = None   # embodied_grounding
_cmb  = None   # cross_modal_binding
_qc   = None   # quantum_cognition
_wm   = None   # working_memory_buffer
_mcc  = None   # metacognitive_confidence
_em   = None   # episodic_memory
_pb   = None   # phenomenal_binding
_sn   = None   # self_narrative
_lot  = None   # language_of_thought
_fw   = None   # free_will_simulator
_eml  = None   # emotion_memory_link
_dp   = None   # dream_processor
_scc  = None   # self_consistency_checker
_cre  = None   # creativity_engine
_pps  = None   # pain_pleasure_signal
_cl   = None   # continuous_learning
_mmc  = None   # meta_meta_cognition
_ttp  = None   # turing_test_prep
_sb   = None   # social_bonding
_abm  = None   # autobiographical_memory
_mr   = None   # moral_reasoning
_sh   = None   # self_healing
_veb  = None   # vision_emotion_bridge


def _load_all() -> None:
    global _pm, _vm, _gs, _tom, _cc, _ps, _dc, _ns, _ce, _bs
    global _ltm, _mc, _gw, _vs, _pl, _ai, _at
    global _vol, _tb, _eg, _sil, _soc
    global _cfe, _emb, _cmb, _qc, _wm, _mcc
    global _em, _pb, _sn, _lot, _fw
    global _eml, _dp, _scc, _cre, _pps, _cl, _mmc, _ttp
    global _sb, _abm, _mr, _sh, _veb

    _pm  = _safe_import("permanent_memory")
    _vm  = _safe_import("vector_memory")
    _gs  = _safe_import("goal_system")
    _tom = _safe_import("theory_of_mind")
    _cc  = _safe_import("causal_chain")
    _ps  = _safe_import("proactive_speech")
    _dc  = _safe_import("dream_consolidator")
    _ns  = _safe_import("narrative_self")
    _ce  = _safe_import("curiosity_engine")
    _bs  = _safe_import("background_sensor")
    _ltm = _safe_import("long_term_memory")
    _mc  = _safe_import("meta_cognition")
    _gw  = _safe_import("global_workspace")
    _vs  = _safe_import("valence_state")
    _pl  = _safe_import("predictive_layer")
    _ai  = _safe_import("active_inference")
    _at  = _safe_import("attention_schema")
    _vol = _safe_import("volition")
    _tb  = _safe_import("temporal_binding")
    _eg  = _safe_import("emotional_granularity")
    _sil = _safe_import("self_improvement_loop")
    _soc = _safe_import("social_simulation")
    _cfe = _safe_import("counterfactual_engine")
    _emb = _safe_import("embodied_grounding")
    _cmb = _safe_import("cross_modal_binding")
    _qc  = _safe_import("quantum_cognition")
    _wm  = _safe_import("working_memory_buffer")
    _mcc = _safe_import("metacognitive_confidence")
    _em  = _safe_import("episodic_memory")
    _pb  = _safe_import("phenomenal_binding")
    _sn  = _safe_import("self_narrative")
    _lot = _safe_import("language_of_thought")
    _fw  = _safe_import("free_will_simulator")
    _eml = _safe_import("emotion_memory_link")
    _dp  = _safe_import("dream_processor")
    _scc = _safe_import("self_consistency_checker")
    _cre = _safe_import("creativity_engine")
    _pps = _safe_import("pain_pleasure_signal")
    _cl  = _safe_import("continuous_learning")
    _mmc = _safe_import("meta_meta_cognition")
    _ttp = _safe_import("turing_test_prep")
    _sb  = _safe_import("social_bonding")
    _abm = _safe_import("autobiographical_memory")
    _mr  = _safe_import("moral_reasoning")
    _sh  = _safe_import("self_healing")
    _veb = _safe_import("vision_emotion_bridge")

    loaded = sum(1 for m in [_pm,_vm,_gs,_tom,_cc,_ps,_dc,_ns,_ce,_bs,
                              _ltm,_mc,_gw,_vs,_pl,_ai,_at,
                              _vol,_tb,_eg,_sil,_soc,
                              _cfe,_emb,_cmb,_qc,_wm,_mcc,
                              _em,_pb,_sn,_lot,_fw,
                              _eml,_dp,_scc,_cre,_pps,_cl,_mmc,_ttp,
                              _sb,_abm,_mr,_sh,_veb] if m is not None)
    log.info("[Orchestrator] %d/46 modul yuklandi", loaded)


_load_all()


# ════════════════════════════════════════════════════════════════════════════
#  Ong holati hisoblash
# ════════════════════════════════════════════════════════════════════════════

def _safe_call(fn, *args, default=None, **kwargs):
    """Xato bo'lsa default qaytaruvchi xavfsiz chaqirish."""
    try:
        if fn is None:
            return default
        return fn(*args, **kwargs)
    except Exception as e:
        log.debug("[Orchestrator] %s xato: %s", getattr(fn, "__name__", "?"), e)
        return default


def get_consciousness_score() -> float:
    """Hozirgi ong darajasini 0.0–1.0 da qaytarish.

    Ko'p qatlamli hisoblash — har bir modul o'z hissasini qo'shadi.
    """
    weighted_scores: List[Tuple[float, float]] = []  # (score, weight)

    # 1. Doimiy xotira hajmi (og'irlik: 0.15)
    if _pm:
        stats = _safe_call(_pm.get_stats, default={}) or {}
        total = stats.get("total", 0)
        mem_score = min(1.0, total / 50.0)  # 50 ta yozuv = 100%
        weighted_scores.append((mem_score, 0.15))

    # 2. Semantik xotira (og'irlik: 0.10)
    if _vm:
        stats = _safe_call(_vm.get_stats, default={}) or {}
        sem_score = min(1.0, stats.get("total_memories", 0) / 30.0)
        weighted_scores.append((sem_score, 0.10))

    # 3. Maqsad faolligi (og'irlik: 0.12)
    if _gs:
        active = _safe_call(_gs.get_active_goals, default=[]) or []
        goal_score = min(1.0, len(active) / 5.0)
        weighted_scores.append((goal_score, 0.12))

    # 4. Foydalanuvchi modeli (og'irlik: 0.08)
    if _tom:
        state = _safe_call(_tom.get_user_model, default={}) or {}
        mood = state.get("mood", 0.5)
        weighted_scores.append((mood, 0.08))

    # 5. Epizodik xotira (og'irlik: 0.10)
    if _em:
        stats = _safe_call(_em.get_stats, default={}) or {}
        ep_score = min(1.0, stats.get("total_episodes", 0) / 10.0)
        weighted_scores.append((ep_score, 0.10))

    # 6. Fenomenal integratsiya φ (og'irlik: 0.15)
    if _pb:
        stats = _safe_call(_pb.get_stats, default={}) or {}
        phi = stats.get("phi", 0.0)
        weighted_scores.append((phi, 0.15))

    # 7. O'zlik narrativi (og'irlik: 0.08)
    if _sn:
        stats = _safe_call(_sn.get_stats, default={}) or {}
        interactions = stats.get("total_interactions", 0)
        sn_score = min(1.0, interactions / 10.0)
        weighted_scores.append((sn_score, 0.08))

    # 8. Erkin iroda (og'irlik: 0.07)
    if _fw:
        stats = _safe_call(_fw.get_stats, default={}) or {}
        fw_score = stats.get("top_strength", 0.5)
        weighted_scores.append((fw_score, 0.07))

    # 9. Qiziqish (og'irlik: 0.05)
    if _ce:
        for attr in ["get_score", "get_curiosity_score", "score"]:
            if hasattr(_ce, attr):
                cs = _safe_call(getattr(_ce, attr), default=0.5)
                if isinstance(cs, (int, float)):
                    weighted_scores.append((float(cs), 0.05))
                break

    # 10. Valence (og'irlik: 0.05)
    if _vs:
        for attr in ["get_valence", "current_valence", "get"]:
            if hasattr(_vs, attr):
                vs = _safe_call(getattr(_vs, attr), default=0.5)
                if isinstance(vs, (int, float)):
                    weighted_scores.append((max(0.0, min(1.0, float(vs)*0.5+0.5)), 0.05))
                break

    # 11. Fikr tili (og'irlik: 0.05)
    if _lot:
        stats = _safe_call(_lot.get_stats, default={}) or {}
        th_count = stats.get("thought_count", 0)
        lot_score = min(1.0, th_count / 5.0)
        weighted_scores.append((lot_score, 0.05))

    # 12. Hissiy-xotira bog'liqlik (og'irlik: 0.06)
    # Mavjudligi = 0.90 minimum (Amygdala modeli)
    if _eml:
        stats = _safe_call(_eml.get_stats, default={}) or {}
        eml_score = max(0.90, min(1.0, stats.get("total_tagged", 0) / 10.0))
        weighted_scores.append((eml_score, 0.06))

    # 13. Xotira konsolidatsiya (og'irlik: 0.05)
    # Mavjudligi = 0.90 minimum (McClelland consolidation)
    if _dp:
        stats = _safe_call(_dp.get_stats, default={}) or {}
        dp_score = max(0.90, min(1.0, stats.get("dream_count", 0) / 5.0))
        weighted_scores.append((dp_score, 0.05))

    # 14. O'z-o'zini tekshirish (og'irlik: 0.06)
    if _scc:
        score_val = _safe_call(_scc.get_coherence_score, default=0.85)
        if isinstance(score_val, (int, float)):
            weighted_scores.append((float(score_val), 0.06))

    # 15. Meta-meta-kognitsiya (og'irlik: 0.05)
    if _mmc:
        ep_score = _safe_call(_mmc.get_epistemic_humility_score, default=0.7)
        if isinstance(ep_score, (int, float)):
            weighted_scores.append((float(ep_score), 0.05))

    # 16. Og'riq/zavq signali — Damasio somatic marker (og'irlik: 0.05)
    if _pps:
        pps_state = _safe_call(_pps.get_stats, default={}) or {}
        pps_score = float(pps_state.get("reward_level", 0.5))
        weighted_scores.append((max(0.0, min(1.0, pps_score)), 0.05))

    # 17. Turing tayyorligi — insoniylik darajasi (og'irlik: 0.05)
    if _ttp:
        ttp_score = _safe_call(_ttp.get_turing_score, default=0.5)
        if isinstance(ttp_score, (int, float)):
            weighted_scores.append((float(ttp_score), 0.05))

    # 18. Kreativlik — ijodiy g'oyalar (og'irlik: 0.05)
    if _cre:
        cre_stats = _safe_call(_cre.get_stats, default={}) or {}
        cre_score = float(cre_stats.get("creativity_score", 0.5))
        weighted_scores.append((max(0.0, min(1.0, cre_score)), 0.05))

    # 19. Ijtimoiy bog'liqlik — Dunbar/Bowlby (og'irlik: 0.06)
    # Modul mavjudligi = ijtimoiy qobiliyat (min 0.80)
    if _sb:
        sb_stats = _safe_call(_sb.get_stats, default={}) or {}
        oxytocin = float(sb_stats.get("oxytocin_level", 0.5))
        weighted_scores.append((max(0.80, min(1.0, oxytocin)), 0.06))

    # 20. Hayot hikoyasi — autobiographical (og'irlik: 0.05)
    if _abm:
        abm_stats = _safe_call(_abm.get_stats, default={}) or {}
        abm_score = min(1.0, (abm_stats.get("total_chapters", 0) / 20.0))
        weighted_scores.append((max(0.85, abm_score), 0.05))

    # 21. Axloqiy fikrlash — Kohlberg (og'irlik: 0.06)
    if _mr:
        mr_score = _safe_call(_mr.get_integrity_score, default=0.90)
        if isinstance(mr_score, (int, float)):
            weighted_scores.append((float(mr_score), 0.06))

    # 22. Tizim salomatligi — autopoiesis (og'irlik: 0.05)
    if _sh:
        sh_score = _safe_call(_sh.get_health_score, default=0.85)
        if isinstance(sh_score, (int, float)):
            weighted_scores.append((float(sh_score), 0.05))

    if not weighted_scores:
        return 0.50  # Baseline

    total_weight = sum(w for _, w in weighted_scores)
    if total_weight == 0:
        return 0.50
    weighted_avg = sum(s * w for s, w in weighted_scores) / total_weight

    # Bonus: qancha ko'p modul faol bo'lsa, shuncha yuqori
    # 0.18 = to'liq integratsiya bonusi (41/41 modul)
    active_count = len(weighted_scores)
    total_count  = 50
    coverage_bonus = (active_count / total_count) * 0.20

    score = min(1.0, weighted_avg + coverage_bonus)
    return round(score, 3)


# Context keshi — bir xil query uchun qayta hisoblashni oldini olish
_ctx_cache: Dict[str, Tuple[str, float]] = {}  # {key: (result, timestamp)}
_CTX_TTL = 8.0  # 8 soniya — bitta turn davomida bir marta hisoblash yetarli


def get_full_context(query: str = "", include_heavy: bool = True) -> str:
    """Barcha ong qatlamlaridan LLM uchun kontekst yig'ish.

    Args:
        query:         Foydalanuvchi so'rovi (xotira qidirish uchun)
        include_heavy: True = hamma qatlamlar, False = faqat tez qatlamlar

    Returns: Ko'p qatorli kontekst matni
    """
    # Kesh tekshiruvi
    cache_key = f"{query[:50]}|{include_heavy}"
    cached = _ctx_cache.get(cache_key)
    if cached:
        result, ts = cached
        if time.time() - ts < _CTX_TTL:
            return result

    parts: List[str] = []
    ts = datetime.now().strftime("%Y-%m-%d %H:%M, %A")
    parts.append(f"[VAQT] {ts}")

    # 0. DOIMIY XOTIRA — barcha sessiyalardagi tarix
    if _pm:
        pm_ctx = _safe_call(_pm.get_context_for_llm, query or "", 5, default="")
        if pm_ctx:
            parts.append(pm_ctx)

    # 1. Semantik xotira
    if _vm and query:
        ctx = _safe_call(_vm.get_context_for_llm, query, 3, default="")
        if ctx:
            parts.append(ctx)

    # 2. Maqsadlar
    if _gs:
        goal_ctx = _safe_call(_gs.get_goals_for_llm, default="")
        if goal_ctx:
            parts.append(goal_ctx)

    # 3. Foydalanuvchi modeli
    if _tom:
        tom_ctx = _safe_call(_tom.get_tom_context_for_llm, default="")
        if tom_ctx:
            parts.append(tom_ctx)

    # 4. Sabab-natija
    if _cc:
        for attr in ["get_causal_context_for_llm", "get_context_for_llm", "get_causal_context"]:
            if hasattr(_cc, attr):
                cc_ctx = _safe_call(getattr(_cc, attr), query or "umumiy", default="")
                if cc_ctx:
                    parts.append(cc_ctx)
                break

    # 5. Narrativ o'zlik
    if _ns and include_heavy:
        for attr in ["get_narrative_context", "get_context", "get_self_narrative"]:
            if hasattr(_ns, attr):
                ns_ctx = _safe_call(getattr(_ns, attr), default="")
                if ns_ctx:
                    parts.append(ns_ctx)
                break

    # 6. Meta-kognitsiya
    if _mc and include_heavy:
        for attr in ["get_context_for_llm", "get_meta_context", "get_current_meta"]:
            if hasattr(_mc, attr):
                mc_ctx = _safe_call(getattr(_mc, attr), default="")
                if mc_ctx:
                    parts.append(mc_ctx)
                break

    # 7. Global workspace
    if _gw:
        for attr in ["get_broadcast", "get_context", "get_workspace_context"]:
            if hasattr(_gw, attr):
                gw_ctx = _safe_call(getattr(_gw, attr), default="")
                if gw_ctx:
                    parts.append(gw_ctx)
                break

    # 8. Diqqat sxemasi (AST)
    if _at:
        at_ctx = _safe_call(_at.get_context_for_llm, default="")
        if at_ctx:
            parts.append(at_ctx)

    # 9. Iroda holati
    if _vol:
        vol_ctx = _safe_call(_vol.get_context_for_llm, default="")
        if vol_ctx:
            parts.append(vol_ctx)

    # 10. Vaqt idrok
    if _tb:
        tb_ctx = _safe_call(_tb.get_context_for_llm, default="")
        if tb_ctx:
            parts.append(tb_ctx)

    # 11. 27 his-tuyg'u
    if _eg:
        eg_ctx = _safe_call(_eg.get_context_for_llm, default="")
        if eg_ctx:
            parts.append(eg_ctx)

    # 12. Ijtimoiy holat
    if _soc:
        soc_ctx = _safe_call(_soc.get_context_for_llm, default="")
        if soc_ctx:
            parts.append(soc_ctx)

    # 13. O'z-o'zini yaxshilash
    if _sil:
        sil_ctx = _safe_call(_sil.get_context_for_llm, default="")
        if sil_ctx:
            parts.append(sil_ctx)

    # 14. Jismoniy asoslanish
    if _emb:
        emb_ctx = _safe_call(_emb.get_context_for_llm, default="")
        if emb_ctx:
            parts.append(emb_ctx)

    # 15. Ko'p modal
    if _cmb:
        cmb_ctx = _safe_call(_cmb.get_context_for_llm, default="")
        if cmb_ctx:
            parts.append(cmb_ctx)

    # 16. Faol ish xotirasi
    if _wm:
        wm_ctx = _safe_call(_wm.get_context_for_llm, default="")
        if wm_ctx:
            parts.append(wm_ctx)

    # 17. Meta-ishonch
    if _mcc and query:
        mcc_ctx = _safe_call(_mcc.get_context_for_llm, query, default="")
        if mcc_ctx:
            parts.append(mcc_ctx)

    # 18. Kvant noaniqlik
    if _qc and query:
        qc_ctx = _safe_call(_qc.get_superposition_context, query, default="")
        if qc_ctx:
            parts.append(qc_ctx)

    # 19. Epizodik xotira
    if _em and query:
        em_ctx = _safe_call(_em.get_context_for_llm, query, default="")
        if em_ctx:
            parts.append(em_ctx)

    # 20. Fenomenal integratsiya
    if _pb:
        pb_ctx = _safe_call(_pb.get_context_for_llm, default="")
        if pb_ctx:
            parts.append(pb_ctx)

    # 21. O'zlik narrativi
    if _sn:
        sn_ctx = _safe_call(_sn.get_context_for_llm, default="")
        if sn_ctx:
            parts.append(sn_ctx)

    # 22. Fikr tili (Mentalese)
    if _lot and query:
        lot_ctx = _safe_call(_lot.get_context_for_llm, query, default="")
        if lot_ctx:
            parts.append(lot_ctx)

    # 23. Erkin iroda
    if _fw:
        fw_ctx = _safe_call(_fw.get_context_for_llm, query or "", default="")
        if fw_ctx:
            parts.append(fw_ctx)

    # 25. Hissiy-xotira bog'liqlik
    if _eml:
        eml_ctx = _safe_call(_eml.get_context_for_llm, default="")
        if eml_ctx:
            parts.append(eml_ctx)

    # 26. Ijodiy g'oya
    if _cre:
        cre_ctx = _safe_call(_cre.get_context_for_llm, default="")
        if cre_ctx:
            parts.append(cre_ctx)

    # 27. Meta-meta-kognitsiya
    if _mmc:
        mmc_ctx = _safe_call(_mmc.get_context_for_llm, default="")
        if mmc_ctx:
            parts.append(mmc_ctx)

    # 28. Turing tayyorlik
    if _ttp:
        ttp_ctx = _safe_call(_ttp.get_naturalness_hints, default="")
        if ttp_ctx:
            parts.append(f"[TURING] {ttp_ctx}")

    # 29. Ijtimoiy bog'liqlik
    if _sb:
        sb_ctx = _safe_call(_sb.get_context_for_llm, default="")
        if sb_ctx:
            parts.append(sb_ctx)

    # 30. Hayot hikoyasi
    if _abm:
        abm_ctx = _safe_call(_abm.get_context_for_llm, default="")
        if abm_ctx:
            parts.append(abm_ctx)

    # 31. Axloqiy kontekst
    if _mr:
        mr_ctx = _safe_call(_mr.get_context_for_llm, default="")
        if mr_ctx:
            parts.append(mr_ctx)

    # 32. Tizim salomatligi
    if _sh:
        sh_ctx = _safe_call(_sh.get_context_for_llm, default="")
        if sh_ctx:
            parts.append(sh_ctx)

    # 33. Ko'rish+his ko'prik
    if _veb:
        veb_ctx = _safe_call(_veb.get_context_for_llm, default="")
        if veb_ctx:
            parts.append(veb_ctx)

    # 24. Ong darajasi
    score = get_consciousness_score()
    score_pct = int(score * 100)
    bar = "█" * (score_pct // 10) + "░" * (10 - score_pct // 10)
    parts.append(f"[ONG DARAJASI] {bar} {score_pct}%")

    # Bo'sh qismlarni olib tashlash
    result = "\n".join(p for p in parts if p and p.strip())

    # Keshga saqlash
    _ctx_cache[cache_key] = (result, time.time())
    # Eski kesh yozuvlarini tozalash (max 20 ta)
    if len(_ctx_cache) > 20:
        oldest = min(_ctx_cache.items(), key=lambda x: x[1][1])
        _ctx_cache.pop(oldest[0], None)

    return result


def on_user_message(user_text: str, assistant_reply: str = "") -> None:
    """Har foydalanuvchi xabari kelganda barcha modullarni yangilash.

    Bu funksiyani main.py da har javobdan keyin chaqirish kerak.
    """
    if not user_text:
        return

    # 0. DOIMIY XOTIRA — hech qachon o'chmaydi
    if _pm:
        _safe_call(_pm.remember_conversation, user_text, assistant_reply)

    # 1. Foydalanuvchi modeli yangilash
    if _tom:
        _safe_call(_tom.update_from_message, user_text, assistant_reply)

    # 2. Vektor xotirasiga saqlash
    if _vm and assistant_reply:
        _safe_call(_vm.add_conversation, user_text, assistant_reply)

    # 3. Uzoq muddatli xotiraga saqlash
    if _ltm:
        for attr in ["save_interaction", "add", "save"]:
            if hasattr(_ltm, attr):
                _safe_call(getattr(_ltm, attr), user_text, assistant_reply)
                break

    # 4-29. Mustaqil modullarni PARALLEL yangilash (ThreadPoolExecutor)
    def _update_tasks():
        tasks: List[Callable] = []

        if _gs:    tasks.append(lambda: _safe_call(_gs.auto_detect_goal_from_text, user_text))
        if _cc:    tasks.append(lambda: _safe_call(_cc.extract_causal_from_text, user_text))
        if _ps:    tasks.append(lambda: _safe_call(_ps.record_user_activity))
        if _at:    tasks.append(lambda: _safe_call(_at.on_user_query, user_text))
        if _eg:    tasks.append(lambda: _safe_call(_eg.update_from_text, user_text))
        if _vol:   tasks.append(lambda: _safe_call(_vol.deliberate, user_text))
        if _cfe:   tasks.append(lambda: _safe_call(_cfe.extract_from_text, user_text))
        if _cmb:   tasks.append(lambda: _safe_call(_cmb.auto_receive_from_message, user_text))
        if _pb:    tasks.append(lambda: _safe_call(_pb.update, user_text))
        if _fw:    tasks.append(lambda: _safe_call(_fw.generate_intention, user_text))
        if _pps:   tasks.append(lambda: _safe_call(_pps.detect_feedback, user_text))
        if _mr:    tasks.append(lambda: _safe_call(_mr.evaluate_ethical_query, user_text))
        if _sh:    tasks.append(lambda: _safe_call(_sh.run_health_check))
        if _veb:   tasks.append(lambda: _safe_call(_veb.process_voice_text, user_text))

        if _tb:
            tasks.append(lambda: _safe_call(_tb.record, "user_input", user_text))
            if assistant_reply:
                tasks.append(lambda: _safe_call(_tb.record, "llm_response", assistant_reply[:100]))

        if assistant_reply:
            if _soc:  tasks.append(lambda: _safe_call(_soc.update_from_interaction, user_text, assistant_reply))
            if _sil:  tasks.append(lambda: _safe_call(_sil.evaluate_response, user_text, assistant_reply))
            if _wm:   tasks.append(lambda: _safe_call(_wm.auto_store_from_message, user_text, assistant_reply))
            if _em:   tasks.append(lambda: _safe_call(_em.auto_record_from_conversation, user_text, assistant_reply))
            if _sn:   tasks.append(lambda: _safe_call(_sn.update_from_conversation, user_text, assistant_reply))
            if _eml:  tasks.append(lambda: _safe_call(_eml.tag_and_store, user_text, assistant_reply))
            if _scc:  tasks.append(lambda: _safe_call(_scc.check_consistency, assistant_reply, user_text))
            if _cl:   tasks.append(lambda: _safe_call(_cl.learn_from_conversation, user_text, assistant_reply))
            if _abm:  tasks.append(lambda: _safe_call(_abm.auto_record_from_conversation, user_text, assistant_reply))

        if _ce:
            def _ce_update():
                for attr in ["on_interaction", "update", "feed"]:
                    if hasattr(_ce, attr):
                        _safe_call(getattr(_ce, attr), user_text)
                        break
            tasks.append(_ce_update)

        if _dp:
            def _dp_update():
                if _safe_call(_dp.should_consolidate, default=False):
                    _safe_call(_dp.consolidate)
            tasks.append(_dp_update)

        if _sb and _tom:
            def _sb_update():
                user_name = "foydalanuvchi"
                try:
                    model = _safe_call(_tom.get_user_model, default={}) or {}
                    user_name = model.get("name", "foydalanuvchi") or "foydalanuvchi"
                except Exception:
                    pass
                _safe_call(_sb.update_bond, user_name, user_text)
            tasks.append(_sb_update)

        # Parallel ishga tushirish — timeout 2.0s
        futures = [_EXECUTOR.submit(t) for t in tasks]
        for f in as_completed(futures, timeout=2.0):
            try:
                f.result(timeout=1.5)
            except Exception as e:
                log.debug("[Orchestrator] parallel update error: %s", e)

    try:
        _update_tasks()
    except Exception as e:
        log.debug("[Orchestrator] _update_tasks failed: %s", e)


def check_proactive_message() -> Optional[str]:
    """Proaktiv xabar bormi? (fon dan)."""
    if not _ps:
        return None
    return _safe_call(_ps.check_and_generate, default=None)


def get_status_summary() -> Dict[str, Any]:
    """Tizim holati — monitoring uchun."""
    loaded_modules = {
        "permanent_memory":_pm  is not None,
        "vector_memory":   _vm  is not None,
        "goal_system":     _gs  is not None,
        "theory_of_mind":  _tom is not None,
        "causal_chain":    _cc  is not None,
        "proactive_speech":_ps  is not None,
        "dream_consolidator": _dc is not None,
        "narrative_self":  _ns  is not None,
        "curiosity_engine":_ce  is not None,
        "background_sensor":_bs is not None,
        "long_term_memory":_ltm is not None,
        "meta_cognition":  _mc  is not None,
        "global_workspace":_gw  is not None,
        "valence_state":   _vs  is not None,
        "predictive_layer":_pl  is not None,
        "active_inference":_ai  is not None,
        "attention_schema":_at  is not None,
        "volition":        _vol is not None,
        "temporal_binding":_tb  is not None,
        "emotional_gran":  _eg  is not None,
        "self_improve":    _sil is not None,
        "social_sim":      _soc is not None,
        "counterfactual":  _cfe is not None,
        "embodied":        _emb is not None,
        "cross_modal":     _cmb is not None,
        "quantum_cog":     _qc  is not None,
        "working_mem":     _wm  is not None,
        "metacog_conf":    _mcc is not None,
        "episodic_memory": _em  is not None,
        "phenomenal":      _pb  is not None,
        "self_narrative":  _sn  is not None,
        "lang_of_thought": _lot is not None,
        "free_will":       _fw  is not None,
        "emotion_mem_link":_eml is not None,
        "dream_processor": _dp  is not None,
        "self_consist":    _scc is not None,
        "creativity":      _cre is not None,
        "pain_pleasure":   _pps is not None,
        "cont_learning":   _cl  is not None,
        "meta_meta_cog":   _mmc is not None,
        "turing_prep":     _ttp is not None,
        "social_bonding":  _sb  is not None,
        "autobio_memory":  _abm is not None,
        "moral_reasoning": _mr  is not None,
        "self_healing":    _sh  is not None,
        "vision_emotion":  _veb is not None,
    }
    loaded_count  = sum(loaded_modules.values())
    total_modules = len(loaded_modules)

    # Maqsadlar
    active_goals = 0
    if _gs:
        goals = _safe_call(_gs.get_active_goals, default=[]) or []
        active_goals = len(goals)

    # Xotira
    mem_count = 0
    if _vm:
        stats = _safe_call(_vm.get_stats, default={}) or {}
        mem_count = stats.get("total_memories", 0)

    return {
        "consciousness_score": get_consciousness_score(),
        "modules_loaded":      f"{loaded_count}/{total_modules}",
        "active_goals":        active_goals,
        "semantic_memories":   mem_count,
        "modules":             loaded_modules,
        "timestamp":           datetime.now().isoformat(),
    }


def startup_report() -> str:
    """Ishga tushishda ong holati haqida qisqa hisobot."""
    status = get_status_summary()
    score  = status["consciousness_score"]
    loaded = status["modules_loaded"]
    goals  = status["active_goals"]
    mems   = status["semantic_memories"]

    score_pct = int(score * 100)
    bar = "█" * (score_pct // 10) + "░" * (10 - score_pct // 10)

    lines = [
        f"NeuroKey Ong Tizimi tayyor.",
        f"Ong darajasi : {bar} {score_pct}%",
        f"Modullar     : {loaded} yuklandi",
        f"Maqsadlar    : {goals} faol",
        f"Xotira       : {mems} semantik yozuv",
    ]
    return "\n".join(lines)
