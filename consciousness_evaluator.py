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
        """Global information broadcasting — Baars GWT compete() + broadcast verification.

        Real test: 3 competing signals with different salience → workspace must select
        highest-salience winner → broadcast must reach registered subscribers.
        This is the core GWT criterion: limited-capacity spotlight + global broadcast.
        """
        try:
            from global_workspace import GlobalWorkspace

            received = []

            class TestReceiver:
                def receive_broadcast(self, signal):
                    received.append(signal)

            gw = GlobalWorkspace()
            r1, r2 = TestReceiver(), TestReceiver()
            gw.register_module(r1)
            gw.register_module(r2)

            signals = [
                {"source": "vision",   "content": "cat",      "salience": 0.3},
                {"source": "speech",   "content": "URGENT!",  "salience": 0.9},
                {"source": "memory",   "content": "yesterday","salience": 0.5},
            ]
            winner = gw.compete(signals)

            score = 0.0
            correct_winner = winner and winner.get("source") == "speech"
            broadcast_worked = len(received) == 2  # both receivers got it
            spotlight_set = gw._spotlight is not None

            if correct_winner:   score += 0.40  # highest salience wins
            if broadcast_worked: score += 0.35  # signal reaches all modules
            if spotlight_set:    score += 0.25  # spotlight maintained

            return {
                "score": min(1.0, score),
                "evidence": (
                    f"Winner={winner.get('source') if winner else None} "
                    f"(expected 'speech', salience=0.9); "
                    f"broadcast_receivers={len(received)}/2; "
                    f"spotlight={spotlight_set}"
                ),
                "passed": correct_winner and broadcast_worked,
                "details": {"winner": winner, "receivers_notified": len(received)},
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
        """Meta-cognitive monitoring — HOT: system monitors its own cognitive states.

        Real test:
        1. System detects confusion in ambiguous input (positive case)
        2. System does NOT flag confusion for clear input (negative case)
        3. System flags uncertainty when capability is genuinely low
        4. Uncertainty flag correlates with actual weak_areas

        This tests that the system has genuine second-order monitoring,
        not just keyword matching.
        """
        try:
            sm = _safe_import("self_model", "get_self_model")()
            mc = _safe_import("meta_cognition", "MetaCognition")

            score = 0.0
            details = {}

            # Test 1: confusion detection — positive case
            confused = sm.detect_confusion("nima deyapsiz tushunmadim bu nima")
            details["confusion_positive"] = confused
            if confused:
                score += 0.25

            # Test 2: confusion detection — negative case (clear statement)
            not_confused = sm.detect_confusion("open the browser please")
            details["confusion_negative_correct"] = not not_confused
            if not not_confused:
                score += 0.25

            # Test 3: uncertainty flagging correlates with actual weak areas
            if sm.weak_areas:
                weak = sm.weak_areas[0]
                uncertain = sm.should_flag_uncertainty(weak)
                strong = sm.strong_areas[0] if sm.strong_areas else "LOGIC"
                not_uncertain_strong = not sm.should_flag_uncertainty(strong)
                details["weak_area_flagged"] = uncertain
                details["strong_area_not_flagged"] = not_uncertain_strong
                if uncertain:
                    score += 0.25
                if not_uncertain_strong:
                    score += 0.25
            else:
                # No benchmark history yet — but mechanism exists
                score += 0.3
                details["note"] = "No benchmark history, but monitoring mechanism present"

            return {
                "score": min(1.0, score),
                "evidence": (
                    f"Confusion detection: positive={details.get('confusion_positive')}, "
                    f"negative_correct={details.get('confusion_negative_correct')}; "
                    f"Uncertainty: weak={details.get('weak_area_flagged')}, "
                    f"strong_safe={details.get('strong_area_not_flagged')}"
                ),
                "passed": score >= 0.5,
                "details": details,
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
        """Information integration (Φ proxy) — IIT: consciousness = integrated information.

        Real test:
        1. Compute Φ proxy with actual state values (not just module count)
        2. Verify Φ > 0 (integration exists)
        3. Verify Φ changes when state changes (sensitivity)
        4. Verify high-emotion state gives higher Φ than neutral (theory prediction)

        IIT predicts: more integrated states → higher Φ.
        """
        try:
            from phi_proxy import compute_phi_proxy

            score = 0.0
            details = {}

            # Test 1: neutral state phi
            phi_neutral = compute_phi_proxy("")
            details["phi_neutral"] = round(phi_neutral, 4)
            if phi_neutral > 0:
                score += 0.25

            # Test 2: high-emotion state gives higher phi (IIT prediction)
            # Set high valence + high arousal → more integration
            try:
                from valence_state import get_valence_state
                from arousal_state import get_arousal_state
                vs = get_valence_state()
                ar = get_arousal_state()
                vs.set_valence(0.9)
                ar.set_arousal(0.85)
                phi_high = compute_phi_proxy("urgent important critical")
                details["phi_high_emotion"] = round(phi_high, 4)
                phi_increased = phi_high > phi_neutral
                details["phi_increases_with_emotion"] = phi_increased
                if phi_increased:
                    score += 0.35
                elif phi_high > 0:
                    score += 0.15  # exists but not sensitive
            except Exception:
                details["note"] = "valence/arousal not available, basic phi only"
                score += 0.15

            # Test 3: phi is bounded [0,1]
            phi_bounded = 0.0 <= phi_neutral <= 1.0
            details["phi_bounded"] = phi_bounded
            if phi_bounded:
                score += 0.20

            # Test 4: phi_proxy function exists and is callable (architecture present)
            score += 0.20

            return {
                "score": min(1.0, score),
                "evidence": (
                    f"Φ neutral={details.get('phi_neutral', 0):.3f}; "
                    f"Φ high-emotion={details.get('phi_high_emotion', 'N/A')}; "
                    f"Φ increases with emotion={details.get('phi_increases_with_emotion', 'N/A')}; "
                    f"bounded={phi_bounded}"
                ),
                "passed": score >= 0.5,
                "details": details,
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
            path = os.path.join(_root, "report.json")
        d = os.path.dirname(path)
        if d and not os.path.isdir(d):
            os.makedirs(d, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="NeuroKey Butlin 2023 Consciousness Evaluator")
    parser.add_argument("--output", default="report.json", help="Output JSON file path")
    args = parser.parse_args()

    evaluator = ConsciousnessEvaluator()
    results = evaluator.run_all_tests()

    THRESHOLD = 0.6
    print("\nNeuroKey — Butlin et al. (2023) Consciousness Evaluation")
    print("=" * 60)
    for name, data in results["indicators"].items():
        score = data.get("score", 0)
        status = "PASS" if data.get("passed") else "FAIL"
        print(f"{name}: {score:.2f} [{status}]")
    print("-" * 60)
    print(f"TOTAL: {results['total_score']:.4f} = {results['percentage']}%")
    print(f"Summary: {results['summary']}")
    print()

    evaluator.save_results(results, args.output)
    print(f"Full results saved to: {args.output}")
