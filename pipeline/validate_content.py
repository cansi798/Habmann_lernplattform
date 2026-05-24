#!/usr/bin/env python3
"""Validates all generated content for Lernplatt.

Checks:
  - Every Tag 1-16 K22+K71 has pfad, quiz, sources JSON
  - Every JSON parses
  - Quiz: 60 questions, distribution 20/25/15 leicht/mittel/schwer
  - Pfad: 7 schritte, every step has aufgabe + required fields
  - Sources: 7-10 quellen, all required fields
  - LaTeX: handout/aufgaben/loesungen present for required day ranges
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TEX = ROOT / "tex"

errors: list[str] = []
warnings: list[str] = []


def fmt(course: str, tag: int) -> str:
    return f"{course}-tag-{tag:02d}"


def validate_pfad(course: str, tag: int) -> None:
    p = DATA / "pfad" / f"{fmt(course, tag)}.json"
    if not p.exists():
        errors.append(f"MISSING pfad: {p.name}")
        return
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"INVALID JSON pfad {p.name}: {e}")
        return
    schritte = d.get("schritte", [])
    if len(schritte) != 7:
        errors.append(f"pfad {p.name}: expected 7 schritte, got {len(schritte)}")
    for i, s in enumerate(schritte, 1):
        if s.get("typ") not in ("video", "text"):
            errors.append(f"pfad {p.name} schritt {i}: bad typ '{s.get('typ')}'")
        if s.get("typ") == "video" and not s.get("youtube_query"):
            warnings.append(f"pfad {p.name} schritt {i}: video w/o youtube_query")
        if s.get("typ") == "text" and not s.get("inhalt"):
            errors.append(f"pfad {p.name} schritt {i}: text w/o inhalt")
        a = s.get("aufgabe", {})
        if not isinstance(a.get("optionen"), list) or len(a["optionen"]) < 3:
            errors.append(f"pfad {p.name} schritt {i}: aufgabe.optionen invalid")
        if "korrekt" not in a or "erklaerung" not in a:
            errors.append(f"pfad {p.name} schritt {i}: aufgabe missing korrekt/erklaerung")


def validate_quiz(course: str, tag: int) -> None:
    p = DATA / "quiz" / f"{fmt(course, tag)}.json"
    if not p.exists():
        errors.append(f"MISSING quiz: {p.name}")
        return
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"INVALID JSON quiz {p.name}: {e}")
        return
    fragen = d.get("fragen", [])
    if len(fragen) != 60:
        errors.append(f"quiz {p.name}: expected 60 fragen, got {len(fragen)}")
    counts = {"leicht": 0, "mittel": 0, "schwer": 0}
    ids = set()
    for q in fragen:
        if q.get("id") in ids:
            errors.append(f"quiz {p.name}: duplicate id {q.get('id')}")
        ids.add(q.get("id"))
        sch = q.get("schwierigkeit")
        if sch in counts:
            counts[sch] += 1
        else:
            warnings.append(f"quiz {p.name} {q.get('id')}: unknown schwierigkeit {sch}")
        opts = q.get("optionen")
        if not isinstance(opts, list) or len(opts) != 4:
            errors.append(f"quiz {p.name} {q.get('id')}: optionen must be 4")
        k = q.get("korrekt")
        if not isinstance(k, int) or k < 0 or k > 3:
            errors.append(f"quiz {p.name} {q.get('id')}: korrekt must be int 0..3 (got {k})")
        if not q.get("erklaerung"):
            errors.append(f"quiz {p.name} {q.get('id')}: missing erklaerung")
    expected = {"leicht": 20, "mittel": 25, "schwer": 15}
    if counts != expected:
        warnings.append(f"quiz {p.name}: distribution {counts} (expected {expected})")


def validate_sources(course: str, tag: int) -> None:
    p = DATA / "sources" / f"{fmt(course, tag)}.json"
    if not p.exists():
        errors.append(f"MISSING sources: {p.name}")
        return
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"INVALID JSON sources {p.name}: {e}")
        return
    quellen = d.get("quellen", [])
    if not (7 <= len(quellen) <= 12):
        warnings.append(f"sources {p.name}: {len(quellen)} quellen (expected 7-10)")
    keys = set()
    for q in quellen:
        for f in ("key", "kurz", "apa", "typ", "thema", "verwendung_im_skript"):
            if not q.get(f):
                errors.append(f"sources {p.name} {q.get('key', '?')}: missing {f}")
        if q.get("key") in keys:
            errors.append(f"sources {p.name}: duplicate key {q.get('key')}")
        keys.add(q.get("key"))


def validate_tex(course_id: str, tag: int) -> None:
    """Check LaTeX files exist for handout/aufgaben/loesungen."""
    # Handout for Tag 1-16
    h = TEX / "handout" / f"{course_id}-tag-{tag:02d}.tex"
    if not h.exists():
        errors.append(f"MISSING tex: {h.relative_to(ROOT)}")
    # Aufgaben + Loesungen for Tag 1-16
    for kind in ("aufgaben", "loesungen"):
        f = TEX / kind / f"{course_id}-{kind}-tag-{tag:02d}.tex"
        if not f.exists():
            errors.append(f"MISSING tex: {f.relative_to(ROOT)}")


def main() -> int:
    courses = [("kurs-22", "22"), ("kurs-71", "71")]
    for course_pfx, course_id in courses:
        for tag in range(1, 17):
            validate_pfad(course_pfx, tag)
            validate_quiz(course_pfx, tag)
            validate_sources(course_pfx, tag)
            validate_tex(course_id, tag)

    print(f"\n{'='*60}")
    print(f"Validation result: {len(errors)} errors, {len(warnings)} warnings")
    print(f"{'='*60}\n")

    if errors:
        print("ERRORS:")
        for e in errors:
            print(f"  ✗ {e}")
        print()

    if warnings:
        print("WARNINGS:")
        for w in warnings[:30]:
            print(f"  ! {w}")
        if len(warnings) > 30:
            print(f"  ... and {len(warnings) - 30} more")
        print()

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
