# Audit K71 -- Cross-Day-Konsistenz (READ-ONLY)

Korpus: 16 Handouts `tex/handout/71-tag-01.tex` ... `71-tag-16.tex`, Lernpfade `data/pfad/kurs-71-tag-*.json`, Glossar `docs/glossar.html` (1095 Eintraege). Audit-Datum: 2026-05-26.

---

## 1. Definitions-Drift

### 1.1 BPMN -- "2.0" vs. nackt vs. ISO 19510

- Tag 1 (`71-tag-01.tex:308`) definiert BPMN als "Business Process Model and Notation ... Version 2.0 ist seit 2011 ein Standard der Object Management Group (OMG), aktuell in Version 2.0.2 von 2014".
- Tag 4 (`71-tag-04.tex:391`) erwaehnt "BPMN 2.0" als Notation in der Modellierungs-Policy ohne erneute Definition (legitim).
- Glossar (`docs/glossar.html:322-323`) definiert BPMN ueber "ISO 19510" -- *eine dritte Quellenangabe* fuer denselben Begriff.

**Drift:** OMG 2014 (Tag 1) vs. ISO 19510 (Glossar). Beide stimmen sachlich (ISO 19510 = adoptierte OMG-Spec), aber der Lernende sieht zwei verschiedene Referenzen ohne Vermittlung.

### 1.2 Process Mining -- doppelte Definition Tag 2 + Tag 7

- Tag 2 (`71-tag-02.tex:494-496`) fuehrt Process Mining ein: "jüngste der drei Methoden ... TU Eindhoven (van der Aalst) ... Anfang der 2000er Jahre".
- Tag 7 (`71-tag-07.tex:248`) fuehrt es *erneut* ein: "seit etwa 2010 von einem akademischen Spezialthema zu einer breit eingesetzten Management-Disziplin geworden".

**Drift:** Tag 2 sagt "Anfang 2000er", Tag 7 sagt "seit etwa 2010". Inhaltlich kompatibel (Entstehung vs. Breitenwirkung), didaktisch wirkt es jedoch wie zwei Geburtsdaten. Tag 7 referenziert Tag 2 *nicht*, obwohl 3 Pflicht-Spalten (C-A-T) bereits in Tag 2 (Case ID, Aktivität, Zeitstempel) eingefuehrt waren.

### 1.3 Event Log -- 3 Pflicht-Spalten, zweimal definiert

- Tag 2 (`71-tag-02.tex:500-506`) definiert Event Log mit "Case ID / Aktivität / Zeitstempel".
- Tag 7 (`71-tag-07.tex:268-276`) definiert das identische Konzept erneut, diesmal mit der Eselsbruecke "C-A-T". Es gibt *keinen* expliziten Rueckverweis auf Tag 2 (erst Tag 8 referenziert "C-A-T, siehe Tag 7" -- `71-tag-08.tex:303`).

### 1.4 Service -- vier konkurrierende Definitionen

| Tag | Quelle | Definition |
|-----|--------|------------|
| 3 (`71-tag-03.tex:430,434`) | SOA-Service | "klar abgegrenzte Fähigkeit ... Vertrag (Input/Output) ... wiederverwendbar ... Owner" |
| 5 (Glossar im Tex) | EA / Capability | "Fähigkeit der Organisation (Kunde identifizieren). Stabil ueber Reorganisationen." |
| 10 (`71-tag-10.tex:292`) | Microservice / Bounded Context | "Geschäftsfähigkeit ... eigenständige Leistung ... Bounded Context" |
| 13 (`71-tag-13.tex:251-253`) | IT-Service (ITIL 4) | "Leistung, die einem Geschäftsbereich ... einen Wert bietet" |

**Drift:** Vier Begriffsfacetten, ohne dass eine Tag-zu-Tag-Brueck explizit benannt wird ("ein Service in SOA-Logik ist nicht dasselbe wie ein IT-Service in ITIL-Logik"). Der Glossareintrag `service` ist nur an Tag 3 verlinkt (`docs/glossar.html:1897`), waehrend `service-owner` an Tag 13 haengt -- die Vernetzung fehlt.

### 1.5 Workflow-Engine vs. WMS vs. BPMS

- Tag 3 (`71-tag-03.tex:551`) fuehrt **WMS** (Workflow Management System) ein -- van der Aalst & van Hee, 2002.
- Tag 4 (`71-tag-04.tex:294`) spricht von **Workflow-Engine** (Camunda, Flowable, jBPM) und nennt im Klammerzusatz "BPMS-Produkte".
- Tag 6 (`71-tag-06.tex:304-306,375`) definiert **BPMS** als Plattform, die "eine Workflow-Engine ... umschließt" und grenzt es explizit von "nur Workflow-Engine" ab.

**Drift:** Drei Begriffe, drei Definitionen, eine sich entwickelnde Plattformidee. Tag 6 erklaert die Begriffshierarchie zwar in der `merkbox`, aber Tag 3 (WMS) wird nirgends rueckblickend eingeordnet -- der Lernende muss selbst rekonstruieren, dass WMS (Tag 3) und Workflow-Engine (Tag 4) nahezu deckungsgleich sind.

**Empfehlung:** Tag 6 sollte am Anfang oder im Glossar einen Satz wie "WMS (Tag 3) und Workflow-Engine (Tag 4) sind Vorlaeufer/Bestandteile eines BPMS" einfuegen. Konsistenzgewinn ohne inhaltliche Verbiegung.

---

## 2. Schreibweisen- und Notations-Inkonsistenzen

| Begriff | Variante / Haeufigkeit | Empfehlung |
|---------|------------------------|------------|
| BPMN 2.0 | Tag 1: 41x "BPMN", 11x "BPMN 2.0", 1x "BPMN-2.0" (`71-tag-01.tex` Zeilen 281, 391, 451 etc.); Tag 4: 34x "BPMN", 3x "BPMN 2.0" | Standardisieren: "BPMN 2.0" bei erster Erwaehnung pro Tag, danach "BPMN" |
| Durchlaufzeit / DLZ / Lead Time | Tag 2: 17x "Durchlaufzeit" + 10x "DLZ"; Tag 3: 9x "Lead Time" + 1x "Durchlaufzeit"; Tag 5: gemischt; Tag 9 / 10: ausschliesslich "Lead Time" | Begriffstabelle: "Durchlaufzeit (DLZ, engl. Lead Time)" einmal in Tag 2 verankern, danach durchhalten |
| End-to-End / E2E / end-to-end | Tag 1: 2x "End-to-End"; Tag 4: 11x "E2E" + 4x "End-to-End"; Tag 10: 5x "End-to-End" + 2x "E2E" + 2x "end-to-end" (kleinschreibung) | Innerhalb eines Tages eine Form. "E2E" als Akronym nach erster Vollform |
| SLA vs. SLO | Tag 3: 18x SLA, 0 SLO; Tag 6: 21x SLA + 9x SLO; Tag 10: 4x SLA + 15x SLO; Tag 13: 26x SLO, 1x SLA | Begriffstrennung kommunizieren -- SLA = Vertrag, SLO = messbares Ziel. Aktuell nicht expliziert |
| CO₂ | tex-Quellen 22x `CO\textsubscript{2}`; Pfad-Titel Tag 14 schreibt "CO2-Messung" (`data/pfad/kurs-71-tag-14.json`) | Pfad-Titel an Handout-Notation angleichen oder umgekehrt |
| Bot / Roboter / RPA-Bot | Tag 11: 47x "Bot", 1x "Roboter" (`:239`), 2x "RPA-Bot" (Glossar); Tag 12: 58x "Bot", 1x "RPA-Bot" (`:481`) | Konsistent: "RPA-Bot" bei erster Nennung, dann "Bot". "Roboter" als rein rhetorische Variante kennzeichnen |
| 7PMG / GoM | Tag 1: 8x "GoM", 2x "7PMG"; Tag 2: 1x "GoM"; Tag 4: 1x je | OK, aber beide Akronyme einmal in Tag 1 voll auflösen ("Sieben Process Modeling Guidelines", "Grundsaetze ordnungsmaessiger Modellierung") |
| **Titelblatt-Header "Lehrskript -- Tag X von Y"** | Tag 1: "von 3"; Tag 2: "von 2"; Tag 3: "von 4"; Tag 4-16: "von 16" | **Klarer Fehler.** Tag 1-3 wurden offenbar in einer fruehen Korpus-Definition geschrieben und nicht nachgezogen |

**Empfehlung:** Pflicht-Fix der Titelblatt-Inkonsistenz Tag 1-3 (Header "von 3", "von 2", "von 4"). Diese Anomalie ist ohne Mehraufwand korrigierbar und schadet sonst dem Eindruck eines kohaerenten 16-tägigen Kurses unmittelbar auf der ersten Seite.

---

## 3. Didaktische Spruenge und fehlende Vorverweise

### 3.1 Tag 4 -> Tag 3 (Repository-Schicht baut auf SOA/Workflow auf)

Tag 4 (`71-tag-04.tex:220`) verweist auf "Tag 1 bis 3" als gemeinsame Modellierungs-Grundlage, aber das WMS-Konzept aus Tag 3 (Section 7) wird in Tag 4 als "Workflow-Engine" wieder eingefuehrt, ohne Bruecke. Sprung: Tag 3-Leser erwartet eine Vertiefung von WMS, bekommt Repository.

### 3.2 Tag 7 ignoriert Tag 2

Tag 7 (`71-tag-07.tex:248`) eroeffnet Process Mining vollstaendig neu, obwohl Tag 2 (`71-tag-02.tex:494ff`) das Thema bereits in 130 Zeilen ausgebaut hatte -- mit Discovery, Conformance, Enhancement, Alpha/Heuristic/Inductive Miner, Fitness/Precision, sechs Datenquellen, drei-Case-Mini-Log. Tag 7 wiederholt etwa 60 % davon. Tag 7 sollte mit "An Tag 2 haben Sie ... heute vertiefen wir Discovery und Conformance operational" beginnen, statt mit einem zweiten Einstieg auf Niveau 0.

### 3.3 Tag 8 -> Tag 7 (positives Beispiel)

`71-tag-08.tex:303` referenziert C-A-T explizit als "siehe Tag 7" und `:309-311` setzt Discovery + Conformance + Enhancement zusammen. Genau die Form, die Tag 7 zu Tag 2 fehlt.

### 3.4 Tag 9 -> Tag 10 (Sprung Liefer-Architektur -> Microservices)

Tag 9 endet bei CI/CD und IaC; Tag 10 startet mit "Warum klassische Architektur an Grenzen stoesst" und entwickelt Microservices unabhaengig. Es fehlt der explizite Brueckensatz "CI/CD und IaC sind die Voraussetzung dafuer, dass Microservices ueberhaupt betreibbar werden". Konsequenz: Lernende sehen zwei thematisch enge Tage als getrennte Welten.

### 3.5 Tag 11 -> Tag 3/4 (RPA setzt SOA/Service ungeklaert ein)

Tag 11 (`71-tag-11.tex:271`) "Stabiler Prozess, stabile Systeme, API verfuegbar -> eher API-Integration" -- nutzt API-Begriff aus Tag 6, ohne Rueckverweis. Tag 11 erwaehnt nirgends, dass die "Servicegrenzen" aus Tag 3 (SOA) genau das Werkzeug sind, mit dem die "Eignungsfrage" RPA vs. API begruendet wuerde.

### 3.6 Tag 13 -> Tag 3 / Tag 10 (Service-Begriff dritte Mutation)

Tag 13 fuehrt "IT-Service" ein, ohne mit den drei vorherigen Service-Begriffen (SOA, Capability, Microservice) auch nur einen Vergleichssatz zu liefern. Hier liegt der groesste verpasste Vertiefungs-Moment des Kurses.

**Empfehlung pro Sprung:** Ein einzelner Brueckensatz im Einstieg ("An Tag X haben Sie Y kennengelernt; heute ergaenzen wir Z") senkt die kognitive Last erheblich, ohne Inhalt zu kuerzen. Zwei bis drei Saetze pro Tag, in der Praxis 30-60 Minuten Editoraufwand pro Tag.

---

## 4. Vokabular- und Verlinkungs-Hygiene (Glossar)

- Glossar-Tag-Tags: BPMN ist mit Tag 1, 2, 4, 6, 16 verlinkt; tatsaechlich erscheint BPMN auch in Tag 3, 5, 7, 8 (Volltext). Die `<meta>`-Liste in `docs/glossar.html` ist somit nicht vollstaendig.
- `service` ist nur an Tag 3 verlinkt -- Tag 5 (Capability), Tag 10 (Microservice), Tag 13 (IT-Service) fehlen.
- `event-log` ist an Tag 2 und 7 verlinkt -- korrekt.
- `rpa` ist an Tag 1, 11, 12, 16 verlinkt -- Tag 1 enthaelt keinen RPA-Inhalt; vermutlich falsche Zuordnung.

**Empfehlung:** Skript-basierter Re-Sync der `<meta>`-Tag-Listen im Glossar gegen den tex-Volltext. Wenn die HTML aus YAML/JSON generiert wird, dort fixen.

---

## 5. Zusammenfassende Empfehlungen (priorisiert)

1. **Titel-Header Tag 1-3 fixen** ("von 3"/"von 2"/"von 4" -> "von 16"). Sichtbarster Fehler, trivialer Fix.
2. **Service-Begriff explizit abgrenzen** in einem Block "Vier Service-Begriffe des Kurses" -- entweder in Tag 13 oder als zusaetzliche Glossar-Sektion. Verhindert den haeufigsten Verwirrungspunkt.
3. **Brueckensaetze in den Einstiegen** der Tage 4, 7, 10, 11, 13 (je 2-3 Saetze). Klingt nach Kleinigkeit, ist didaktisch der groesste Hebel.
4. **Schreibweisen-Tabelle als Style-Guide** in `tex/STYLE.md` (DLZ vs. Lead Time, E2E vs. End-to-End, SLA vs. SLO, BPMN 2.0). Verhindert weitere Drift bei neuen Tagen.
5. **Glossar `<meta>`-Liste regenerieren** auf Basis tatsaechlicher Vorkommen im tex-Korpus.

---

*Audit beendet. Keine Datei-Edits vorgenommen.*
