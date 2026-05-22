// Lernplatt — progress.js
// Per-device progress tracking via localStorage.

const PROGRESS_KEY = "lernplatt-progress";

function loadProgress() {
  try { return JSON.parse(localStorage.getItem(PROGRESS_KEY)) || {}; }
  catch { return {}; }
}
function saveProgress(state) { localStorage.setItem(PROGRESS_KEY, JSON.stringify(state)); }

function markViewed(kursId, tagNr, material) {
  const state = loadProgress();
  const k = `kurs-${kursId}`;
  const t = `tag-${String(tagNr).padStart(2, "0")}`;
  state[k] = state[k] || {};
  state[k][t] = state[k][t] || {};
  if (!state[k][t][material]) {
    state[k][t][material] = "viewed";
    saveProgress(state);
  }
}

function recordQuizResult(kursId, tagNr, score) {
  const state = loadProgress();
  const k = `kurs-${kursId}`;
  const t = `tag-${String(tagNr).padStart(2, "0")}`;
  state[k] = state[k] || {};
  state[k][t] = state[k][t] || {};
  const prev = state[k][t].quiz || { best: 0, tries: 0 };
  state[k][t].quiz = {
    best: Math.max(prev.best || 0, score),
    tries: (prev.tries || 0) + 1,
  };
  saveProgress(state);
}

function recordPfadStep(kursId, tagNr, stepNr) {
  const state = loadProgress();
  const k = `kurs-${kursId}`;
  const t = `tag-${String(tagNr).padStart(2, "0")}`;
  state[k] = state[k] || {};
  state[k][t] = state[k][t] || {};
  state[k][t].lernpfad = state[k][t].lernpfad || { completed_steps: [] };
  if (!state[k][t].lernpfad.completed_steps.includes(stepNr)) {
    state[k][t].lernpfad.completed_steps.push(stepNr);
    saveProgress(state);
  }
}

function getDayStatus(kursId, tagNr) {
  const state = loadProgress();
  const k = `kurs-${kursId}`;
  const t = `tag-${String(tagNr).padStart(2, "0")}`;
  const d = (state[k] && state[k][t]) || {};
  return {
    skript:   !!(d.praesentation || d.handout),
    video:    !!d.video,
    quiz:     !!(d.quiz && d.quiz.best),
    aufgaben: !!d.aufgaben,
    lernpfad: !!(d.lernpfad && d.lernpfad.completed_steps && d.lernpfad.completed_steps.length > 0),
  };
}
