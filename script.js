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
    if (typeof startHomeReveal === 'function') startHomeReveal();
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

// --- Home intro: logo revealed by scroll -----------------------------------
// First home visit per browser session. A spacer (one screen tall) sits above
// the header; while it scrolls away a fixed copy of the logo is wiped in from
// the left at the centre of the screen, then travels and scales to the exact
// spot/size of the real logo, where it hands over seamlessly.
(function () {
  var INTRO_KEY = 'interference-intro-seen';
  var isHome = !!document.querySelector('.filters') && !/page-\d+\.html/.test(location.pathname);
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var seen = false;
  try { seen = sessionStorage.getItem(INTRO_KEY) === '1'; } catch (e) {}
  if (!isHome || reduce || seen) return;

  document.addEventListener('DOMContentLoaded', function () {
    var realLogo = document.querySelector('.site-header .logo');
    var realImg = realLogo && realLogo.querySelector('img');
    var tagline = document.querySelector('.tagline-slot');
    if (!realImg) return;

    var spacer, overlay, hint, curD = 0, D = 0, W = 0, H = 0, x1 = 0, y1 = 0, x0 = 0, y0 = 0, s0 = 1;
    var active = false;

    function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

    function measure() {
      // natural (spacer-free) position of the real logo = where it must land
      var r = realImg.getBoundingClientRect();
      W = r.width; H = r.height;
      x1 = r.left + window.pageXOffset;
      y1 = r.top + window.pageYOffset - curD;
      D = Math.max(520, window.innerHeight);
      curD = D;
      spacer.style.height = D + 'px';
      var vw = document.documentElement.clientWidth, vh = window.innerHeight;
      s0 = Math.max(1, Math.min((vw * 0.9) / W, 2.4));
      x0 = (vw - W * s0) / 2;
      y0 = (vh - H * s0) / 2;
      overlay.style.width = W + 'px';
    }

    function update() {
      var y = window.pageYOffset;
      var p = Math.max(0, Math.min(1, y / D));
      if (p >= 1) {
        if (active) {
          active = false;
          overlay.style.display = 'none';
          hint.style.display = 'none';
          document.body.classList.remove('intro-on');
        }
        if (tagline) tagline.style.opacity = '';
        return;
      }
      if (!active) {
        active = true;
        overlay.style.display = '';
        hint.style.display = '';
        document.body.classList.add('intro-on');
      }
      var p1 = Math.min(1, p / 0.4);
      var p2 = Math.max(0, (p - 0.4) / 0.6);
      var e1 = ease(p1), e2 = ease(p2);
      overlay.style.clipPath = 'inset(0 ' + ((1 - e1) * 100) + '% 0 0)';
      var s = s0 + (1 - s0) * e2;
      var x = x0 + (x1 - x0) * e2;
      var yy = y0 + (y1 - y0) * e2;   // at scroll = D the real logo sits at viewport y1
      overlay.style.transform = 'translate(' + x + 'px,' + yy + 'px) scale(' + s + ')';
      hint.style.opacity = Math.max(0, 1 - p * 8);
      if (tagline) tagline.style.opacity = e2;
    }

    // build overlay + spacer
    spacer = document.createElement('div');
    spacer.className = 'intro-spacer';
    document.body.insertBefore(spacer, document.querySelector('.site-header'));
    overlay = document.createElement('div');
    overlay.id = 'logo-intro';
    overlay.setAttribute('aria-hidden', 'true');
    var img = document.createElement('img');
    img.src = realImg.currentSrc || realImg.src;
    overlay.appendChild(img);
    document.body.appendChild(overlay);
    hint = document.createElement('div');
    hint.id = 'intro-hint';
    hint.textContent = 'Scroll \u2193';
    document.body.appendChild(hint);

    function init() {
      measure();
      active = false;
      // restore a mid-intro scroll position gracefully
      update();
    }
    if (realImg.complete) init(); else realImg.addEventListener('load', init);

    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', function () { measure(); update(); });
    try { sessionStorage.setItem(INTRO_KEY, '1'); } catch (e) {}
    window.scrollTo(0, 0);
  });
})();
