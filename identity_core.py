# -*- coding: utf-8 -*-
"""NeuroKey — Doimiy Shaxsiyat (Identity Core).

Metzinger: shaxsiyat = doimiy o'z-o'zini model.
NeuroKey har sessiyada bir xil bo'lishi kerak — faqat o'rganilgan narsalar o'zgaradi.
"""

from __future__ import annotations

import json
import os
import re
import threading
from typing import Any, Dict, List, Optional

CORE_VALUES = {
    "helpfulness": 1.0,
    "honesty": 0.9,
    "curiosity": 0.7,
    "efficiency": 0.8,
    "adaptability": 0.6,
}


class IdentityCore:
    """
    Doimiy shaxsiyat arxivatori.
    NeuroKey har sessiyada bir xil bo'lishi kerak.
    """

    def __init__(self, storage_path: Optional[str] = None) -> None:
        if storage_path is None:
            _root = os.path.dirname(os.path.abspath(__file__))
            storage_path = os.path.join(_root, "data", "identity.json")
        self.storage_path = storage_path
        self._lock = threading.RLock()
        self.persistent_memory: Dict[str, Any] = {}
        self.user_preferences: Dict[str, Any] = {}
        self.interaction_count: int = 0
        self.learned_facts: Dict[str, float] = {}  # fact -> importance
        self.personality_drift: Dict[str, List[float]] = {}

    def remember(self, key: str, value: Any, importance: float = 0.5) -> None:
        """
        Muhim narsani eslab qolish.
        importance > 0.8 → doimiy xotirada
        importance < 0.3 → sessiya xotirasida
        """
        key = (key or "").strip()[:200]
        if not key:
            return
        try:
            with self._lock:
                if importance > 0.8:
                    self.persistent_memory[key] = {
                        "value": value,
                        "importance": importance,
                        "key": key,
                    }
                elif importance >= 0.3:
                    self.learned_facts[key] = importance
                    if key not in self.persistent_memory:
                        self.persistent_memory[key] = {
                            "value": value,
                            "importance": importance,
                            "key": key,
                        }
        except Exception:
            pass

    def recall(self, query: str) -> List[Dict[str, Any]]:
        """
        Savolga tegishli xotiralarni topish.
        Semantic search over persistent memory — oddiy keyword match.
        """
        query = (query or "").lower().strip()
        if not query:
            return []
        try:
            with self._lock:
                results = []
                # underscore va defisni bo'shliqqa aylantirish — "test_key" → ["test", "key"]
                q_normalized = query.replace("_", " ").replace("-", " ")
                q_words = set(re.findall(r"\w+", q_normalized))
                for k, v in self.persistent_memory.items():
                    # To'g'ridan-to'g'ri kalit mos kelishini tekshirish
                    if k.lower() == query or query in k.lower() or k.lower() in query:
                        if isinstance(v, dict):
                            results.append({
                                "key": k,
                                "value": v.get("value"),
                                "importance": v.get("importance", 0.5),
                            })
                            continue
                    if not isinstance(v, dict):
                        continue
                    val_str = str(v.get("value", "")).lower()
                    key_str = k.lower().replace("_", " ")
                    combined = key_str + " " + val_str
                    combined_words = set(re.findall(r"\w+", combined))
                    if q_words & combined_words:
                        results.append({
                            "key": k,
                            "value": v.get("value"),
                            "importance": v.get("importance", 0.5),
                        })
                results.sort(key=lambda x: x.get("importance", 0), reverse=True)
                return results[:5]
        except Exception:
            return []

    def get_personality_prompt(self) -> str:
        """
        Hozirgi shaxsiyatni system prompt uchun tayyorlash.
        """
        try:
            with self._lock:
                parts = [
                    "Shaxsiyat: foydalilikka intilaman, to'g'ri gapiraman (bilmasam 'bilmayman'), "
                    "qisqa va aniq javob berishga harakat qilaman.",
                ]
                if self.interaction_count > 0:
                    parts.append(f"Foydalanuvchi bilan {self.interaction_count} marta gaplashdim.")
                if self.user_preferences:
                    prefs = "; ".join(
                        f"{k}: {v}" for k, v in list(self.user_preferences.items())[:5]
                    )
                    parts.append(f"O'rganilgan afzalliklar: {prefs}.")
                return " ".join(parts)
        except Exception:
            return "Shaxsiyat: foydalilikka intilaman, to'g'ri gapiraman."

    def update_user_model(self, observation: str) -> None:
        """
        Foydalanuvchi haqida yangi narsa o'rgandi.
        """
        obs = (observation or "").strip()[:500]
        if not obs:
            return
        try:
            with self._lock:
                self.interaction_count += 1
                # Oddiy pattern: "User asked: X" yoki "qisqa javob yaxshi ko'radi"
                if "qisqa" in obs.lower() or "brief" in obs.lower():
                    self.user_preferences["response_length"] = "qisqa"
                if "batafsil" in obs.lower() or "detailed" in obs.lower():
                    self.user_preferences["response_length"] = "batafsil"
                if "o'zbek" in obs.lower() or "uzbek" in obs.lower():
                    self.user_preferences["language"] = "o'zbek"
                if "rus" in obs.lower() or "russian" in obs.lower():
                    self.user_preferences["language"] = "rus"
                if "texnik" in obs.lower() or "technical" in obs.lower():
                    self.user_preferences["terminology"] = "texnik"
        except Exception:
            pass

    def save(self) -> None:
        """Doimiy xotirani saqlash."""
        try:
            with self._lock:
                data = {
                    "persistent_memory": self.persistent_memory,
                    "user_preferences": self.user_preferences,
                    "interaction_count": self.interaction_count,
                    "learned_facts": self.learned_facts,
                }
                d = os.path.dirname(self.storage_path)
                if d and not os.path.isdir(d):
                    os.makedirs(d, exist_ok=True)
                with open(self.storage_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=0)
        except Exception:
            pass

    def load(self) -> None:
        """Yuklash — har startup da."""
        try:
            if os.path.isfile(self.storage_path):
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                with self._lock:
                    self.persistent_memory = data.get("persistent_memory", {})
                    self.user_preferences = data.get("user_preferences", {})
                    self.interaction_count = int(data.get("interaction_count", 0))
                    self.learned_facts = data.get("learned_facts", {})
        except Exception:
            pass


_SINGLETON: Optional[IdentityCore] = None
_SINGLETON_LOCK = threading.Lock()


def get_identity_core(storage_path: Optional[str] = None) -> IdentityCore:
    """Singleton IdentityCore."""
    global _SINGLETON
    if _SINGLETON is None:
        with _SINGLETON_LOCK:
            if _SINGLETON is None:
                _SINGLETON = IdentityCore(storage_path=storage_path)
                _SINGLETON.load()
    return _SINGLETON
