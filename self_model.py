# -*- coding: utf-8 -*-
"""NeuroKey — Self Model (O'z Modeli).

Ong uchun birinchi shart: tizim o'zini ANIQ bilishi kerak.
- Qaysi sohalarda kuchli, qayerda zaif
- Qachon ishonchli, qachon ishonchsiz
- Xatolardan real vaqtda o'rganish

Bu modul benchmark natijalaridan o'rganib,
har savolga javob berishdan OLDIN sifatni bashorat qiladi.
"""
from __future__ import annotations

import json
import logging
import os
import time
from typing import Dict, List, Optional, Tuple

log = logging.getLogger(__name__)

_BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
_STATE_PATH = os.path.join(_BASE_DIR, "data", "self_model.json")

LEARNING_RATE     = 0.25   # yangi ma'lumot ta'sir kuchi
DEFAULT_CAPABILITY = 0.65  # birinchi ishga tushganda default
CAP_MIN = 0.10
CAP_MAX = 0.98


class SelfModel:
    """Tizimning o'z qobiliyatlari haqida aniq modeli.

    Har benchmark natijasidan keyin yangilanadi.
    Har savolga javob berishdan oldin sifat taxminini beradi.
    """

    def __init__(self) -> None:
        self.capabilities: Dict[str, float] = {
            "LOGIC":     DEFAULT_CAPABILITY,
            "FACTS":     DEFAULT_CAPABILITY,
            "MEMORY":    DEFAULT_CAPABILITY,
            "META":      DEFAULT_CAPABILITY,
            "TRAPS":     DEFAULT_CAPABILITY,
            "LIE":       DEFAULT_CAPABILITY,
            "COMPARE":   DEFAULT_CAPABILITY,
            "EMOTION":   DEFAULT_CAPABILITY,
            "CHARACTER": DEFAULT_CAPABILITY,
            "CONSCIOUS": DEFAULT_CAPABILITY,
        }
        self.overall_confidence: float = DEFAULT_CAPABILITY
        self.history: List[dict] = []
        self.update_count: int = 0
        self.weak_areas: List[str] = []
        self.strong_areas: List[str] = []
        self.last_updated: float = time.time()
        self._load()

    # ── O'rganish ─────────────────────────────────────────────────────────────

    def update_from_benchmark(self, results: Dict[str, float]) -> Dict[str, float]:
        """Benchmark natijalaridan o'rganadi.

        Args:
            results: {"LOGIC": 0.76, "FACTS": 0.82, ...}
        Returns:
            o'zgarishlar {"LOGIC": +0.02, ...}
        """
        changes: Dict[str, float] = {}
        for dim, score in results.items():
            if dim not in self.capabilities:
                continue
            old = self.capabilities[dim]
            new = old * (1 - LEARNING_RATE) + score * LEARNING_RATE
            new = max(CAP_MIN, min(CAP_MAX, new))
            self.capabilities[dim] = new
            changes[dim] = round(new - old, 4)

        self.overall_confidence = sum(self.capabilities.values()) / len(self.capabilities)

        srt = sorted(self.capabilities.items(), key=lambda x: x[1])
        self.weak_areas   = [k for k, _ in srt[:3]]
        self.strong_areas = [k for k, _ in srt[-3:]]

        self.history.append({
            "ts":      time.time(),
            "overall": round(self.overall_confidence, 4),
            "scores":  {k: round(v, 4) for k, v in results.items()},
        })
        if len(self.history) > 20:
            self.history.pop(0)

        self.update_count += 1
        self.last_updated = time.time()
        self._save()
        log.info("[SelfModel] yangilandi: %.1f%%  zaif=%s",
                 self.overall_confidence * 100, self.weak_areas)
        return changes

    # ── Bashorat ──────────────────────────────────────────────────────────────

    def predict_quality(self, dimension: str) -> float:
        return self.capabilities.get(dimension, DEFAULT_CAPABILITY)

    def predict_with_uncertainty(self, dimension: str) -> Tuple[float, float]:
        cap = self.capabilities.get(dimension, DEFAULT_CAPABILITY)
        unc = max(0.05, 0.30 - self.update_count * 0.01)
        return cap, min(unc, 0.30)

    def should_flag_uncertainty(self, dimension: str) -> bool:
        cap, unc = self.predict_with_uncertainty(dimension)
        return cap < 0.70 or unc > 0.20

    # ── Tahlil ────────────────────────────────────────────────────────────────

    def get_improvement_trend(self) -> str:
        if len(self.history) < 2:
            return "ma'lumot yetarli emas"
        vals = [h["overall"] for h in self.history[-3:]]
        delta = vals[-1] - vals[0]
        if delta >  0.02: return f"yaxshilanmoqda (+{delta:.3f})"
        if delta < -0.02: return f"yomonlashmoqda ({delta:.3f})"
        return "barqaror"

    def get_context_for_llm(self) -> str:
        return (
            f"[O'Z MODELI] daraja={self.overall_confidence:.0%} | "
            f"kuchli={','.join(self.strong_areas)} | "
            f"zaif={','.join(self.weak_areas)} | "
            f"trend={self.get_improvement_trend()}"
        )

    def get_self_description(self) -> str:
        """llm_router.py bilan moslik uchun alias."""
        return self.get_context_for_llm()

    def get_full_report(self) -> str:
        lines = ["\n+== O'Z MODELI ==+",
                 f"  Yangilanish: {self.update_count}x",
                 f"  Umumiy: {self.overall_confidence:.1%}",
                 f"  Trend: {self.get_improvement_trend()}",
                 "  Qobiliyatlar:"]
        for dim, cap in sorted(self.capabilities.items(), key=lambda x: -x[1]):
            bar = "#" * int(cap * 20) + "." * (20 - int(cap * 20))
            tag = " !" if dim in self.weak_areas else (" *" if dim in self.strong_areas else "")
            lines.append(f"  {dim:12s} [{bar}] {cap:.1%}{tag}")
        lines.append("+================+")
        return "\n".join(lines)

    # ── Disk ──────────────────────────────────────────────────────────────────

    def _save(self) -> None:
        try:
            os.makedirs(os.path.dirname(_STATE_PATH), exist_ok=True)
            with open(_STATE_PATH, "w", encoding="utf-8") as f:
                json.dump({
                    "capabilities":       self.capabilities,
                    "overall_confidence": self.overall_confidence,
                    "update_count":       self.update_count,
                    "weak_areas":         self.weak_areas,
                    "strong_areas":       self.strong_areas,
                    "last_updated":       self.last_updated,
                    "history":            self.history[-10:],
                }, f, ensure_ascii=False, indent=2)
        except Exception as e:
            log.debug("[SelfModel] saqlash xato: %s", e)

    def _load(self) -> None:
        if not os.path.exists(_STATE_PATH):
            return
        try:
            with open(_STATE_PATH, encoding="utf-8") as f:
                d = json.load(f)
            self.capabilities.update(d.get("capabilities", {}))
            self.overall_confidence = d.get("overall_confidence", DEFAULT_CAPABILITY)
            self.update_count       = d.get("update_count", 0)
            self.weak_areas         = d.get("weak_areas", [])
            self.strong_areas       = d.get("strong_areas", [])
            self.last_updated       = d.get("last_updated", time.time())
            self.history            = d.get("history", [])
            log.info("[SelfModel] yuklandi: %.1f%% (%d run)",
                     self.overall_confidence * 100, self.update_count)
        except Exception as e:
            log.debug("[SelfModel] yuklash xato: %s", e)


# ── Global API ────────────────────────────────────────────────────────────────

_instance: Optional[SelfModel] = None


def get() -> SelfModel:
    global _instance
    if _instance is None:
        _instance = SelfModel()
    return _instance


def update(results: Dict[str, float]) -> Dict[str, float]:
    return get().update_from_benchmark(results)


def predict(dimension: str) -> float:
    return get().predict_quality(dimension)


def context_for_llm() -> str:
    return get().get_context_for_llm()


def get_self_model():
    """llm_router.py bilan moslik uchun alias."""
    return get()
