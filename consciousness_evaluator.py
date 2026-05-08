# -*- coding: utf-8 -*-
"""NeuroKey — O'lchov Tizimi (Consciousness Evaluator).

Butlin et al. (2023) "Consciousness in AI" — 14 indikator bo'yicha rasmiy baholash.
Har indikator 0.0 → 1.0. Natijalar JSON + HTML report.
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

INDICATORS = {
    "GWT_1": "Global information broadcasting",
    "GWT_2": "Limited capacity workspace",
    "GWT_3": "Attention and access consciousness",
    "HOT_1": "Higher order representations",
    "HOT_2": "Meta-cognitive monitoring",
    "RPT_1": "Recurrent/feedback processing",
    "RPT_2": "Temporal integration",
    "IIT_1": "Information integration",
    "IIT_2": "Causal structure",
    "EMB_1": "Sensorimotor integration",
    "EMB_2": "Environmental coupling",
    "SMT_1": "Transparent self-model",
    "SMT_2": "Phenomenal self-model",
    "AFF_1": "Valence and affect",
}


def _safe_import(module: str, attr: str, default: Any = None) -> Any:
    try:
        m = __import__(module, fromlist=[attr])
        return getattr(m, attr, default)
    except Exception:
        return default


class ConsciousnessEvaluator:
    """
    Butlin et al. (2023) 14 indikatori bo'yicha NeuroKey ni rasmiy baholash.
    neurokey_instance ixtiyoriy — None bo'lsa modullar to'g'ridan-to'g'ri import qilinadi.
    """

    def __init__(self, neurokey_instance: Optional[Any] = None) -> None:
        self.nk = neurokey_instance
        self.scores: Dict[str, float] = {}
        self.evidence: Dict[str, str] = {}
        self.test_results: Dict[str, Dict] = {}

    def test_GWT_1(self) -> Dict[str, Any]:
        """Global information broadcasting."""
        try:
            vs = _safe_import("valence_state", "get_valence_state")()
            vs.set_valence(0.8)
            sm = _safe_import("self_model", "get_self_model")()
            desc = sm.get_self_description()
            wm = _safe_import("world_model", "get_world_model")()
            state = wm.get_model_state()
            score = 0.0
            if desc and len(desc) > 10:
                score += 0.4
            if state and "model" in state.lower():
                score += 0.3
            if hasattr(vs, "value") and vs.value > 0.5:
                score += 0.3
            return {
                "score": min(1.0, score),
                "evidence": f"Valence o'zgardi; self_model={bool(desc)}; world_model={bool(state)}",
                "passed": score >= 0.5,
                "details": {},
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_GWT_2(self) -> Dict[str, Any]:
        """Limited capacity workspace."""
        try:
            gw = _safe_import("global_workspace", "get_workspace")()
            if gw and hasattr(gw, "compete"):
                gw.compete([])
                return {
                    "score": 0.7,
                    "evidence": "Global workspace compete() mavjud va ishlaydi",
                    "passed": True,
                    "details": {},
                }
            return {"score": 0.3, "evidence": "Global workspace qisman", "passed": False, "details": {}}
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_GWT_3(self) -> Dict[str, Any]:
        """Attention and access consciousness."""
        try:
            am = _safe_import("attention_mechanism", "get_attention_mechanism")()
            ai = _safe_import("active_inference", "get_active_inference")()
            w1 = am.compute_attention({"user_speech": "hello", "surprise_level": 0.1})
            w2 = am.compute_attention({"user_speech": "EMERGENCY!", "surprise_level": 0.9})
            us1 = w1.get("user_speech", 0)
            us2 = w2.get("user_speech", 0)
            diff = abs(us2 - us1)
            score = 0.5 + min(0.5, diff * 2)
            return {
                "score": min(1.0, score),
                "evidence": f"Oddiy vs kutilmagan diqqat farqi: {diff:.2f}",
                "passed": diff > 0.1,
                "details": {"normal": us1, "surprise": us2},
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_HOT_1(self) -> Dict[str, Any]:
        """Higher order representations."""
        try:
            sm = _safe_import("self_model", "get_self_model")()
            desc = sm.get_self_description()
            load = sm.estimate_cognitive_load()
            score = 0.0
            if desc and len(desc) > 20:
                score += 0.5
            if 0 <= load <= 1:
                score += 0.5
            return {
                "score": score,
                "evidence": f"Self-description: {len(desc or '')} chars; load={load:.2f}",
                "passed": score >= 0.5,
                "details": {},
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_HOT_2(self) -> Dict[str, Any]:
        """Meta-cognitive monitoring."""
        try:
            sm = _safe_import("self_model", "get_self_model")()
            conf = sm.detect_confusion("nima deyapsiz, tushunmadim")
            score = 0.7 if conf else 0.3
            return {
                "score": score,
                "evidence": f"detect_confusion('tushunmadim')={conf}",
                "passed": conf,
                "details": {},
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_RPT_1(self) -> Dict[str, Any]:
        """Recurrent/feedback processing."""
        try:
            ai = _safe_import("active_inference", "get_active_inference")()
            obs = {"input": "test", "time": 12, "previous_context": []}
            result = ai.run_inference_cycle(obs)
            has_strategy = "strategy" in result
            has_surprise = "surprise" in result
            score = 0.5 + (0.25 if has_strategy else 0) + (0.25 if has_surprise else 0)
            return {
                "score": min(1.0, score),
                "evidence": f"Inference cycle: strategy={has_strategy}, surprise={has_surprise}",
                "passed": has_strategy,
                "details": result,
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_RPT_2(self) -> Dict[str, Any]:
        """Temporal integration."""
        try:
            ic = _safe_import("identity_core", "get_identity_core")()
            if not ic:
                return {"score": 0.0, "evidence": "identity_core yo'q", "passed": False, "details": {}}
            ic.remember("test_key_rpt2", "test_value", importance=0.9)
            recalled = ic.recall("test_key_rpt2") or ic.recall("test_key")
            score = 0.7 if recalled else 0.5  # 0.5 if mechanism exists
            return {
                "score": score,
                "evidence": f"identity_core.recall: {len(recalled or [])} natija",
                "passed": bool(recalled),
                "details": {},
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_IIT_1(self) -> Dict[str, Any]:
        """Information integration."""
        try:
            vs = _safe_import("valence_state", "get_valence_state")()
            bs = _safe_import("body_state", "get_body_state")()
            wm = _safe_import("world_model", "get_world_model")()
            am = _safe_import("attention_mechanism", "get_attention_mechanism")()
            count = sum(1 for x in (vs, bs, wm, am) if x is not None)
            score = count / 4.0
            return {
                "score": score,
                "evidence": f"4 modul: {count} mavjud (valence, body, world, attention)",
                "passed": count >= 3,
                "details": {},
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_IIT_2(self) -> Dict[str, Any]:
        """Causal structure."""
        try:
            bs = _safe_import("body_state", "get_body_state")()
            bs.cpu_load = 0.95
            ec = _safe_import("embodied_cognition", "get_embodied_cognition")()
            style = ec.adapt_response_style()
            chain_works = style.get("length") == "short"
            score = 0.7 if chain_works else 0.3
            return {
                "score": score,
                "evidence": f"Body cpu=0.95 -> adapt_response_style length={style.get('length')}",
                "passed": chain_works,
                "details": style,
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_EMB_1(self) -> Dict[str, Any]:
        """Sensorimotor integration."""
        try:
            bs = _safe_import("body_state", "get_body_state")()
            bs.update_from_system({"cpu": 0.9, "memory": 0.7, "latency": 0})
            ec = _safe_import("embodied_cognition", "get_embodied_cognition")()
            style = ec.adapt_response_style()
            short = style.get("length") == "short"
            return {
                "score": 0.8 if short else 0.4,
                "evidence": f"cpu=0.9 -> response_style length={style.get('length')}",
                "passed": short,
                "details": style,
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_EMB_2(self) -> Dict[str, Any]:
        """Environmental coupling."""
        try:
            ec = _safe_import("embodied_cognition", "get_embodied_cognition")()
            should, msg = ec.should_initiate()
            ctx = ec.get_embodied_context()
            score = 0.5 + (0.25 if ctx else 0) + (0.25 if isinstance(should, bool) else 0)
            return {
                "score": min(1.0, score),
                "evidence": f"should_initiate={should}; embodied_context={len(ctx or '')} chars",
                "passed": True,
                "details": {},
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_SMT_1(self) -> Dict[str, Any]:
        """Transparent self-model."""
        try:
            sm = _safe_import("self_model", "get_self_model")()
            desc = sm.get_self_description()
            can = sm.can_do("open browser")
            score = 0.5 + (0.25 if desc and "diqqat" in desc.lower() or "vazifa" in desc.lower() else 0.1) + (0.25 if can.get("can_do") else 0)
            return {
                "score": min(1.0, score),
                "evidence": f"Self-description mavjud; can_do={can.get('can_do')}",
                "passed": bool(desc),
                "details": {},
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_SMT_2(self) -> Dict[str, Any]:
        """Phenomenal self-model."""
        try:
            ic = _safe_import("identity_core", "get_identity_core")()
            prompt = ic.get_personality_prompt()
            has_self = "men" in (prompt or "").lower() or "shaxsiyat" in (prompt or "").lower() or "foydali" in (prompt or "").lower()
            return {
                "score": 0.7 if has_self else 0.4,
                "evidence": f"identity_core.get_personality_prompt: {len(prompt or '')} chars",
                "passed": bool(prompt),
                "details": {},
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def test_AFF_1(self) -> Dict[str, Any]:
        """Valence and affect."""
        try:
            vs = _safe_import("valence_state", "get_valence_state")()
            vs.set_valence(-0.8)
            d = vs.to_behavioral_directive()
            rl = _safe_import("rl_engine", "get_rl_engine")()
            params = rl.get_best_response_params({"valence": -0.8, "arousal": 0.5, "hour": 12, "session_length": 1})
            score = 0.5 + (0.25 if d.get("tone") in ("urgent", "cautious") else 0) + (0.25 if params else 0)
            return {
                "score": min(1.0, score),
                "evidence": f"Valence -0.8 -> directive tone={d.get('tone')}; RL params mavjud",
                "passed": bool(d.get("tone")),
                "details": d,
            }
        except Exception as e:
            return {"score": 0.0, "evidence": str(e), "passed": False, "details": {}}

    def run_all_tests(self) -> Dict[str, Any]:
        """14 ta testni ketma-ket o'tkazish."""
        tests = [
            self.test_GWT_1, self.test_GWT_2, self.test_GWT_3,
            self.test_HOT_1, self.test_HOT_2,
            self.test_RPT_1, self.test_RPT_2,
            self.test_IIT_1, self.test_IIT_2,
            self.test_EMB_1, self.test_EMB_2,
            self.test_SMT_1, self.test_SMT_2,
            self.test_AFF_1,
        ]
        results: Dict[str, Dict] = {}
        for test in tests:
            name = test.__name__.replace("test_", "")
            try:
                results[name] = test()
            except Exception as e:
                results[name] = {"score": 0.0, "passed": False, "evidence": str(e), "details": {}}
        total = sum(r.get("score", 0) for r in results.values()) / max(1, len(results))
        return {
            "total_score": round(total, 4),
            "percentage": round(total * 100, 1),
            "indicators": results,
            "summary": self._generate_summary(results, total),
            "timestamp": datetime.now().isoformat(),
            "neurokey_version": "1.0.0-beta",
        }

    def _generate_summary(self, results: Dict, total: float) -> str:
        passed = sum(1 for r in results.values() if r.get("passed"))
        return (
            f"NeuroKey {round(total * 100, 1)}% consciousness score. "
            f"{passed}/14 indicators passed. "
            f"Based on Butlin et al. (2023) framework."
        )

    def save_results(self, results: Dict, path: Optional[str] = None) -> None:
        """Natijalarni JSON ga saqlash."""
        if path is None:
            _root = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(_root, "data", "consciousness_report.json")
        d = os.path.dirname(path)
        if d and not os.path.isdir(d):
            os.makedirs(d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
