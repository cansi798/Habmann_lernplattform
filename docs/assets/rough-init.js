// Lernplatt — rough-init.js
// Shared rough.js renderer:
//   1) Canvas accents   <canvas data-rough="underline|box|arrow|check" data-color="#...">
//   2) SVG diagrams     <div data-rough-diagram="layer|flow|matrix2x2|funnel|cycle|scorecard"
//                             data-spec='<JSON>'
//                             data-color="#9d4a1a"
//                             data-aspect="3" >
//
// Specs (JSON):
//   layer:     [{label, sub?}, ...]                                  // top → bottom
//   flow:      [{label}, ...]                                        // left → right, wraps after 5
//   matrix2x2: {x:{label,lo,hi}, y:{label,lo,hi}, q:[Q1,Q2,Q3,Q4]}   // Q1=top-right, ccw
//   funnel:    [{label}, ...]                                        // wide → narrow
//   cycle:     [{label}, ...]                                        // ringförmig im Uhrzeigersinn
//   scorecard: [{label, value:0..5}, ...]                            // horizontale Bars
//
// Activation: lädt rough-init.js und wird bei DOMContentLoaded ausgeführt.
// Idempotent: jeder Host wird nur einmal gerendert.

(function() {
  'use strict';
  const SVG_NS = 'http://www.w3.org/2000/svg';
  const DEFAULT_COLOR = '#9d4a1a';
  const FILL_BG = 'rgba(157,74,26,0.08)';

  function $svg(name, attrs) {
    const el = document.createElementNS(SVG_NS, name);
    if (attrs) for (const k in attrs) el.setAttribute(k, attrs[k]);
    return el;
  }

  function svgText(x, y, text, opts) {
    opts = opts || {};
    const t = $svg('text', {
      x, y,
      'text-anchor': opts.anchor || 'middle',
      'dominant-baseline': opts.baseline || 'middle',
      'font-family': 'Source Sans 3, system-ui, sans-serif',
      'font-size': opts.size || 13,
      'font-weight': opts.weight || 400,
      fill: opts.fill || '#222'
    });
    t.textContent = text;
    return t;
  }

  // Naive word-wrap: returns array of lines, max maxChars per line.
  function wrap(text, maxChars) {
    if (!text) return [''];
    const words = String(text).split(/\s+/);
    const lines = [];
    let cur = '';
    for (const w of words) {
      if ((cur + ' ' + w).trim().length > maxChars && cur) { lines.push(cur); cur = w; }
      else cur = (cur ? cur + ' ' : '') + w;
    }
    if (cur) lines.push(cur);
    return lines;
  }

  function addLabel(svg, cx, cy, text, opts) {
    opts = opts || {};
    const maxChars = opts.maxChars || 22;
    const size = opts.size || 13;
    const lines = wrap(text, maxChars);
    const lineH = size * 1.15;
    const yStart = cy - ((lines.length - 1) * lineH) / 2;
    lines.forEach((line, i) => {
      svg.appendChild(svgText(cx, yStart + i * lineH, line, { ...opts, size }));
    });
  }

  // -------- Canvas accents (Tag 1 compat) ------------------------------------
  function initCanvasAccents() {
    if (typeof rough === 'undefined') return;
    document.querySelectorAll('canvas[data-rough]:not([data-rough-done])').forEach(canvas => {
      try {
        const rc = rough.canvas(canvas);
        const w = canvas.width, h = canvas.height;
        const color = canvas.dataset.color || DEFAULT_COLOR;
        const type = canvas.dataset.rough;
        if (type === 'underline') {
          rc.line(0, h/2, w, h/2, { stroke: color, strokeWidth: 3, roughness: 1.8 });
        } else if (type === 'box') {
          rc.rectangle(2, 2, w-4, h-4, { stroke: color, strokeWidth: 1.5, roughness: 2.0, fill: 'rgba(157,74,26,0.05)', fillStyle: 'solid' });
        } else if (type === 'arrow') {
          rc.line(0, h/2, w-10, h/2, { stroke: color, strokeWidth: 2, roughness: 1.4 });
          rc.line(w-15, h/2-7, w-3, h/2, { stroke: color, strokeWidth: 2, roughness: 1.2 });
          rc.line(w-15, h/2+7, w-3, h/2, { stroke: color, strokeWidth: 2, roughness: 1.2 });
        } else if (type === 'check') {
          rc.line(4, h/2, w/2.4, h-6, { stroke: color, strokeWidth: 3, roughness: 1.4 });
          rc.line(w/2.4, h-6, w-4, 4, { stroke: color, strokeWidth: 3, roughness: 1.4 });
        }
        canvas.dataset.roughDone = '1';
      } catch (e) { console.warn('rough canvas init failed', e); }
    });
  }

  // -------- SVG diagrams -----------------------------------------------------
  function makeSvg(viewW, viewH) {
    const svg = $svg('svg', {
      viewBox: `0 0 ${viewW} ${viewH}`,
      xmlns: SVG_NS,
      preserveAspectRatio: 'xMidYMid meet',
      style: 'width:100%;height:auto;max-width:100%;display:block'
    });
    return svg;
  }

  function roughOpts(color, extra) {
    return Object.assign({
      stroke: color,
      strokeWidth: 1.8,
      roughness: 1.6,
      fill: FILL_BG,
      fillStyle: 'solid'
    }, extra || {});
  }

  function renderLayer(svg, rs, spec, w, h, color) {
    const n = spec.length;
    const pad = 14, gap = 8;
    const itemH = (h - 2 * pad - (n - 1) * gap) / n;
    spec.forEach((item, i) => {
      const y = pad + i * (itemH + gap);
      const node = rs.rectangle(pad, y, w - 2 * pad, itemH, roughOpts(color, { roughness: 1.4 }));
      svg.appendChild(node);
      addLabel(svg, w/2, y + itemH/2 - (item.sub ? 8 : 0), item.label, { size: 15, weight: 600, fill: '#1a1a1a', maxChars: 60 });
      if (item.sub) addLabel(svg, w/2, y + itemH/2 + 12, item.sub, { size: 11, fill: '#555', maxChars: 70 });
    });
  }

  function renderFlow(svg, rs, spec, w, h, color) {
    const n = spec.length;
    const perRow = Math.min(n, 5);
    const rows = Math.ceil(n / perRow);
    const pad = 12;
    const boxW = (w - 2 * pad - (perRow - 1) * 28) / perRow;
    const boxH = Math.min(60, (h - 2 * pad - (rows - 1) * 24) / rows);
    spec.forEach((item, i) => {
      const row = Math.floor(i / perRow);
      const colInRow = (row % 2 === 0) ? (i % perRow) : (perRow - 1 - (i % perRow));
      const x = pad + colInRow * (boxW + 28);
      const y = pad + row * (boxH + 24) + (h - 2 * pad - rows * boxH - (rows - 1) * 24) / 2;
      svg.appendChild(rs.rectangle(x, y, boxW, boxH, roughOpts(color, { roughness: 1.5 })));
      addLabel(svg, x + boxW/2, y + boxH/2, item.label, { size: 12, weight: 600, fill: '#1a1a1a', maxChars: Math.floor(boxW/7) });
      // Arrow to next
      if (i < n - 1) {
        const nextRow = Math.floor((i + 1) / perRow);
        if (nextRow === row) {
          const ax1 = (row % 2 === 0) ? x + boxW : x;
          const ax2 = (row % 2 === 0) ? x + boxW + 24 : x - 24;
          const ay = y + boxH/2;
          svg.appendChild(rs.line(ax1, ay, ax2, ay, { stroke: color, strokeWidth: 1.6, roughness: 1.2 }));
          // arrow head
          const sign = (row % 2 === 0) ? 1 : -1;
          svg.appendChild(rs.line(ax2 - sign * 6, ay - 5, ax2, ay, { stroke: color, strokeWidth: 1.6, roughness: 0.8 }));
          svg.appendChild(rs.line(ax2 - sign * 6, ay + 5, ax2, ay, { stroke: color, strokeWidth: 1.6, roughness: 0.8 }));
        } else {
          // U-turn down
          const ax = (row % 2 === 0) ? x + boxW + 8 : x - 8;
          const ay1 = y + boxH;
          const ay2 = y + boxH + 24 - 6;
          svg.appendChild(rs.line(ax, ay1, ax, ay2, { stroke: color, strokeWidth: 1.6, roughness: 1.2 }));
          svg.appendChild(rs.line(ax - 5, ay2 - 6, ax, ay2, { stroke: color, strokeWidth: 1.6, roughness: 0.8 }));
          svg.appendChild(rs.line(ax + 5, ay2 - 6, ax, ay2, { stroke: color, strokeWidth: 1.6, roughness: 0.8 }));
        }
      }
    });
  }

  function renderMatrix2x2(svg, rs, spec, w, h, color) {
    const padL = 70, padR = 16, padT = 16, padB = 56;
    const ax = padL, ay = padT;
    const aw = w - padL - padR, ah = h - padT - padB;
    // Outer box
    svg.appendChild(rs.rectangle(ax, ay, aw, ah, roughOpts(color, { fill: 'transparent', roughness: 1.2 })));
    // Cross
    svg.appendChild(rs.line(ax + aw/2, ay, ax + aw/2, ay + ah, { stroke: color, strokeWidth: 1.4, roughness: 1.2 }));
    svg.appendChild(rs.line(ax, ay + ah/2, ax + aw, ay + ah/2, { stroke: color, strokeWidth: 1.4, roughness: 1.2 }));
    // Quadrants Q1=TR, Q2=TL, Q3=BL, Q4=BR
    const q = spec.q || ['', '', '', ''];
    const cellW = aw/2, cellH = ah/2;
    const centers = [
      { cx: ax + cellW + cellW/2, cy: ay + cellH/2 }, // Q1 top-right
      { cx: ax + cellW/2,         cy: ay + cellH/2 }, // Q2 top-left
      { cx: ax + cellW/2,         cy: ay + cellH + cellH/2 }, // Q3 bottom-left
      { cx: ax + cellW + cellW/2, cy: ay + cellH + cellH/2 }, // Q4 bottom-right
    ];
    q.forEach((label, i) => addLabel(svg, centers[i].cx, centers[i].cy, label, { size: 13, weight: 600, fill: '#1a1a1a', maxChars: Math.floor(cellW/7) }));
    // Axis labels
    if (spec.x) {
      svg.appendChild(svgText(ax + 6, ay + ah + 14, spec.x.lo || '', { anchor: 'start', size: 11, fill: '#666' }));
      svg.appendChild(svgText(ax + aw - 6, ay + ah + 14, spec.x.hi || '', { anchor: 'end', size: 11, fill: '#666' }));
      svg.appendChild(svgText(ax + aw/2, ay + ah + 32, spec.x.label || '', { size: 12, weight: 700, fill: color }));
    }
    if (spec.y) {
      const yLabel = $svg('text', {
        x: 16, y: ay + ah/2,
        'text-anchor': 'middle',
        'dominant-baseline': 'middle',
        'font-family': 'Source Sans 3, system-ui, sans-serif',
        'font-size': 12, 'font-weight': 700, fill: color,
        transform: `rotate(-90 16 ${ay + ah/2})`
      });
      yLabel.textContent = spec.y.label || '';
      svg.appendChild(yLabel);
      svg.appendChild(svgText(ax - 6, ay + 12, spec.y.hi || '', { anchor: 'end', size: 11, fill: '#666' }));
      svg.appendChild(svgText(ax - 6, ay + ah - 6, spec.y.lo || '', { anchor: 'end', size: 11, fill: '#666' }));
    }
  }

  function renderFunnel(svg, rs, spec, w, h, color) {
    const n = spec.length;
    const pad = 12;
    const stepH = (h - 2 * pad) / n;
    const wTop = w - 2 * pad;
    const wBot = wTop * 0.30;
    for (let i = 0; i < n; i++) {
      const t0 = i / n, t1 = (i + 1) / n;
      const x0 = pad + (wTop - (wTop - wBot) * t0) * 0 + (wTop * (1 - (1 - wBot/wTop) * t0)) * 0 + (w - (wTop - (wTop - wBot) * t0)) / 2;
      const w0 = wTop - (wTop - wBot) * t0;
      const w1 = wTop - (wTop - wBot) * t1;
      const y0 = pad + i * stepH;
      const y1 = y0 + stepH - 4;
      // Trapezoid via polygon
      const cxTop = w/2, cxBot = w/2;
      const pts = [
        [cxTop - w0/2, y0],
        [cxTop + w0/2, y0],
        [cxBot + w1/2, y1],
        [cxBot - w1/2, y1],
      ];
      const poly = rs.polygon(pts, roughOpts(color, { roughness: 1.4 }));
      svg.appendChild(poly);
      addLabel(svg, w/2, (y0 + y1)/2, spec[i].label, { size: 13, weight: 600, fill: '#1a1a1a', maxChars: Math.floor(((w0 + w1)/2)/7) });
    }
  }

  function renderCycle(svg, rs, spec, w, h, color) {
    const n = spec.length;
    const cx = w/2, cy = h/2;
    const radius = Math.min(w, h) * 0.36;
    const boxW = Math.min(140, w * 0.28);
    const boxH = 44;
    // Outer ring (decorative)
    svg.appendChild(rs.circle(cx, cy, radius * 2, { stroke: color, strokeWidth: 1.2, roughness: 1.6, fill: 'transparent' }));
    spec.forEach((item, i) => {
      const ang = (i / n) * 2 * Math.PI - Math.PI/2;
      const x = cx + radius * Math.cos(ang) - boxW/2;
      const y = cy + radius * Math.sin(ang) - boxH/2;
      svg.appendChild(rs.rectangle(x, y, boxW, boxH, roughOpts(color, { roughness: 1.4 })));
      addLabel(svg, x + boxW/2, y + boxH/2, item.label, { size: 11, weight: 600, fill: '#1a1a1a', maxChars: Math.floor(boxW/6) });
      // Arrow to next along the ring
      const ang2 = ((i + 1) / n) * 2 * Math.PI - Math.PI/2;
      const midAng = (ang + ang2) / 2;
      const x1 = cx + radius * Math.cos(ang + 0.18);
      const y1 = cy + radius * Math.sin(ang + 0.18);
      const x2 = cx + radius * Math.cos(ang2 - 0.18);
      const y2 = cy + radius * Math.sin(ang2 - 0.18);
      svg.appendChild(rs.line(x1, y1, x2, y2, { stroke: color, strokeWidth: 1.4, roughness: 1.2 }));
      // Tiny arrowhead
      const dx = x2 - x1, dy = y2 - y1, len = Math.hypot(dx, dy) || 1;
      const ux = dx/len, uy = dy/len;
      const headX = x2 - ux * 6, headY = y2 - uy * 6;
      const perpX = -uy * 4, perpY = ux * 4;
      svg.appendChild(rs.line(x2, y2, headX + perpX, headY + perpY, { stroke: color, strokeWidth: 1.4, roughness: 0.8 }));
      svg.appendChild(rs.line(x2, y2, headX - perpX, headY - perpY, { stroke: color, strokeWidth: 1.4, roughness: 0.8 }));
    });
  }

  function renderScorecard(svg, rs, spec, w, h, color) {
    const n = spec.length;
    const padL = 130, padR = 60, padT = 14, padB = 24;
    const rowH = (h - padT - padB) / n;
    const barAreaW = w - padL - padR;
    // Axis 0..5
    for (let v = 0; v <= 5; v++) {
      const x = padL + (v/5) * barAreaW;
      svg.appendChild($svg('line', { x1: x, y1: padT, x2: x, y2: h - padB, stroke: '#ddd', 'stroke-width': v === 0 || v === 5 ? 1 : 0.5 }));
      svg.appendChild(svgText(x, h - padB + 12, String(v), { size: 10, fill: '#888' }));
    }
    spec.forEach((item, i) => {
      const y = padT + i * rowH + 4;
      const barH = rowH - 12;
      const barW = (Math.max(0, Math.min(5, item.value || 0)) / 5) * barAreaW;
      svg.appendChild(rs.rectangle(padL, y, barW, barH, roughOpts(color, { roughness: 1.2 })));
      svg.appendChild(svgText(padL - 8, y + barH/2, item.label, { anchor: 'end', size: 12, weight: 600, fill: '#1a1a1a' }));
      svg.appendChild(svgText(padL + barW + 6, y + barH/2, String(item.value), { anchor: 'start', size: 12, weight: 700, fill: color }));
    });
  }

  function initSvgDiagrams() {
    if (typeof rough === 'undefined') return;
    document.querySelectorAll('[data-rough-diagram]:not([data-rough-done])').forEach(host => {
      try {
        const type = host.dataset.roughDiagram;
        let spec;
        try { spec = JSON.parse(host.dataset.spec); }
        catch (e) { console.warn('rough diagram spec parse failed', host, e); return; }
        const color = host.dataset.color || DEFAULT_COLOR;
        const aspect = parseFloat(host.dataset.aspect) || 2.4;
        const viewW = 800;
        const viewH = Math.round(viewW / aspect);
        const svg = makeSvg(viewW, viewH);
        const rs = rough.svg(svg);
        switch (type) {
          case 'layer':     renderLayer(svg, rs, spec, viewW, viewH, color); break;
          case 'flow':      renderFlow(svg, rs, spec, viewW, viewH, color); break;
          case 'matrix2x2': renderMatrix2x2(svg, rs, spec, viewW, viewH, color); break;
          case 'funnel':    renderFunnel(svg, rs, spec, viewW, viewH, color); break;
          case 'cycle':     renderCycle(svg, rs, spec, viewW, viewH, color); break;
          case 'scorecard': renderScorecard(svg, rs, spec, viewW, viewH, color); break;
          default: console.warn('unknown rough diagram type:', type);
        }
        host.appendChild(svg);
        host.dataset.roughDone = '1';
      } catch (e) { console.warn('rough diagram init failed', e); }
    });
  }

  function init() {
    initCanvasAccents();
    initSvgDiagrams();
  }

  // Public API for dynamically-mounted content (e.g. quiz engine renders cards
  // after DOMContentLoaded; it calls refresh() to render any new diagrams).
  window.LernplattRough = { refresh: init };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
