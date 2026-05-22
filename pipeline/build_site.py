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


def main():
    write_day_lists()
    print("Built day lists.")


if __name__ == "__main__":
    main()
