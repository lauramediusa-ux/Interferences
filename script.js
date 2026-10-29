// ============================================================
// INTERFERENCE — script condiviso (homepage + articoli)
// ============================================================

var DFREE_KEY = 'interference-distraction-free';

// --- Preloader: si nasconde quando la pagina (immagini incluse) è pronta,
// ma resta visibile almeno MIN_MS per essere percepibile anche sulle
// connessioni veloci, con un tetto massimo di attesa (MAX_MS) per non
// bloccare la navigazione sulle connessioni lente --------------------------
(function () {
  var MIN_MS = 900;
  var MAX_MS = 2500;
  var start = Date.now();
  var revealed = false;

  function reveal() {
    if (revealed) return;
    revealed = true;
    document.body.classList.add('preloaded');
    if (typeof startHome === 'function') startHome();
  }
  function revealAfterMin() {
    var elapsed = Date.now() - start;
    var wait = Math.max(0, MIN_MS - elapsed);
    setTimeout(reveal, wait);
  }

  if (document.readyState === 'complete') {
    revealAfterMin();
  } else {
    window.addEventListener('load', revealAfterMin);
  }
  setTimeout(reveal, MAX_MS);
})();

// --- Selettore lingua: chiude il menu quando si clicca fuori --------------
document.addEventListener('click', function (e) {
  document.querySelectorAll('.lang-switcher[open]').forEach(function (d) {
    if (!d.contains(e.target)) d.removeAttribute('open');
  });
});

// --- Modalità distraction free (applicata su ogni pagina del sito) --------
(function () {
  var enabled = localStorage.getItem(DFREE_KEY) === '1';
  if (enabled) document.documentElement.classList.add('dfree-pending');

  document.addEventListener('DOMContentLoaded', function () {
    if (enabled) document.body.classList.add('distraction-free');
    document.documentElement.classList.remove('dfree-pending');

    var toggle = document.getElementById('dfree-toggle');
    if (toggle) {
      if (enabled) toggle.classList.add('active');
      toggle.addEventListener('click', function () {
        var isOn = document.body.classList.toggle('distraction-free');
        toggle.classList.toggle('active', isOn);
        localStorage.setItem(DFREE_KEY, isOn ? '1' : '0');
        if (typeof drawRowLines === 'function') drawRowLines();
      });
    }
  });
})();

// --- Filtro categorie in homepage -----------------------------------------
document.addEventListener('DOMContentLoaded', function () {
  var pills = document.querySelectorAll('.filter-pill[data-cat]');
  var cards = document.querySelectorAll('.card');

  pills.forEach(function (pill) {
    pill.addEventListener('click', function () {
      pills.forEach(function (p) { p.classList.remove('active'); });
      pill.classList.add('active');

      var cat = pill.getAttribute('data-cat');
      cards.forEach(function (card) {
        if (cat === 'all' || card.getAttribute('data-cat') === cat) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
      drawRowLines();
    });
  });
});

// --- Linee orizzontali ai confini di ogni riga ------------------------------
// La fascia testo è flessibile, quindi le posizioni si misurano dal DOM:
// una linea sopra e una sotto ogni fascia-immagini, a tutta larghezza.
var drawRowLines;
(function () {
  var raf = null;
  drawRowLines = function () {
    var grid = document.querySelector('.grid');
    if (!grid) return;
    var overlay = grid.querySelector('.row-lines');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.className = 'row-lines';
      overlay.setAttribute('aria-hidden', 'true');
      grid.appendChild(overlay);
    }
    overlay.innerHTML = '';
    var overlayRect = overlay.getBoundingClientRect();
    var ys = [];
    grid.querySelectorAll('.card-media').forEach(function (m) {
      if (m.offsetParent === null) return;
      var r = m.getBoundingClientRect();
      [r.top - overlayRect.top, r.bottom - overlayRect.top].forEach(function (y) {
        var dup = ys.some(function (v) { return Math.abs(v - y) < 0.5; });
        if (!dup) ys.push(y);
      });
    });
    // Closing line: bottom edge of the last row (each .card spans the full
    // media+text subgrid tracks, so its own bottom edge equals the row's).
    var maxBottom = 0;
    grid.querySelectorAll('.card').forEach(function (c) {
      if (c.offsetParent === null) return;
      var b = c.getBoundingClientRect().bottom - overlayRect.top;
      if (b > maxBottom) maxBottom = b;
    });
    if (maxBottom > 0) {
      var dupBottom = ys.some(function (v) { return Math.abs(v - maxBottom) < 0.5; });
      if (!dupBottom) ys.push(maxBottom);
    }
    ys.forEach(function (y) {
      var line = document.createElement('div');
      line.className = 'row-line';
      line.style.top = y + 'px';
      line.style.marginTop = '-0.5px';
      overlay.appendChild(line);
    });
  };

  document.addEventListener('DOMContentLoaded', drawRowLines);
  window.addEventListener('load', drawRowLines);
  window.addEventListener('resize', function () {
    if (raf) cancelAnimationFrame(raf);
    raf = requestAnimationFrame(drawRowLines);
  });
})();

// --- Condivisione articolo --------------------------------------------------
function shareArticle(platform) {
  var url = window.location.href;
  var title = document.title;
  var descTag = document.querySelector('meta[name="description"]');
  var desc = descTag ? descTag.getAttribute('content') : '';

  var targets = {
    whatsapp: 'https://api.whatsapp.com/send?text=' + encodeURIComponent(title + ' — ' + url),
    telegram: 'https://t.me/share/url?url=' + encodeURIComponent(url) + '&text=' + encodeURIComponent(title),
    facebook: 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url),
    twitter: 'https://twitter.com/intent/tweet?url=' + encodeURIComponent(url) + '&text=' + encodeURIComponent(title),
    threads: 'https://www.threads.net/intent/post?text=' + encodeURIComponent(title + ' — ' + url)
  };

  if (platform === 'native' && navigator.share) {
    navigator.share({ title: title, text: desc, url: url }).catch(function () {});
    return;
  }

  if (platform === 'copy') {
    navigator.clipboard.writeText(url).then(function () {
      var btn = document.getElementById('copy-btn');
      if (btn) {
        var original = btn.innerHTML;
        btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>';
        btn.setAttribute('title', 'Link copiato');
        setTimeout(function () {
          btn.innerHTML = original;
          btn.setAttribute('title', 'Copia link');
        }, 1800);
      }
    });
    return;
  }

  if (targets[platform]) {
    window.open(targets[platform], '_blank', 'noopener,noreferrer,width=600,height=600');
  }
}


// --- Home: cards reveal (black curtain) as they enter the viewport ----------
function startHomeReveal() {
  var cards = document.querySelectorAll('.grid .card');
  if (!cards.length) return;

  function play(batch) {
    batch.forEach(function (c, i) { c.style.setProperty('--i', i % 4); c.classList.add('in'); });
    setTimeout(function () { batch.forEach(function (c) { c.classList.add('done'); }); }, 2200);
  }

  if (!('IntersectionObserver' in window)) { play([].slice.call(cards)); return; }
  var io = new IntersectionObserver(function (entries) {
    var batch = entries.filter(function (e) { return e.isIntersecting; })
                       .map(function (e) { return e.target; });
    if (!batch.length) return;
    batch.forEach(function (c) { io.unobserve(c); });
    play(batch);
  }, { threshold: 0.12 });
  cards.forEach(function (c) { io.observe(c); });
}

// --- Home intro: photo veil (plays once per session; ?intro forces it) -------
var PANEL_MS = 900, STAGGER_MS = 170, OVERLAP_MS = 220, LIFT_MS = 1200;

function startHome() {
  var body = document.body;
  if (!body.classList.contains('home')) return;
  var overlay = document.getElementById('introOverlay');
  var panels = overlay ? [].slice.call(overlay.querySelectorAll('.intro-panel')) : [];
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var force = /[?&]intro\b/.test(location.search);
  var seen = false;
  try { seen = sessionStorage.getItem('interference-intro-seen') === '1'; } catch (e) {}

  function ready(delay) {
    setTimeout(function () {
      body.classList.add('is-ready');
      setTimeout(startHomeReveal, 500);
    }, delay);
  }

  if (!overlay || !panels.length || reduce || (seen && !force)) {
    if (overlay) overlay.remove();
    ready(80);
    return;
  }
  try { sessionStorage.setItem('interference-intro-seen', '1'); } catch (e) {}

  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  window.scrollTo(0, 0);

  var imgs = [].slice.call(overlay.querySelectorAll('img'));
  var loaded = Promise.all(imgs.map(function (im) {
    return im.complete ? Promise.resolve() : new Promise(function (r) { im.onload = im.onerror = r; });
  }));
  var timeout = new Promise(function (r) { setTimeout(r, 1500); });

  Promise.race([loaded, timeout]).then(function () {
    requestAnimationFrame(function () {
      setTimeout(function () {
        document.documentElement.classList.add('intro-lock');
        panels.forEach(function (p, i) { setTimeout(function () { p.classList.add('is-in'); }, i * STAGGER_MS); });
        var lastEnds = (panels.length - 1) * STAGGER_MS + PANEL_MS;
        setTimeout(function () {
          overlay.classList.add('is-lifting');
          document.documentElement.classList.remove('intro-lock');
          ready(380);
          setTimeout(function () { overlay.remove(); }, LIFT_MS + 100);
        }, Math.max(0, lastEnds - OVERLAP_MS));
      }, 120);
    });
  });
}

// --- Home: lime aura following the pointer over the logo ----------------------
document.addEventListener('DOMContentLoaded', function () {
  if (!document.body.classList.contains('home')) return;
  if (!window.matchMedia('(hover: hover) and (pointer: fine)').matches) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var link = document.querySelector('.site-header .logo a');
  var img = link && link.querySelector('img');
  if (!img) return;
  var glow = document.createElement('span');
  glow.className = 'logo-aura';
  glow.setAttribute('aria-hidden', 'true');
  glow.style.setProperty('--logo-url', 'url("' + (img.currentSrc || img.src) + '")');
  link.appendChild(glow);

  var header = document.querySelector('.site-header');
  var cx = 0, cy = 0, tx = 0, ty = 0, running = false;
  function loop() {
    cx += (tx - cx) * 0.18; cy += (ty - cy) * 0.18;
    glow.style.setProperty('--gx', cx.toFixed(1) + 'px');
    glow.style.setProperty('--gy', cy.toFixed(1) + 'px');
    if (Math.abs(tx - cx) > 0.3 || Math.abs(ty - cy) > 0.3) requestAnimationFrame(loop); else running = false;
  }
  header.addEventListener('mousemove', function (e) {
    var r = link.getBoundingClientRect();
    tx = e.clientX - r.left; ty = e.clientY - r.top;
    if (!glow.classList.contains('on')) { cx = tx; cy = ty; glow.classList.add('on'); }
    if (!running) { running = true; requestAnimationFrame(loop); }
  });
  header.addEventListener('mouseleave', function () { glow.classList.remove('on'); });
});
