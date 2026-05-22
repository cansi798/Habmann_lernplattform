// Lernplatt — quiz.js
// Quiz engine: shuffles, 3-state per question, manual evaluate, summary.
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
    this.current = 0;
    this.selected = null;
    this.evaluated = false;
    this.correctCount = 0;
  }

  render() {
    clear(this.container);
    if (this.current >= this.questions.length) return this.renderSummary();
    const q = this.questions[this.current];

    this.evalBtn = el('button', { class: 'quiz-button', id: 'quiz-eval', disabled: true,
      on: { click: () => this.evaluate() } }, 'Auswerten');
    this.feedback = el('div', { class: 'quiz-feedback', style: 'display:none' });

    const card = el('div', { class: 'quiz-card' },
      el('div', { class: 'quiz-progress' }, `Frage ${this.current + 1} von ${this.questions.length}`),
      el('div', { class: 'quiz-question' }, q.frage),
      el('div', { class: 'quiz-options' },
        ...q.optionen.map((opt, i) =>
          el('div', { class: 'quiz-option', 'data-idx': i,
            on: { click: () => this.select(i) } }, opt))
      ),
      this.evalBtn,
      this.feedback,
    );
    this.container.append(card);
  }

  select(idx) {
    if (this.evaluated) return;
    this.selected = idx;
    this.container.querySelectorAll('.quiz-option').forEach((node, i) =>
      node.classList.toggle('selected', i === idx));
    this.evalBtn.disabled = false;
  }

  evaluate() {
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
      el('div', { class: 'source' }, `Quelle: ${q.quelle}`),
    );
    this.feedback.style.display = 'block';
    this.evalBtn.textContent = 'Weiter →';
    this.evalBtn.disabled = false;
    this.evalBtn.onclick = () => this.next();
  }

  next() {
    this.current++;
    this.selected = null;
    this.evaluated = false;
    this.render();
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
