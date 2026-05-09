"""
NeuroKey Consciousness Architecture — Quick Usage Example

Demonstrates core consciousness modules working together.
No API keys required for this example.
"""

from consciousness import Consciousness
from global_workspace import GlobalWorkspace
from consciousness_state import ConsciousnessState
from episodic_memory import EpisodicMemory
from emotion_state import EmotionState
from meta_cognition import MetaCognition
from phi_proxy import compute_phi
from self_model import SelfModel


def main():
    print("=== NeuroKey Consciousness Architecture Demo ===\n")

    # 1. Initialize consciousness state
    consciousness = Consciousness(path=":memory:")  # in-memory, no file needed
    print("[GWT] Consciousness initialized")

    # 2. Global Workspace
    gw = GlobalWorkspace()
    print("[GWT] Global Workspace initialized")

    # 3. Simulate a conversation turn
    user_input = "What is consciousness?"
    consciousness.set_focus(f"Answering: {user_input}")

    # 4. Get context for LLM (this is what gets injected into system prompt)
    context = consciousness.get_context_for_llm(current_time="2026-01-01 12:00")
    print(f"\n[CONTEXT] LLM context ({len(context)} chars):\n{context[:200]}...\n")

    # 5. Compressed context (for Realtime API)
    compressed = consciousness.get_context_compressed()
    print(f"[CONTEXT COMPRESSED] {compressed}\n")

    # 6. Emotion state
    emotion = EmotionState()
    print(f"[AFFECT] Valence: {emotion.valence:.2f}, Arousal: {emotion.arousal:.2f}")

    # 7. Meta-cognition (HOT — Higher-Order Thought)
    meta = MetaCognition()
    report = meta.introspect(
        consciousness_state=consciousness.data,
        valence_state=emotion,
        arousal_state=None,
    )
    print(f"[META] Self-report: {report.get('self_report', 'N/A')}")
    print(f"[META] Certainty: {report.get('certainty', 0):.2f}")

    # 8. IIT Phi (proxy calculation)
    phi = compute_phi(valence=emotion.valence, arousal=emotion.arousal, coherence=0.7)
    print(f"[IIT] Φ (phi proxy): {phi:.4f}")

    # 9. Save turn to working memory
    assistant_response = "Consciousness is the experience of being aware."
    consciousness.add_turn(user_input, assistant_response)
    print(f"\n[MEMORY] Turn saved to working memory ({len(consciousness.data['working_memory'])} turns)")

    # 10. Run Butlin 2023 evaluation
    print("\n[EVAL] Run full evaluation:")
    print("  python consciousness_evaluator.py --output report.json")

    print("\n=== Demo complete ===")
    print("Mean Butlin 2023 score (published): 0.668 / 1.0")


if __name__ == "__main__":
    main()
