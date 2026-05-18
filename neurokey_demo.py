# -*- coding: utf-8 -*-
"""
NeuroKey Interactive Behavioral Demo
=====================================
Run:  python neurokey_demo.py
Env:  set GROQ_API_KEY=your_key

Demonstrates real behavioral differences based on internal state.
Same question → different answers depending on mood, confidence, energy.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from behavioral_engine import BehavioralEngine, MOOD_ICON

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MEMORY_FILE  = os.path.join(BASE_DIR, "neurokey_memory.json")

try:
    from groq import Groq
    GROQ_OK = bool(GROQ_API_KEY)
except ImportError:
    GROQ_OK = False


# ── DISPLAY ───────────────────────────────────────────────────────────────────

def bar(value: float, width: int = 18) -> str:
    filled = int(max(0.0, min(1.0, value)) * width)
    return "#" * filled + "." * (width - filled)


MOOD_LABEL = {
    "FOCUSED":   "[*] FOCUSED",
    "CURIOUS":   "[?] CURIOUS",
    "UNCERTAIN": "[~] UNCERTAIN",
    "ENERGIZED": "[!] ENERGIZED",
    "TIRED":     "[-] TIRED",
    "NEUTRAL":   "[ ] NEUTRAL",
}


def print_panel(engine: BehavioralEngine):
    d = engine.get_panel_data()
    print("\n" + "-" * 54)
    print("  NEUROKEY  --  INTERNAL STATE")
    print("-" * 54)
    print(f"  Mood:       {MOOD_LABEL.get(d['mood'], d['mood']):<22}")
    print(f"  Attention:  [{bar(d['attention'])}] {d['attention']:.0%}")
    print(f"  Confidence: [{bar(d['confidence'])}] {d['confidence']:.0%}")
    print(f"  Energy:     [{bar(d['energy'])}] {d['energy']:.0%}")
    print(f"  Curiosity:  [{bar(d['curiosity'])}] {d['curiosity']:.0%}")
    print("-" * 54)
    print(f"  Queries: {d['queries']}  |  Memory: {d['memory']}  |  Pred.Errors: {d['pred_errors']}")
    print("-" * 54)


def print_summary(engine: BehavioralEngine):
    s = engine.get_session_summary()
    print("\n" + "=" * 54)
    print("  NEUROKEY  --  SESSION SUMMARY  (self-assessment)")
    print("=" * 54)
    print(f"  Duration:          {s['duration_min']:.1f} min")
    print(f"  Total queries:     {s['total_queries']}")
    print(f"  Avg confidence:    {s['avg_confidence']:.0%}")
    print(f"  Uncertain ratio:   {s['uncertain_ratio']:.0%}")
    print(f"  Final mood:        {s['mood_final']}")
    print(f"  Final energy:      {s['energy_final']:.0%}")
    print(f"  Topic switches:    {s['topic_switches']}")
    print(f"  Prediction errors: {s['pred_errors']}")
    print(f"  Facts stored:      {s['facts_stored']}")
    print(f"  Hardest query:     {s['hardest_query'][:46]}")
    print("=" * 54)


# ── AI RESPONSE ───────────────────────────────────────────────────────────────

def get_response(user_input: str, system_prompt: str) -> str:
    if GROQ_OK:
        try:
            client = Groq(api_key=GROQ_API_KEY)
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system",  "content": system_prompt},
                    {"role": "user",    "content": user_input},
                ],
                max_tokens=350,
                temperature=0.75,
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            return f"[Groq error: {e}]"

    # Fallback: rule-based responses that still show behavioral difference
    if "UNCERTAIN" in system_prompt or "not certain" in system_prompt:
        return (
            f"I'm not certain, but regarding '{user_input[:40]}' — "
            f"my current confidence is limited. I can offer a partial analysis "
            f"but recommend external verification."
        )
    if "TIRED" in system_prompt:
        return f"Processing at reduced capacity. Brief answer: '{user_input[:30]}' requires further analysis."
    if "FOCUSED" in system_prompt:
        return f"Direct response: '{user_input[:40]}' — systematic analysis in progress. Key points follow."
    if "CURIOUS" in system_prompt:
        return (
            f"Fascinating question about '{user_input[:40]}'. "
            f"This connects to multiple domains I find compelling. "
            f"Curiosity prompt: What aspect interests you most?"
        )
    return f"Analyzing '{user_input[:40]}' through my consciousness architecture layers."


# ── MAIN LOOP ─────────────────────────────────────────────────────────────────

def main():
    print("=" * 54)
    print("  NEUROKEY  --  Behavioral Consciousness Demo")
    print("  Butlin et al. (2023) Implementation")
    print("  github.com/tymitry/neurokey-consciousness")
    print("=" * 54)

    if not GROQ_OK:
        print("\n  [!] GROQ_API_KEY not set — using fallback responses.")
        print("  Set it: set GROQ_API_KEY=gsk_...")

    print("\n  Watch the INTERNAL STATE panel change with each query.")
    print("  Same question asked twice = different answer (state changed).")
    print("\n  Commands: 'quit' | 'summary' | 'goal <text>'")

    engine = BehavioralEngine(memory_file=MEMORY_FILE)

    prev_mood = engine.state.mood

    while True:
        try:
            print_panel(engine)
            user_input = input("\n  You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("quit", "exit", "q"):
                break

            if user_input.lower() == "summary":
                print_summary(engine)
                continue

            if user_input.lower().startswith("goal "):
                goal = user_input[5:].strip()
                engine.add_goal(goal) if hasattr(engine, "add_goal") else None
                print(f"\n  [Goal added: {goal}]")
                continue

            # Process through behavioral engine
            context     = engine.process_input(user_input)
            sys_prompt  = engine.build_system_prompt(context)
            curr_mood   = context["mood"]
            conf        = context["confidence"]

            # State change notification
            if prev_mood != curr_mood:
                print(f"\n  [State change: {prev_mood} -> {curr_mood}]")

            print(f"\n  NeuroKey [{curr_mood} | conf:{conf:.0%}]: ", end="", flush=True)
            response = get_response(user_input, sys_prompt)
            print(response)

            # Prediction error notification
            if engine.state.prediction_errors > 0 and engine.state.prediction_errors % 3 == 0:
                print(f"\n  [Prediction error #{engine.state.prediction_errors} — internal model updating...]")

            engine.record_response(user_input, response)
            prev_mood = curr_mood

        except KeyboardInterrupt:
            print("\n")
            break
        except EOFError:
            break

    print_summary(engine)
    print("\n  NeuroKey session ended.\n")


if __name__ == "__main__":
    main()
