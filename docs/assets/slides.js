// Lernplatt — slides.js
// Minimal slide engine: arrow keys, F = fullscreen, O = overview, touch swipe.

class SlideShow {
  constructor(container) {
    this.container = container;
    this.slides = Array.from(container.querySelectorAll('.slide'));
    this.current = 0;
    this.overview = false;
    this._touchStartX = 0;
    this._touchStartY = 0;
    this._navPrev = null;
    this._navNext = null;
    this._navCounter = null;
    this.show();
    this._buildNav();
    this.bindKeys();
    this._bindTouch();
  }

  show() {
    this.slides.forEach((s, i) => { s.style.display = (i === this.current) ? 'block' : 'none'; });
    this.container.dataset.current = this.current + 1;
    this.container.dataset.total = this.slides.length;
    this._updateNav();
  }

  next() { if (this.current < this.slides.length - 1) { this.current++; this.show(); } }
  prev() { if (this.current > 0) { this.current--; this.show(); } }

  toggleFullscreen() {
    if (!document.fullscreenElement) this.container.requestFullscreen?.();
    else document.exitFullscreen?.();
  }

  toggleOverview() {
    this.overview = !this.overview;
    if (this.overview) {
      this.container.classList.add('overview');
      this.slides.forEach(s => { s.style.display = 'inline-block'; });
    } else {
      this.container.classList.remove('overview');
      this.show();
    }
  }

  _buildNav() {
    const nav = document.createElement('div');
    nav.className = 'slide-nav';

    const prevBtn = document.createElement('button');
    prevBtn.className = 'slide-prev';
    prevBtn.title = 'Zurück';
    prevBtn.textContent = '←';
    prevBtn.addEventListener('click', () => this.prev());

    const counter = document.createElement('span');
    counter.className = 'slide-counter';

    const nextBtn = document.createElement('button');
    nextBtn.className = 'slide-next';
    nextBtn.title = 'Weiter';
    nextBtn.textContent = '→';
    nextBtn.addEventListener('click', () => this.next());

    nav.appendChild(prevBtn);
    nav.appendChild(counter);
    nav.appendChild(nextBtn);

    this._navPrev = prevBtn;
    this._navNext = nextBtn;
    this._navCounter = counter;

    this.container.insertAdjacentElement('afterend', nav);
    this._updateNav();
  }

  _updateNav() {
    if (!this._navCounter) return;
    this._navCounter.textContent = (this.current + 1) + ' / ' + this.slides.length;
    this._navPrev.disabled = this.current === 0;
    this._navNext.disabled = this.current === this.slides.length - 1;
  }

  bindKeys() {
    document.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === ' ') this.next();
      else if (e.key === 'ArrowLeft') this.prev();
      else if (e.key === 'f' || e.key === 'F') this.toggleFullscreen();
      else if (e.key === 'Escape') { if (this.overview) this.toggleOverview(); }
      else if (e.key === 'o' || e.key === 'O') this.toggleOverview();
    });
  }

  _bindTouch() {
    this.container.addEventListener('touchstart', e => {
      this._touchStartX = e.touches[0].clientX;
      this._touchStartY = e.touches[0].clientY;
    }, { passive: true });

    this.container.addEventListener('touchend', e => {
      const dx = e.changedTouches[0].clientX - this._touchStartX;
      const dy = e.changedTouches[0].clientY - this._touchStartY;
      if (Math.abs(dx) < 40 || Math.abs(dy) > Math.abs(dx)) return;
      if (dx < 0) this.next();
      else this.prev();
    }, { passive: true });
  }
}
