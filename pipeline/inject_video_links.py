#!/usr/bin/env python3
"""Inject 'Hilfsvideos zum Tag' section into every Aufgaben/Lösungen .tex.

For each (course, day):
  - Read pfad JSON, extract video steps with non-empty youtube_id
  - Build a LaTeX block with \href{url}{title} + (URL) in parentheses
  - Insert into both 22-aufgaben-tag-NN.tex and 22-loesungen-tag-NN.tex
    (and 71-*) right before the first \aufgabenkopf{1}{...} call.
Idempotent: skips files that already contain HILFSVIDEOS_MARKER.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_PFAD = ROOT / "data" / "pfad"
TEX_AUFG = ROOT / "tex" / "aufgaben"
TEX_LOES = ROOT / "tex" / "loesungen"

MARKER = "% LERNPLATT_HILFSVIDEOS"


def tex_escape(s: str) -> str:
    repl = {
        "&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#",
        "$": r"\$", "^": r"\^{}", "~": r"\~{}", "{": r"\{", "}": r"\}",
    }
    out = []
    for ch in s:
        out.append(repl.get(ch, ch))
    return "".join(out)


def build_block(videos: list[dict]) -> str:
    lines = [
        MARKER,
        r"\section*{Hilfsvideos zu diesem Tag}",
        r"\addcontentsline{toc}{section}{Hilfsvideos zu diesem Tag}",
        r"\thispagestyle{plain}",
        r"",
        r"\noindent Die folgenden YouTube-Erkl\"arvideos vermitteln die Inhalte, die Sie zur Bearbeitung der Aufgaben ben\"otigen. Klicken Sie auf den Titel, um das Video direkt zu \"offnen; die vollst\"andige URL steht in Klammern.",
        r"",
        r"\begin{description}[style=nextline,leftmargin=18pt,labelindent=0pt,itemsep=8pt]",
    ]
    for i, v in enumerate(videos, 1):
        yid = v["youtube_id"]
        url = f"https://youtu.be/{yid}"
        title = tex_escape(v.get("titel", f"Video {i}"))
        lines.append(rf"  \item[{i}.~{title}] \href{{{url}}}{{\textcolor{{lpAccent}}{{{url}}}}}\\[2pt]")
        lines.append(rf"  {{\footnotesize\color{{lpGray}}(URL: \nolinkurl{{{url}}})}}")
    lines += [
        r"\end{description}",
        r"\vspace{0.6em}",
        r"\noindent{\footnotesize\color{lpGray}\textit{Tipp:} \"Offnen Sie das Video, lassen Sie es im Hintergrund laufen und arbeiten Sie parallel an der Aufgabe.}",
        r"",
        r"\clearpage",
        r"",
    ]
    return "\n".join(lines)


def inject_into_file(path: Path, block: str) -> tuple[bool, str]:
    """Return (changed, reason). Idempotent."""
    if not path.exists():
        return (False, "missing")
    raw = path.read_text(encoding="utf-8")
    if MARKER in raw:
        return (False, "already present")
    # Find first \aufgabenkopf{1}{ usage (not the \newcommand definition)
    m = re.search(r"^(\\aufgabenkopf\{1\}\{)", raw, flags=re.MULTILINE)
    if not m:
        # Fallback: try any \aufgabenkopf{ that is NOT preceded by \newcommand
        m = re.search(r"^(\\aufgabenkopf\{[0-9]+\}\{)", raw, flags=re.MULTILINE)
        if not m:
            return (False, "no \\aufgabenkopf{N}{ pattern")
    pos = m.start(1)
    new_raw = raw[:pos] + block + "\n" + raw[pos:]
    path.write_text(new_raw, encoding="utf-8")
    return (True, "injected")


def main() -> int:
    summary = {"changed": 0, "already": 0, "missing": 0, "error": 0}
    for course in ("22", "kurs-22"), ("71", "kurs-71"):
        cid, ppath = course
        for tag in range(1, 17):
            pfad_file = DATA_PFAD / f"{ppath}-tag-{tag:02d}.json"
            if not pfad_file.exists():
                print(f"  skip {pfad_file.name}: no pfad JSON")
                continue
            d = json.loads(pfad_file.read_text(encoding="utf-8"))
            videos = [
                {"titel": s.get("titel", ""), "youtube_id": s["youtube_id"]}
                for s in d["schritte"]
                if s.get("typ") == "video" and s.get("youtube_id") and s["youtube_id"] != "TODO_VIDEO_ID"
            ]
            if not videos:
                print(f"  skip Tag {tag} K{cid}: no real video IDs")
                continue
            block = build_block(videos)
            for kind, tdir in (("aufgaben", TEX_AUFG), ("loesungen", TEX_LOES)):
                f = tdir / f"{cid}-{kind}-tag-{tag:02d}.tex"
                changed, reason = inject_into_file(f, block)
                tag_label = f"K{cid} T{tag:02d} {kind:>9}"
                if changed:
                    summary["changed"] += 1
                    print(f"  ✓ {tag_label}: {reason} ({len(videos)} videos)")
                elif reason == "already present":
                    summary["already"] += 1
                elif reason == "missing":
                    summary["missing"] += 1
                else:
                    summary["error"] += 1
                    print(f"  ✗ {tag_label}: {reason}")
    print()
    print(f"Summary: changed={summary['changed']}, already={summary['already']}, missing={summary['missing']}, error={summary['error']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
