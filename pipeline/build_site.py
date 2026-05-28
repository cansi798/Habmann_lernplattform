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


def _media_crumbs(kurs: dict, tag: dict, label: str):
    return [
        {"label": "Kurse", "href": "../../dashboard.html"},
        {"label": f"Kurs {kurs['id']}", "href": "../index.html"},
        {"label": f"Tag {tag['nr']}", "href": "index.html"},
        {"label": label, "href": None},
    ]


VIDEO_EXTS = (".mp4", ".webm", ".mov")
PODCAST_EXTS = (".m4a", ".mp3", ".ogg", ".wav")


def _find_media_file(kurs_short: str, tag_nn: str, kind: str, exts: tuple) -> Path | None:
    """Suche Mediendatei unter docs/media/kurs-{short}/tag-{NN}-{kind}.{ext}."""
    media_dir = DOCS / "media" / f"kurs-{kurs_short}"
    for ext in exts:
        candidate = media_dir / f"tag-{tag_nn}-{kind}{ext}"
        if candidate.exists():
            return candidate
    return None


def build_video_page_html(kurs: dict, tag: dict) -> str:
    kurs_short = kurs["id"].split("_")[0]
    tag_nn = f"{tag['nr']:02d}"
    media_file = _find_media_file(kurs_short, tag_nn, "video", VIDEO_EXTS)
    if media_file is not None:
        src = f"../../media/kurs-{kurs_short}/{media_file.name}"
        mime = {"mp4": "video/mp4", "webm": "video/webm", "mov": "video/quicktime"}[media_file.suffix[1:]]
        player = f"""
  <video controls preload="metadata" playsinline style="width:100%;max-width:960px;border-radius:8px;background:#000">
    <source src="{src}" type="{mime}">
    Dein Browser unterstützt kein HTML5-Video. <a href="{src}">Video herunterladen</a>.
  </video>
  <p style="margin-top:12px;color:var(--color-muted)">
    <a href="{src}" download>⬇ Download (MP4)</a>
  </p>"""
    else:
        player = """
  <div class="pfad-video-placeholder">📺 Video-Platzhalter<br>
    <small>Datei nach <code>docs/media/kurs-XX/tag-NN-video.mp4</code> legen</small>
  </div>"""
    body = f"""
{brand_bar(asset_prefix="../../")}
{crumbs(_media_crumbs(kurs, tag, "Video"))}
<main>
  <h1>Tagesvideo · Tag {tag['nr']}</h1>{player}
</main>
<script src="../../assets/progress.js"></script>
<script>markViewed("{kurs['id']}", {tag['nr']}, "video");</script>
"""
    return page(title=f"Video · Tag {tag['nr']}", body=body, asset_prefix="../../", scripts=[])


def build_podcast_page_html(kurs: dict, tag: dict) -> str:
    kurs_short = kurs["id"].split("_")[0]
    tag_nn = f"{tag['nr']:02d}"
    media_file = _find_media_file(kurs_short, tag_nn, "podcast", PODCAST_EXTS)
    if media_file is not None:
        src = f"../../media/kurs-{kurs_short}/{media_file.name}"
        mime = {"m4a": "audio/mp4", "mp3": "audio/mpeg", "ogg": "audio/ogg", "wav": "audio/wav"}[media_file.suffix[1:]]
        player = f"""
  <audio controls preload="metadata" style="width:100%;max-width:720px">
    <source src="{src}" type="{mime}">
    Dein Browser unterstützt kein HTML5-Audio. <a href="{src}">Podcast herunterladen</a>.
  </audio>
  <p style="margin-top:12px;color:var(--color-muted)">
    <a href="{src}" download>⬇ Download</a>
  </p>"""
    else:
        player = """
  <div class="pfad-video-placeholder">🎧 Podcast-Platzhalter<br>
    <small>Datei nach <code>docs/media/kurs-XX/tag-NN-podcast.m4a</code> legen</small>
  </div>"""
    body = f"""
{brand_bar(asset_prefix="../../")}
{crumbs(_media_crumbs(kurs, tag, "Podcast"))}
<main>
  <h1>Tagespodcast · Tag {tag['nr']}</h1>{player}
</main>
<script src="../../assets/progress.js"></script>
<script>markViewed("{kurs['id']}", {tag['nr']}, "podcast");</script>
"""
    return page(title=f"Podcast · Tag {tag['nr']}", body=body, asset_prefix="../../", scripts=[])


def build_praesentation_page_html(kurs: dict, tag: dict) -> str:
    kurs_short = kurs["id"].split("_")[0]
    tag_nn = f"{tag['nr']:02d}"
    body = f"""
{brand_bar(asset_prefix="../../")}
{crumbs(_media_crumbs(kurs, tag, "Präsentation"))}
<main>
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;margin-bottom:8px">
    <h1 style="margin:0">Präsentation · Tag {tag['nr']}</h1>
    <a href="praesentation.html" download="kurs-{kurs_short}-tag-{tag_nn}-praesentation.html"
       class="quiz-button" style="text-decoration:none;display:inline-flex;align-items:center;gap:6px">
      ⬇ HTML-Download
    </a>
  </div>
  <p style="color:var(--color-muted);margin-top:0">Pfeil-Tasten ← → · F = Vollbild · O = Übersicht</p>
  <div id="slides" style="border:1.5px solid var(--color-line-dark);padding:40px;min-height:400px;background:#fff;border-radius:8px">
    <div class="slide">
      <h2 class="handwritten" style="font-size:36px">{tag['thema']}</h2>
      <p>Modul {tag['modul']['nr']} · Tag {tag['nr']}</p>
      <p style="margin-top:32px;color:var(--color-muted)"><em>Wird automatisch generiert.</em></p>
    </div>
    <div class="slide" style="display:none">
      <h2>Slide 2 — Platzhalter</h2>
      <p>Inhalt folgt.</p>
    </div>
  </div>
</main>
<script src="../../assets/progress.js"></script>
<script src="../../assets/slides.js"></script>
<script>
  new SlideShow(document.getElementById("slides"));
  markViewed("{kurs['id']}", {tag['nr']}, "praesentation");
</script>
"""
    return page(title=f"Präsentation · Tag {tag['nr']}", body=body, asset_prefix="../../", scripts=[])


# Generated präsentation.html files larger than this threshold are treated as
# real content and not overwritten by the stub-builder. Stub-output is ~1.5 kB.
PRAESENTATION_PROTECT_BYTES = 3000


def write_media_pages():
    plan = load_course_plan()
    for kurs in plan["kurse"]:
        kurs_short = kurs["id"].split("_")[0]
        for tag in kurs["tage"]:
            tag_nn = f"{tag['nr']:02d}"
            out_dir = DOCS / f"kurs-{kurs_short}" / f"tag-{tag_nn}"
            (out_dir / "video.html").write_text(build_video_page_html(kurs, tag), encoding="utf-8")
            (out_dir / "podcast.html").write_text(build_podcast_page_html(kurs, tag), encoding="utf-8")
            praesentation_path = out_dir / "praesentation.html"
            if praesentation_path.exists() and praesentation_path.stat().st_size > PRAESENTATION_PROTECT_BYTES:
                continue
            praesentation_path.write_text(build_praesentation_page_html(kurs, tag), encoding="utf-8")


def main():
    write_day_lists()
    write_material_pickers()
    write_material_pages()
    write_media_pages()
    print("Built all generated pages.")


if __name__ == "__main__":
    main()
