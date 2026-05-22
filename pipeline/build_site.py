"""Site builder: renders all HTML pages from data/*.json + asset folder."""
from __future__ import annotations
import json
from datetime import date
from pathlib import Path

from pipeline.lib.html_templates import page, brand_bar, crumbs

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = ROOT / "data"


def load_course_plan(path: Path | None = None) -> dict:
    p = path or (DATA / "course-plan.json")
    return json.loads(p.read_text(encoding="utf-8"))


def today_iso() -> str:
    return date.today().isoformat()


def render_day_row(tag: dict, kurs_id: str, today: str) -> str:
    is_today = tag["datum"] == today
    cls = "day-row today" if is_today else "day-row"
    tag_nn = f"{tag['nr']:02d}"
    href = f"tag-{tag_nn}/index.html"
    pips = (
        f'<div class="pips" data-kurs="{kurs_id}" data-tag="{tag["nr"]}">'
        + "".join(f'<span class="pip" data-key="{k}"></span>'
                  for k in ["skript", "video", "quiz", "aufgaben", "lernpfad"])
        + "</div>"
    )
    star = '<span class="today-star">★</span>' if is_today else "<span></span>"
    return f"""<a class="{cls}" href="{href}">
  <div>
    <div class="day-date">{tag['datum']} ({tag['wochentag']})</div>
    <div class="day-meta">M{tag['modul']['nr']} · Tag {tag['tag_im_modul']}</div>
  </div>
  <div class="day-title">{tag['thema']}</div>
  {pips}
  {star}
</a>"""


def build_day_list_html(kurs: dict, today: str | None = None) -> str:
    today = today or today_iso()
    rows = "\n".join(render_day_row(t, kurs["id"], today) for t in kurs["tage"])
    crumb_items = [
        {"label": "Kurse", "href": "../dashboard.html"},
        {"label": f"Kurs {kurs['id']}", "href": None},
    ]
    body = f"""
{brand_bar(asset_prefix="../")}
{crumbs(crumb_items)}
<main>
  <h1>{kurs['titel']}</h1>
  <p style="color:var(--color-muted)">{len(kurs['tage'])} Tage</p>
  <div class="day-list">
    {rows}
  </div>
</main>
<script src="../assets/progress.js"></script>
<script>
  document.querySelectorAll(".pips").forEach(el => {{
    const kursId = el.dataset.kurs, tag = parseInt(el.dataset.tag);
    const status = getDayStatus(kursId, tag);
    el.querySelectorAll(".pip").forEach(p => {{
      if (status[p.dataset.key]) p.classList.add("done");
    }});
  }});
</script>
"""
    return page(title=f"Kurs {kurs['id']}", body=body, asset_prefix="../", scripts=[])


def write_day_lists():
    plan = load_course_plan()
    for kurs in plan["kurse"]:
        out_dir = DOCS / f"kurs-{kurs['id'].split('_')[0]}"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(build_day_list_html(kurs), encoding="utf-8")


PHASES = [
    {"nr": "1", "title": "PRÄSENTATION · HANDOUT", "sub": "Theorie aufnehmen", "items": [
        {"name": "Präsentation", "meta": "HTML · Slides", "icon": "🎞", "href": "praesentation.html"},
        {"name": "Handout",      "meta": "PDF · ~30 S.", "icon": "📄", "href": "../../pdf/{kurs_short}-handout-tag-{tag_nn}.pdf"},
    ]},
    {"nr": "2", "title": "VIDEO · PODCAST", "sub": "Vertiefen über Medien", "items": [
        {"name": "Tagesvideo",   "meta": "≈ 20 min", "icon": "📺", "href": "video.html"},
        {"name": "Tagespodcast", "meta": "≈ 25 min", "icon": "🎧", "href": "podcast.html"},
    ]},
    {"nr": "3", "title": "VERTIEFUNG 1 · QUIZ", "sub": "Wissen prüfen", "items": [
        {"name": "Quiz",         "meta": "60 Fragen", "icon": "❓", "href": "quiz.html"},
    ]},
    {"nr": "4", "title": "VERTIEFUNG 2 & ÜBEN · AUFGABEN", "sub": "Anwenden mit Lösungen", "items": [
        {"name": "Aufgabenheft", "meta": "PDF · Übung", "icon": "📝", "href": "../../pdf/{kurs_short}-aufgaben-tag-{tag_nn}.pdf"},
        {"name": "Musterlösung", "meta": "PDF",        "icon": "💡", "href": "../../pdf/{kurs_short}-loesungen-tag-{tag_nn}.pdf"},
    ]},
    {"nr": "5", "title": "VERTIEFUNG 3 & ÜBEN · LERNPFAD", "sub": "Geführter Pfad", "items": [
        {"name": "Lernpfad", "meta": "interaktiv", "icon": "🧭", "href": "lernpfad.html"},
    ]},
]


def build_material_picker_html(kurs: dict, tag: dict) -> str:
    kurs_short = kurs["id"].split("_")[0]
    tag_nn = f"{tag['nr']:02d}"
    phase_blocks = []
    for phase in PHASES:
        cards = []
        for item in phase["items"]:
            href = item["href"].format(kurs_short=kurs_short, tag_nn=tag_nn)
            cards.append(
                f'<a class="material-card" href="{href}">'
                f'<div class="material-icon">{item["icon"]}</div>'
                f'<div>'
                f'<div class="material-name">{item["name"]}</div>'
                f'<div class="material-meta">{item["meta"]}</div>'
                f'</div></a>'
            )
        phase_blocks.append(
            f'<div class="phase-block">'
            f'<div class="phase-header">'
            f'<span class="phase-number">{phase["nr"]}</span>'
            f'<span class="phase-title">{phase["title"]}</span>'
            f'<span class="phase-sub">{phase["sub"]}</span>'
            f'</div>'
            f'<div class="material-row">{"".join(cards)}</div>'
            f'</div>'
        )

    crumb_items = [
        {"label": "Kurse", "href": "../../dashboard.html"},
        {"label": f"Kurs {kurs['id']}", "href": "../index.html"},
        {"label": f"Tag {tag['nr']} ({tag['datum']})", "href": None},
    ]
    body = f"""
{brand_bar(asset_prefix="../../")}
{crumbs(crumb_items)}
<main>
  <h1>Tag {tag['nr']} · {tag['thema']}</h1>
  <p style="color:var(--color-muted)">Modul {tag['modul']['nr']} · {tag['datum']} ({tag['wochentag']}) · {tag['schwerpunkt']}</p>
  {"".join(phase_blocks)}
</main>
"""
    return page(title=f"Tag {tag['nr']}", body=body, asset_prefix="../../", scripts=[])


def write_material_pickers():
    plan = load_course_plan()
    for kurs in plan["kurse"]:
        kurs_short = kurs["id"].split("_")[0]
        for tag in kurs["tage"]:
            tag_nn = f"{tag['nr']:02d}"
            out_dir = DOCS / f"kurs-{kurs_short}" / f"tag-{tag_nn}"
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / "index.html").write_text(build_material_picker_html(kurs, tag), encoding="utf-8")


def build_quiz_page_html(kurs: dict, tag: dict) -> str:
    kurs_short = kurs["id"].split("_")[0]
    tag_nn = f"{tag['nr']:02d}"
    json_path = f"../../../data/quiz/kurs-{kurs_short}-tag-{tag_nn}.json"
    crumb_items = [
        {"label": "Kurse", "href": "../../dashboard.html"},
        {"label": f"Kurs {kurs['id']}", "href": "../index.html"},
        {"label": f"Tag {tag['nr']}", "href": "index.html"},
        {"label": "Quiz", "href": None},
    ]
    body = f"""
{brand_bar(asset_prefix="../../")}
{crumbs(crumb_items)}
<main>
  <div id="quiz-container">Quiz wird geladen …</div>
</main>
<script src="../../assets/dom.js"></script>
<script src="../../assets/progress.js"></script>
<script src="../../assets/quiz.js"></script>
<script>
  (async () => {{
    const data = await loadQuiz("{json_path}");
    new QuizSession(data, document.getElementById("quiz-container")).render();
  }})();
</script>
"""
    return page(title=f"Quiz · Tag {tag['nr']}", body=body, asset_prefix="../../", scripts=[])


def build_lernpfad_page_html(kurs: dict, tag: dict) -> str:
    kurs_short = kurs["id"].split("_")[0]
    tag_nn = f"{tag['nr']:02d}"
    json_path = f"../../../data/pfad/kurs-{kurs_short}-tag-{tag_nn}.json"
    crumb_items = [
        {"label": "Kurse", "href": "../../dashboard.html"},
        {"label": f"Kurs {kurs['id']}", "href": "../index.html"},
        {"label": f"Tag {tag['nr']}", "href": "index.html"},
        {"label": "Lernpfad", "href": None},
    ]
    body = f"""
{brand_bar(asset_prefix="../../")}
{crumbs(crumb_items)}
<main>
  <div id="pfad-container">Lernpfad wird geladen …</div>
</main>
<script src="../../assets/dom.js"></script>
<script src="../../assets/progress.js"></script>
<script src="../../assets/pfad.js"></script>
<script>
  (async () => {{
    const data = await loadPfad("{json_path}");
    new PfadSession(data, document.getElementById("pfad-container")).render();
  }})();
</script>
"""
    return page(title=f"Lernpfad · Tag {tag['nr']}", body=body, asset_prefix="../../", scripts=[])


def write_material_pages():
    plan = load_course_plan()
    for kurs in plan["kurse"]:
        kurs_short = kurs["id"].split("_")[0]
        for tag in kurs["tage"]:
            tag_nn = f"{tag['nr']:02d}"
            out_dir = DOCS / f"kurs-{kurs_short}" / f"tag-{tag_nn}"
            (out_dir / "quiz.html").write_text(build_quiz_page_html(kurs, tag), encoding="utf-8")
            (out_dir / "lernpfad.html").write_text(build_lernpfad_page_html(kurs, tag), encoding="utf-8")


def main():
    write_day_lists()
    write_material_pickers()
    write_material_pages()
    print("Built all generated pages.")


if __name__ == "__main__":
    main()
