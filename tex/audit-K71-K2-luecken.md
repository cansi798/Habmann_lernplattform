# Audit K71 — Lücken & Vollständigkeit (16 Tage, alle Materialien)

**Datum:** 2026-05-26
**Scope:** `tex/handout/71-tag-XX.tex`, `tex/aufgaben/71-aufgaben-tag-XX.tex`, `tex/loesungen/71-loesungen-tag-XX.tex`, `data/pfad/kurs-71-tag-XX.json`, `data/quiz/kurs-71-tag-XX.json` (Tage 01–16).

## TL;DR

**Strukturell ist K71 vollständig und sauber.** Alle 80 erwarteten Artefakte (16 Tage × 5 Quellen) liegen vor. Keine fehlenden Lösungen, keine kaputten URL-Syntax, keine unbelegten numerischen Behauptungen, keine Quiz-Defizite, keine Pfad-Schritte ohne Aufgaben.

### Quantitative Befunde

| Prüfung | Soll | Ist | Status |
|---|---|---|---|
| Quiz-Fragen pro Tag | 60 | 60 (alle 16 Tage) | OK |
| Pfad-Schritte pro Tag | 7 | 7 (alle 16 Tage) | OK |
| Aufgaben pro Heft | 11 nummerierte | 11 (alle 16 Tage) | OK |
| Lösungen pro Heft | 11 (1:1) | 11 (alle 16 Tage), je mit `loesungbox` | OK |
| `\href{...}` URL-Syntax | gültig | 94 unique URLs, alle sauber | OK |
| Pfad `aufgabe`-Block | je Schritt 1 | 112/112 vorhanden | OK |
| Pfad `youtube_id` (für `typ=video`) | gültig (11 Zeichen) | alle gültig | OK |

### Aufgabentyp-Verteilung Pfad (112 Schritte)
- `single`: 33, `multi`: 32, `zuordnung`: 17, `lueckentext`: 15, `text`: 15
- MC-Typen haben `erklaerung`+`korrekt`, Freitext (`text`) hat `musterloesung` — beide Schema-Pfade vollständig befüllt.

### Citations (Handouts)
| Tag | `\quelle`/`\cite` | Tag | Citations |
|---|---|---|---|
| 01 | 9 | 09 | 6 |
| 02 | 16 | 10 | 23 |
| 03 | 16 | 11 | 14 |
| 04 | 9 | 12 | 13 |
| 05 | 9 | 13 | 9 |
| 06 | 7 | 14 | 5 |
| 07 | 6 | 15 | 9 |
| 08 | 7 | 16 | 9 |

Tag 14 mit nur 5 Citations und Tag 06–09 mit 6–7 — siehe Flags unten.

---

## Direkt-Fixes (in diesem Audit angewendet)

**Keine.** Es wurden keine Fehler gefunden, die ein automatisches Fix erlaubten:
- Keine syntaktisch kaputten URLs (die `#1`/`#2` in `\newcommand{\ytquery}`/`\ytvideo` sind LaTeX-Parameter, keine echten Hrefs).
- Keine offensichtlichen URL-Tippfehler.
- Keine fehlenden Punctuation in Citations.

---

## Flags (manuelle Review empfohlen)

### F1 — Potenziell veraltete Quelle (Tag 08)
- `https://tdwi.org/research/2011/09/best-practices-report-q4-big-data-analytics.aspx`
  Quelle von 2011 (15 Jahre alt) zu Big-Data-Best-Practices. Inhalt vermutlich noch valide, aber Link-Rot wahrscheinlich. Aktualisieren auf neueren TDWI- oder Gartner-Report empfohlen.

### F2 — Niedrige Citation-Dichte (Tag 14)
Tag 14 hat nur 5 Citations. Thema ist „Green-IT/CSRD/Recycling" (Inhaltsstichworte). Bei nachhaltigkeitsbezogenen Zahlen-Aussagen (PUE, CO2, ISO-Normen) sollten zusätzliche Belege ergänzt werden. Empfehlung: prüfen, ob im Fließtext Behauptungen wie „typische PUE liegt bei …" oder „nach ISO 14001 …" ohne `\quelle` vorkommen.

### F3 — Niedrige Citation-Dichte (Tag 06, 07, 08, 09)
6–7 Citations bei vollen Handouts. Kein konkreter unbelegter Anspruch im Numeric-Claim-Scan (`/(%|Prozent|Mrd|Mio|Studien?|Studie)/`) gefunden, aber Tage in der Mittelphase könnten von zusätzlichen Quellen profitieren (z.B. Forrester/Gartner für RPA-Reifegrade, IEEE/ACM für DevOps-Metriken).

### F4 — `\fachbegriff{}`-Semantik
`\fachbegriff` ist in K71 nur ein Formatierungs-Makro (`\textbf{#1}`), kein Glossar-Eintrag-Trigger. **Strukturell unbedenklich**, aber ein automatischer Glossar-Abgleich ist damit nicht möglich. Bei 581 unique markierten Begriffen über 16 Tage sind sicher einige nicht im `docs/glossar.html` definiert (z.B. „Send/Receive Task", „FinOps", „ISO/IEC 20000"). Empfehlung: separates Glossar-Audit oder Wechsel auf `\glsadd{}`-Schema, falls Glossar-Tracking gewünscht.

### F5 — Studyflix-/YouTube-Such-Templates (kein Bug, dokumentarisch)
Im LaTeX-Makro `\ytquery{#1}` werden Such-URLs `https://studyflix.de/search?query=#1` und `https://www.youtube.com/results?search\_query=#1` generiert. Diese Templates funktionieren als Aufruf-Form, sind aber lediglich Suchtreffer-Listen — die Qualität hängt von der Stichwort-Übergabe ab. Bei Aufrufen ohne brauchbare Stichworte führen sie zu wenig nützlichen Treffern. Empfehlung: stichprobenartig kontrollieren, dass jeder `\ytquery{...}`-Aufruf sinnvolle Suchterms enthält.

---

## Section pro Tag

Da das Audit pro Tag dieselben Befunde liefert (alles strukturell vollständig), nur Ausnahmen aufgeführt:

### Tag 01
- 11 Aufgaben mit Lösungen, 60 Quiz, 7 Pfad-Schritte (4 Video + 3 Text), 9 Citations. **OK.**

### Tag 02 / 03
- 16 Citations (überdurchschnittlich gut belegt). **OK.**

### Tag 04 / 05
- Standard. **OK.**

### Tag 06 / 07
- 6–7 Citations — Flag F3 (niedrigere Belegdichte). Keine konkreten Lücken im Scan.

### Tag 08
- 7 Citations, enthält Tag-08-spezifischen Link `tdwi.org/research/2011/…` — Flag F1.

### Tag 09
- 6 Citations — Flag F3. Pfad Schritt 6 ist `typ=text` mit `musterloesung` (korrekt).

### Tag 10
- 23 Citations — Top-Performer. **OK.**

### Tag 11
- 14 Citations. Pfad Schritt 6 ist `typ=text` mit `musterloesung` (korrekt). **OK.**

### Tag 12
- 13 Citations. Pfad hat 3 Video + 4 Text (statt 4/3). Pfad-Schritt 6 ist `typ=text`. **OK.**

### Tag 13
- 9 Citations. Pfad 3 Video + 4 Text. **OK.**

### Tag 14
- **Nur 5 Citations** — niedrigster Wert. Pfad 3 Video + 4 Text, Schritt 7 ist `typ=text` (korrekt). Flag F2.

### Tag 15 / 16
- 9 Citations je. Tag 16 ist Capstone-Tag mit Capstone-Aufgabe in Schritt 6 (Freitext, `musterloesung` vorhanden). **OK.**

---

## Methodik & Tooling

- URL-Validierung: rein syntaktisch (Schema, Whitespace, Braces). HTTP-HEAD nicht durchgeführt (auftragsgemäß).
- Aufgabenkopf-Zählung via `grep -aoE "aufgabenkopf\{[0-9]+\}"` mit C-Locale (Locale-Pitfall: Standard-Locale erkannte UTF-8-Dateien fälschlich als „binary").
- Quiz-Schema: `fragen[].{id,frage,optionen,korrekt,erklaerung,quelle,schwierigkeit,thema_tag}` — alle Pflichtfelder 100 % vorhanden.
- Pfad-Schema: `schritte[].{nr,typ(video|text),titel,youtube_id,youtube_query,dauer_min,aufgabe{frage,typ,…}}` — schema-konsistent. `aufgabe.typ` und Schritt-`typ` sauber unterschieden (kein Befund zum bekannten Pitfall aus MEMORY).
- Glossar-Abgleich: nur Stichprobe, da `\fachbegriff` als reine Bold-Formatierung definiert.

## Fazit

K71 ist auf den geprüften Ebenen **vollständig**. Keine fehlenden Lösungen, keine kaputten Strukturen, keine syntaktisch defekten Links. Verbesserungspotenzial ausschließlich auf inhaltlicher Belegtiefe (Tag 14, leichter Bedarf 06/07/09) und einem alten TDWI-Link (Tag 08). Keine Direkt-Fixes durchgeführt — alle Flags benötigen redaktionelle Entscheidung.
