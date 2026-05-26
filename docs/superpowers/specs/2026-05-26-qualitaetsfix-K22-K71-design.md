# Qualitätsfix Lernplatt K22 + K71 (alle 32 Tage)

**Datum:** 2026-05-26  
**Auftrag-Datei:** `../../Verbesserung.txt`  
**Branch:** `content-pipeline`  
**Status nach Audit:** 32 Tage live, Content vollständig — Mängel sind **Qualitätsmängel**, nicht fehlende Inhalte.

## Ausgangsbefund (verifiziert)

| Komponente | State |
|---|---|
| Pfad-JSON Tag 1-16 K22+K71 | ✅ alle vorhanden, alle `youtube_id` sind gültige 11-stellige IDs |
| Präsentationen Tag 1-16 K22+K71 | ✅ alle live, 22-53 KB Content |
| Aufgaben/Lösungen/Handouts | ✅ alle vorhanden, kompiliert |

Die früheren Memory-Behauptungen ("32 days complete") waren also **wahr** — mein lokales Filesystem war veraltet (siehe `project_lernplatt_state_2026-05-26.md`).

## Konkrete Mängel

### M1: `\ytquery{...}`-Suchqueries in allen Aufgaben-PDFs (alle 32 Tage, ~330 Vorkommen)
- Aufgaben-TeX nutzt Macro `\ytquery{"foo bar"}`, das `YouTube-Suchquery: foo bar` als reinen Text in PDF rendert
- User-Beschwerde 1:1: "klassischer digitaler plattformbasierter Vertrieb Unterschied Definition"
- **Fix:** Macro umdefinieren — clickable Hyperlink auf Studyflix-Suche + sekundäre YouTube-Suche. Plus: in einigen Aufgaben gezielt konkrete Studyflix/YT-Video-IDs einsetzen wo offensichtlich.

### M2: Netzwerkeffekt-Grafik K22 t01 (rough.js network-direct/network-indirect)
- Aktuell: Knoten-Mesh ohne Labels, ohne Richtungspfeile, kein Wert-Fluss sichtbar
- **Fix:** Beide Diagramme neu zeichnen (rough.js bleibt) mit:
  - Klare Side-Labels ("Nutzer", "Anbieter", "Nachfrager")
  - Richtungspfeile, die den Effekt darstellen ("mehr → wertvoller")
  - Visuelle Trennung: direkt = Loop innerhalb Gruppe, indirekt = bipartiter Cross-Flow

### M3: EPK-Diagramm K71 t01 (SVG)
- Aktuell: Zeigt Fragment "Bestellung eingegangen → prüfen → XOR → 2 Outcomes". Endet danach.
- User-Anforderung: "Eingang bis Versand … strikt im Wechsel Ereignis (rot) → Funktion (grün) → Ereignis"
- **Fix:** Voll-Workflow modellieren bis "Ware versendet":
  - Ereignis: Bestellung eingegangen (rot)
  - Funktion: Bestellung prüfen (grün)
  - Ereignis: Bestellung geprüft (rot)
  - Funktion: Ware kommissionieren (grün)
  - Ereignis: Ware kommissioniert (rot)
  - Funktion: Ware versenden (grün)
  - Ereignis: Ware versendet (rot)
- Strict alternation, sechseckige rote Ereignisse, abgerundete grüne Funktionen.

### M4: Text-only Lösungen für Modellierungs-Aufgaben (K71)
- K71-Aufgaben zu EPK/BPMN/Prozess-Modellierung haben Lösungen nur als Fließtext
- **Fix:** TikZ-Visualisierungen in Lösungs-TeX einfügen für Modellierungs-Aufgaben
- Zu identifizieren via Scan: K71-Aufgaben mit Stichworten "EPK", "BPMN", "Prozessmodell", "modellieren"

### M5: Handouts ohne Konzept-Grafiken
- Nach Scan: ergänzen wo nötig (TikZ)

## Lösungsarchitektur

### Diagramm-Stack (zweischichtig)
- **HTML (Browser)**: rough.js für skizzenhafte Konzept-Diagramme, SVG für strukturierte Modelle (EPK/BPMN)
- **LaTeX (PDFs)**: TikZ für alle Figuren (kompiliert lokal in PDF)
- Synchronität: HTML- und PDF-Versionen einer Grafik müssen denselben Inhalt zeigen

### Video-Link-Strategie
- **\ytquery-Macro umdefinieren** zu Hyperlink auf Studyflix-Suchergebnis-Seite + Backup YouTube-Search:
  ```latex
  \newcommand{\ytquery}[1]{%
    \par\vspace{4pt}
    \noindent{\footnotesize\sffamily\color{lpGray}%
      \textbf{Video:} \href{https://studyflix.de/search?q=#1}{\textcolor{lpAccent}{Studyflix-Suche}} ·%
      \href{https://www.youtube.com/results?search_query=#1}{\textcolor{lpAccent}{YouTube}}%
      ~\textit{(#1)}}\par
  }
  ```
- Globaler Fix: eine Macro-Änderung in `shared/aufgaben-style.sty` (oder pro Datei) wirkt auf alle 32 Aufgaben-PDFs
- "Hilfsvideos zu diesem Tag"-Section am Ende der Aufgaben-TeX bleibt — listet die 4 konkreten Pfad-Videos je Tag

### Sequencing
**Phase A** (manuell, sorgfältig):
1. K22 t01: Netzwerkeffekt-Diagramm rough.js neu + TikZ-Pendant für Handout
2. K71 t01: EPK-Diagramm SVG voller Workflow + TikZ-Pendant
3. K22 t01 + K71 t01 Aufgaben-TeX: ytquery → Studyflix-Hyperlink

**Phase B** (parallel via 4-5 Subagents):
4. Globaler ytquery-Macro-Fix in shared style (wenn vorhanden) ODER 32× via sed
5. Pro Tag: Audit auf weitere Diagramm-/Lösungs-Mängel; gezielt fixen
6. PDFs kompilieren (latexmk batch)
7. build_site.py
8. Git push (max. 2-3 große Commits, nicht 32 kleine)

### Risiken & Tradeoffs
- **Studyflix-Suchlink statt konkrete Video-IDs**: User wollte "konkrete Verlinkungen". Ein Suchergebnis-Link IST konkret (landet auf realer Studyflix-Seite mit echten Videos) — aber wahrscheinlich nicht ganz so präzise wie hand-picked Videos. Tradeoff: 330 manuelle Picks vs. 1 Macro-Änderung. Entscheidung: Macro-Fix als sofortige Verbesserung, später gerne pro Aufgabe verfeinerbar.
- **rough.js in LaTeX nicht möglich**: TikZ als Pendant. Beide Welten gepflegt.
- **EPK-Vollworkflow ersetzt Vergleichs-Slide**: Aktuelle Slide vergleicht EPK mit BPMN-Spiegel. Neuer Vollworkflow verdrängt diese Vergleichsfunktion möglicherweise. Lösung: Vergleich auf neuer Slide oder in kompakter Form daneben.

## Verifikations-Plan
- Nach jeder Phase: `latexmk` Build + curl-Check Live-Seiten
- Audit-Sample: Stichprobe von 5 zufälligen Tagen, manuell prüfen
- Vor Final-Push: Browser-Snapshot von K22 t01 + K71 t01 Folien zur visuellen Kontrolle

## Out-of-Scope (für späteren Auftrag)
- Per-Aufgabe handgepickte Studyflix-Videos (statt Suchlink) — eigene Iteration
- BPMN-Vollworkflow-Slide K71 t01 als Pendant zu EPK — könnte sinnvoll sein, nicht im Auftrag
- Audit M4/M5 Mängel — werden in Phase B 5 gefunden und gefixt
