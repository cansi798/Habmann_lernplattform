# K71 Multi-Agent Audit + Fix-Welle

**Datum:** 2026-05-26  
**Branch:** main (Worktrees pro Agent)  
**Auftrag:** User möchte alle 16 Tage Kurs 71 systematisch prüfen mit 5 parallel laufenden Agenten.

## Ziel

Audit aller 16 Tage von Kurs 71 (Digital Business Modelling & Transformation) gegen 4 Qualitätsachsen + eindeutige Fixes direkt durchführen, Rest in strukturierten Audit-Berichten flaggen.

## Agenten-Architektur (5 parallel in Worktrees)

### K1 — Korrektheit (Handout + Skript)
- **Scope:** `tex/handout/71-tag-*.tex` (16 Files)
- **Fokus:** Fakten, Definitionen, Modell-Beschreibungen sachlich richtig?
- **Direkt fixen:** Tippfehler, Grammatik, offensichtlich falsche Fakten (mit Begründung im Bericht)
- **Flaggen:** Wertungsfragen, didaktische Entscheidungen, umstrittene Definitionen
- **Out-of-scope:** Aufgaben/Lösungen/Quiz (haben eigenen Agent)

### K2 — Lücken/Vollständigkeit
- **Scope:** alle 96 K71-Artefakte
- **Fokus:** 
  - Verweise auf Konzepte ohne Erklärung
  - Defekte Hyperlinks (URLs nicht erreichbar)
  - Fehlende Quellen-Citations
  - Aufgaben ohne Lösung im Lösungsheft
  - Fachbegriffe ohne Definition
- **Direkt fixen:** fehlende Fachbegriff-Definitionen aus Kontext ableiten, broken-link Warnungen einbauen
- **Flaggen:** strukturelle Lücken (z.B. fehlender Abschnitt)

### K3 — Cross-Day-Konsistenz
- **Scope:** Handouts + Lernpfade als Korpus, Glossar als Referenz
- **Fokus:**
  - Werden Begriffe ab Tag X später konsistent benutzt?
  - Definitionsdrift (Tag 2 sagt X, Tag 9 sagt X')?
  - Didaktische Bauchfolge: nutzt Tag N+1 Konzepte aus Tag N angemessen?
  - Wiederholungen vs. fehlende Vor-Verweise
- **READ-ONLY** — fliegt nur Befund-Report
- **Why:** Cross-Day-Edits zu invasiv für autonomes Agent

### K4 — Qualität Aufgaben & Lösungen
- **Scope:** `tex/aufgaben/71-*.tex` + `tex/loesungen/71-*.tex` (32 Files)
- **Fokus:**
  - L1/L2/L3 Verteilung plausibel (sollte etwa 3-4 / 4-5 / 3-4 sein pro Tag)?
  - Aufgaben-Formulierungen klar/eindeutig?
  - Lösungen vollständig + nachvollziehbar?
  - Modellierungs-Aufgaben mit Visualisierung in Lösung (M4-Fortsetzung)?
- **Direkt fixen:** unklare Formulierungen umformulieren, fehlende Sub-Bullets in Lösungen, Tippfehler
- **Flaggen:** Schwierigkeitsstufen-Drift, didaktische Wahl

### K5 — Quiz-Qualität (B6-Fortsetzung)
- **Scope:** `data/quiz/kurs-71-tag-*.json` (16 Files × 60 Fragen = 960 Fragen)
- **Fokus:**
  - Triviale Distraktoren ("Marketing", "UI-Theme", "beliebig", "irrelevant")
  - Längen-Tells (korrekte Antwort >>> Distraktoren)
  - Korrekte Antworten in same Position-Bias
- **Direkt fixen:** Distraktor-Ersetzung wo offensichtlich trivial → durch plausibel-falsche Alternative
- **Flaggen:** inhaltlich falsche korrekte Antwort

## Datenfluss

```
main → 5 worktrees → 5 Agenten parallel → 5 Berichte + Edits
       ↓
    Ich konsoldiere → 5 Commits auf main (1 pro Agent)
       ↓
    Push → CI → Pages-Deploy
       ↓
    Bericht an User mit zusammengefasstem Befund
```

## Fix-Heuristik (für alle Agenten)

**Direkt fixen wenn:**
- Tippfehler/Grammatik (eindeutig falsch)
- Studyflix/YouTube-URL syntaktisch broken
- Distraktor enthält "Marketing"/"UI-Theme"/"beliebig"/"irrelevant" (B6-Patterns)
- Fachbegriff im Text genutzt aber nicht definiert + Definition aus Kontext eindeutig ableitbar
- Lückentext-Alternative redundant (z.B. exakte case-Duplikate)

**Flaggen (nicht fixen) wenn:**
- Sachliche Korrektheit eines Faktums
- Wahl zwischen mehreren Definitionen
- Didaktische Wertung (zu schwierig / zu leicht)
- Cross-Day-Konsistenz-Verletzungen
- Schwerwiegende strukturelle Lücken
- Unsicherheit über User-Intention

## Verifikation

Pro Agent ein Bericht `tex/audit-K71-{K1..K5}.md` mit:
- Anzahl direkt-Fixes
- Liste der geflaggten Items mit File-Pfad + Zeilen-Nummer
- Empfehlung pro geflagged Item (3 Sätze max)

## Aufwand-Budget

- Jeder Agent max ~60 min Background-Time
- Worktree-Konsolidierung ~5 min
- 5 Commits + 1 Push  
- Final-CI ~10 min
- **Gesamt: ~75-90 min Wall-Clock**

## Out-of-Scope

- K22 (eigener Audit eigenen Tages)
- Praesentations-HTML (visuell, M2-Audit schon durch)
- Re-Strukturierung des Curriculums (Curriculum-Owner-Entscheidung)
