// Lernplatt — slides.js
// Minimal slide engine: arrow keys, F = fullscreen, O = overview.

class SlideShow {
  constructor(container) {
    this.container = container;
    this.slides = Array.from(container.querySelectorAll('.slide'));
    this.current = 0;
    this.overview = false;
    this.show();
    this.bindKeys();
  }

  show() {
    this.slides.forEach((s, i) => { s.style.display = (i === this.current) ? 'block' : 'none'; });
    this.container.dataset.current = this.current + 1;
    this.container.dataset.total = this.slides.length;
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

  bindKeys() {
    document.addEventListener('keydown', e => {
      if (e.key === 'ArrowRight' || e.key === ' ') this.next();
      else if (e.key === 'ArrowLeft') this.prev();
      else if (e.key === 'f' || e.key === 'F') this.toggleFullscreen();
      else if (e.key === 'Escape') { if (this.overview) this.toggleOverview(); }
      else if (e.key === 'o' || e.key === 'O') this.toggleOverview();
    });
  }
}
