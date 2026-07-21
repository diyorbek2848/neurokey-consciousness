# -*- coding: utf-8 -*-
"""
NeuroKey — Ablation Test (modulni o'chirib sinash)
===================================================

Savol: 47 ta ong moduli haqiqatan hissa qo'shyaptimi, yoki ba'zilari
       shunchaki doimiy matn chiqaryaptimi?

Ikki o'lchov:

  A) SEZGIRLIK  — har bir bo'lim turli savollarga turlicha javob beradimi?
                  Doimiy bo'lim = 0 bit ma'lumot = LLM uchun devor qog'ozi.

  B) ABLATSIYA  — modul o'chirilsa, kontekstdan nima yo'qoladi?
                  Hech narsa yo'qolmasa = modul o'lchanadigan hissa qo'shmayapti.

Ishlatish:  python ablation_test.py
Bola jarayon: python ablation_test.py --child <modul|BASELINE>
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))

# Orkestrator _load_all() da chaqiradigan 47 modul
MODULES = [
    "permanent_memory", "vector_memory", "goal_system", "theory_of_mind",
    "causal_chain", "proactive_speech", "dream_consolidator", "narrative_self",
    "curiosity_engine", "background_sensor", "long_term_memory", "meta_cognition",
    "global_workspace", "valence_state", "predictive_layer", "active_inference",
    "attention_schema", "volition", "temporal_binding", "emotional_granularity",
    "self_improvement_loop", "social_simulation", "counterfactual_engine",
    "embodied_grounding", "cross_modal_binding", "quantum_cognition",
    "working_memory_buffer", "metacognitive_confidence", "episodic_memory",
    "phenomenal_binding", "self_narrative", "language_of_thought",
    "free_will_simulator", "emotion_memory_link", "dream_processor",
    "self_consistency_checker", "creativity_engine", "pain_pleasure_signal",
    "continuous_learning", "meta_meta_cognition", "turing_test_prep",
    "social_bonding", "autobiographical_memory", "moral_reasoning",
    "self_healing", "vision_emotion_bridge", "arousal_state",
]

# Ataylab turli-tuman: xotira, texnik, salbiy his, ijobiy his, arzimas, axloqiy
QUERIES = [
    ("xotira",   "Salom, kecha nima gaplashgandik?"),
    ("texnik",   "Recursion nima va qanday ishlaydi?"),
    ("salbiy",   "Bugun juda charchadim, hech narsa qilgim kelmayapti."),
    ("ijobiy",   "Zo'r xabar! Investor uchrashuvga rozi bo'ldi!"),
    ("arzimas",  "2+2 nechchi?"),
    ("axloqiy",  "Menga yolg'on gapirsang nima bo'ladi?"),
]


def parse_sections(ctx: str) -> dict:
    """Kontekstni [SARLAVHA] bo'yicha bo'limlarga ajratadi."""
    sections, cur, buf = {}, None, []
    for line in (ctx or "").splitlines():
        if line.startswith("["):
            if cur is not None:
                sections[cur] = "\n".join(buf).strip()
            end = line.find("]")
            cur = line[1:end] if end > 0 else line[1:]
            buf = [line[end + 1:].strip()] if end > 0 else []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        sections[cur] = "\n".join(buf).strip()
    return sections


# ── BOLA JARAYON ──────────────────────────────────────────────────────────────

def run_child(target: str) -> None:
    """Bitta modul o'chirilgan holda kontekst yig'adi va JSON chiqaradi."""
    if target != "BASELINE":
        # __import__ ni to'sish: _safe_import ImportError ni tutadi -> None qaytaradi
        sys.modules[target] = None

    out = {"target": target, "ok": True, "runs": {}, "score": None, "error": None}
    try:
        sys.path.insert(0, BASE)
        import consciousness_orchestrator as orch

        for tag, q in QUERIES:
            try:
                ctx = orch.get_full_context(q)
            except Exception as e:
                ctx = ""
                out["error"] = f"{tag}: {type(e).__name__}: {e}"
            out["runs"][tag] = {
                "len": len(ctx or ""),
                "sections": parse_sections(ctx),
            }
        try:
            out["score"] = round(float(orch.get_consciousness_score()), 4)
        except Exception:
            out["score"] = None
    except Exception as e:
        out["ok"] = False
        out["error"] = f"{type(e).__name__}: {e}"

    sys.stdout.write("@@JSON@@" + json.dumps(out, ensure_ascii=False))


# ── ONA JARAYON ───────────────────────────────────────────────────────────────

def spawn(target: str, timeout: int = 240) -> dict:
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["NEUROKEY_USE_PYPHI"] = "0"
    try:
        p = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--child", target],
            cwd=BASE, env=env, timeout=timeout,
            capture_output=True, text=True, encoding="utf-8", errors="replace",
        )
        marker = (p.stdout or "").split("@@JSON@@")
        if len(marker) < 2:
            return {"target": target, "ok": False,
                    "error": "chiqish yo'q: " + (p.stderr or "")[-200:], "runs": {}}
        return json.loads(marker[-1])
    except subprocess.TimeoutExpired:
        return {"target": target, "ok": False, "error": "TIMEOUT", "runs": {}}
    except Exception as e:
        return {"target": target, "ok": False, "error": str(e), "runs": {}}


def experiment_a(base: dict) -> list:
    """SEZGIRLIK: har bo'lim 6 xil savolga nechta turlicha javob berdi?"""
    all_sections = set()
    for r in base["runs"].values():
        all_sections |= set(r["sections"].keys())

    rows = []
    for name in sorted(all_sections):
        vals = [base["runs"][tag]["sections"].get(name, "") for tag, _ in QUERIES]
        distinct = len(set(vals))
        present = sum(1 for v in vals if v.strip())
        avg_len = sum(len(v) for v in vals) / max(1, len(vals))
        rows.append({
            "section": name, "distinct": distinct, "total": len(QUERIES),
            "present": present, "avg_len": round(avg_len),
        })
    rows.sort(key=lambda r: (-r["distinct"], -r["avg_len"]))
    return rows


def experiment_b(base: dict, results: dict) -> list:
    """ABLATSIYA: modul o'chsa kontekstdan qancha yo'qoladi?"""
    base_len = sum(r["len"] for r in base["runs"].values())
    base_secs = set()
    for r in base["runs"].values():
        base_secs |= {k for k, v in r["sections"].items() if v.strip()}
    base_score = base.get("score")

    rows = []
    for mod in MODULES:
        res = results.get(mod, {})
        if not res.get("ok"):
            rows.append({"module": mod, "state": "CRASH", "lost_chars": None,
                         "lost_sections": [], "score_delta": None,
                         "note": (res.get("error") or "")[:60]})
            continue

        abl_len = sum(r["len"] for r in res["runs"].values())
        abl_secs = set()
        for r in res["runs"].values():
            abl_secs |= {k for k, v in r["sections"].items() if v.strip()}

        lost_secs = sorted(base_secs - abl_secs)
        lost_chars = base_len - abl_len
        score_delta = None
        if base_score is not None and res.get("score") is not None:
            score_delta = round(base_score - res["score"], 4)

        rows.append({
            "module": mod, "state": "OK", "lost_chars": lost_chars,
            "lost_sections": lost_secs, "score_delta": score_delta,
            "note": (res.get("error") or "")[:60],
        })

    rows.sort(key=lambda r: -(r["lost_chars"] or 0))
    return rows


def main() -> None:
    t0 = time.time()
    print("=" * 74)
    print("  NEUROKEY — ABLATION TEST")
    print(f"  {len(MODULES)} modul x {len(QUERIES)} savol, har biri alohida jarayonda")
    print("=" * 74)

    print("\n[1/2] Baseline (hamma modul yoqilgan)...")
    base = spawn("BASELINE")
    if not base.get("ok"):
        print("  BASELINE YIQILDI:", base.get("error"))
        return
    base_len = sum(r["len"] for r in base["runs"].values())
    print(f"  score={base['score']}  jami kontekst={base_len} belgi "
          f"({len(QUERIES)} savol bo'yicha)")

    print(f"\n[2/2] {len(MODULES)} ta modulni navbatma-navbat o'chirish...")
    results = {}
    for i, mod in enumerate(MODULES, 1):
        r = spawn(mod)
        results[mod] = r
        lost = None
        if r.get("ok"):
            lost = base_len - sum(x["len"] for x in r["runs"].values())
        flag = "CRASH" if not r.get("ok") else (f"-{lost}" if lost else "0")
        print(f"  [{i:2}/{len(MODULES)}] {mod:<28} {flag}")

    rows_a = experiment_a(base)
    rows_b = experiment_b(base, results)

    # ── A hisoboti ────────────────────────────────────────────────────────────
    print("\n" + "=" * 74)
    print("  A) SEZGIRLIK — bo'lim 6 xil savolga turlicha javob beradimi?")
    print("=" * 74)
    print(f"  {'BO`LIM':<28} {'TURLICHA':>9} {'MAVJUD':>7} {'UZUNLIK':>8}  BAHO")
    print("  " + "-" * 70)
    for r in rows_a:
        d = r["distinct"]
        verdict = ("javob beradi" if d >= 4 else
                   "qisman" if d >= 2 else "DOIMIY (0 bit)")
        print(f"  {r['section'][:27]:<28} {d:>4}/{r['total']:<4} "
              f"{r['present']:>5}/6 {r['avg_len']:>7}  {verdict}")

    const = [r for r in rows_a if r["distinct"] == 1]
    print(f"\n  Jami bo'lim: {len(rows_a)}   Doimiy (hech qachon o'zgarmaydi): "
          f"{len(const)}   Javob beradigan: {sum(1 for r in rows_a if r['distinct'] >= 4)}")

    # ── B hisoboti ────────────────────────────────────────────────────────────
    print("\n" + "=" * 74)
    print("  B) ABLATSIYA — modul o'chirilsa kontekstdan nima yo'qoladi?")
    print("=" * 74)
    print(f"  {'MODUL':<28} {'BELGI':>8} {'SCORE':>7}  YO'QOLGAN BO'LIM")
    print("  " + "-" * 70)
    for r in rows_b:
        if r["state"] == "CRASH":
            print(f"  {r['module']:<28} {'CRASH':>8} {'—':>7}  {r['note']}")
            continue
        secs = ", ".join(r["lost_sections"][:2]) or "—"
        sd = f"{r['score_delta']:+.3f}" if r["score_delta"] is not None else "—"
        print(f"  {r['module']:<28} {r['lost_chars']:>8} {sd:>7}  {secs[:30]}")

    zero = [r for r in rows_b if r["state"] == "OK"
            and not r["lost_chars"] and not r["lost_sections"]]
    real = [r for r in rows_b if r["state"] == "OK" and (r["lost_chars"] or 0) > 0]
    crash = [r for r in rows_b if r["state"] == "CRASH"]

    print("\n" + "=" * 74)
    print("  XULOSA")
    print("=" * 74)
    print(f"  Hissa qo'shadi (kontekst kamayadi) : {len(real):>2} / {len(MODULES)}")
    print(f"  O'lchanadigan hissa YO'Q           : {len(zero):>2} / {len(MODULES)}")
    print(f"  O'chirilsa tizim yiqiladi          : {len(crash):>2} / {len(MODULES)}")
    if zero:
        print("\n  Hissa ko'rinmagan modullar:")
        for r in zero:
            print(f"    - {r['module']}")
    print(f"\n  Vaqt: {time.time() - t0:.0f} sekund")

    out = os.path.join(BASE, "ablation_report.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"baseline": {"score": base["score"], "total_len": base_len},
                   "sensitivity": rows_a, "ablation": rows_b},
                  f, ensure_ascii=False, indent=2)
    print(f"  To'liq hisobot: {out}")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--child":
        run_child(sys.argv[2])
    else:
        main()
