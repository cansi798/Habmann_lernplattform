#!/usr/bin/env python3
"""Build platform-wide glossar from HTML presentations and LaTeX handouts.

Sources
-------
1. docs/kurs-{22,71}/tag-*/praesentation.html
   Regex: <abbr title="DEFINITION">TERM</abbr>
   Yields clean (term, definition) pairs, one per occurrence.

2. tex/handout/{22,71}-tag-NN.tex
   Regex: \\fachbegriff{TERM}
   Yields term + following sentence as definition snippet.

Both sources contribute tag references for cross-linking. Output is
written to docs/glossar.html and is deterministic (sorted).
"""

from __future__ import annotations

import glob
import html
import os
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(BASE, 'docs')
TEX_DIR = os.path.join(BASE, 'tex', 'handout')
OUT_HTML = os.path.join(DOCS, 'glossar.html')


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Entry:
    term: str
    definition: str = ''
    occurrences: set = field(default_factory=set)  # (kurs, tag) tuples
    sources: set = field(default_factory=set)      # 'html' / 'tex'


def norm_key(term: str) -> str:
    """Normalize a term for dedup. Keep case-insensitive, strip trailing punct."""
    t = term.strip().rstrip('.,;:!?')
    t = re.sub(r'\s+', ' ', t)
    # NFC + casefold for robust dedup
    return unicodedata.normalize('NFC', t).casefold()


def display_term(term: str) -> str:
    """Cleaned-up display form of a term."""
    t = term.strip().rstrip('.,;:!?')
    return re.sub(r'\s+', ' ', t)


def anchor_for(term: str) -> str:
    """Create a URL-safe anchor for a term."""
    a = unicodedata.normalize('NFKD', term).encode('ascii', 'ignore').decode('ascii')
    a = a.lower()
    a = re.sub(r'[^a-z0-9]+', '-', a).strip('-')
    return a or 'term'


def first_letter(term: str) -> str:
    s = unicodedata.normalize('NFKD', term).encode('ascii', 'ignore').decode('ascii')
    s = s.upper()
    for c in s:
        if c.isalpha():
            return c
    return '#'


# ---------------------------------------------------------------------------
# LaTeX cleanup
# ---------------------------------------------------------------------------

_LATEX_COMMAND_RE = re.compile(r'\\([a-zA-Z@]+)(\s*\*)?\s*(\{[^{}]*\}|\[[^\[\]]*\])?')
_LATEX_INLINE_MATH_RE = re.compile(r'\$[^$]+\$')


def latex_to_text(s: str) -> str:
    """Light LaTeX -> plain text conversion for definition snippets."""
    s = _LATEX_INLINE_MATH_RE.sub('', s)
    # Common inline commands -> just keep their text arg.
    for cmd in ('emph', 'textbf', 'textit', 'fachbegriff', 'underline'):
        s = re.sub(r'\\' + cmd + r'\{([^{}]*)\}', r'\1', s)
    # Drop \quelle{...}
    s = re.sub(r'\\quelle\{[^{}]*\}', '', s)
    # Drop standalone commands like \\, \footnote{...}
    s = re.sub(r'\\footnote\{[^{}]*\}', '', s)
    s = re.sub(r'\\[a-zA-Z@]+\*?(\{[^{}]*\}|\[[^\[\]]*\])?', '', s)
    s = s.replace('--', '–').replace('~', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------

ABBR_RE = re.compile(r'<abbr title="([^"]+)">([^<]+)</abbr>')
FACHBEGRIFF_RE = re.compile(r'\\fachbegriff\{([^{}]+)\}')


def parse_tag_path(path: str) -> tuple[str, int]:
    """Return (kurs, tag_num) from a docs/kurs-XX/tag-YY/* path."""
    m = re.search(r'kurs-(\d+)[\\/]+tag-(\d+)', path)
    if not m:
        raise ValueError(f'cannot parse tag from {path}')
    return m.group(1), int(m.group(2))


def parse_tex_tag(path: str) -> tuple[str, int]:
    """Return (kurs, tag_num) from a tex/handout/XX-tag-YY.tex path."""
    m = re.search(r'(\d{2})-tag-(\d+)\.tex$', path)
    if not m:
        raise ValueError(f'cannot parse tex tag from {path}')
    return m.group(1), int(m.group(2))


def extract_from_html(entries: dict) -> int:
    """Walk all praesentation.html files, gather <abbr> entries."""
    pattern = os.path.join(DOCS, 'kurs-*', 'tag-*', 'praesentation.html')
    n_occurrences = 0
    for path in sorted(glob.glob(pattern)):
        kurs, tag = parse_tag_path(path)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        for m in ABBR_RE.finditer(content):
            raw_def = html.unescape(m.group(1)).strip()
            raw_term = html.unescape(m.group(2)).strip()
            key = norm_key(raw_term)
            e = entries.get(key)
            if e is None:
                e = Entry(term=display_term(raw_term), definition=raw_def)
                entries[key] = e
            else:
                # Prefer the longest definition (most informative)
                if len(raw_def) > len(e.definition):
                    e.definition = raw_def
            e.occurrences.add((kurs, tag))
            e.sources.add('html')
            n_occurrences += 1
    return n_occurrences


def extract_from_tex(entries: dict) -> int:
    """Walk all handout .tex files, gather \\fachbegriff entries."""
    pattern = os.path.join(TEX_DIR, '*.tex')
    n_occurrences = 0
    for path in sorted(glob.glob(pattern)):
        # Only handouts that match XX-tag-YY.tex
        if not re.search(r'\d{2}-tag-\d+\.tex$', path):
            continue
        kurs, tag = parse_tex_tag(path)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Strip TeX comments (lines starting with %) and trailing %... in lines
        content_nc = re.sub(r'(?<!\\)%[^\n]*', '', content)

        for m in FACHBEGRIFF_RE.finditer(content_nc):
            raw_term = m.group(1).strip()
            # Capture some context after the term for definition fallback
            tail = content_nc[m.end(): m.end() + 600]
            # Snippet up to next sentence boundary
            snippet_match = re.search(r'[^.!?]{5,400}[.!?]', tail)
            snippet = snippet_match.group(0) if snippet_match else tail[:300]
            snippet = latex_to_text(snippet)

            key = norm_key(raw_term)
            e = entries.get(key)
            if e is None:
                e = Entry(term=display_term(raw_term), definition=snippet)
                entries[key] = e
            else:
                # Only fill definition if empty / much shorter
                if not e.definition or (
                    'html' not in e.sources and len(snippet) > len(e.definition) * 1.2
                ):
                    e.definition = snippet
            e.occurrences.add((kurs, tag))
            e.sources.add('tex')
            n_occurrences += 1
    return n_occurrences


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

JUNK_PREFIXES = ('http', 'www', 'item ', 'begin', 'end ')

# Patterns that signal a sentence-label rather than a real glossary term.
_SENTENCE_LIKE_RE = re.compile(
    r"(``|''|‚|‘|’|“|”|\.\.\.|/|\\\\|vs\.|--\s)"
)


def is_keepable(e: Entry) -> bool:
    t = e.term.strip()
    if not t or len(t) < 2:
        return False
    # Always keep entries coming from HTML <abbr> — curated.
    if 'html' in e.sources:
        return True
    # For tex-only entries: limit to ~4 words, drop quote-style sentence labels.
    if len(t.split()) > 4:
        return False
    if len(t) > 60:
        return False
    if _SENTENCE_LIKE_RE.search(t):
        return False
    if any(t.lower().startswith(p) for p in JUNK_PREFIXES):
        return False
    return True


# ---------------------------------------------------------------------------
# HTML rendering
# ---------------------------------------------------------------------------

def format_occurrences(occs: set) -> str:
    """Format occurrences as 'K22 Tag 1, 4; K71 Tag 2, 3'."""
    by_kurs = defaultdict(list)
    for kurs, tag in occs:
        by_kurs[kurs].append(tag)
    parts = []
    for kurs in sorted(by_kurs.keys()):
        tags = sorted(set(by_kurs[kurs]))
        parts.append(f'K{kurs} Tag ' + ', '.join(str(t) for t in tags))
    return '; '.join(parts)


def render_html(entries_list: list[Entry]) -> str:
    """Render the full glossar.html page."""
    # Group by first letter
    letters = sorted({first_letter(e.term) for e in entries_list})
    nav_links = '\n      '.join(
        f'<a href="#letter-{l}">{l}</a>' for l in letters
    )

    sections = []
    by_letter: dict[str, list[Entry]] = defaultdict(list)
    for e in entries_list:
        by_letter[first_letter(e.term)].append(e)

    for letter in letters:
        items = []
        for e in by_letter[letter]:
            anchor = anchor_for(e.term)
            meta = format_occurrences(e.occurrences)
            defn = e.definition or '<em style="color:var(--color-muted)">(keine Definition erfasst)</em>'
            items.append(
                f'      <dt id="{anchor}" data-term="{html.escape(e.term.lower())}">'
                f'{html.escape(e.term)} '
                f'<span class="meta">({html.escape(meta)})</span></dt>\n'
                f'      <dd>{defn}</dd>'
            )
        sections.append(
            f'    <section class="letter-block" id="letter-{letter}">\n'
            f'      <h2>{letter}</h2>\n'
            f'      <dl class="glossar">\n' + '\n'.join(items) + '\n      </dl>\n'
            f'    </section>'
        )

    total = len(entries_list)
    sections_html = '\n'.join(sections)
    nav_html = nav_links

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lernplatt · Glossar</title>
  <link rel="stylesheet" href="assets/style.css">
  <style>
    .glossar-toolbar {{
      position: sticky; top: 0; z-index: 5;
      background: var(--color-paper);
      border-bottom: 1px solid var(--color-line);
      padding: 12px 24px;
      display: flex; gap: 16px; align-items: center; flex-wrap: wrap;
    }}
    .glossar-toolbar input {{
      flex: 1 1 280px; min-width: 200px;
      padding: 8px 12px; font-size: 16px;
      border: 1.5px solid var(--color-line-dark); border-radius: var(--radius);
      font-family: inherit;
    }}
    .alpha-nav {{
      display: flex; flex-wrap: wrap; gap: 4px; font-size: 14px;
    }}
    .alpha-nav a {{
      display: inline-block; min-width: 22px; text-align: center;
      padding: 2px 6px; color: var(--kurs-22);
      border: 1px solid var(--color-line); border-radius: 4px;
      text-decoration: none; background: var(--color-bg);
    }}
    .alpha-nav a:hover {{ background: var(--kurs-22-bg); }}
    .letter-block {{ margin: 32px 0; scroll-margin-top: 100px; }}
    .letter-block h2 {{
      color: var(--kurs-22); border-bottom: 2px solid var(--color-line);
      padding-bottom: 4px; margin-bottom: 12px;
    }}
    dl.glossar {{ margin: 0; }}
    dl.glossar dt {{
      font-weight: 700; margin-top: 14px; scroll-margin-top: 100px;
    }}
    dl.glossar dt .meta {{
      font-weight: 400; font-size: 13px; color: var(--color-muted);
      margin-left: 4px;
    }}
    dl.glossar dd {{
      margin: 4px 0 0 0; padding-left: 0; color: var(--color-ink);
      font-size: 15px; line-height: 1.5;
    }}
    .stats {{ font-size: 13px; color: var(--color-muted); }}
    .no-results {{ padding: 40px; text-align: center; color: var(--color-muted); }}
    .letter-block.hidden, dl.glossar dt.hidden, dl.glossar dt.hidden + dd {{
      display: none;
    }}
  </style>
</head>
<body>
<script src="assets/auth.js"></script>
<script>requireAuth();</script>

<div class="brand-bar">
  <a href="dashboard.html">Lernplatt · by Can Siebert</a>
  <a href="#" class="logout">Logout</a>
</div>

<div class="crumbs">
  <a href="dashboard.html">Kurse</a> &rsaquo; Glossar
</div>

<div class="glossar-toolbar">
  <input type="search" id="glossar-search" placeholder="Begriff oder Definition suchen…" autocomplete="off">
  <div class="alpha-nav">
      {nav_html}
  </div>
  <span class="stats">{total} Einträge</span>
</div>

<main>
  <h1>Glossar</h1>
  <p style="color:var(--color-muted);margin-top:0">
    Fachbegriffe und Abkürzungen aus allen 32 Tagen
    (Kurse 22 &amp; 71), zusammengeführt aus Präsentationen und Handouts.
  </p>

{sections_html}

  <p class="no-results" id="no-results" style="display:none">Keine Treffer.</p>
</main>

<script>
(function() {{
  var input = document.getElementById('glossar-search');
  var noResults = document.getElementById('no-results');
  var blocks = document.querySelectorAll('.letter-block');

  function applyFilter() {{
    var q = input.value.trim().toLowerCase();
    var totalVisible = 0;
    blocks.forEach(function(block) {{
      var anyVisible = false;
      var dts = block.querySelectorAll('dl.glossar dt');
      dts.forEach(function(dt) {{
        var dd = dt.nextElementSibling;
        var text = (dt.textContent + ' ' + (dd ? dd.textContent : '')).toLowerCase();
        var match = q === '' || text.indexOf(q) !== -1;
        if (match) {{
          dt.classList.remove('hidden');
          if (dd) dd.style.display = '';
          anyVisible = true;
          totalVisible++;
        }} else {{
          dt.classList.add('hidden');
          if (dd) dd.style.display = 'none';
        }}
      }});
      block.classList.toggle('hidden', !anyVisible);
    }});
    noResults.style.display = totalVisible === 0 ? 'block' : 'none';
  }}

  input.addEventListener('input', applyFilter);
}})();
</script>

<script src="assets/app.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def main():
    entries: dict[str, Entry] = {}

    n_html = extract_from_html(entries)
    print(f'HTML <abbr> occurrences: {n_html}')

    n_tex = extract_from_tex(entries)
    print(f'TeX \\fachbegriff occurrences: {n_tex}')

    # Filter
    filtered = [e for e in entries.values() if is_keepable(e)]
    print(f'Unique terms (raw): {len(entries)}')
    print(f'Unique terms (after filter): {len(filtered)}')

    # Sort alphabetically (locale-aware-ish via NFKD)
    filtered.sort(key=lambda e: (
        first_letter(e.term),
        unicodedata.normalize('NFKD', e.term).encode('ascii', 'ignore').decode().lower(),
    ))

    html_out = render_html(filtered)
    with open(OUT_HTML, 'w', encoding='utf-8') as f:
        f.write(html_out)
    print(f'Wrote {OUT_HTML} ({len(filtered)} entries)')


if __name__ == '__main__':
    main()
