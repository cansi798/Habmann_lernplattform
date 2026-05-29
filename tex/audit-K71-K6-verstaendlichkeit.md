# Audit K71 · K6 Verständlichkeit der Folien (2026-05-29)

**Scope:** docs/kurs-71/tag-03 bis tag-16 — Präsentationsfolien (HTML).
Tag 01 + Tag 02 ausgenommen (Onboarding-Tage; Folien-Nummerierung ebenfalls deaktiviert via `class="no-slide-num"`).

**Methode:** 7 parallele Subagenten, je 2 Tage pro Agent. Pro Folien-Datei wurden innerhalb der `<section class="slide">`-Blöcke geprüft:

1. Abkürzungen ohne Langform beim ersten Vorkommen
2. Englische Fachbegriffe ohne deutsche Glosse
3. Fachbegriffe ohne Inline-Definition

**Regeln:**

- Nur erstes Vorkommen pro Datei patchen (keine Wiederholungen).
- Bereits via `<abbr title="…">` vorhandene Glossen unangetastet (kein Duplikat).
- SVG-Texte unverändert (Layoutbruch-Risiko); stattdessen das erste Nicht-SVG-Vorkommen patchen.
- Glossen in **deutscher Sprache**, in Klammern oder per Bindestrich; keine deutschen Anführungszeichen.

## Bilanz pro Tag

| Tag | Patches | Schwerpunkte |
|----:|--------:|--------------|
| 03  | 10 | SOA, Lagging/Leading, PMO/CDO, F&E, QM, Audit Trail, Microservices |
| 04  |  9 | Single Source of Truth, E2E, Boundary Events/Compensation, KSt, Rollback, Value Chain |
| 05  |  6 | Lifecycle, Stakeholder, Onboarding/E2E, IAM, Lead Time/First-Pass-Yield, Enabler |
| 06  | 10 | Closed Loop, Cloud-native, FinOps, DMN, REST, OAuth2, Dead-Letter-Queue, Idempotenz, TMS |
| 07  | 12 | Discovery/Conformance, Event Logs, Happy Path, False Compliance, Bottleneck-Analyse, Procure-to-Pay, 3-Way-Match |
| 08  | 15 | Enhancement/Predictive, Drift, False Positive/Negative, Gaming, FTE/First-Pass-Yield, Data/Concept Drift |
| 09  | 11 | Scrum/Kanban/IaC, Sprint Goal/DoD, Cargo Cult Scrum, Lead Times, Quality Gates, Drift-Detection, Canary Release |
| 10  | 13 | Microservices/K8s, SLOs, Polyglott, Observability, Idempotenz, Circuit Breaker, GitOps, Anti-Corruption-Layer |
| 11  | 10 | Attended/Unattended, Exception Queue, Automation Funnel, Low-Code/Schatten-IT, SoD, PoC, Vault, CoE |
| 12  | 13 | Audit Trail, Bot Governance Lifecycle, MVG, MTTR, Credential Vault, Hash-Chain, PII, Human-in-the-Loop |
| 13  | 12 | ITIL-4, Capacity/Rightsizing, Guardrails, Quick-Wins, Egress-Kosten, On-Call, FinOps, SRE |
| 14  | 13 | Carbon Footprint, Sustainable SD, E-Waste, PDCA, Profiling, Caching/Async/Batch, Scope 1/2/3, GHG |
| 15  | 12 | Sustainment, DoD, Trade-off, WIIFM/Co-Design, Playbooks, Pulse Survey, Q&A, Weekly Standup |
| 16  | 15 | Capstone, Evidence Packs, Risk Appetite, ESRS, CapEx/OpEx, DNSH, Greenwashing, Scope 1+2+3, Single Source of Truth |

**Summe: ~161 Patches** (Mehrfach-Begriffe pro Eintrag eingerechnet, Reineinträge ≈ 153).

## Begleitende Maßnahme — Foliennummer

Eigener Commit (`63f4ea8`):

- `docs/assets/style.css` — globale CSS-Counter-Regel auf `#slides:not(.no-slide-num)`. Folien-Nr als dezentes Badge unten rechts.
- `docs/kurs-71/tag-01/praesentation.html` + `tag-02` — `class="no-slide-num"` am `#slides`-Container (Opt-out).

Wirkung: alle K71-Tage ab Tag 3 bekommen automatisch Folien-Nummern. K22 ebenfalls (wirkt global), jedoch laut Scope nicht Fokus dieses Audits.

## Konvention für künftige Folien

Beim ersten Vorkommen pro Datei:

- **Abkürzung:** `XYZ (Langform)` — z.B. `DSGVO (Datenschutz-Grundverordnung)`
- **Englischer Fachbegriff:** `Begriff (deutsche Glosse)` — z.B. `Churn (Kundenabwanderung)`
- **Komplexer Begriff:** Inline-Erläuterung max. 8-12 Wörter — z.B. `Idempotenz (d.h. mehrfacher Aufruf hat gleichen Effekt wie einer)`
- **Wo `<abbr title="…">` existiert:** dort lassen, nicht doppelt glossen.

## Nicht verändert (bewusst)

- Tag 01 + Tag 02 (Onboarding, fachterminologie-arm).
- SVG-eingebettete Texte (Layoutbruch).
- Style/Script-Blöcke.
- Bereits via `<abbr title="…">` annotierte Begriffe.
- K22-Kurs (außerhalb Scope).
