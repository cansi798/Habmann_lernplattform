# Audit K71 (Kurs 71 / Dig 42) – Aufgaben + Lösungen, Tag 01–16

**Scope:** `tex/aufgaben/71-aufgaben-tag-01.tex … -16.tex` und `tex/loesungen/71-loesungen-tag-01.tex … -16.tex` (32 Files).
**Datum:** 2026-05-26.
**Methodik:** L1/L2/L3-Marker-Count, Aufgaben/Lösungs-Paarung, Stichprobe der Sub-Bullet-Vollständigkeit, TikZ-Vorkommen bei Modellierungs-Aufgaben, gezielte Tippfehler-/Konsistenz-Suche.

---

## 1. L1/L2/L3-Verteilung – sehr konsistent

Alle 16 Tage halten **exakt** dasselbe Schema ein:

| Niveau | Anzahl pro Tag |
|---|---|
| L1 (Wissen) | 3 |
| L2 (Anwendung) | 5 |
| L3 (Management) | 3 |
| **Gesamt** | **11** |

Lösungs-Files spiegeln das 1:1 (3/5/3 in allen 16 Files).
Das liegt innerhalb der Toleranz (3–4 L1 / 4–5 L2 / 3–4 L3) und sogar darunter (sehr einheitlich).
**Keine Drifts.**

Hinweis: Die Aufgaben-Titel sind in den Lösungs-Files häufig **gekürzt** (z. B. „Workflow-Orchestrierung – Aufgaben, SLAs, Eskalation" → „Workflow-Orchestrierung"). Das ist stilistisch konsistent über alle Tage und kein Fehler, aber es lohnt sich, das als bewusste Konvention zu vermerken (Vorteil: kürzere Inhaltsverzeichnisse).

---

## 2. Aufgaben-Klarheit – grundsätzlich sehr gut

Stichprobe Tag 01 (BPMN), 02 (UML/VSM), 07 (Discovery), 08 (Predictive), 09 (Scrum), 10 (Microservices), 13 (Capacity), 16 (CSRD):

- Aufgaben-Texte sind klar gegliedert, jede Aufgabe hat **Infobox + Arbeitsauftrag + nummerierte Sub-Punkte**.
- Sub-Punkte enthalten meist Mindestmengen („mindestens 5 Activities", „6–8 Use Cases", „acht Features") – das beugt Mehrdeutigkeit vor.
- Hinweise / Cheat-Sheets in den Infoboxen erleichtern den Einstieg in L2/L3-Aufgaben.

**Keine schwerwiegenden Unklarheiten** festgestellt.

---

## 3. Direkte Fixes (in Files angewendet)

### 3.1 Tippfehler: Tag 13 – Titel/Inhalt-Mismatch

`tex/aufgaben/71-aufgaben-tag-13.tex`, L1-Aufgabe 3
- **Titel war:** „Sieben Hebel für Energy-Efficient Data Centers"
- Aufgaben-Text und Arbeitsauftrag listen **acht** Hebel, Lösung antwortet auf alle acht.
- **Fix:** Titel auf „**Acht** Hebel für Energy-Efficient Data Centers" geändert (deckt sich mit Lösungs-Titel und Aufgaben-Inhalt).

### 3.2 Wort-Korruption: Tag 03 Lösung – „östlich" statt „autonom"

`tex/loesungen/71-loesungen-tag-03.tex`, L1-Aufgabe 3 (SOA Orchestrierung vs. Choreographie):

Original (offensichtlich Korruption, vermutlich Autocomplete/Umlaut-Fehler):
> „… E-Commerce: Bestellung **\\"ostlich**, Lager **ostlich**, Versand **ostlich** – jeder reagiert auf Events"

**Fix:** „**autonom**, Lager **autonom**, Versand **autonom**" – passt zur Choreographie-Definition (lose gekoppelte, eigenständig reagierende Services).

---

## 4. Modellierungs-Aufgaben – TikZ-Befund (Flag, kein Fix)

Aufgaben verlangen kein TikZ; Lösungen liefern in 6 von 16 Tagen TikZ-Grafiken (Tag 01, 02, 04, 06, 11) — d. h. jeweils eine Visualisierung pro Tag.

**Modellierungs-Aufgaben mit grafischer Lösung (✓ vorhanden):**

| Tag | Aufgabe | Lösung |
|---|---|---|
| 01 Aufg. 4 | „Bestellprozess BPMN modellieren" | TikZ BPMN-Pool mit Lanes, Gateways, Events ✓ |
| 02 Aufg. 7 | „UML Activity Swimlanes" | TikZ Activity-Diagramm mit 4 Lanes, 3 XOR-Gates ✓ |
| 04 Aufg. 6 | „Execution-BPMN modellieren" | TikZ Execution-BPMN ✓ |
| 06 Aufg. 8 | „E2E Model→Run→Improve" | TikZ Zyklus-Diagramm ✓ |

**Modellierungs-Aufgabe ohne grafische Lösung (Flag):**

- **Tag 02 Aufg. 6 – „UML Use Case – CloudWorks B2B Onboarding".**
  Aufgabe verlangt explizit „Skizzieren Sie ein UML-Use-Case-Diagramm" und „Zeichnen Sie die Beziehungen über Linien".
  Lösung ist **rein textuell** (Akteure, Use Cases, Beziehungen als Bullet-Listen). Konsistenzbruch zu Aufg. 7 (gleicher Tag, UML Activity, hat TikZ).
  **Empfehlung:** TikZ Use-Case-Diagramm in der Lösung ergänzen (Akteure als Strichmännchen, Use Cases als Ellipsen, Linien als Beziehungen), analog zu Tag 02 Aufg. 7. — *Nicht im Audit gefixt, da Umfang einer Neumodellierung außerhalb Tippfehler-Scope.*

**Nicht-Modellierungs-Tage ohne TikZ (kein Flag):**
Tag 03 (Stakeholder-Matrix textuell ok), 05 (EA/MDA Capability Map – tabellarisch ok), 07 (Discovery – Pfad-Listen ok), 08–10, 12–16 (Capacity / DevOps / RPA-Governance / Sustainability / Change / CSRD – konzeptionell, tabellarisch, ohne harten Modellierungsauftrag). Hier ist die textuelle/tabellarische Form thematisch passend.

---

## 5. Lösungs-Vollständigkeit – Stichprobe

Geprüft (alle Sub-Bullets in der Aufgabe finden im Lösungs-Block ihre Antwort):

| Tag/Aufgabe | Sub-Bullets Aufgabe | Sub-Bullets Lösung | Vollständig |
|---|---|---|---|
| Tag 01 / 4 (Modellieren) | 4 | 4 (BPMN + Zweck + 3 Annahmen + 2 Fragen) | ✓ |
| Tag 02 / 6 (Use Case) | 4 | 4 (Use Cases + Beziehungen + Out-of-Scope + Verantw.) | ✓ (Text) |
| Tag 02 / 7 (Activity) | 4 | 4 (+ TikZ) | ✓ |
| Tag 07 / 4 (Discovery) | 4 | 4 (Happy Path + Varianten + Engpässe + Fragen) | ✓ |
| Tag 08 / 9 (Fallstudie FinServe) | 6 | 6 (UC + Features + Label + ETL + Dashboard/Playbook + MVP) | ✓ |
| Tag 10 / 4 (Service-Schnitt O2C) | 3 | 3 (6 Services + 3 Steckbriefe + 1 Guardrail) | ✓ |
| Tag 13 / 3 (Hebel) | 3 | 3 (Tabelle 8 Hebel + Low-Regret + Trugschluss) | ✓ |
| Tag 16 / 4 (ESG-Reportingprozess) | 5 | 5 (9 Schritte + 3 Kontrollen + 5 Evidence + 2 Transparenz + Trade-off) | ✓ |

**Befund:** Stichproben-Lösungen sind durchweg vollständig, gut strukturiert, mit textuell expliziter Zuordnung („1. … 2. … 3. …") zur Aufgabe.

---

## 6. Weitere Befunde / Wertungsfragen

- **Zeitbudget L3-Aufgaben:** Mehrere L3-Aufgaben (Transferprojekte) sind mit 45–60 min angegeben. Realistisch knapp; für Kursteilnehmende ist 60 min für Tag-16-Capstone-Transfer (11) sehr ambitioniert – aber innerhalb des Genres ok. *Kein Fix nötig, ggf. im Begleitmaterial transparent machen.*

- **Wertung „zu schwer/zu leicht":** Subjektiv ausgewogen. L1 ist konsequent reproduzierend (8–10 min, klare Hinweise), L2 hat genügend Cheat-Sheets, L3 ist anspruchsvoll aber durch Fallstudien-Anker geerdet.

- **Numerische Konsistenz:** Außer dem Tag-13-Mismatch („Sieben"↔„Acht") keine weiteren gefundenen Title-vs-Body-Differenzen. (Vergleichs-Skript über alle 16 Paare ausgeführt: nur Kürzungs-Diffs in den Lösungs-Titeln, keine semantischen.)

- **LaTeX-Hygiene:** Keine `TODO`/`FIXME`/`???`-Marker. Keine doppelten Wörter, keine fehlenden Klammern in der Stichprobe.

- **YouTube-Embeds:** `\ytvideo{…}{…}` ist in jeder Aufgabe und jeder Lösung vorhanden. Konsistent.

- **Symmetrie Aufgabe↔Lösung:** Alle 16 Tage haben identische Aufgaben-Nummern und L-Niveaus in beiden Files (Aufgabe 1 = L1 in Aufgaben **und** Lösung etc.). Kein Drift.

---

## 7. Empfehlungen (nicht im Audit gefixt)

1. **Tag 02 Aufg. 6 (UML Use Case):** TikZ-Use-Case-Diagramm in `71-loesungen-tag-02.tex` nachziehen, damit Modellierungs-Aufgaben konsistent grafisch beantwortet werden (M4-Folge-Finding).
2. **Tag 05 / Tag 10:** Optionale TikZ-Visualisierung (Capability Map / Service-Architektur) als Bonus – aktuell tabellarisch, vertretbar.
3. **Lösungs-Titel-Kürzung:** Falls als Konvention dokumentiert, ggf. zentral im Style Guide festhalten.

---

## 8. Direkt-Fixes – Zusammenfassung

| Datei | Position | Fix |
|---|---|---|
| `tex/aufgaben/71-aufgaben-tag-13.tex` | Aufg. 3 Titel | „Sieben Hebel" → „Acht Hebel" (Konsistenz mit Aufgaben-Inhalt & Lösung) |
| `tex/loesungen/71-loesungen-tag-03.tex` | Aufg. 3 SOA | „östlich/ostlich" → „autonom" (Wort-Korruption) |

---

## 9. Gesamteinschätzung

K71 ist auf den 16 Tagen sehr **gleichförmig und qualitativ hoch**: identische Struktur, klare Aufgaben, durchgehend vollständige Lösungen, mehrfache TikZ-Visualisierungen bei den Modellierungs-Schwerpunkten (Tag 01, 02, 04, 06, 11). Die Symmetrie 3/5/3 über alle Tage erleichtert Lernrhythmus und Erwartungsmanagement.

Wichtigste verbleibende Schwachstelle: **Tag 02 Aufg. 6 (UML Use Case) ohne grafische Lösung** – Modellierungs-Aufgabe, die im Vergleich zur direkt folgenden Aufg. 7 (UML Activity mit TikZ) auffällt. Empfohlene Ergänzung außerhalb des Audit-Scopes.

Alle anderen Tage und Aufgaben sind aus Sicht des Audits **freigegeben**.
