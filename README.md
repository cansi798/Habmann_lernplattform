# Lernplatt · by Can Siebert

Statische Lernplattform für zwei parallel unterrichtete Kurse, gehostet auf GitHub Pages.

**Kurszeitraum:** 28.05.–19.06.2026

## Aufbau

- `docs/` — GitHub Pages Root (HTML, CSS, JS, PDFs)
- `pipeline/` — Python-Generatoren (Inhalt, Build)
- `data/` — JSON-Datenbestand (Kursplan, Quizzes, Lernpfade)
- `tex/` — LaTeX-Quellen für PDFs

## Lokale Entwicklung

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r pipeline/requirements.txt
python pipeline/build_site.py
```

Site-Vorschau:
```bash
cd docs && python -m http.server 8000
```
Dann http://localhost:8000 öffnen. Zugangscode: `Habmann`.

## Stand der Implementierung

- [x] Plan 1 · Plattform-Skelett (HTML, CSS, JS-Engines, Site-Builder, Dummy-Daten)
- [ ] Plan 2 · Content-Pipeline (Excel-Parser, Quellen, LLM-Generatoren)
- [ ] Plan 3 · LaTeX-Build & Deployment
