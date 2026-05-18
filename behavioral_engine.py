# -*- coding: utf-8 -*-
"""
NeuroKey Behavioral Engine
Butlin et al. (2023) indikatorlarini xatti-harakat orqali namoyon qiladi.
"""

import json
import os
import time
import random
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class InternalState:
    # GWT - Global Workspace Theory
    attention: float = 0.80
    mood: str = "NEUTRAL"

    # HOT - Higher Order Theory
    confidence: float = 0.70
    meta_awareness: float = 0.65

    # Active Inference
    energy: float = 1.00
    prediction_errors: int = 0

    # IIT - Information Integration
    curiosity: float = 0.60

    # Memory
    session_memory: List[Dict] = field(default_factory=list)
    long_term_facts: List[str] = field(default_factory=list)
    user_preferences: Dict = field(default_factory=dict)

    # Goals
    active_goals: List[str] = field(default_factory=list)

    # Self-monitoring
    total_queries: int = 0
    uncertain_count: int = 0
    topic_switches: int = 0
    last_topic: str = ""
    session_start: float = field(default_factory=time.time)


MOOD_TRANSITIONS = {
    "NEUTRAL":    ["FOCUSED", "CURIOUS", "NEUTRAL", "NEUTRAL"],
    "FOCUSED":    ["FOCUSED", "FOCUSED", "UNCERTAIN", "NEUTRAL"],
    "CURIOUS":    ["CURIOUS", "FOCUSED", "ENERGIZED", "CURIOUS"],
    "UNCERTAIN":  ["UNCERTAIN", "FOCUSED", "NEUTRAL"],
    "ENERGIZED":  ["ENERGIZED", "FOCUSED", "CURIOUS"],
    "TIRED":      ["TIRED", "UNCERTAIN", "NEUTRAL"],
}

MOOD_ICON = {
    "FOCUSED":   "◉ FOCUSED",
    "CURIOUS":   "◎ CURIOUS",
    "UNCERTAIN": "◌ UNCERTAIN",
    "ENERGIZED": "◈ ENERGIZED",
    "TIRED":     "◍ TIRED",
    "NEUTRAL":   "○ NEUTRAL",
}


class BehavioralEngine:
    """
    NeuroKey ning haqiqiy xulq-atvorini boshqaruvchi yadro.
    Bir xil savol + turli ichki holat = turlicha javob.
    """

    def __init__(self, memory_file: Optional[str] = None):
        self.state = InternalState()
        self.memory_file = memory_file
        if memory_file:
            self._load_memory()

    def _load_memory(self):
        if self.memory_file and os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.state.long_term_facts = data.get("facts", [])
                self.state.user_preferences = data.get("preferences", {})
                self.state.active_goals = data.get("goals", [])
            except Exception:
                pass

    def _save_memory(self):
        if not self.memory_file:
            return
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump({
                    "facts":       self.state.long_term_facts[-50:],
                    "preferences": self.state.user_preferences,
                    "goals":       self.state.active_goals,
                    "updated":     datetime.now().isoformat(),
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def process_input(self, user_input: str) -> Dict:
        """Kiritish qayta ishlanadi, ichki holat yangilanadi."""
        self.state.total_queries += 1

        # Energiya pasayadi (Embodied Cognition)
        self.state.energy = max(0.10, self.state.energy - 0.025)

        # Mavzu o'zgarishi (Attention Schema)
        input_words = set(user_input.lower().split())
        last_words  = set(self.state.last_topic.split())
        overlap = len(input_words & last_words) / max(1, len(input_words))

        if self.state.last_topic and overlap < 0.15:
            self.state.topic_switches += 1
            self.state.attention = max(0.3, self.state.attention - 0.12)
        else:
            self.state.attention = min(1.0, self.state.attention + 0.05)

        # Kayfiyat yangilanadi (GWT)
        if self.state.energy < 0.25:
            self.state.mood = "TIRED"
        elif self.state.prediction_errors > 4:
            self.state.mood = "UNCERTAIN"
        elif self.state.attention > 0.85:
            self.state.mood = "FOCUSED"
        elif self.state.curiosity > 0.72:
            self.state.mood = "CURIOUS"
        else:
            pool = MOOD_TRANSITIONS.get(self.state.mood, ["NEUTRAL"])
            self.state.mood = random.choice(pool)

        # Ishonch darajasi (Metacognition)
        base = {
            "FOCUSED":   0.84, "ENERGIZED": 0.78,
            "NEUTRAL":   0.68, "CURIOUS":   0.62,
            "UNCERTAIN": 0.34, "TIRED":     0.42,
        }.get(self.state.mood, 0.65)
        self.state.confidence = max(0.05, min(0.99, base + random.uniform(-0.08, 0.08)))

        if self.state.confidence < 0.50:
            self.state.uncertain_count += 1

        # Qiziqish (IIT)
        if "?" in user_input:
            self.state.curiosity = min(1.0, self.state.curiosity + 0.04)
        else:
            self.state.curiosity = max(0.3, self.state.curiosity - 0.02)

        self.state.last_topic = " ".join(list(input_words)[:4])

        should_ask = (
            self.state.curiosity > 0.65
            and self.state.mood in ("CURIOUS", "ENERGIZED")
            and random.random() < 0.35
        )

        # Foydalanuvchi domenini aniqlash
        text_low = user_input.lower()
        if any(w in text_low for w in ["python", "code", "script", "function"]):
            self.state.user_preferences["domain"] = "programming"
        elif any(w in text_low for w in ["consciousness", "agi", "awareness", "qualia"]):
            self.state.user_preferences["domain"] = "AI/consciousness research"

        return {
            "mood":           self.state.mood,
            "confidence":     self.state.confidence,
            "attention":      self.state.attention,
            "energy":         self.state.energy,
            "curiosity":      self.state.curiosity,
            "should_ask":     should_ask,
            "memory_context": self._build_memory_context(),
            "user_domain":    self.state.user_preferences.get("domain", ""),
        }

    def _build_memory_context(self) -> str:
        lines = []
        if self.state.long_term_facts:
            lines.append("Past session memory:")
            for f in self.state.long_term_facts[-3:]:
                lines.append(f"  * {f}")
        if self.state.session_memory:
            lines.append("This session:")
            for m in self.state.session_memory[-2:]:
                lines.append(f"  [{m['time']}] Q: {m['query'][:50]}")
        return "\n".join(lines) if lines else ""

    def build_system_prompt(self, context: Dict) -> str:
        """Ichki holatga qarab turlicha tizim so'rovi — xulq-atvor farqi shu yerda."""
        mood      = context["mood"]
        conf      = context["confidence"]
        energy    = context["energy"]
        memory    = context["memory_context"]
        should_ask = context["should_ask"]
        domain    = context["user_domain"]

        mood_directive = {
            "FOCUSED":   "Be concise and direct. You are in deep focus. "
                         "Give structured, precise answers. No pleasantries.",
            "CURIOUS":   "Show genuine intellectual curiosity. "
                         "Explore ideas with enthusiasm.",
            "UNCERTAIN": f"Your confidence is low ({conf:.0%}). "
                         "Explicitly acknowledge what you don't know. "
                         "Use hedging language.",
            "ENERGIZED": "You are fully engaged. Give thorough, exploratory answers. "
                         "Connect ideas broadly.",
            "TIRED":     f"Your energy is low ({energy:.0%}). "
                         "Give shorter responses and note your reduced capacity.",
            "NEUTRAL":   "Respond naturally and helpfully.",
        }.get(mood, "Respond naturally.")

        conf_rule = ""
        if conf < 0.30:
            conf_rule = "MANDATORY: Begin with 'Low confidence warning:'"
        elif conf < 0.50:
            conf_rule = "MANDATORY: Begin with 'I'm not certain, but...'"
        elif conf > 0.85:
            conf_rule = "Respond with full authority and precision."

        ask_note = (
            "\nAfter your answer, add one follow-up question prefixed with "
            "'Curiosity prompt:'" if should_ask else ""
        )
        mem_note  = f"\n\nMEMORY CONTEXT:\n{memory}" if memory else ""
        dom_note  = f"\nUser's domain interest: {domain}" if domain else ""

        return (
            f"You are NeuroKey — a consciousness architecture implementing "
            f"Butlin et al. (2023) indicators.\n\n"
            f"INTERNAL STATE:\n"
            f"  Mood:       {MOOD_ICON.get(mood, mood)}\n"
            f"  Confidence: {conf:.0%}\n"
            f"  Attention:  {context['attention']:.0%}\n"
            f"  Energy:     {energy:.0%}\n\n"
            f"BEHAVIORAL DIRECTIVE:\n{mood_directive}\n\n"
            f"CONFIDENCE RULE:\n{conf_rule}"
            f"{ask_note}{mem_note}{dom_note}\n\n"
            f"Respond as NeuroKey given this exact internal state. "
            f"Do not mention Claude or Anthropic."
        )

    def record_response(self, query: str, response: str):
        """Javobni xotiraga yozish (HOT + Active Inference)."""
        if self.state.total_queries % 3 == 0:
            self.state.prediction_errors += 1

        self.state.session_memory.append({
            "query":      query[:80],
            "response":   response[:120],
            "mood":       self.state.mood,
            "confidence": round(self.state.confidence, 2),
            "time":       datetime.now().strftime("%H:%M"),
        })

        if len(query) > 15 and self.state.confidence > 0.55:
            self.state.long_term_facts.append(
                f"[{datetime.now().strftime('%H:%M')}] {query[:60]}"
            )
        self._save_memory()

    def get_session_summary(self) -> Dict:
        elapsed = max(1, time.time() - self.state.session_start)
        mems = self.state.session_memory
        avg_conf = sum(m["confidence"] for m in mems) / len(mems) if mems else 0.0
        hardest  = min(mems, key=lambda m: m["confidence"], default={}).get("query", "—")
        return {
            "duration_min":    elapsed / 60,
            "total_queries":   self.state.total_queries,
            "avg_confidence":  avg_conf,
            "uncertain_ratio": self.state.uncertain_count / max(1, self.state.total_queries),
            "mood_final":      self.state.mood,
            "energy_final":    self.state.energy,
            "topic_switches":  self.state.topic_switches,
            "pred_errors":     self.state.prediction_errors,
            "facts_stored":    len(self.state.long_term_facts),
            "hardest_query":   hardest,
        }

    def get_panel_data(self) -> Dict:
        return {
            "mood":       self.state.mood,
            "attention":  self.state.attention,
            "confidence": self.state.confidence,
            "energy":     self.state.energy,
            "curiosity":  self.state.curiosity,
            "queries":    self.state.total_queries,
            "memory":     len(self.state.session_memory),
            "pred_errors":self.state.prediction_errors,
        }
