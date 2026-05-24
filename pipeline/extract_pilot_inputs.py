"""course-plan.json → data/pilot-tag-XX-kurs-YY.input.json für alle 32 Tage.

Erzeugt aus dem von parse_curriculum.py erzeugten course-plan.json die einzelnen
Pilot-Input-Dateien, die als Eingabe für den Content-Generierungs-Workflow dienen
(Lernpfad, Quiz, Skript, Quellen).

Format der Pilot-Inputs entspricht exakt dem bestehenden
pilot-tag-01-kurs-71.input.json, damit der Workflow konsistent bleibt.

Standardverhalten: erzeugt nur fehlende Dateien (keine Überschreibung).
Mit --force werden alle Pilot-Inputs überschrieben.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = REPO_ROOT / "data"


def kurs_kurz(kurs_id: str) -> str:
    """22_Bo_143 → 22, 71_Dig_42 → 71."""
    return kurs_id.split("_", 1)[0]


def day_to_pilot(kurs: dict, tag: dict) -> dict:
    """Tag-Datensatz aus course-plan in Pilot-Input-Format umwandeln."""
    return {
        "kurs_id": kurs["id"],
        "tag_nr": tag["nr"],
        "datum": tag["datum"],
        "modul": {
            "nr": tag["modul"]["nr"],
            "titel": tag["modul"]["titel"],
        },
        "thema": tag["thema"],
        "schwerpunkt": tag.get("schwerpunkt", ""),
        "lernziele": tag.get("lernziele", {"wissen": [], "anwendung": [], "management": []}),
        "ue_inhalte": [
            {
                "nr": ue.get("nr"),
                "level": ue.get("level", ""),
                "methodik": ue.get("methodik", ""),
                "inhalt": ue.get("inhalt", ""),
            }
            for ue in tag.get("ue", [])
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="bestehende Pilot-Inputs überschreiben")
    args = ap.parse_args()

    plan = json.loads((DATA_DIR / "course-plan.json").read_text(encoding="utf-8"))

    written = 0
    skipped = 0
    for kurs in plan["kurse"]:
        kurz = kurs_kurz(kurs["id"])
        for tag in kurs["tage"]:
            target = DATA_DIR / f"pilot-tag-{tag['nr']:02d}-kurs-{kurz}.input.json"
            if target.exists() and not args.force:
                skipped += 1
                continue
            pilot = day_to_pilot(kurs, tag)
            target.write_text(
                json.dumps(pilot, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            written += 1

    print(f"Geschrieben: {written}, übersprungen (bestehend): {skipped}")


if __name__ == "__main__":
    main()
