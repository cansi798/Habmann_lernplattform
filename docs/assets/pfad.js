// Lernplatt — pfad.js
// Learnpath engine: linear steps, video or text + task, validate before next.
// Task types: single, multi, text, lueckentext, zuordnung.
// Uses el()/clear() from dom.js.

async function loadPfad(jsonPath) {
  const r = await fetch(jsonPath);
  if (!r.ok) throw new Error(`Pfad not found: ${jsonPath}`);
  return r.json();
}

class PfadSession {
  constructor(data, container) {
    this.kursId = data.kurs_id;
    this.tagNr = data.tag_nr;
    this.steps = data.schritte;
    this.title = data.titel;
    this.container = container;
    this.current = 0;
  }

  render() {
    clear(this.container);
    if (this.current >= this.steps.length) return this.renderDone();
    const step = this.steps[this.current];
    this.container.append(
      el('h2', {}, this.title),
      this.renderProgress(),
      el('h3', {}, `Schritt ${step.nr}: ${step.titel}`),
      step.typ === 'video' ? this.renderVideo(step) : this.renderText(step),
      this.renderTask(step.aufgabe),
    );
    this.bindTask(step.aufgabe);
  }

  renderProgress() {
    const bar = el('div', { class: 'pfad-progress-bar' });
    for (let i = 0; i < this.steps.length; i++) {
      const cls = i < this.current ? 'pfad-progress-step done'
                : (i === this.current ? 'pfad-progress-step active' : 'pfad-progress-step');
      bar.append(el('div', { class: cls }, String(i + 1)));
      if (i < this.steps.length - 1) bar.append(el('div', { class: 'pfad-progress-line' }));
    }
    return bar;
  }

  renderVideo(step) {
    if (step.youtube_id && step.youtube_id !== 'TODO_VIDEO_ID') {
      const iframe = el('iframe', { src: `https://www.youtube.com/embed/${step.youtube_id}`, allowfullscreen: true });
      return el('div', { class: 'pfad-video' }, iframe);
    }
    const query = step.youtube_query || '—';
    const searchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(query)}`;
    return el('div', { class: 'pfad-video-placeholder' },
      '📺 Video-Platzhalter', el('br'),
      el('small', {}, 'Such-Vorschlag: ',
        el('a', { href: searchUrl, target: '_blank', rel: 'noopener' }, query)));
  }

  renderText(step) {
    return el('div', { class: 'pfad-text' }, el('p', {}, step.inhalt));
  }

  renderTask(task) {
    this.taskFeedback = el('div', { class: 'quiz-feedback', style: 'display:none' });

    if (task.typ === 'text') return this.renderTextTask(task);
    if (task.typ === 'lueckentext') return this.renderLueckentextTask(task);
    if (task.typ === 'zuordnung') return this.renderZuordnungTask(task);
    return this.renderChoiceTask(task);
  }

  renderTextTask(task) {
    this.taskTextarea = el('textarea', {
      id: 'pfad-text-answer',
      placeholder: 'Hier eigene Antwort eintippen — Musterlösung nach Klick auf "Musterlösung anzeigen"',
      rows: 6,
      style: 'width:100%;padding:12px;font-size:15px;font-family:inherit;border:1.5px solid var(--color-line-dark);border-radius:var(--radius);resize:vertical;margin-top:8px',
    });
    this.taskBtn = el('button', { class: 'quiz-button', id: 'pfad-eval',
      on: { click: () => this.evaluate() } }, 'Musterlösung anzeigen');
    return el('div', { class: 'quiz-card', style: 'margin-top:24px' },
      el('div', { class: 'quiz-question' }, task.frage),
      this.taskTextarea,
      this.taskBtn,
      this.taskFeedback,
    );
  }

  renderChoiceTask(task) {
    this.taskBtn = el('button', { class: 'quiz-button', id: 'pfad-eval', disabled: true,
      on: { click: () => this.evaluate() } }, 'Antwort prüfen');
    return el('div', { class: 'quiz-card', style: 'margin-top:24px' },
      el('div', { class: 'quiz-question' }, task.frage),
      el('div', { class: 'quiz-options' },
        ...task.optionen.map((opt, i) =>
          el('div', { class: 'quiz-option', 'data-idx': i }, opt))),
      this.taskBtn,
      this.taskFeedback,
    );
  }

  renderLueckentextTask(task) {
    // text contains placeholders like {0}, {1}, ... -> inputs
    const segments = task.text.split(/(\{\d+\})/g);
    const luecken = task.luecken || [];
    this.lueckenInputs = [];
    const flow = el('div', { class: 'lueckentext-flow', style: 'line-height:2.2;font-size:16px;margin-top:12px' });
    segments.forEach(seg => {
      const m = seg.match(/^\{(\d+)\}$/);
      if (m) {
        const idx = parseInt(m[1], 10);
        const inp = el('input', {
          type: 'text',
          class: 'lueckentext-input',
          'data-lueck': idx,
          autocomplete: 'off',
          spellcheck: 'false',
          placeholder: `_____`,
          style: 'border:none;border-bottom:2px solid var(--kurs-22);padding:2px 6px;min-width:96px;font-family:inherit;font-size:16px;background:transparent;color:var(--color-ink)',
        });
        this.lueckenInputs[idx] = inp;
        flow.append(inp);
      } else {
        flow.append(document.createTextNode(seg));
      }
    });
    this.taskBtn = el('button', { class: 'quiz-button', id: 'pfad-eval',
      on: { click: () => this.evaluate() } }, 'Antwort prüfen');
    return el('div', { class: 'quiz-card', style: 'margin-top:24px' },
      el('div', { class: 'quiz-question' }, task.frage),
      flow,
      this.taskBtn,
      this.taskFeedback,
    );
  }

  renderZuordnungTask(task) {
    // paare: [{links, rechts}] — display left items in order, right items shuffled.
    // User clicks one left, then one right; pair gets locked with a number.
    const paare = task.paare || [];
    this.zuordnungOriginalIdx = paare.map((_, i) => i);
    // Shuffle the right column once
    const rightOrder = [...paare.keys()];
    for (let i = rightOrder.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [rightOrder[i], rightOrder[j]] = [rightOrder[j], rightOrder[i]];
    }
    this.zuordnungRightOrder = rightOrder;
    this.zuordnungSelectedLeft = null;
    this.zuordnungSelectedRight = null;
    this.zuordnungMatches = new Map(); // leftIdx -> rightIdx (both original indices)
    this.zuordnungPairs = paare;

    const leftCol = el('div', { class: 'zuordnung-col zuordnung-left' });
    const rightCol = el('div', { class: 'zuordnung-col zuordnung-right' });

    paare.forEach((p, i) => {
      leftCol.append(el('div', { class: 'zuordnung-item', 'data-side': 'links', 'data-idx': i }, p.links));
    });
    rightOrder.forEach(origIdx => {
      rightCol.append(el('div', { class: 'zuordnung-item', 'data-side': 'rechts', 'data-idx': origIdx }, paare[origIdx].rechts));
    });

    const grid = el('div', { class: 'zuordnung-grid', style: 'display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:12px' }, leftCol, rightCol);

    const resetBtn = el('button', { type: 'button', class: 'quiz-button-secondary',
      style: 'margin-top:8px;margin-right:8px;background:transparent;border:1.5px solid var(--color-line-dark);color:var(--color-ink);padding:8px 14px;border-radius:var(--radius);cursor:pointer',
      on: { click: () => this.resetZuordnung() } }, '↺ Zurücksetzen');
    this.taskBtn = el('button', { class: 'quiz-button', id: 'pfad-eval', disabled: true,
      on: { click: () => this.evaluate() } }, 'Antwort prüfen');

    return el('div', { class: 'quiz-card', style: 'margin-top:24px' },
      el('div', { class: 'quiz-question' }, task.frage),
      el('p', { style: 'color:var(--color-muted);font-size:14px;margin:4px 0 0' },
        'Klick zuerst links, dann rechts auf das passende Gegenstück.'),
      grid,
      el('div', { style: 'margin-top:8px' }, resetBtn, this.taskBtn),
      this.taskFeedback,
    );
  }

  resetZuordnung() {
    if (this.evaluated) return;
    this.zuordnungMatches.clear();
    this.zuordnungSelectedLeft = null;
    this.zuordnungSelectedRight = null;
    this.container.querySelectorAll('.zuordnung-item').forEach(node => {
      node.classList.remove('selected', 'matched', 'correct', 'wrong');
      const badge = node.querySelector('.zuordnung-badge');
      if (badge) badge.remove();
    });
    this.taskBtn.disabled = true;
  }

  bindTask(task) {
    if (task.typ === 'text') {
      this.evaluated = false;
      return;
    }
    if (task.typ === 'lueckentext') {
      this.evaluated = false;
      // Button always enabled — empty answer counted as wrong.
      return;
    }
    if (task.typ === 'zuordnung') {
      this.evaluated = false;
      this.container.querySelectorAll('.zuordnung-item').forEach(node => {
        node.addEventListener('click', () => {
          if (this.evaluated) return;
          if (node.classList.contains('matched')) return;
          const side = node.dataset.side;
          const idx = parseInt(node.dataset.idx, 10);
          if (side === 'links') {
            this.container.querySelectorAll('.zuordnung-left .zuordnung-item').forEach(n => n.classList.remove('selected'));
            node.classList.add('selected');
            this.zuordnungSelectedLeft = idx;
          } else {
            this.container.querySelectorAll('.zuordnung-right .zuordnung-item').forEach(n => n.classList.remove('selected'));
            node.classList.add('selected');
            this.zuordnungSelectedRight = idx;
          }
          if (this.zuordnungSelectedLeft !== null && this.zuordnungSelectedRight !== null) {
            this.zuordnungMatches.set(this.zuordnungSelectedLeft, this.zuordnungSelectedRight);
            // Lock both items
            const leftNode = this.container.querySelector(`.zuordnung-left .zuordnung-item[data-idx="${this.zuordnungSelectedLeft}"]`);
            const rightNode = this.container.querySelector(`.zuordnung-right .zuordnung-item[data-idx="${this.zuordnungSelectedRight}"]`);
            const num = this.zuordnungMatches.size;
            leftNode.classList.remove('selected'); leftNode.classList.add('matched');
            rightNode.classList.remove('selected'); rightNode.classList.add('matched');
            leftNode.prepend(el('span', { class: 'zuordnung-badge' }, `${num}`));
            rightNode.prepend(el('span', { class: 'zuordnung-badge' }, `${num}`));
            this.zuordnungSelectedLeft = null;
            this.zuordnungSelectedRight = null;
            if (this.zuordnungMatches.size === this.zuordnungPairs.length) {
              this.taskBtn.disabled = false;
            }
          }
        });
      });
      return;
    }
    // Single / multi choice
    const multi = task.typ === 'multi';
    this.selected = multi ? [] : null;
    this.evaluated = false;
    this.container.querySelectorAll('.quiz-option').forEach((node, i) => {
      node.addEventListener('click', () => {
        if (this.evaluated) return;
        if (multi) {
          const k = this.selected.indexOf(i);
          if (k >= 0) this.selected.splice(k, 1); else this.selected.push(i);
          node.classList.toggle('selected', this.selected.includes(i));
        } else {
          this.selected = i;
          this.container.querySelectorAll('.quiz-option').forEach((n, j) =>
            n.classList.toggle('selected', j === i));
        }
        this.taskBtn.disabled = multi ? this.selected.length === 0 : this.selected === null;
      });
    });
  }

  evaluate() {
    if (this.evaluated) return;
    this.evaluated = true;
    const step = this.steps[this.current];
    const task = step.aufgabe;

    if (task.typ === 'text') return this.evaluateText(task);
    if (task.typ === 'lueckentext') return this.evaluateLueckentext(task);
    if (task.typ === 'zuordnung') return this.evaluateZuordnung(task);
    return this.evaluateChoice(task);
  }

  evaluateText(task) {
    const own = this.taskTextarea ? this.taskTextarea.value.trim() : '';
    clear(this.taskFeedback);
    this.taskFeedback.append(
      el('div', { style: 'background:#fffce0;border-left:4px solid #d4a000;padding:10px 12px;border-radius:4px;margin-bottom:10px' },
        el('strong', {}, '📝 Musterlösung'),
        el('div', { style: 'margin-top:6px;white-space:pre-wrap' }, document.createTextNode(task.musterloesung || task.erklaerung || '—')),
      ),
      own ? el('div', { style: 'background:#f3f3f3;padding:10px 12px;border-radius:4px;font-size:14px;color:var(--color-muted)' },
        el('strong', {}, 'Deine Antwort '),
        document.createTextNode('(bleibt lokal in deinem Browser):'),
        el('div', { style: 'margin-top:6px;white-space:pre-wrap;color:var(--color-ink)' }, own),
      ) : null,
    );
    this.taskFeedback.style.display = 'block';
    this.advanceButton();
  }

  evaluateLueckentext(task) {
    const luecken = task.luecken || [];
    const results = luecken.map((l, i) => {
      const inp = this.lueckenInputs[i];
      const value = (inp ? inp.value : '').trim();
      const candidates = [l.antwort, ...(l.alternativen || [])].map(s => s.toLowerCase().trim());
      const ok = value && candidates.includes(value.toLowerCase());
      if (inp) {
        inp.style.borderBottomColor = ok ? '#2a8a2a' : 'var(--today)';
        inp.style.color = ok ? '#1a6a1a' : '#9d1a1a';
        inp.disabled = true;
      }
      return { ok, value, expected: l.antwort };
    });
    const allOk = results.every(r => r.ok);
    clear(this.taskFeedback);
    this.taskFeedback.append(
      el('strong', {}, allOk ? '✓ Alle Lücken richtig!' : '✗ Nicht alle Lücken stimmen.'),
    );
    if (!allOk) {
      const list = el('ul', { style: 'margin:6px 0 0;padding-left:18px' });
      results.forEach((r, i) => {
        if (!r.ok) list.append(el('li', {},
          el('em', {}, `Lücke ${i + 1}: `),
          'erwartet ', el('strong', {}, r.expected),
          r.value ? document.createTextNode(`, deine Eingabe: „${r.value}"`) : document.createTextNode(' (nicht ausgefüllt)'),
        ));
      });
      this.taskFeedback.append(list);
    }
    if (task.erklaerung) {
      this.taskFeedback.append(el('div', { style: 'margin-top:8px' }, task.erklaerung));
    }
    this.taskFeedback.style.display = 'block';
    this.advanceButton();
  }

  evaluateZuordnung(task) {
    let correctCount = 0;
    this.zuordnungMatches.forEach((rightIdx, leftIdx) => {
      const ok = rightIdx === leftIdx;
      if (ok) correctCount++;
      const leftNode = this.container.querySelector(`.zuordnung-left .zuordnung-item[data-idx="${leftIdx}"]`);
      const rightNode = this.container.querySelector(`.zuordnung-right .zuordnung-item[data-idx="${rightIdx}"]`);
      if (leftNode) leftNode.classList.add(ok ? 'correct' : 'wrong');
      if (rightNode) rightNode.classList.add(ok ? 'correct' : 'wrong');
    });
    const total = this.zuordnungPairs.length;
    const allOk = correctCount === total;
    clear(this.taskFeedback);
    this.taskFeedback.append(
      el('strong', {}, allOk ? `✓ Alle ${total} Zuordnungen richtig!` : `✗ ${correctCount} von ${total} korrekt.`),
    );
    if (!allOk) {
      const list = el('ul', { style: 'margin:6px 0 0;padding-left:18px' });
      this.zuordnungPairs.forEach((p, i) => {
        list.append(el('li', {},
          el('strong', {}, p.links),
          document.createTextNode(' → '),
          el('em', {}, p.rechts),
        ));
      });
      this.taskFeedback.append(el('div', { style: 'margin-top:6px;font-size:14px' }, 'Richtige Zuordnung:'), list);
    }
    if (task.erklaerung) {
      this.taskFeedback.append(el('div', { style: 'margin-top:8px' }, task.erklaerung));
    }
    this.taskFeedback.style.display = 'block';
    this.advanceButton();
  }

  evaluateChoice(task) {
    const multi = task.typ === 'multi';
    let correct;
    if (multi) {
      const sel = new Set(this.selected); const exp = new Set(task.korrekt);
      correct = sel.size === exp.size && [...sel].every(x => exp.has(x));
    } else {
      correct = this.selected === task.korrekt;
    }
    this.container.querySelectorAll('.quiz-option').forEach((node, i) => {
      const isCorrect = multi ? task.korrekt.includes(i) : i === task.korrekt;
      const isSelected = multi ? this.selected.includes(i) : i === this.selected;
      if (isCorrect) node.classList.add('correct');
      else if (isSelected) node.classList.add('wrong');
    });
    clear(this.taskFeedback);
    this.taskFeedback.append(
      el('strong', {}, correct ? '✓ Richtig!' : '✗ Nicht ganz.'),
      el('br'),
      document.createTextNode(task.erklaerung),
    );
    this.taskFeedback.style.display = 'block';
    this.advanceButton();
  }

  advanceButton() {
    this.taskBtn.textContent = this.current + 1 < this.steps.length ? 'Weiter →' : 'Lernpfad abschließen';
    this.taskBtn.disabled = false;
    this.taskBtn.onclick = () => this.next();
  }

  next() {
    if (typeof recordPfadStep === 'function') {
      recordPfadStep(this.kursId, this.tagNr, this.steps[this.current].nr);
    }
    this.current++;
    this.render();
  }

  renderDone() {
    this.container.append(
      el('h2', {}, this.title),
      el('p', { style: 'font-size:20px' }, '✓ Lernpfad abgeschlossen!'),
      el('a', { href: './index.html' }, 'Zurück zur Materialauswahl'),
    );
  }
}
