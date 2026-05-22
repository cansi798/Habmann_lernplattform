// Lernplatt — dom.js
// Tiny DOM builder so engines avoid innerHTML/XSS risks.

function el(tag, attrs, ...children) {
  const e = document.createElement(tag);
  if (attrs) {
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === 'class') e.className = v;
      else if (k === 'style') e.setAttribute('style', v);
      else if (k.startsWith('data-')) e.setAttribute(k, String(v));
      else if (k === 'on' && typeof v === 'object') {
        for (const [ev, fn] of Object.entries(v)) e.addEventListener(ev, fn);
      }
      else e[k] = v;
    }
  }
  for (const c of children) {
    if (c == null || c === false) continue;
    if (Array.isArray(c)) c.forEach(x => x && e.append(x));
    else e.append(c);
  }
  return e;
}

function clear(node) { while (node.firstChild) node.removeChild(node.firstChild); }
