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
