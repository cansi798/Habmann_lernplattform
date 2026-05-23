// Lernplatt — quiz.js
// Quiz engine with 2 modes: 'single' (eine Frage pro Bildschirm) und 'all' (alle Fragen scrollend).
// Uses el()/clear() from dom.js — no string-based HTML injection.

function shuffleArray(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

function shuffleQuestion(q) {
  const withIdx = q.optionen.map((opt, i) => ({ opt, originalIdx: i }));
  const shuffled = shuffleArray(withIdx);
  return {
    ...q,
    optionen: shuffled.map(x => x.opt),
    korrekt: shuffled.findIndex(x => x.originalIdx === q.korrekt),
  };
}

async function loadQuiz(jsonPath) {
  const r = await fetch(jsonPath);
  if (!r.ok) throw new Error(`Quiz not found: ${jsonPath}`);
  return r.json();
}

class QuizSession {
  constructor(data, container) {
    this.kursId = data.kurs_id;
    this.tagNr = data.tag_nr;
    this.questions = shuffleArray(data.fragen).map(shuffleQuestion);
    this.container = container;
    this.mode = null;
    this.current = 0;
    this.selected = null;
    this.evaluated = false;
    this.correctCount = 0;
  }

  render() {
    if (this.mode === null) return this.renderModeSelector();
    if (this.mode === 'all') return this.renderAll();
    if (this.current >= this.questions.length) return this.renderSummary();
    return this.renderSingle();
  }

  renderModeSelector() {
    clear(this.container);
    this.container.append(
      el('div', { class: 'quiz-card' },
        el('h2', {}, 'Quiz · 60 Fragen'),
        el('p', {}, 'Wie möchtest du das Quiz bearbeiten?'),
        el('div', { style: 'display:flex;gap:12px;flex-wrap:wrap;margin-top:16px' },
          el('button', {
            class: 'quiz-button',
            on: { click: () => { this.mode = 'single'; this.render(); } },
          }, 'Eine Frage nach der anderen'),
          el('button', {
            class: 'quiz-button',
            style: 'background:var(--phase)',
            on: { click: () => { this.mode = 'all'; this.render(); } },
          }, 'Alle Fragen untereinander'),
        ),
        el('p', { style: 'margin-top:16px;color:var(--color-muted);font-size:14px' },
          'Einzelmodus: geführt, ideal für unterwegs. Alle-untereinander: gut zum Überfliegen oder gezielten Nachschlagen.'),
      ),
    );
  }

  renderSingle() {
    clear(this.container);
    const q = this.questions[this.current];

    this.evalBtn = el('button', { class: 'quiz-button', id: 'quiz-eval', disabled: true,
      on: { click: () => this.evaluateSingle() } }, 'Auswerten');
    this.feedback = el('div', { class: 'quiz-feedback', style: 'display:none' });

    const card = el('div', { class: 'quiz-card' },
      el('div', { class: 'quiz-progress' }, `Frage ${this.current + 1} von ${this.questions.length}`),
      el('div', { class: 'quiz-question' }, q.frage),
      el('div', { class: 'quiz-options' },
        ...q.optionen.map((opt, i) =>
          el('div', { class: 'quiz-option', 'data-idx': i,
            on: { click: () => this.selectSingle(i) } }, opt))
      ),
      this.evalBtn,
      this.feedback,
    );
    this.container.append(card);
  }

  selectSingle(idx) {
    if (this.evaluated) return;
    this.selected = idx;
    this.container.querySelectorAll('.quiz-option').forEach((node, i) =>
      node.classList.toggle('selected', i === idx));
    this.evalBtn.disabled = false;
  }

  evaluateSingle() {
    if (this.selected === null || this.evaluated) return;
    this.evaluated = true;
    const q = this.questions[this.current];
    const correct = this.selected === q.korrekt;
    if (correct) this.correctCount++;
    this.container.querySelectorAll('.quiz-option').forEach((node, i) => {
      if (i === q.korrekt) node.classList.add('correct');
      else if (i === this.selected) node.classList.add('wrong');
    });
    clear(this.feedback);
    this.feedback.append(
      el('strong', {}, correct ? '✓ Richtig!' : '✗ Falsch.'),
      el('br'),
      document.createTextNode(q.erklaerung),
      q.quelle ? el('div', { class: 'source' }, `Quelle: ${q.quelle}`) : null,
    );
    this.feedback.style.display = 'block';
    this.evalBtn.textContent = 'Weiter →';
    this.evalBtn.disabled = false;
    this.evalBtn.onclick = () => this.nextSingle();
  }

  nextSingle() {
    this.current++;
    this.selected = null;
    this.evaluated = false;
    this.render();
  }

  renderAll() {
    clear(this.container);
    // State pro Frage: { selected: null|idx, evaluated: false }
    this.allState = this.questions.map(() => ({ selected: null, evaluated: false }));
    const allCorrectCount = () => this.allState.filter((s, i) => s.evaluated && s.selected === this.questions[i].korrekt).length;
    const allEvaluatedCount = () => this.allState.filter(s => s.evaluated).length;

    const header = el('div', { class: 'quiz-card', style: 'margin-bottom:16px' },
      el('h2', { style: 'margin:0 0 8px' }, 'Quiz · alle Fragen'),
      el('p', { style: 'margin:0;color:var(--color-muted)' },
        `${this.questions.length} Fragen. Jede Frage hat ihren eigenen Auswerten-Button.`),
      el('div', { id: 'quiz-summary-line', style: 'margin-top:8px;font-weight:600' },
        `Beantwortet: 0 / ${this.questions.length}`),
      el('button', {
        class: 'quiz-button', style: 'margin-top:12px',
        on: { click: () => this.evaluateAllRemaining() }
      }, 'Alle noch nicht bewerteten auf einmal auswerten'),
    );
    this.container.append(header);

    this.questions.forEach((q, qi) => {
      const cardId = `qcard-${qi}`;
      const evalBtn = el('button', {
        class: 'quiz-button', disabled: true,
        on: { click: () => this.evaluateAt(qi, card, evalBtn, feedback) }
      }, 'Auswerten');
      const feedback = el('div', { class: 'quiz-feedback', style: 'display:none' });
      const card = el('div', { class: 'quiz-card', id: cardId, style: 'margin-bottom:16px' },
        el('div', { class: 'quiz-progress' }, `Frage ${qi + 1} von ${this.questions.length} · ${q.schwierigkeit || ''}`),
        el('div', { class: 'quiz-question' }, q.frage),
        el('div', { class: 'quiz-options' },
          ...q.optionen.map((opt, oi) =>
            el('div', {
              class: 'quiz-option', 'data-idx': oi,
              on: { click: () => this.selectAt(qi, oi, card, evalBtn) }
            }, opt))
        ),
        evalBtn,
        feedback,
      );
      this.container.append(card);
    });

    this.updateAllSummary();
  }

  selectAt(qi, oi, card, evalBtn) {
    if (this.allState[qi].evaluated) return;
    this.allState[qi].selected = oi;
    card.querySelectorAll('.quiz-option').forEach((node, i) =>
      node.classList.toggle('selected', i === oi));
    evalBtn.disabled = false;
  }

  evaluateAt(qi, card, evalBtn, feedback) {
    const st = this.allState[qi];
    if (st.selected === null || st.evaluated) return;
    st.evaluated = true;
    const q = this.questions[qi];
    const correct = st.selected === q.korrekt;
    card.querySelectorAll('.quiz-option').forEach((node, i) => {
      if (i === q.korrekt) node.classList.add('correct');
      else if (i === st.selected) node.classList.add('wrong');
    });
    clear(feedback);
    feedback.append(
      el('strong', {}, correct ? '✓ Richtig!' : '✗ Falsch.'),
      el('br'),
      document.createTextNode(q.erklaerung),
      q.quelle ? el('div', { class: 'source' }, `Quelle: ${q.quelle}`) : null,
    );
    feedback.style.display = 'block';
    evalBtn.disabled = true;
    evalBtn.textContent = correct ? '✓ Ausgewertet' : '✗ Ausgewertet';
    this.updateAllSummary();
  }

  evaluateAllRemaining() {
    this.allState.forEach((st, qi) => {
      if (st.evaluated || st.selected === null) return;
      const card = document.getElementById(`qcard-${qi}`);
      if (!card) return;
      const evalBtn = card.querySelector('.quiz-button');
      const feedback = card.querySelector('.quiz-feedback');
      this.evaluateAt(qi, card, evalBtn, feedback);
    });
  }

  updateAllSummary() {
    const line = document.getElementById('quiz-summary-line');
    if (!line) return;
    const evaluated = this.allState.filter(s => s.evaluated).length;
    const correct = this.allState.filter((s, i) => s.evaluated && s.selected === this.questions[i].korrekt).length;
    line.textContent = `Beantwortet: ${evaluated} / ${this.questions.length} · richtig: ${correct}`;
    if (evaluated === this.questions.length && typeof recordQuizResult === 'function') {
      recordQuizResult(this.kursId, this.tagNr, correct);
    }
  }

  renderSummary() {
    if (typeof recordQuizResult === 'function') {
      recordQuizResult(this.kursId, this.tagNr, this.correctCount);
    }
    const total = this.questions.length;
    const pct = Math.round((this.correctCount / total) * 100);
    clear(this.container);
    this.container.append(
      el('div', { class: 'quiz-card' },
        el('h2', {}, 'Geschafft!'),
        el('p', { style: 'font-size:24px' },
          `${this.correctCount} von ${total} richtig (${pct}%)`),
        el('button', { class: 'quiz-button',
          on: { click: () => location.reload() } }, 'Nochmal versuchen'),
      )
    );
  }
}
