/* Auto Konserwacja – ruch strony. Każdy blok w try/catch. */
(function () {
  var d = document.documentElement;
  var RM = false;
  try { RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { }

  var lenis = null;
  try {
    if (!RM && window.Lenis && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      lenis = new window.Lenis({ lerp: 0.09, smoothWheel: true, anchors: { offset: -60 } });
      var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
      if (d.classList.contains('intro-on')) lenis.stop();
    }
  } catch (e) { lenis = null; }

  /* intro raz na sesję, potem hero */
  var heroGo = function () { requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.add('hero-go'); }); }); };
  try {
    var przyjscie = false;
    try { przyjscie = sessionStorage.getItem('ak_kurtyna') === '1'; sessionStorage.removeItem('ak_kurtyna'); } catch (e) { }
    if (d.classList.contains('intro-on')) {
      requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.add('intro-gra'); }); });
      var t0 = Date.now();
      var koniec = function () {
        if (!d.classList.contains('intro-on')) return;
        d.classList.add('intro-out'); setTimeout(heroGo, 250);
        setTimeout(function () { d.classList.remove('intro-on', 'intro-gra', 'intro-out'); if (lenis) lenis.start(); }, 950);
        try { sessionStorage.setItem('ak_intro', '1'); } catch (e) { }
      };
      var gotowe = function () { setTimeout(koniec, Math.max(0, 1900 - (Date.now() - t0))); };
      if (document.readyState === 'complete') gotowe(); else window.addEventListener('load', gotowe);
      setTimeout(koniec, 4500);
    } else if (przyjscie) {
      d.classList.add('przyjscie');
      requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.add('odslon'); }); });
      setTimeout(heroGo, 200);
    } else heroGo();
    setTimeout(function () { d.classList.add('hero-go'); }, 5000);
  } catch (e) { d.classList.add('hero-go'); }

  /* kurtyna przy przejściu między podstronami */
  try {
    var kurtyna = document.querySelector('.kurtyna');
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      if (a.target || a.hasAttribute('data-lb')) return;
      var u = new URL(a.href, location.href);
      if (u.origin !== location.origin || u.protocol.indexOf('http') !== 0) return;
      if (u.pathname === location.pathname) return;
      e.preventDefault();
      try { sessionStorage.setItem('ak_kurtyna', '1'); } catch (er) { }
      kurtyna.classList.add('idz');
      setTimeout(function () { location.href = a.href; }, 520);
    });
    window.addEventListener('pageshow', function (ev) { if (ev.persisted) kurtyna.classList.remove('idz'); });
  } catch (e) { }

  /* nagłówek */
  try {
    var top = document.querySelector('.top'), last = 0;
    var onS = function () {
      var y = window.pageYOffset;
      top.classList.toggle('zwin', y > 40);
      top.classList.toggle('schowaj', y > 600 && y > last && !d.classList.contains('menu-open'));
      last = y;
      var st = document.querySelector('.sticky-tel'); if (st) st.classList.toggle('on', y > 500);
    };
    window.addEventListener('scroll', onS, { passive: true }); onS();
    document.querySelector('.burger').addEventListener('click', function () {
      var o = d.classList.toggle('menu-open'); this.setAttribute('aria-expanded', o);
    });
    document.querySelectorAll('.menu a').forEach(function (a) { a.addEventListener('click', function () { d.classList.remove('menu-open'); }); });
  } catch (e) { }

  /* odsłanianie */
  try {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } });
    }, { rootMargin: '0px 0px -12% 0px' });
    document.querySelectorAll('.lines, .rv, .rv-img').forEach(function (el) {
      if (el.closest('.hero')) return; io.observe(el);
    });
    var hl = document.querySelector('.hero .lines');
    if (hl) { var hg = function () { hl.classList.add('in'); }; if (d.classList.contains('hero-go')) hg(); else new MutationObserver(function (m, o) { if (d.classList.contains('hero-go')) { hg(); o.disconnect(); } }).observe(d, { attributes: true }); }
  } catch (e) { document.querySelectorAll('.lines,.rv,.rv-img').forEach(function (el) { el.classList.add('in'); }); }

  /* wybór auta */
  try {
    var taby = document.querySelectorAll('.taby [role=tab]'), pasek = document.querySelector('.taby-pasek');
    var ustawPasek = function (b) { pasek.style.width = (b.offsetWidth - 26) + 'px'; pasek.style.transform = 'translateX(' + b.offsetLeft + 'px)'; };
    var wybierz = function (b) {
      taby.forEach(function (t) { var on = t === b; t.setAttribute('aria-selected', on); var p = document.getElementById(t.getAttribute('aria-controls')); p.hidden = !on; p.classList.toggle('wchodzi', on); });
      ustawPasek(b);
    };
    taby.forEach(function (b, i) {
      b.addEventListener('click', function () { wybierz(b); });
      b.addEventListener('keydown', function (e) {
        var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (!k) return;
        var n = taby[(i + k + taby.length) % taby.length]; n.focus(); wybierz(n);
      });
    });
    if (taby.length) { ustawPasek(taby[0]); window.addEventListener('resize', function () { ustawPasek(document.querySelector('.taby [aria-selected=true]')); }); }
  } catch (e) { }

  /* proces: przekrój warstw */
  try {
    var diag = document.querySelector('.diagram'), kroki = document.querySelectorAll('.krok');
    if (diag && kroki.length) {
      var kio = new IntersectionObserver(function (en) {
        en.forEach(function (x) {
          if (x.isIntersecting) {
            kroki.forEach(function (k) { k.classList.toggle('on', k === x.target); });
            diag.setAttribute('data-step', x.target.getAttribute('data-s'));
          }
        });
      }, { rootMargin: '-45% 0px -45% 0px' });
      kroki.forEach(function (k) { kio.observe(k); });
    }
  } catch (e) { }

  /* taśma realizacji – przeciąganie myszą */
  try {
    var ts = document.querySelector('[data-tasma]');
    if (ts) {
      var dn = false, sx = 0, sl = 0, ruch = false;
      ts.addEventListener('mousedown', function (e) { dn = true; ruch = false; sx = e.pageX; sl = ts.scrollLeft; ts.style.scrollSnapType = 'none'; });
      window.addEventListener('mouseup', function () { if (dn) { dn = false; ts.style.scrollSnapType = ''; } });
      ts.addEventListener('mousemove', function (e) { if (!dn) return; var dx = e.pageX - sx; if (Math.abs(dx) > 5) ruch = true; ts.scrollLeft = sl - dx; });
      ts.addEventListener('click', function (e) { if (ruch) { e.preventDefault(); e.stopPropagation(); } }, true);
      ts.addEventListener('dragstart', function (e) { e.preventDefault(); });
    }
  } catch (e) { }

  /* galeria: filtr i podgląd */
  try {
    var fb = document.querySelectorAll('.filtry button');
    fb.forEach(function (b) {
      b.addEventListener('click', function () {
        fb.forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
        var f = b.getAttribute('data-f');
        document.querySelectorAll('.m-it').forEach(function (m) { m.classList.toggle('ukryj', f !== 'wszystkie' && m.getAttribute('data-c') !== f); m.classList.add('in'); });
      });
    });
    var lb = document.querySelector('.lb');
    if (lb) {
      document.querySelectorAll('[data-lb]').forEach(function (a) {
        a.addEventListener('click', function (e) {
          e.preventDefault(); lb.querySelector('img').src = a.href; lb.querySelector('img').alt = a.querySelector('img').alt;
          lb.querySelector('p').textContent = a.querySelector('img').alt; lb.hidden = false; if (lenis) lenis.stop();
        });
      });
      var zamknij = function () { lb.hidden = true; if (lenis) lenis.start(); };
      lb.addEventListener('click', function (e) { if (e.target !== lb.querySelector('img')) zamknij(); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) zamknij(); });
    }
  } catch (e) { }

  /* formularz */
  try {
    var q = new URLSearchParams(location.search).get('auto'), sel = document.getElementById('f-auto');
    if (q && sel) sel.value = q;
    document.querySelectorAll('.form').forEach(function (f) {
      f.addEventListener('submit', function (e) {
        e.preventDefault();
        var msg = f.querySelector('.form-msg'), imie = f.imie.value.trim(), tel = f.tel.value.trim();
        if (!imie || tel.replace(/\D/g, '').length < 9) { msg.textContent = 'Podaj imię i numer telefonu – oddzwonię.'; return; }
        var body = 'Auto: ' + f.auto.options[f.auto.selectedIndex].text + '\nMarka i model: ' + f.model.value + '\nRocznik: ' + f.rok.value +
          '\nImię: ' + imie + '\nTelefon: ' + tel + '\nAuto zastępcze: ' + (f.zastepcze.checked ? 'tak' : 'nie');
        location.href = 'mailto:' + f.getAttribute('data-mail') + '?subject=' + encodeURIComponent('Konserwacja podwozia – prośba o telefon') + '&body=' + encodeURIComponent(body);
        msg.textContent = 'Dziękuję! Oddzwonię, jak tylko zejdę spod auta.';
      });
    });
  } catch (e) { }

  /* mapa */
  try {
    var m = document.getElementById('mapa');
    if (m && window.L) {
      var ll = [parseFloat(m.dataset.lat), parseFloat(m.dataset.lon)];
      var map = L.map(m, { scrollWheelZoom: false }).setView(ll, 14);
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '© OpenStreetMap' }).addTo(map);
      L.marker(ll).addTo(map).bindPopup('<b>Zakład Konserwacji Samochodowej</b><br>ul. Leśna 1a, Chrzanów');
    }
  } catch (e) { }
})();
