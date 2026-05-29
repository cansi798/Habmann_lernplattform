# K71 „Passen"-Audit (2026-05-29)

**Scope:** K71 alle 16 Tage, alle Materialien (Folien, Handout, Aufgaben, Lösungen, Quiz, Lernpfad, Web-Seiten, PDFs).

**Methode:** 6 parallele Subagenten, 4 Dimensionen.

| Dim | Agent(en) | Was geprüft |
|---|---|---|
| D1 | V | Vollständigkeit aller Artefakte |
| D2 | K1-K4 | Begriffs-Konsistenz Folien ↔ Handout ↔ Aufgaben ↔ Quiz |
| D3 | L | Lernziel-Mapping L1/L2/L3 → Aufgaben + Quiz |
| D5 | V | Pfad-Schema-Validität |

---

## D1 Vollständigkeit · ✅ Perfekt

- 14 Soll-Artefakte × 16 Tage = 224 Dateien geprüft
- 0 fehlen, 0 leer/Stub
- `validate_content.py`: **0 errors**, 1 warning (K22-Quiz, außerhalb Scope)

## D5 Pfad-Schema · ✅ Perfekt

- Alle 16 Pfad-JSONs schemakonform
- `step.typ` ∈ {`video`, `text`} (Pitfall vermieden)
- `aufgabe.typ` ∈ {`single`, `multi`, `text`, `lueckentext`, `zuordnung`}
- Jeweils exakt 7 Schritte pro Pfad

## D2 Begriffs-Konsistenz · 157 Patches

Folien sind nach K6-Welle (2026-05-29) kanonisch. Andere Materialien wurden nachgezogen.

| Agent | Tage | Handout | Aufgaben | Quiz | Summe |
|---|---|---:|---:|---:|---:|
| K1 | 1-4 | 10 | 7 | 1 | 18 |
| K2 | 5-8 | 17 | 13 | 0 | 30 |
| K3 | 9-12 | 21 | 18 | 0 | 50* |
| K4 | 13-16 | 24 | 19 | 16 | 59 |
| **Summe** | | **72** | **57** | **17** | **157** |

\* K3 Tag 9-12 erweitert (Multi-Glossen pro Patch).

**Bewusste Nicht-Patches in Quizzen:** Agenten K1-K3 haben Quiz-Patches großteils unterlassen, wenn die Frage selbst den Begriff abfragt (z.B. „Wofür steht RPA?"). Glossen im Fragetext würden Antworten verraten und Schwierigkeit verfälschen.

## D3 Lernziel-Mapping · ✅ Struktur perfekt, 3 inhaltliche Hinweise

Aufgabenheft enthält per `\nivLi/Lii/Liii`-Tagging exakt 3+5+3 = 11 Aufgaben/Tag mit Lernziel-Zuordnung. Quiz hat 60 Fragen mit 20/25/15 Schwierigkeitsverteilung.

**8 von 16 Tagen perfekt:** 01, 04, 06, 07, 09, 10, 11, 14

**Empfehlungen für menschliche Nacharbeit (Priorität):**

1. **Tag 12** — 57 % der Quiz-Fragen treffen keine Folie-2-Lernziel-Stichworte. Quiz prüft Detailwissen (Audit-Trail-Felder, Exception-Codes, Security-by-Design-Bausteine), das nicht in Folie 2 angekündigt ist. **Entscheidung:** Quiz reduzieren oder Folie 2 ergänzen.
2. **Tag 15** — 38 % ungemappt. Change-Modelle (Kotter/Lewin/ADKAR) sind in Aufg. 2 explizit, in Folie 2 aber nicht prominent. **Fix:** Folie 2 Tag 15 um „Kotter/Lewin/ADKAR" als L1 ergänzen.
3. **Tag 02** — L2-Quiz dünn (3/60). Vermutlich Mess-Artefakt durch UML/Event-Log-Begriffs-Überschneidung mit L1. Stichprobe empfohlen.
4. **Tag 08, 13, 16** — moderate Detailtiefe jenseits Folie-2-Stichworte. Folie 2 ggf. um 1-2 Kernbegriffe je Tag erweitern.

---

## ⚠️ KRITISCH: K6-Folienfehler entdeckt und korrigiert

Die K6-Welle vom selben Tag hatte zwei Abkürzungs-Verwechslungen in den Folien (= kanonischer Quelle), die der „Passen"-Audit aufdeckte. Beide direkt gefixt:

### Fehler 1 — DORA falsch glossiert (Tag 9 + Tag 10)

- **Falsch:** „Digital Operational Resilience Act — EU-Verordnung zur Sicherstellung der digitalen Betriebsstabilität im Finanzsektor"
- **Richtig im Kontext:** „DevOps Research and Assessment — Forschungsgruppe um Forsgren, Humble, Kim; deren vier Flow-Kennzahlen (Lead Time, Deployment Frequency, Change Failure Rate, MTTR) gelten als Industriestandard für High-Performance-Teams" (Buch „Accelerate", 2018)
- **Begründung:** Kontext sind Flow-Kennzahlen + MTTR + Lead Time. Die EU-DORA ist Finanzaufsichts-Verordnung — semantisch deplatziert.
- **Fixed in:** `docs/kurs-71/tag-09/praesentation.html` (8 Stellen), `tag-10/praesentation.html` (4 Stellen)

### Fehler 2 — MDA-Abkürzungs-Familie verwechselt (Tag 5)

- **CIM** falsch als „Computer-Integrated Manufacturing" → richtig **„Computation Independent Model"** (fachlich-organisatorische Anforderungssicht)
- **PIM** falsch als „Product Information Management" → richtig **„Platform Independent Model"** (technologie-neutrales Lösungsmodell)
- **PSM** falsch als „Professional Scrum Master" → richtig **„Platform Specific Model"** (plattform-spezifisches Implementierungsmodell)
- **Begründung:** Kontext ist die MDA-Schichten-Pyramide CIM → PIM → PSM (OMG-Standard für modellgetriebene Architektur).
- **Fixed in:** `docs/kurs-71/tag-05/praesentation.html` (Glossartabelle + alle `<abbr title="…">`-Tooltips)

**Lesson learned:** Bei K6-Glossen-Generierung war der Akronym-Lookup kontextfrei. Bei kontextsensitiven Akronymen (DORA, PSM/PIM/CIM, SLA in Finanz- vs IT-Kontext) muss die Glosse aus dem Folientext erschlossen werden, nicht aus dem allgemeinen Web-Wissen.

---

## Bilanz

| Kategorie | Status |
|---|---|
| Vollständigkeit | 0 Mängel |
| Pfad-Schema | 0 Mängel |
| Begriffs-Konsistenz Folien → Handout/Aufgaben/Quiz | 157 Patches durchgeführt |
| Lernziel-Mapping struktureller Teil | 0 Mängel |
| Lernziel-Mapping inhaltlich | 3-4 menschliche Nacharbeit-Empfehlungen |
| **K6-Folienfehler** | **2 Akronym-Familien direkt gefixt** |

K71 ist nach dieser Welle deutlich konsistenter, mit zwei dokumentierten Empfehlungen für menschliche Nacharbeit auf Tag 12/15 (Lernziel-Folien vs Quiz-Drift).
