# Audit K71 Handouts — Korrektheit

**Scope:** `tex/handout/71-tag-01.tex` bis `tex/handout/71-tag-16.tex` (16 Files, ca. 12.900 Zeilen)
**Auditor-Modus:** Sachlich + Tippfehler + Modell-Konsistenz, kein Stil-Polishing.

## Zusammenfassung

- **3 Direkt-Fixes** in den Files
- **5 geflaggte Items** (zur Entscheidung durch Autor)

Insgesamt sind die 16 Handouts inhaltlich solide. Fachbegriffe (BPMN-Elemente, EPC-Notation, GoM, TOGAF/ADM, Zachman, MDA/CIM/PIM/PSM, ITIL 4 Portfolio-Status, DORA-Metriken, Scrum-2020-Guide, Kotter-8-Steps, Lewin Unfreeze/Change/Refreeze, Schein-3-Schichten, EU-Taxonomie 6 Umweltziele, CSRD/ESRS, Doppelte Wesentlichkeit, Scope 1/2/3, Saltzer & Schroeder 1975, Parnas 1972 high-cohesion/low-coupling, Mendelow 1981, Goodhart via Strathern 1997, Toyota 7+1 Verschwendungen, IEEE XES, van der Aalst Process Mining, Camunda/Flowable, REST/Fielding 2000) sind sachlich korrekt eingesetzt. Quellen sind durchgehend mit APA-7-Stil zitiert. Modell-Beschreibungen (BPMN Pools/Lanes, EPC strikte Alternation, RACI, SLI/SLO/SLA, Error Budgets, Test-Pyramide, Team Topologies, Bot-Lifecycle, ISO-14001-PDCA) sind durchweg lehrbuchkonform.

## Direkt-Fixes

### Fix 1 — `71-tag-02.tex`, Zeile 706

**Original:** „vier Verträgsarten gibt"
**Korrektur:** „vier Vertragsarten gibt"
**Begründung:** Reiner Tippfehler (Umlaut falsch). Plural von „Vertragsart" ist „Vertragsarten" ohne Umlaut.

Diff:
```
- \emph{UML Use Case} -- klärt, dass es vier Verträgsarten gibt mit unterschiedlichen Akteuren
+ \emph{UML Use Case} -- klärt, dass es vier Vertragsarten gibt mit unterschiedlichen Akteuren% Korr: Tippfehler "Verträgsarten" -> "Vertragsarten"
```

### Fix 2 — `71-tag-03.tex`, Zeile 522

**Original:** „kann zur Engpass werden"
**Korrektur:** „kann zum Engpass werden"
**Begründung:** Falscher Artikel. „Engpass" ist Maskulinum, deshalb Dativ „zum" (zu dem), nicht „zur" (zu der).

Diff:
```
- \textbf{Nachteile:} Single Point of Failure (wenn der Dirigent ausfällt), kann zur Engpass werden.
+ \textbf{Nachteile:} Single Point of Failure (wenn der Dirigent ausfällt), kann zum Engpass werden.% Korr: Grammatik "kann zur Engpass" -> "kann zum Engpass" (Maskulinum)
```

### Fix 3 — `71-tag-04.tex`, Zeile 502 (geflaggt unter „Geflaggte Items" — siehe unten)

Dieser Punkt ist als Stilfrage geflaggt, nicht als Direkt-Fix, weil die Intention unklar ist.

---

## Geflaggte Items

### F1 — Modul-/Tag-Nummerierung inkonsistent (Tag 4, 5, 6)

**Files:** `71-tag-04.tex:184`, `71-tag-05.tex:172`, `71-tag-06.tex:177`
**Problem:** Die Cover-Header verwenden in Modulen 1–3 module-relative Tag-Zählung („MODUL 1 · TAG 1 VON 3", „MODUL 2 · TAG 3 VON 4"), wechseln aber ab Tag 9 auf absolute Zählung („MODUL 4 · TAG 9 VON 16"). Inkonsistenzen:
- Tag 4: „MODUL 2 · TAG 4 VON 4" — Modul 2 hätte demnach 4 Tage, das passt aber nur, wenn Tag 5+6 nicht zu Modul 2 gehören.
- Tag 5: „MODUL 2 · TAG 5 VON 4" — unmöglich (Tag 5 von nur 4 Modul-Tagen).
- Tag 6: „MODUL 2 · TAG 6 VON 4" — ebenfalls unmöglich.
- Tag 7: „MODUL 3 · TAG 7 VON 2" — Tag 7 ist erst der erste Tag im Modul 3, müsste also „TAG 1 VON 2" oder „TAG 7 VON 16" sein.

**Empfehlung:** Konsistent auf eine Logik umstellen — entweder durchgängig absolut („TAG x VON 16") wie ab Tag 9, oder durchgängig module-relativ („MODUL m · TAG x VON M") und Modulgrenzen sauber ziehen. Da Tag 9–16 schon absolut zählen, ist absolute Zählung der einfachere Fix. Strukturelle Entscheidung, deshalb geflaggt.

### F2 — Merkbox-Satz unklar formuliert

**File:** `71-tag-04.tex:502`
**Original:** „Geteilte Verantwortung ist Geheimnis um Verantwortung."
**Problem:** Der Satz ergibt grammatikalisch und semantisch keinen klaren Sinn. Wahrscheinlich gemeint: „Geteilte Verantwortung ist Anonymisierung der Verantwortung" oder „Geteilte Verantwortung ist verteilte Verantwortungslosigkeit". Die Intention des Autors lässt sich nicht eindeutig ableiten.
**Empfehlung:** Vom Autor neu formulieren. Drei Optionen:
1. „Geteilte Verantwortung ist anonyme Verantwortung."
2. „Geteilte Verantwortung ist niemandes Verantwortung."
3. „Wenn alle verantwortlich sind, ist es niemand."

### F3 — „PUE 2,0 = doppelter Stromverbrauch" — Formulierung präzisierbar

**File:** `71-tag-13.tex:388`
**Original:** „Ein PUE von 2,0 bedeutet: Für jeden Kilowatt IT werden ein weiterer Kilowatt für Kühlung, Licht, USV etc. verbraucht."
**Problem:** Sachlich korrekt, aber die Formulierung „ein weiterer Kilowatt" (m./f.?) ist unglücklich (Kilowatt ist Neutrum: „ein weiteres Kilowatt"). Außerdem: PUE 1,1 für Hyperscaler ist plausibel (Google reports ~1.10, Meta ~1.09), aber Branchenmittel ist nicht zwingend 1,2–1,4 — laut Uptime Institute Global Survey 2023 liegt der globale Durchschnitt eher bei 1,55.
**Empfehlung:** Grammatik („ein weiteres Kilowatt"); Branchenmittel-Zahl optional aktualisieren oder als „in modernen Hyperscalern" formulieren. Geflaggt, da Fact-check-Detail.

### F4 — Tag 7 Case 102: „Rechnung vor Versand" als Compliance-Risiko

**File:** `71-tag-07.tex:462`, im Vergleich zur Case-Sequenz auf Zeile 327
**Problem:** Tabelle deklariert „Rechnung vor Versand (Case 102)" als Compliance-Risiko mit der Soll-Regel „Rechnung erst nach Versand". Das passt zur Case-Sequenz (Case 102 hat tatsächlich Rechnung → Versand). Sachlich ok. Aber: Die Soll-Regel „Rechnung erst nach Versand" ist nicht universell — in vielen Geschäftsfeldern (Abonnements, Vorkasse, Service-Leistungen, Drop-Ship — was in der Fallstudie selbst später als legitime Variante anerkannt wird, Zeilen 622–633) ist Rechnung vor Versand normal.
**Empfehlung:** Im Lehrtext ergänzen, dass die Beispiel-Regel branchenabhängig ist; oder die Klassifikation explizit als „in dieser Fallstudie" markieren. Konsistenz-Frage, nicht Fehler.

### F5 — Tag 4: Cover-Header „TAG 4 VON 4" plus „Tag 4 von 16" auf gleicher Seite

**File:** `71-tag-04.tex:184` und `:193`
**Problem:** Zeile 184: „MODUL 2 · TAG 4 VON 4". Zeile 193: „Lehrskript -- Tag 4 von 16". Beide stehen auf der Titelseite und widersprechen sich (4-von-4 vs. 4-von-16).
**Empfehlung:** Teil derselben Inkonsistenz wie F1. Vereinheitlichen auf absolute Zählung.

---

## Geprüft, OK (keine Findings)

- **Tag 1 (BPMN/EPC):** BPMN 2.0.2 OMG 2014 ✓; EPC strikte Alternation Ereignis↔Funktion ✓; GoM 7 Grundsätze nach Becker/Rosemann/Schütte 1995 ✓; 7PMG Mendling et al. 2010 ✓; Lanes/Pools-Definition ✓
- **Tag 2 (UML/VSM/Process Mining):** UML 14 Diagrammtypen (UML 2.5.1) ✓; VSM Rother & Shook 1999 ✓; 7 Wastes Ohno/Toyota + 8. „ungenutztes Wissen" ✓; Discovery/Conformance/Enhancement Disziplinen ✓; Event-Log Mindestfelder (Case-ID, Activity, Timestamp) ✓; Alpha/Heuristic/Inductive Miner ✓; Fitness/Precision/Generalization/Simplicity ✓
- **Tag 3 (Stakeholder/KPI/SOA):** Mendelow 1981 Power/Interest-Matrix ✓; Goodhart-Effekt via Strathern 1997 ✓; SOA-Kohäsion/Kopplung mit Parnas-Verweis ✓; Orchestrierung vs. Choreographie ✓
- **Tag 4 (Repository/Execution):** Business-BPMN vs. Execution-BPMN Unterscheidung ✓; Camunda/Flowable/jBPM ✓; FEEL als DMN-Sprache ✓; User/Service/Send/Receive/Script/Business Rule Tasks ✓
- **Tag 5 (EA/MDA):** TOGAF ADM Phasen-Zyklus ✓; Zachman 6×6-Matrix ✓; MDA CIM/PIM/PSM nach OMG ✓; Capability-vs-Prozess-vs-Applikation ✓
- **Tag 6 (BPMS/APIs/Cloud-native):** REST-Architectural Style Fielding 2000 ✓; CMMN/DMN OMG-Standards ✓; SLA/SLO/SLI ✓; Circuit Breaker/Retry/Bulkhead/Timeout Resilienz-Patterns ✓
- **Tag 7 (Discovery/Conformance):** XES IEEE 1849-2016 ✓; Discovery-Algorithmen ✓; Rozinat & van der Aalst 2008 für Conformance ✓
- **Tag 8 (Predictive/Dashboards):** Maggi et al. 2014 Predictive Monitoring ✓; Shmueli 2010 To Explain or to Predict ✓; Kimball Star Schema ✓; Stephen Few Dashboard-Design ✓
- **Tag 9 (Agile/CI/IaC):** Scrum Guide 2020 (3 Rollen, 5 Events inkl. Sprint, 3 Artefakte) — Anmerkung: das Handout listet 4 Events ohne den Sprint selbst zu nennen, der Sprint ist im Guide als 5. Event enthalten — pedantisch, aber im Lehrkontext akzeptabel; DORA-Metriken Forsgren/Humble/Kim 2018 ✓; Kanban Anderson 2010 ✓
- **Tag 10 (Microservices/K8s/DevOps):** Evans 2003 Bounded Context ✓; Skelton & Pais 2019 Team Topologies (4 Typen) ✓; Beck TDD ✓; „You build it, you run it" Werner Vogels ✓; Bezos Two-Way/One-Way-Door ✓
- **Tag 11 (RPA Plattform):** RPA-Eignungskriterien ✓; Attended/Unattended ✓; Kahneman System 1/2 ✓
- **Tag 12 (RPA Skalierung):** Saltzer & Schroeder 1975 Sicherheitsprinzipien ✓ (Least Privilege, Economy of Mechanism, Fail-safe Defaults, Complete Mediation, Separation of Privilege — von ursprünglich 8 Prinzipien sind die 5 wichtigsten hier; vollständige Liste enthält noch Open Design, Least Common Mechanism, Psychological Acceptability — Auslassung unkritisch); Kotter 8 Steps ✓
- **Tag 13 (Sustainable IT/ITIL 4):** ITIL 4 Portfolio Pipeline/Catalogue/Retired ✓; PUE-Definition ✓ (siehe F3 für Detail); Capacity-Dimensionen ✓
- **Tag 14 (Green IT/ISO 14001):** ISO 14001 PDCA ✓; Scope 1/2/3 ✓; A/B/C-Datenqualitätslabels (Branchen-Best-Practice) ✓
- **Tag 15 (Change Management):** Lewin Unfreeze/Change/Refreeze 1951 ✓; Kotter 8 Steps ✓; Schein 3-Schichten-Kulturmodell ✓; Edmondson 1999 psychologische Sicherheit ✓
- **Tag 16 (Regulatorik/CSRD/EU-Taxonomie):** EU-Taxonomie 6 Umweltziele ✓; CSRD doppelte Wesentlichkeit ✓; ESRS Set 1 EFRAG 2023 ✓; Limited/Reasonable Assurance ✓; Scope 1/2/3 ✓

---

## Methodische Anmerkung

Die Audits konzentrieren sich auf Lehrbuch-Fakten und Modell-Beschreibungen. Pädagogische, didaktische und stilistische Aspekte sind aus Scope ausgeschlossen.

Alle 16 Handouts sind aus Korrektheits-Sicht produktionstauglich. Die zwei vorgenommenen Direkt-Fixes (Tippfehler + Grammatik-Artikel) sind nicht-invasiv und tragen Korrektur-Kommentare. Die geflaggten Items sind strukturelle und Stilfragen, die der Autor bewusst entscheiden sollte.
