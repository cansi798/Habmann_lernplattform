// Lernplatt — pfad.js
// Learnpath engine: linear steps, video or text + task, validate before next.
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
    return el('div', { class: 'pfad-video-placeholder' },
      '📺 Video-Platzhalter', el('br'),
      el('small', {}, 'Such-Vorschlag: ',
        el('em', {}, step.youtube_query || '—')));
  }

  renderText(step) {
    return el('div', { class: 'pfad-text' }, el('p', {}, step.inhalt));
  }

  renderTask(task) {
    this.taskBtn = el('button', { class: 'quiz-button', id: 'pfad-eval', disabled: true,
      on: { click: () => this.evaluate() } }, 'Antwort prüfen');
    this.taskFeedback = el('div', { class: 'quiz-feedback', style: 'display:none' });
    return el('div', { class: 'quiz-card', style: 'margin-top:24px' },
      el('div', { class: 'quiz-question' }, task.frage),
      el('div', { class: 'quiz-options' },
        ...task.optionen.map((opt, i) =>
          el('div', { class: 'quiz-option', 'data-idx': i }, opt))),
      this.taskBtn,
      this.taskFeedback,
    );
  }

  bindTask(task) {
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
