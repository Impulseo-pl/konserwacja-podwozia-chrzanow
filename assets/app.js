/* Auto Konserwacja v2 – ruch strony (wzór ruchu: Bryki z Ameryki). Każdy blok w try/catch. */
(function () {
  var d = document.documentElement;
  var RM = false;
  try { RM = window.matchMedia('(prefers-reduced-motion: reduce)').matches; } catch (e) { }
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* płynne przewijanie */
  var lenis = null;
  try {
    if (!RM && window.Lenis && window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
      lenis = new window.Lenis({ lerp: 0.09, smoothWheel: true, anchors: { offset: -80 } });
      var raf = function (t) { lenis.raf(t); requestAnimationFrame(raf); };
      requestAnimationFrame(raf);
      if (d.classList.contains('intro-on')) lenis.stop();
    }
  } catch (e) { lenis = null; }

  /* pętla przewijania – wszystkie efekty zależne od pozycji */
  var naScroll = [], tik = false;
  var przelicz = function () { tik = false; for (var i = 0; i < naScroll.length; i++) { try { naScroll[i](); } catch (e) { } } };
  var zglos = function () { if (!tik) { tik = true; requestAnimationFrame(przelicz); } };
  window.addEventListener('scroll', zglos, { passive: true });
  window.addEventListener('resize', zglos, { passive: true });

  /* intro raz na sesję */
  var heroGo = function () { requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.add('hero-go'); }); }); };
  try {
    var przyjscie = false;
    try { przyjscie = sessionStorage.getItem('ak_kurtyna') === '1'; sessionStorage.removeItem('ak_kurtyna'); } catch (e) { }
    if (d.classList.contains('intro-on')) {
      requestAnimationFrame(function () { requestAnimationFrame(function () { d.classList.add('intro-gra'); }); });
      var t0 = Date.now();
      var koniec = function () {
        if (!d.classList.contains('intro-on') || d.classList.contains('intro-out')) return;
        d.classList.add('intro-out'); setTimeout(heroGo, 300);
        setTimeout(function () { d.classList.remove('intro-on', 'intro-gra', 'intro-out'); if (lenis) lenis.start(); }, 1000);
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

  /* kurtyna między podstronami */
  try {
    var kurtyna = $('.kurtyna');
    document.addEventListener('click', function (e) {
      var a = e.target.closest('a');
      if (!a || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
      if (a.target || a.hasAttribute('data-lb')) return;
      var u = new URL(a.href, location.href);
      if (u.origin !== location.origin || u.protocol.indexOf('http') !== 0 || u.pathname === location.pathname) return;
      e.preventDefault();
      try { sessionStorage.setItem('ak_kurtyna', '1'); } catch (er) { }
      kurtyna.classList.add('idz');
      setTimeout(function () { location.href = a.href; }, 520);
    });
    window.addEventListener('pageshow', function (ev) { if (ev.persisted) kurtyna.classList.remove('idz'); });
  } catch (e) { }

  /* nagłówek, menu, przyklejony telefon */
  try {
    var top = $('.top'), st = $('.sticky-tel');
    naScroll.push(function () { var y = window.pageYOffset; top.classList.toggle('zwin', y > 30); if (st) st.classList.toggle('on', y > 500); });
    $('.burger').addEventListener('click', function () { var o = d.classList.toggle('menu-open'); this.setAttribute('aria-expanded', o); });
    $$('.menu a').forEach(function (a) { a.addEventListener('click', function () { d.classList.remove('menu-open'); }); });
  } catch (e) { }

  /* odsłanianie */
  try {
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    $$('.lines, .rv').forEach(function (el) { if (!el.closest('.hero')) io.observe(el); });
    var hl = $('.hero .lines') || $('.pod-hero .lines');
    if (hl) {
      var hg = function () { hl.classList.add('in'); };
      if (d.classList.contains('hero-go')) hg();
      else new MutationObserver(function (m, o) { if (d.classList.contains('hero-go')) { hg(); o.disconnect(); } }).observe(d, { attributes: true });
    }
  } catch (e) { $$('.lines,.rv').forEach(function (el) { el.classList.add('in'); }); }

  /* hero: paralaksa tła i napis w tle przesuwany przewijaniem (Bryki) */
  try {
    var hbg = $('[data-par]'), tlo = $('[data-tlo]');
    if (hbg && !RM) naScroll.push(function () {
      var y = window.pageYOffset; if (y > window.innerHeight * 1.2) return;
      hbg.style.transform = 'translate3d(0,' + (y * 0.28) + 'px,0)';
      if (tlo) tlo.style.transform = 'translate3d(' + (-y * 0.55) + 'px,0,0)';
    });
  } catch (e) { }

  /* liczniki (Bryki) */
  try {
    var cio = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        if (!x.isIntersecting) return; cio.unobserve(x.target);
        var el = x.target, cel = +el.getAttribute('data-cnt'), od = el.getAttribute('data-od'), t0 = null, dur = 1400;
        if (RM) return;
        var krok = function (t) {
          if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur), v = Math.round(cel * (1 - Math.pow(1 - p, 3)));
          el.textContent = od ? (Math.min(+od, v) + '–' + v) : v;
          if (p < 1) requestAnimationFrame(krok); else el.textContent = od ? od + '–' + cel : cel;
        };
        requestAnimationFrame(krok);
      });
    }, { threshold: .6 });
    $$('[data-cnt]').forEach(function (el) { cio.observe(el); });
  } catch (e) { }

  /* napis na drodze – prostuje się przy przewijaniu (Bryki „NASZA OFERTA”) */
  try {
    var dr = $('[data-droga]');
    if (dr && !RM) naScroll.push(function () {
      var r = dr.parentNode.getBoundingClientRect(), vh = window.innerHeight;
      var p = Math.max(0, Math.min(1, (vh - r.top) / (vh + r.height * 0.4)));
      dr.style.transform = 'rotateX(' + (68 - p * 40) + 'deg) rotateZ(' + (-10 + p * 7) + 'deg) translateY(' + (-p * 14) + '%)';
    });
  } catch (e) { }

  /* przed / po */
  try {
    $$('[data-pp]').forEach(function (pp) {
      var r = pp.querySelector('input');
      r.addEventListener('input', function () { pp.style.setProperty('--x', r.value + '%'); });
      var pio = new IntersectionObserver(function (en) {
        if (!en[0].isIntersecting || RM) return; pio.disconnect();
        var t0 = null; var an = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / 1600); var v = 50 + Math.sin(p * Math.PI * 2) * 18 * (1 - p); pp.style.setProperty('--x', v + '%'); r.value = v; if (p < 1) requestAnimationFrame(an); };
        requestAnimationFrame(an);
      }, { threshold: .6 });
      pio.observe(pp);
    });
  } catch (e) { }

  /* karuzela realizacji */
  try {
    var tor = $('[data-tor]');
    if (tor) {
      var pas = $('[data-tor-pasek]');
      var akt = function () { var m = tor.scrollWidth - tor.clientWidth; var widok = tor.clientWidth / tor.scrollWidth; pas.style.transform = 'scaleX(' + Math.min(1, widok + (m ? tor.scrollLeft / m : 0) * (1 - widok)) + ')'; };
      tor.addEventListener('scroll', akt, { passive: true }); akt(); window.addEventListener('resize', akt);
      var krokT = function () { var c = tor.querySelector('.rk'); return c ? c.offsetWidth + 16 : 300; };
      $('[data-tor-l]').addEventListener('click', function () { tor.scrollBy({ left: -krokT(), behavior: 'smooth' }); });
      $('[data-tor-p]').addEventListener('click', function () { tor.scrollBy({ left: krokT(), behavior: 'smooth' }); });
      var dn = false, sx = 0, sl = 0, ruch = false;
      tor.addEventListener('mousedown', function (e) { dn = true; ruch = false; sx = e.pageX; sl = tor.scrollLeft; tor.style.scrollSnapType = 'none'; });
      window.addEventListener('mouseup', function () { if (dn) { dn = false; tor.style.scrollSnapType = ''; } });
      tor.addEventListener('mousemove', function (e) { if (!dn) return; var dx = e.pageX - sx; if (Math.abs(dx) > 5) ruch = true; tor.scrollLeft = sl - dx; });
      tor.addEventListener('click', function (e) { if (ruch) { e.preventDefault(); e.stopPropagation(); } }, true);
      tor.addEventListener('dragstart', function (e) { e.preventDefault(); });
    }
  } catch (e) { }

  /* wycena – podsumowanie na żywo */
  try {
    var f = $('.wyc');
    if (f) {
      var CO = JSON.parse($('#co-typ').textContent);
      var nazwa = function (inp) { return inp ? inp.closest('label').querySelector('b').textContent : ''; };
      var co = $('[data-w-co]'), lista = $('[data-w-lista]'), typL = $('[data-w-typ]'), ost = null;
      var odswiez = function () {
        var t = f.querySelector('[name=typ]:checked'), w = f.querySelector('[name=wiel]:checked');
        var z = $$('[name=zakres]:checked', f).map(nazwa);
        typL.textContent = nazwa(t);
        if (ost !== t.value) { co.classList.add('zm'); setTimeout(function () { co.textContent = CO[t.value]; co.classList.remove('zm'); }, ost === null ? 0 : 220); ost = t.value; }
        lista.innerHTML = '<li>Wielkość<b>' + nazwa(w) + '</b></li>' + z.map(function (x) { return '<li>' + x + '<b>✓</b></li>'; }).join('');
      };
      f.addEventListener('change', odswiez); odswiez();
      var q = new URLSearchParams(location.search).get('auto');
      if (q) { var r = f.querySelector('[name=typ][value="' + q + '"]'); if (r) { r.checked = true; odswiez(); } }
      f.addEventListener('submit', function (e) {
        e.preventDefault();
        var msg = $('.form-msg', f), imie = f.imie.value.trim(), tel = f.tel.value.trim();
        if (!imie || tel.replace(/\D/g, '').length < 9) { msg.textContent = 'Podaj imię i numer telefonu – oddzwonię.'; return; }
        var t = f.querySelector('[name=typ]:checked'), w = f.querySelector('[name=wiel]:checked');
        var body = 'Auto: ' + nazwa(t) + '\nWielkość: ' + nazwa(w) + '\nMarka i rocznik: ' + f.model.value + '\nZakres: ' + $$('[name=zakres]:checked', f).map(nazwa).join(', ') +
          '\nImię: ' + imie + '\nTelefon: ' + tel + '\nKontakt przez: ' + f.querySelector('[name=kanal]:checked').value;
        location.href = 'mailto:' + f.getAttribute('data-mail') + '?subject=' + encodeURIComponent('Wycena konserwacji podwozia') + '&body=' + encodeURIComponent(body);
        msg.textContent = 'Dziękuję! Oddzwonię, jak tylko zejdę spod auta.';
      });
    }
  } catch (e) { }

  /* proces: przekrój warstw */
  try {
    var diag = $('.diagram'), kroki = $$('.krok');
    if (diag && kroki.length) {
      var kio = new IntersectionObserver(function (en) {
        en.forEach(function (x) { if (x.isIntersecting) { kroki.forEach(function (k) { k.classList.toggle('on', k === x.target); }); diag.setAttribute('data-step', x.target.getAttribute('data-s')); } });
      }, { rootMargin: '-45% 0px -45% 0px' });
      kroki.forEach(function (k) { kio.observe(k); });
    }
  } catch (e) { }

  /* galeria: filtr i podgląd */
  try {
    var fb = $$('.filtry button');
    fb.forEach(function (b) {
      b.addEventListener('click', function () {
        fb.forEach(function (x) { x.setAttribute('aria-pressed', x === b); });
        var fl = b.getAttribute('data-f');
        $$('.m-it').forEach(function (m) { m.classList.toggle('ukryj', fl !== 'wszystkie' && m.getAttribute('data-c') !== fl); m.classList.add('in'); });
      });
    });
    var lb = $('.lb');
    if (lb) {
      $$('[data-lb]').forEach(function (a) {
        a.addEventListener('click', function (e) {
          e.preventDefault(); var im = a.querySelector('img');
          lb.querySelector('img').src = a.href; lb.querySelector('img').alt = im.alt; lb.querySelector('p').textContent = im.alt;
          lb.hidden = false; if (lenis) lenis.stop();
        });
      });
      var zamknij = function () { lb.hidden = true; if (lenis) lenis.start(); };
      lb.addEventListener('click', function (e) { if (e.target !== lb.querySelector('img')) zamknij(); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !lb.hidden) zamknij(); });
    }
  } catch (e) { }

  /* mapa – ładowana, gdy podjedzie do ekranu */
  try {
    var m = $('#mapa');
    if (m && window.L) {
      var mio = new IntersectionObserver(function (en) {
        if (!en[0].isIntersecting) return; mio.disconnect();
        var ll = [parseFloat(m.dataset.lat), parseFloat(m.dataset.lon)];
        var map = L.map(m, { scrollWheelZoom: false }).setView(ll, 14);
        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '© OpenStreetMap' }).addTo(map);
        L.marker(ll).addTo(map).bindPopup('<b>Zakład Konserwacji Samochodowej</b><br>ul. Leśna 1a, Chrzanów');
      }, { rootMargin: '300px' });
      mio.observe(m);
    }
  } catch (e) { }

  zglos();
})();
