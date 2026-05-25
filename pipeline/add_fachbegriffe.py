#!/usr/bin/env python3
"""Add Fachbegriffe slide and <abbr> tooltips to all 32 presentation HTML files."""

import re
import os
import glob

GLOSSAR = {
    'KPI':  ('Key Performance Indicator',            'Messgröße zur Überwachung und Steuerung unternehmerischer Ziele'),
    'KPIs': ('Key Performance Indicators',           'Messgrößen zur Überwachung und Steuerung unternehmerischer Ziele'),
    'CRM':  ('Customer Relationship Management',     'Systematische Gestaltung aller Kundenbeziehungen im Unternehmen'),
    'ROI':  ('Return on Investment',                 'Kennzahl für die Rentabilität einer Investition; Gewinn geteilt durch Kosten'),
    'CLV':  ('Customer Lifetime Value',              'Gesamtwert eines Kunden über die gesamte Geschäftsbeziehung hinweg'),
    'CAC':  ('Customer Acquisition Cost',            'Durchschnittliche Kosten zur Gewinnung eines neuen Kunden'),
    'SLA':  ('Service Level Agreement',              'Vertraglich vereinbarte Qualitäts- und Leistungsstandards für Dienstleistungen'),
    'SLO':  ('Service Level Objective',              'Konkrete, messbare Zielgröße innerhalb eines SLA'),
    'API':  ('Application Programming Interface',    'Standardisierte Schnittstelle zur Kommunikation zwischen Softwaresystemen'),
    'MVP':  ('Minimum Viable Product',               'Erste marktreife Produktversion mit minimalem Funktionsumfang'),
    'BPMN': ('Business Process Model and Notation',  'Standardisierte grafische Notation zur Modellierung von Geschäftsprozessen (ISO 19510)'),
    'EPC':  ('Ereignisgesteuerte Prozesskette',       'Methode zur grafischen Darstellung und Dokumentation von Geschäftsprozessen'),
    'RPA':  ('Robotic Process Automation',           'Softwarebasierte Automatisierung repetitiver, regelbasierter Aufgaben'),
    'ERP':  ('Enterprise Resource Planning',         'Integriertes Softwaresystem zur unternehmensweiten Ressourcenplanung'),
    'BI':   ('Business Intelligence',                'Technologien und Methoden zur Analyse und Aufbereitung von Unternehmensdaten'),
    'DWH':  ('Data Warehouse',                       'Zentrales Datenlager, das Daten aus verschiedenen Quellen für Analysen konsolidiert'),
    'ETL':  ('Extract, Transform, Load',             'Prozess zur Datenintegration: Extraktion, Umwandlung und Laden in ein Zielsystem'),
    'UI':   ('User Interface',                       'Benutzeroberfläche; alle Elemente, über die Menschen mit einem System interagieren'),
    'UML':  ('Unified Modeling Language',            'Standardisierte grafische Modellierungssprache für Softwarearchitekturen'),
    'VSM':  ('Value Stream Mapping',                 'Lean-Methode zur Visualisierung und Optimierung des gesamten Wertschöpfungsstroms'),
    'WIP':  ('Work in Progress',                     'Menge der gleichzeitig in Bearbeitung befindlichen Arbeitspakete oder Aufgaben'),
    'DLZ':  ('Durchlaufzeit',                        'Gesamtzeit vom Auftragseingang bis zur vollständigen Fertigstellung eines Vorgangs'),
    'ESG':  ('Environmental, Social, Governance',    'Nachhaltigkeitskriterien für ökologisch, sozial und ethisch verantwortliches Handeln'),
    'RACI': ('Responsible, Accountable, Consulted, Informed', 'Verantwortungsmatrix zur Klärung von Rollen und Zuständigkeiten in Projekten'),
    'MQL':  ('Marketing Qualified Lead',             'Interessent, der durch Marketingmaßnahmen als vertriebsrelevant qualifiziert wurde'),
    'SQL':  ('Sales Qualified Lead',                 'Lead, den der Vertrieb als kaufbereit und relevant eingestuft hat'),
    'NRR':  ('Net Revenue Retention',                'Umsatzbindungsrate: Umsatzentwicklung aus dem Bestandskundengeschäft'),
    'SEO':  ('Search Engine Optimization',           'Maßnahmen zur Verbesserung der organischen Sichtbarkeit in Suchmaschinen'),
    'AGB':  ('Allgemeine Geschäftsbedingungen',      'Vorformulierte Vertragsbedingungen, die für alle Kunden eines Anbieters gelten'),
    'DSA':  ('Digital Services Act',                 'EU-Verordnung zur Regulierung von Online-Plattformen und digitalen Diensten (2022)'),
    'DMA':  ('Digital Markets Act',                  'EU-Verordnung zur Kontrolle marktbeherrschender digitaler Plattformen (Gatekeeper)'),
    'DPIA': ('Data Protection Impact Assessment',    'Datenschutz-Folgenabschätzung gemäß DSGVO bei risikoreichen Verarbeitungen'),
    'CSRD': ('Corporate Sustainability Reporting Directive', 'EU-Richtlinie zur verpflichtenden Nachhaltigkeitsberichterstattung für Unternehmen'),
    'ISO':  ('International Organization for Standardization', 'Internationale Organisation, die globale Normen und Standards entwickelt'),
    'KI':   ('Künstliche Intelligenz',               'Technologiefeld der Informatik zur Simulation menschlicher Denkprozesse durch Maschinen'),
    'ML':   ('Machine Learning',                     'Teilgebiet der KI: Systeme erkennen Muster in Daten und lernen daraus'),
    'IT':   ('Informationstechnologie',              'Gesamtheit der Technologien zur Erfassung, Speicherung und Übertragung von Daten'),
    'CI':   ('Continuous Integration',               'Entwicklungspraxis: Codeänderungen werden regelmäßig automatisch getestet und integriert'),
    'CD':   ('Continuous Deployment',                'Automatisierte Auslieferung validierter Software-Änderungen direkt in die Produktion'),
    'QA':   ('Quality Assurance',                    'Qualitätssicherung: systematische Maßnahmen zur Sicherstellung von Produktqualität'),
    'BPMS': ('Business Process Management System',   'Softwareplattform zur Modellierung, Ausführung und Überwachung von Geschäftsprozessen'),
    'MDA':  ('Model-Driven Architecture',            'OMG-Standard: Softwareentwicklung auf Basis plattformunabhängiger Modelle'),
    'PIM':  ('Product Information Management',       'Zentrales System zur Verwaltung von Produktdaten für alle Vertriebskanäle'),
    'TDD':  ('Test-Driven Development',              'Entwicklungsmethode: Tests werden vor dem eigentlichen Programmcode geschrieben'),
    'FAQ':  ('Frequently Asked Questions',           'Sammlung häufig gestellter Fragen mit zugehörigen Antworten'),
    'EA':   ('Enterprise Architecture',              'Gesamtarchitektur eines Unternehmens aus IT- und Geschäftsprozesssicht'),
    'DORA': ('Digital Operational Resilience Act',   'EU-Verordnung zur Sicherstellung der digitalen Betriebsstabilität im Finanzsektor'),
    'XOR':  ('Exclusive Or (Exklusives Oder)',        'Logischer Operator: genau eine von mehreren Bedingungen trifft zu (BPMN-Gateway)'),
    'BT':   ('Bearbeitungszeit',                     'Zeit, die aktiv für die Bearbeitung eines Vorgangs aufgewendet wird'),
    'WT':   ('Wartezeit',                            'Zeitspanne, in der ein Vorgang auf Ressourcen oder Entscheidungen wartet'),
    'PSM':  ('Professional Scrum Master',            'Zertifizierung für agile Prozessbegleitung nach dem Scrum-Framework (Scrum.org)'),
    'CIM':  ('Computer-Integrated Manufacturing',    'Computergestützte Integration aller Produktionsprozesse im Unternehmen'),
    'B2B':  ('Business-to-Business',                 'Geschäftsbeziehungen zwischen Unternehmen (im Gegensatz zu Endkunden)'),
    'B2C':  ('Business-to-Consumer',                 'Geschäftsbeziehungen zwischen Unternehmen und Endverbrauchern'),
    'USP':  ('Unique Selling Proposition',           'Einzigartiges Alleinstellungsmerkmal eines Produkts oder einer Dienstleistung'),
    'OKR':  ('Objectives and Key Results',           'Führungsmethode: ambitionierte Ziele werden mit messbaren Schlüsselergebnissen verknüpft'),
    'SEM':  ('Search Engine Marketing',              'Bezahlte Werbung in Suchmaschinen zur Steigerung der Sichtbarkeit'),
    'CTA':  ('Call to Action',                       'Aufforderung zur konkreten Handlung (z. B. Kaufen, Anmelden, Downloaden)'),
    'NPS':  ('Net Promoter Score',                   'Kennzahl für Kundenloyalität: Weiterempfehlungsbereitschaft auf einer Skala 0–10'),
    'LTV':  ('Lifetime Value',                       'Gesamtdeckungsbeitrag eines Kunden über die gesamte Beziehungsdauer'),
    'CPL':  ('Cost per Lead',                        'Kosten zur Generierung eines qualifizierten Interessenten'),
}

# For short ambiguous abbrs that might cause false positives, restrict matching
SKIP_IN_ATTR = {'CI', 'CD', 'IT', 'ID', 'EU', 'CO'}


def split_html(html):
    """Split HTML into alternating [text, tag, text, tag, ...] parts."""
    return re.split(r'(<[^>]+>)', html)


def join_parts(parts):
    return ''.join(parts)


def find_abbrs_in_text(text, glossar):
    """Find which glossar keys appear as standalone words in plain text."""
    found = {}
    for abbr, (full, defn) in glossar.items():
        pattern = r'\b' + re.escape(abbr) + r'\b'
        if re.search(pattern, text):
            found[abbr] = (full, defn)
    return found


def wrap_abbrs(html, abbrs_found):
    """Wrap each abbreviation in <abbr title="..."> on every occurrence."""
    parts = split_html(html)
    # Track first occurrence per abbr across entire file for fuller title
    seen = set()

    # Process each abbr from longest to shortest to avoid partial matches
    sorted_abbrs = sorted(abbrs_found.keys(), key=len, reverse=True)

    for abbr in sorted_abbrs:
        full, defn = abbrs_found[abbr]
        pattern = re.compile(r'\b' + re.escape(abbr) + r'\b')
        new_parts = []
        for part in parts:
            if part.startswith('<'):
                new_parts.append(part)
            else:
                def make_replacement(m, _abbr=abbr, _full=full, _defn=defn, _seen=seen):
                    if _abbr not in _seen:
                        _seen.add(_abbr)
                        title = f'{_full} – {_defn}'
                    else:
                        title = _full
                    return f'<abbr title="{title}">{_abbr}</abbr>'
                new_parts.append(pattern.sub(make_replacement, part))
        parts = new_parts

    return join_parts(parts)


def make_fachbegriffe_slide(abbrs_found, is_kurs71):
    accent = 'var(--kurs-71)' if is_kurs71 else 'var(--kurs-22)'
    accent_bg = 'var(--kurs-71-bg)' if is_kurs71 else 'var(--kurs-22-bg)'

    rows = ''
    for abbr in sorted(abbrs_found.keys()):
        if abbr.endswith('s') and abbr[:-1] in abbrs_found:
            continue  # skip plural if singular is also present
        full, defn = abbrs_found[abbr]
        rows += (
            f'          <tr>\n'
            f'            <td><strong style="color:{accent}">{abbr}</strong></td>\n'
            f'            <td style="font-style:italic">{full}</td>\n'
            f'            <td style="font-size:13px">{defn}</td>\n'
            f'          </tr>\n'
        )

    return (
        '    <!-- Fachbegriffe & Definitionen (auto-generated) -->\n'
        '    <section class="slide" style="display:none">\n'
        '      <h2>Fachbegriffe &amp; Definitionen</h2>\n'
        '      <p style="font-size:13px;color:var(--color-muted);margin:0 0 10px">Alle Abkürzungen und Fachbegriffe dieser Präsentation auf einen Blick.</p>\n'
        '      <div style="overflow-x:auto">\n'
        '      <table class="vs-table" style="font-size:13px;width:100%">\n'
        '        <thead>\n'
        '          <tr>\n'
        f'            <th style="width:60px;background:{accent_bg};color:{accent}">Kürzel</th>\n'
        f'            <th style="width:30%;background:{accent_bg};color:{accent}">Ausgeschrieben</th>\n'
        f'            <th style="background:{accent_bg};color:{accent}">Definition</th>\n'
        '          </tr>\n'
        '        </thead>\n'
        '        <tbody>\n'
        f'{rows}'
        '        </tbody>\n'
        '      </table>\n'
        '      </div>\n'
        '    </section>\n'
    )


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'Fachbegriffe &amp; Definitionen' in content:
        print(f'  SKIP (already done): {os.path.basename(os.path.dirname(filepath))}/praesentation.html')
        return

    is_kurs71 = 'kurs-71' in filepath

    # Find abbreviations in plain text (strip tags first for scanning)
    plain_text = re.sub(r'<[^>]+>', ' ', content)
    abbrs_found = find_abbrs_in_text(plain_text, GLOSSAR)

    if not abbrs_found:
        print(f'  NO ABBRS: {filepath}')
        return

    # Wrap abbreviations with <abbr> tags
    content = wrap_abbrs(content, abbrs_found)

    # Build Fachbegriffe slide
    fachbegriffe_html = make_fachbegriffe_slide(abbrs_found, is_kurs71)

    # Find insertion point: last <section class="slide" block containing "Quellen · Weiterarbeiten"
    # or the very last slide if no Quellen slide
    quellen_match = None
    for m in re.finditer(r'<section class="slide"[^>]*>', content):
        segment = content[m.start():m.start() + 200]
        if 'Quellen' in segment or 'Ende' in segment:
            quellen_match = m

    if quellen_match is None:
        # Fall back: insert before last <section class="slide">
        all_matches = list(re.finditer(r'<section class="slide"[^>]*>', content))
        if not all_matches:
            print(f'  ERROR no sections: {filepath}')
            return
        quellen_match = all_matches[-1]

    # Step back to find comment or newline before this section
    insert_pos = quellen_match.start()
    # Look for a comment line right before
    before = content[:insert_pos]
    comment_m = re.search(r'(    <!-- (?:Slide \d+|Quellen|Literatur|Ende)[^\n]*\n)$', before)
    if comment_m:
        insert_pos = insert_pos - len(comment_m.group(1))

    content = content[:insert_pos] + fachbegriffe_html + '\n' + content[insert_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    tag = os.path.basename(os.path.dirname(filepath))
    kurs = 'kurs-71' if is_kurs71 else 'kurs-22'
    print(f'  OK {kurs}/{tag}: {len(abbrs_found)} abbreviations')


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    patterns = [
        os.path.join(base, 'docs', 'kurs-22', 'tag-*', 'praesentation.html'),
        os.path.join(base, 'docs', 'kurs-71', 'tag-*', 'praesentation.html'),
    ]
    files = []
    for p in patterns:
        files.extend(sorted(glob.glob(p)))

    print(f'Processing {len(files)} presentation files...')
    for f in files:
        process_file(f)
    print('Done.')


if __name__ == '__main__':
    main()
