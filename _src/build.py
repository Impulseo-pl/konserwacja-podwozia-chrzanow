# -*- coding: utf-8 -*-
"""Demo v2: układ jak montis-studio.com, kolory i ruch jak brykizameryki.pl. Uruchom: python _src/build.py"""
import os, re, html, json
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://impulseo-pl.github.io/konserwacja-podwozia-chrzanow/'
IMG = os.path.join(ROOT, 'img')
TEL, TELH = '501 199 501', '+48501199501'
MAIL = 'witopoz@wp.pl'
ADR1, ADR2 = 'ul. Leśna 1a', '32-500 Chrzanów'
LAT, LON = 50.1451532, 19.3799083
GMAPS = 'https://www.google.com/maps/search/?api=1&query=50.1451532,19.3799083'
LICZNIK = open(os.path.join(ROOT, '_src', 'licznik.js'), encoding='utf-8').read()
e = html.escape

def variants(name):
    out = {}
    for f in os.listdir(IMG):
        m = re.fullmatch(re.escape(name) + r'-(\d+)\.webp', f)
        if m:
            w, h = Image.open(os.path.join(IMG, f)).size
            out.setdefault(w, (w, f, h))
    if not out: raise SystemExit('brak obrazu ' + name)
    return sorted(out.values())

def img(p, name, alt, sizes='(max-width: 900px) 100vw, 50vw', lazy=True, cls=''):
    v = variants(name); big = v[-1]
    srcset = ', '.join(f'{p}img/{f} {w}w' for w, f, h in v)
    a = f'<img src="{p}img/{big[1]}" srcset="{srcset}" sizes="{sizes}" width="{big[0]}" height="{big[2]}" alt="{e(alt)}"'
    if cls: a += f' class="{cls}"'
    a += ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return a + '>'

def full(p, name): return p + 'img/' + variants(name)[-1][1]

SV = lambda d, c='ico', w='1.8': f'<svg class="{c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>'
TELI = SV('M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2')
CHK = SV('M4 12.5l5 5L20 6.5', 'chk', '2.2')
ARR = SV('M5 12h14M13 6l6 6-6 6', 'ico arr')
GO = SV('M7 17L17 7M9 7h8v8', 'ico go')
PIN = SV('M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21zM12 12.2a2.6 2.6 0 1 0 0-5.2 2.6 2.6 0 0 0 0 5.2')
DOWN = SV('M12 4v16M6 14l6 6 6-6', 'ico down', '1.6')
SMS = SV('M4 5h16v11H9l-5 4z')
IKONY = {
    'nowe': SV('M3 15l2-6a2 2 0 0 1 2-1.4h10A2 2 0 0 1 19 9l2 6v3h-2.5M3 15v3h2.5M3 15h18M8.5 18h7M7 18.5a1.5 1.5 0 1 1-3 0M20 18.5a1.5 1.5 0 1 1-3 0M12 2v3M9.5 3.5l1 1.5M14.5 3.5l-1 1.5'),
    'uzywane': SV('M3 15l2-6a2 2 0 0 1 2-1.4h10A2 2 0 0 1 19 9l2 6v3h-2.5M3 15v3h2.5M3 15h18M8.5 18h7M7 18.5a1.5 1.5 0 1 1-3 0M20 18.5a1.5 1.5 0 1 1-3 0'),
    'starsze': SV('M2 15l3-5h4l2-3h6l3 3h2v5h-2M2 15v3h3M2 15h20M9 18h7M8 18.5a2 2 0 1 1-4 0M20 18.5a2 2 0 1 1-4 0'),
    'dostawcze': SV('M2 16V7h11v9M13 10h5l3 3.5V16h-2M2 16h3M9 16h6M8 16.5a2 2 0 1 1-4 0M19 16.5a2 2 0 1 1-4 0'),
    'quad': SV('M7 17.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM23 17.5a3 3 0 1 1-6 0 3 3 0 0 1 6 0zM7 16l3-5h6l2 5M10 11l-1-3h4M16 11l1.5-3H20'),
}
LOGO = ('<svg class="sygnet" viewBox="0 0 40 40" aria-hidden="true"><rect x="1.5" y="1.5" width="37" height="37" rx="5" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<rect class="s3" x="8" y="12" width="24" height="3.4" rx="1"/><rect class="s2" x="8" y="17.6" width="24" height="3.4" rx="1"/><rect class="s1" x="8" y="23.2" width="24" height="3.4" rx="1"/>'
        '<rect x="8" y="28.8" width="24" height="3.4" rx="1" fill="currentColor"/></svg>')

def H(a, b, tag='h2', cls='h2'):
    """Nagłówek jak u Bryk: lekka linijka + gruba linijka."""
    return f'<{tag} class="{cls} lines"><span class="ln"><span class="ln-i lt">{a}</span></span><span class="ln"><span class="ln-i bd">{b}</span></span></{tag}>'

# ---------- dane ----------
TYPY = [
    ('nowe', 'Nowe z salonu', 'auto z salonu, także marki chińskie'),
    ('uzywane', 'Używane', 'po kilku zimach, z solą na podwoziu'),
    ('starsze', 'Starsze i klasyki', 'gdzie liczy się każdy element'),
    ('dostawcze', 'Bus lub pickup', 'auta dostawcze i terenowe'),
    ('quad', 'Quad lub maszyna', 'quady, maszyny, urządzenia'),
]
WIELKOSC = [('male', 'Miejskie', 'np. Yaris, Fabia, Corsa'), ('srednie', 'Kompakt, sedan, kombi', 'np. Octavia, Corolla, Golf'),
            ('suv', 'SUV, crossover', 'np. Tucson, Yaris Cross, X3'), ('duze', 'Bus, pickup, duży SUV', 'np. Hilux, Transit, Land Cruiser')]
ZAKRES = [('podwozie', 'Konserwacja podwozia', 'mycie, odrdzewianie, 5–6 warstw środka, wosk', True),
          ('profile', 'Profile zamknięte i progi', 'od środka, tam, gdzie rdza zaczyna się niewidocznie', True),
          ('zawieszenie', 'Zawieszenie i podzespoły', 'sanki, wahacze, bak, stalowe przewody hamulcowe', True),
          ('piaskowanie', 'Piaskowanie skorodowanych elementów', 'gdy jest potrzeba i możliwość – ocenię na miejscu', False),
          ('zastepcze', 'Auto zastępcze na czas usługi', 'bezpłatnie – zostawiasz swoje, wracasz moim', True)]
CO_TYP = {
    'nowe': 'W nowym aucie blacha jest cienka, a dealer sam sugeruje konserwację. Zabezpieczam, zanim pojawi się pierwsze ognisko korozji – to ono najmocniej zbija cenę przy sprzedaży.',
    'uzywane': 'Najpierw usuwam rdzę i sól po zimie – odrdzewiaczem, ręcznie i maszynowo. Dopiero na czystą, suchą blachę idzie bloker rdzy, inhibitor i środek konserwujący.',
    'starsze': 'Oglądam podwozie na podnośniku i wysyłam Ci zdjęcia stanu. Ogniska korozji odrdzewiam lub piaskuję, a środek zamyka i niszczy korozję, zamiast ją przykrywać.',
    'dostawcze': 'Busy i pickupy wjeżdżają na podnośnik w hali – nie robię na kanale. Zabezpieczam podwozie, ramę i zawieszenie tak samo dokładnie jak w osobówce.',
    'quad': 'Konserwuję też podwozia quadów, maszyn i urządzeń. Zadzwoń, opowiedz, co masz – powiem, jak to zrobię i ile to potrwa.',
}

USLUGI = [
    ('podwozie-2', 'Konserwacja podwozia', 'Mycie, odtłuszczanie, odrdzewianie i 5–6 warstw środka nakładanego pistoletem.', 'big'),
    ('podwozie-3', 'Profile zamknięte i progi', 'Środek wchodzi tam, gdzie rdza zaczyna się od środka i widać ją za późno.', 'big'),
    ('podwozie-1', 'Zawieszenie i podzespoły', 'Sanki, wahacze, bak, stalowe przewody hamulcowe – w cenie, bez dopłat.', 'big'),
    ('przed-zakladem-1', 'Nowe auta z salonu', 'Zabezpieczenie od pierwszej zimy. Także auta chińskich marek.', 'mid'),
    ('hala-3', 'Używane i starsze auta', 'Usuwanie rdzy, piaskowanie, gdy jest potrzeba, i ochrona na lata.', 'mid'),
]
WIERSZE = [('Busy, pickupy, maszyny', 'Hala i podnośniki na większe auta. Nowość: quady.'),
           ('Zabezpieczenie po zimie', 'Mycie z soli drogowej i ochrona przed kolejnym sezonem.')]

REALIZACJE = [
    ('przed-zakladem-1', 'SUV miejski', 'Toyota Yaris Cross', ['Konserwacja podwozia', 'Profile'], 'Auta z salonu, przed odbiorem z Zakładu. Konserwacja podwozia, progów i nadkoli, zdjęcia przed i po wysłane na telefon.'),
    ('hilux', 'Pickup', 'Toyota Hilux', ['Podwozie', 'Rama i zawieszenie'], 'Pickup na podnośniku w hali. Podwozie, zawieszenie i przewody hamulcowe zabezpieczone środkiem nakładanym w kilku warstwach.'),
    ('podwozie-2', 'Efekt na podwoziu', 'Progi i podłużnice', ['5–6 warstw', 'Wosk'], 'Tak wygląda podwozie po robocie: jednolita warstwa środka na blasze, progach i podłużnicach, bez prześwitów.'),
    ('hala-3', 'Hala Zakładu', 'Dwa stanowiska', ['Podnośniki', 'Hala'], 'Auto stoi na hali przez cały czas – schnie bezpiecznie i nikt go nie wystawia pod chmurkę.'),
    ('podwozie-1', 'Efekt na podwoziu', 'Tył i okolice baku', ['Bak', 'Przewody'], 'Bak, przewody i tył podwozia zabezpieczone dokładnie, z osłoniętym układem wydechowym.'),
]

GWARANCJE = [('Cena na gotowo', 'Podaję cenę z materiałem. Żadnych dopłat za zawieszenie czy przewody.'),
             ('Zdjęcia przed i po', 'Wysyłam na Twój telefon. Widzisz stan podwozia i moją pracę.'),
             ('Gwarancja na piśmie', 'Pisemne zlecenie i gwarancja ze środkami, których użyłem.'),
             ('Auto zastępcze', 'Na czas usługi, bezpłatnie. Zostawiasz swoje, wracasz moim.')]
G_IKO = ['M4 7h16v10H4zM4 11h16M8 15h3', 'M4 7h3l2-2h6l2 2h3v12H4zM12 16.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7', 'M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6zM9 12l2 2 4-4', 'M3 15l2-6a2 2 0 0 1 2-1.4h10A2 2 0 0 1 19 9l2 6v3H3zM7 18.5a1.5 1.5 0 1 1-3 0M20 18.5a1.5 1.5 0 1 1-3 0']

KROKI = [
    ('Mycie i suszenie', 'Całe podwozie i podzespoły myję profesjonalnym środkiem (m.in. FP2) pistoletem natryskowym. Potem suszę kompresorem i ręcznie.'),
    ('Odtłuszczacz', 'Czysta, odtłuszczona blacha to warunek przyczepności. Bez tego nawet najlepszy środek odejdzie po pierwszej zimie.'),
    ('Odrdzewiacz i piaskowanie', 'Ogniska korozji usuwam odrdzewiaczem, ręcznie i maszynowo. Skorodowane elementy piaskuję, gdy jest potrzeba.'),
    ('Bloker rdzy', 'Pierwsza warstwa ochronna. Zatrzymuje to, czego nie da się usunąć mechanicznie.'),
    ('Inhibitor korozji', 'Wnika w pory i spoiny – chroni tam, gdzie pistolet nie sięga wzrokiem.'),
    ('Środek konserwujący ×5–6', 'Profesjonalna masa nakładana maszynowo 5–6 razy, czasem więcej. Odporna na kamienie i sól, wycisza auto.'),
    ('Wosk hydrofobowy', 'Ostatnia warstwa odpycha wodę. Potem auto schnie na hali – dlatego nie oddaję go na drugi dzień.'),
]
POROWNANIE = [
    ('Gdzie', 'Na kanale albo na trawie', 'Hala z podnośnikami – widać każdy centymetr'),
    ('Środek', 'Bitex, „baranek”, środki z internetu – często rozcieńczone', 'Tylko do użytku profesjonalnego, według karty technicznej producenta'),
    ('Przygotowanie', 'Smarowanie po brudzie i rdzy', 'Mycie, suszenie, odtłuszczacz, odrdzewiacz, piaskowanie, gdy trzeba'),
    ('Warstwy', 'Jedna, „na oko”', 'Pistoletem 5–6 razy, czasem więcej – bez braków'),
    ('Zawieszenie', 'Za dopłatą albo wcale', 'Sanki, wahacze, przewody hamulcowe – w cenie'),
    ('Czas', '7–10 dni w kolejce albo „na jutro”', 'Ok. 3–4 dni, od razu po przyjęciu. Schnie na hali'),
    ('Dowód', 'Trzeba uwierzyć na słowo', 'Zdjęcia przed i po, środki wpisane na zleceniu'),
]
FAQ = [
    ('Ile kosztuje konserwacja podwozia?', 'Cenę podaję przez telefon, zawsze z materiałem i na gotowo – bez dopłat za zawieszenie czy przewody. Zależy od wielkości auta i stanu podwozia, dlatego wybierz auto w wycenie albo zadzwoń: 501 199 501.'),
    ('Ile trwa konserwacja?', 'Około 3–4 dni. Biorę się za auto od razu po przyjęciu, nie trzymam go tygodnia w kolejce. Na drugi dzień nie oddam, bo zabezpieczenie musi wyschnąć – auto stoi w tym czasie na hali.'),
    ('Czym wrócę do domu?', 'Moim autem. Na czas usługi daję bezpłatnie auto zastępcze: zostawiasz swoje, wracasz naszym.'),
    ('Czy nowe auto potrzebuje konserwacji?', 'Tak. Blacha w nowych autach jest cienka, a fabryczne zabezpieczenie nie chroni wszystkiego. Korozja na nowym aucie to przede wszystkim utrata wartości przy sprzedaży.'),
    ('Skąd mam wiedzieć, co zostało zrobione?', 'Pokazuję środki i narzędzia, a na telefon wysyłam zdjęcia podwozia przed i po. Środki wpisuję na pisemne zlecenie i gwarancję.'),
    ('Na jak długo starcza zabezpieczenie?', 'Używam środków z okresem ochrony 15 lat podanym przez producenta, nakładanych zgodnie z jego kartą techniczną.'),
    ('Czy wystawiacie fakturę VAT?', 'Tak. Zakład ma też status Rzetelna Firma.'),
]
GALERIA = [
    ('podwozie-2', 'Podwozie po konserwacji – progi i podłużnice', 'podwozia'), ('hala-1', 'Hala Zakładu z podnośnikami', 'hala'),
    ('podwozie-1', 'Podwozie po konserwacji – tył i bak', 'podwozia'), ('przed-zakladem-1', 'Auta po konserwacji, przed Zakładem', 'auta'),
    ('hala-3', 'Dwa auta na podnośnikach', 'hala'), ('podwozie-3', 'Zbliżenie: warstwa środka konserwującego', 'podwozia'),
    ('hilux', 'Toyota Hilux przed Zakładem', 'auta'), ('hala-4', 'Stanowisko z kompresorami', 'hala'),
    ('podwozie-przed', 'Fabryczne podwozie nowego auta przed konserwacją', 'podwozia'), ('przed-zakladem-2', 'Auta klientów pod Zakładem', 'auta'),
    ('hala-2', 'Podnośniki w hali', 'hala'), ('zaklad', 'Budynek Zakładu Konserwacji Samochodowej', 'auta'),
]

# ---------- szkielet ----------
def head(p, title, desc, path, intro=False):
    ld = {"@context": "https://schema.org", "@type": "AutoRepair", "name": "Zakład Konserwacji Samochodowej – Auto Konserwacja", "founder": "Witold Poznański",
          "telephone": "+48 501 199 501", "email": MAIL, "url": BASE, "image": BASE + "img/hala-1-1600.webp",
          "address": {"@type": "PostalAddress", "streetAddress": "Leśna 1a", "addressLocality": "Chrzanów", "postalCode": "32-500", "addressCountry": "PL"},
          "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LON}, "areaServed": ["Chrzanów", "Libiąż", "Trzebinia", "Jaworzno", "Oświęcim", "Kraków"]}
    return f'''<!DOCTYPE html>
<html lang="pl" class="{'intro-on' if intro else ''}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{BASE}{path}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{BASE}img/podwozie-2-1600.webp"><meta property="og:locale" content="pl_PL">
<meta name="theme-color" content="#0a1433">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;800;900&family=Geist:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/styles.css">
<script>{'try{if(sessionStorage.getItem("ak_intro"))document.documentElement.classList.remove("intro-on")}catch(e){}' if intro else ''}</script>
<script>{LICZNIK}</script>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
'''

def header(p, home=False):
    h = '' if home else p
    nav = [('Start', p or './'), ('Usługi', p + 'uslugi/'), ('Realizacje', p + 'realizacje/'), ('Wycena', p + 'wycena/'), ('Kontakt', p + 'kontakt/')]
    links = ''.join(f'<a href="{u}">{t}</a>' for t, u in nav)
    return f'''<div class="kurtyna" aria-hidden="true"></div>
<div class="intro" aria-hidden="true"><div class="intro-in">{LOGO}<div class="intro-name"><span class="lt">Auto</span><span class="bd">Konserwacja</span></div><div class="intro-line"><i></i></div></div></div>
<div class="topbar"><div class="wrap topbar-in"><span>Chrzanów · od strony Libiąża · terminy na bieżąco</span><span>Auto zastępcze gratis</span></div></div>
<header class="top">
  <div class="wrap top-in">
    <a class="logo" href="{p}" aria-label="Auto Konserwacja – strona główna">{LOGO}<span><b>AUTO KONSERWACJA</b><small>Witold Poznański</small></span></a>
    <nav class="menu" aria-label="Główne">{links}</nav>
    <a class="top-tel" href="tel:{TELH}">{TELI}<span>+48 {TEL}</span></a>
    <a class="btn btn-r btn-sm" href="{p}wycena/">Zamów wycenę</a>
    <button class="burger" aria-label="Menu" aria-expanded="false"><i></i><i></i></button>
  </div>
</header>
'''

def footer(p):
    return f'''<footer class="stopka">
  <div class="wrap stopka-grid">
    <div class="st-o">
      <a class="logo" href="{p}">{LOGO}<span><b>AUTO KONSERWACJA</b><small>Witold Poznański</small></span></a>
      <p>Zakład Profesjonalnej Konserwacji Samochodowej oraz Zawieszenia i jego Podzespołów. Członek Polskiego Stowarzyszenia Korozyjnego i Europejskiej Federacji Korozyjnej.</p>
      <p class="st-k">{PIN}{ADR1}, {ADR2}</p><p class="st-k">{TELI}<a href="tel:{TELH}">+48 {TEL}</a></p>
    </div>
    <div><p class="st-h">Usługi</p><a href="{p}uslugi/">Konserwacja podwozia</a><a href="{p}uslugi/">Profile zamknięte i progi</a><a href="{p}uslugi/">Zawieszenie i podzespoły</a><a href="{p}uslugi/#proces">Jak pracuję</a><a href="{p}uslugi/#porownanie">Czym to się różni</a></div>
    <div><p class="st-h">Zakład</p><a href="{p}">Strona główna</a><a href="{p}realizacje/">Realizacje</a><a href="{p}wycena/">Wycena</a><a href="{p}wycena/#faq">Pytania</a><a href="{p}kontakt/">Kontakt i dojazd</a></div>
    <div><p class="st-h">Obszar</p><p class="muted">Chrzanów, Libiąż, Trzebinia, Jaworzno, Oświęcim, Alwernia, Kraków i okolice.</p></div>
  </div>
  <div class="wrap st-dol"><span>© 2026 Zakład Konserwacji Samochodowej · Faktura VAT · Rzetelna Firma</span><span>Zdjęcia własne, z Zakładu · Projekt: Impulseo</span></div>
</footer>
<a class="sticky-tel" href="tel:{TELH}">{TELI}<span>Zadzwoń: {TEL}</span></a>
<script src="{p}assets/lenis.min.js"></script>
<script src="{p}assets/app.js"></script>
</body></html>
'''

# ---------- sekcje ----------
def hero(p):
    return f'''<section class="hero">
  <div class="hero-bg" data-par>{img(p, 'podwozie-2', 'Podwozie po konserwacji w Zakładzie w Chrzanowie', '100vw', lazy=False)}</div>
  <div class="wrap hero-in">
    <p class="eyebrow">Konserwacja podwozia · Chrzanów i okolice</p>
    {H('Podwozie zabezpieczone', 'na kolejne lata.', 'h1', 'h1')}
    <p class="hero-lead">Nowe auta z salonu, używane i starsze. Konserwacja na hali, środkami z 15-letnim okresem ochrony – a na czas usługi dostajesz bezpłatnie auto zastępcze.</p>
    <div class="hero-cta"><a class="btn btn-r" href="{p}wycena/">Zamów wycenę {ARR}</a><a class="btn btn-gh" href="tel:{TELH}">{TELI}Zadzwoń</a></div>
  </div>
  <a class="hero-strz" href="#uslugi" aria-label="Przewiń w dół">{DOWN}</a>
</section>'''

def uslugi(p, skrot=False):
    cel = p + ('uslugi/' if skrot else 'wycena/')
    def card(n, t, d, k):
        return f'<a class="usl usl-{k} rv" href="{cel}">{img(p, n, t, "(max-width: 900px) 100vw, 34vw")}<span class="usl-tx"><b>{t}</b><span>{d}</span></span></a>'
    big = ''.join(card(*u) for u in USLUGI if u[3] == 'big')
    if skrot:
        return f'''<section class="sek" id="uslugi"><div class="wrap">
  <div class="sh sh-row"><div>{H('Co zrobię', 'z Twoim autem')}<p class="lead">Najpierw oglądam podwozie na podnośniku, potem mówię, co trzeba zrobić. Bez dopisywania usług, których auto nie potrzebuje.</p></div><a class="btn btn-gh btn-sm" href="{cel}">Wszystkie usługi {ARR}</a></div>
  <div class="usl-3">{big}</div>
</div></section>'''
    mid = ''.join(card(*u) for u in USLUGI if u[3] == 'mid')
    rows = ''.join(f'<a class="usl-row rv" href="{cel}"><b>{t}</b><span>{d}</span><i>{GO}</i></a>' for t, d in WIERSZE)
    return f'''<section class="sek" id="uslugi"><div class="wrap">
  <div class="usl-3">{big}</div><div class="usl-2">{mid}</div><div class="usl-rows">{rows}</div>
</div></section>'''

def ribbon():
    t = ' · '.join(['Auto zastępcze gratis', 'Zdjęcia przed i po na telefon', 'Gwarancja na piśmie', 'Faktura VAT', 'Rzetelna Firma', 'Bez bitexu i baranka'])
    return f'<div class="tasma" aria-hidden="true"><div class="tasma-in"><span>{t} · </span><span>{t} · </span><span>{t} · </span></div></div>'

def przedpo(p):
    return f'''<section class="sek sek-pp"><div class="wrap">
  <div class="sh">{H('Różnica, którą widać', 'pod autem')}<p class="lead">Przesuń suwak. Z lewej fabryczne podwozie nowego auta, z prawej podwozie po konserwacji w moim Zakładzie.</p></div>
  <div class="pp-grid">
    <div class="pp rv" data-pp style="--x:50%">
      <div class="pp-a">{img(p, 'podwozie-przed', 'Fabryczne podwozie nowego auta przed konserwacją', '(max-width: 900px) 100vw, 60vw')}</div>
      <div class="pp-b">{img(p, 'podwozie-1', 'Podwozie po konserwacji', '(max-width: 900px) 100vw, 60vw')}</div>
      <span class="pp-l pp-l1">Fabrycznie</span><span class="pp-l pp-l2">Po konserwacji</span>
      <span class="pp-h" aria-hidden="true"><i>⇆</i></span>
      <input type="range" min="0" max="100" value="50" aria-label="Porównaj: przed i po konserwacji">
    </div>
    <div class="pp-info rv">
      <h3>Konserwacja podwozia</h3>
      <div class="pp-st"><div><small>Warstwy środka</small><b>5–6×</b></div><div><small>Czas usługi</small><b>3–4 dni</b></div></div>
      <p>Mycie, odtłuszczacz, odrdzewiacz, bloker rdzy, inhibitor korozji, środek konserwujący i wosk. Zdjęcia przed i po dostajesz na telefon.</p>
      <a class="link-r" href="{p}wycena/">Chcę taki efekt {ARR}</a>
      <p class="muted small">Zdjęcia poglądowe – dwa różne auta z Zakładu.</p>
    </div>
  </div>
</div></section>'''

def realizacje_karuzela(p):
    cards = ''
    for n, kat, t, tagi, d in REALIZACJE:
        cards += f'''<article class="rk">{img(p, n, t, "(max-width: 900px) 80vw, 24vw")}<div class="rk-tx"><small>{kat}</small><h3>{t}</h3><p>{d}</p>
<a class="link-r" href="{p}wycena/">Chcę podobny efekt {ARR}</a></div></article>'''
    return f'''<section class="sek sek-rk"><div class="wrap">
  <div class="sh sh-row"><div>{H('Moja praca,', 'nie zdjęcia z internetu')}</div><a class="btn btn-gh btn-sm" href="{p}realizacje/">Wszystkie realizacje {ARR}</a></div></div>
  <div class="rk-tor" data-tor>{cards}</div>
  <div class="wrap rk-nav"><div class="rk-pasek"><i data-tor-pasek></i></div><button class="rk-b" data-tor-l aria-label="Poprzednie">{SV("M15 6l-6 6 6 6")}</button><button class="rk-b" data-tor-p aria-label="Następne">{SV("M9 6l6 6-6 6")}</button></div>
</section>'''

def droga(t1, t2):
    """Napis położony na drodze w perspektywie, prostuje się przy przewijaniu (jak 'NASZA OFERTA' u Bryk)."""
    return f'<div class="droga" aria-hidden="true"><div class="droga-in" data-droga><span>{t1}</span><span>{t2}</span></div></div>'

def wycena(tag='h2'):
    typy = ''.join(f'<label class="opt opt-t"><input type="radio" name="typ" value="{k}"{" checked" if i == 0 else ""}><span class="opt-in">{IKONY[k]}<b>{t}</b><small>{d}</small></span></label>' for i, (k, t, d) in enumerate(TYPY))
    wiel = ''.join(f'<label class="opt opt-w"><input type="radio" name="wiel" value="{k}"{" checked" if i == 1 else ""}><span class="opt-in"><b>{t}</b><small>{d}</small></span></label>' for i, (k, t, d) in enumerate(WIELKOSC))
    zak = ''.join(f'<label class="opt opt-z"><input type="checkbox" name="zakres" value="{k}"{" checked" if c else ""}><span class="opt-in"><i class="box">{CHK}</i><span><b>{t}</b><small>{d}</small></span><em>{"w cenie" if k not in ("piaskowanie",) else "gdy trzeba"}</em></span></label>' for k, t, d, c in ZAKRES)
    co = json.dumps(CO_TYP, ensure_ascii=False)
    return f'''<section class="sek sek-wyc" id="wycena"><div class="wrap">
  <div class="sh">{H('Wycena', 'w 60 sekund', tag, 'h1 h1-pod' if tag == 'h1' else 'h2')}<p class="lead">Wybierz rodzaj auta, wielkość i zakres. Oddzwonię z ceną z materiałem – na gotowo, bez dopłat.</p></div>
  <form class="wyc" data-mail="{MAIL}" novalidate>
    <div class="wyc-l">
      <fieldset><legend><i>1</i>Jakie masz auto?</legend><div class="opts-t">{typy}</div></fieldset>
      <fieldset><legend><i>2</i>Wielkość auta</legend><div class="opts-w">{wiel}</div></fieldset>
      <fieldset><legend><i>3</i>Zakres</legend><div class="opts-z">{zak}</div></fieldset>
    </div>
    <aside class="wyc-r"><div class="wyc-karta">
      <p class="muted small">Twoja wycena: <b data-w-typ>Nowe z salonu</b></p>
      <p class="wyc-cena">Cena na gotowo<small>z materiałem – podam przez telefon</small></p>
      <p class="wyc-co" data-w-co></p>
      <ul class="wyc-lista" data-w-lista></ul>
      <hr>
      <h3>Zarezerwuj termin</h3>
      <label>Imię<input name="imie" placeholder="np. Tomasz" autocomplete="given-name"></label>
      <label>Numer telefonu<input name="tel" type="tel" placeholder="np. 600 123 456" autocomplete="tel"></label>
      <label>Marka i rocznik <span class="muted">(opcjonalnie)</span><input name="model" placeholder="np. Toyota Yaris Cross 2024"></label>
      <p class="wyc-jak">Jak się z Tobą skontaktować?</p>
      <div class="wyc-kanal"><label><input type="radio" name="kanal" value="telefon" checked><span>{TELI}Telefon</span></label><label><input type="radio" name="kanal" value="SMS"><span>{SMS}SMS</span></label></div>
      <button class="btn btn-r btn-full" type="submit">Zamów bezpłatną wycenę</button>
      <p class="form-msg" role="status"></p>
      <p class="muted small">Bez zobowiązań. Numer wykorzystam tylko do kontaktu w sprawie wyceny.</p>
    </div></aside>
  </form>
  <script type="application/json" id="co-typ">{co}</script>
</div></section>'''

def gwarancje():
    li = ''.join(f'<div class="gw rv">{SV(G_IKO[i])}<b>{t}</b><span>{d}</span></div>' for i, (t, d) in enumerate(GWARANCJE))
    return f'<section class="gwar"><div class="wrap gw-in">{li}</div></section>'

def diagram():
    pas = ''.join(f'<rect class="w5 p{i}" x="40" y="{150 - 8 - i * 7}" width="520" height="7"/>' for i in range(6))
    return f'''<svg class="przekroj" viewBox="30 48 540 226" role="img" aria-label="Przekrój blachy podwozia z kolejnymi warstwami zabezpieczenia">
  <defs><pattern id="rdza" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="3"/><circle cx="11" cy="10" r="2.2"/></pattern></defs>
  <rect class="blacha" x="40" y="150" width="520" height="34"/><rect class="blacha-cien" x="40" y="184" width="520" height="6"/>
  <g class="brud"><path d="M40 150h520v-14c-30 6-60-8-95 0s-70 10-110 2-80-8-120 0-70 6-100 0-60-4-95 0z"/></g>
  <g class="tluszcz"><rect x="40" y="143" width="520" height="7"/></g>
  <g class="rdza"><rect x="80" y="146" width="90" height="10" fill="url(#rdza)"/><rect x="300" y="146" width="140" height="10" fill="url(#rdza)"/><rect x="490" y="146" width="50" height="10" fill="url(#rdza)"/></g>
  <rect class="w3" x="40" y="146" width="520" height="4"/><rect class="w4" x="40" y="142" width="520" height="4"/>{pas}
  <rect class="w6" x="40" y="94" width="520" height="5"/>
  <g class="kropla"><path d="M300 66c0 0-10 13-10 20a10 10 0 0 0 20 0c0-7-10-20-10-20z"/></g>
  <g class="podpisy"><text x="44" y="212">BLACHA PODWOZIA</text>
    <text class="t3" x="560" y="214" text-anchor="end">bloker rdzy</text><text class="t4" x="560" y="230" text-anchor="end">inhibitor korozji</text>
    <text class="t5" x="560" y="246" text-anchor="end">środek konserwujący ×5–6</text><text class="t6" x="560" y="262" text-anchor="end">wosk hydrofobowy</text></g>
</svg>'''

def proces():
    kroki = ''.join(f'<li class="krok" data-s="{i + 1}"><span class="krok-n">{i + 1}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(KROKI))
    return f'''<section class="sek sek-proc" id="proces">
  {droga('BEZ KANAŁU.', 'BEZ BITEXU.')}
  <div class="wrap proc-grid">
    <div class="proc-l"><div class="proc-st">{H('Siedem etapów.', 'Żadnego na skróty.')}
      <div class="diagram" data-step="0">{diagram()}</div><p class="muted small">Schemat przekroju blachy – tak przybywa warstw na podwoziu Twojego auta.</p></div></div>
    <ol class="kroki">{kroki}</ol>
  </div>
</section>'''

def porownanie():
    rows = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in POROWNANIE)
    return f'''<section class="sek sek-jasna" id="porownanie"><div class="wrap">
  <div class="sh">{H('Czym to się różni', 'od bitexu na kanale?')}</div>
  <div class="tab-wrap rv"><table class="tabela"><thead><tr><th></th><th>Typowa „konserwacja”</th><th>W moim Zakładzie</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>'''

def wlasciciel(p):
    return f'''<section class="sek sek-wl"><div class="wrap wl-grid">
  <figure class="wl-img rv">{img(p, 'hala-1', 'Hala Zakładu Konserwacji Samochodowej w Chrzanowie')}</figure>
  <div class="wl-tx rv">{H('Samochody to moja', 'pasja i praca.')}
    <p>Nie robię na kanale ani na trawie, jak większość – tak nie da się tego zrobić fachowo. Pracuję na hali, na podnośnikach, środkami do użytku profesjonalnego, według karty technicznej producenta.</p>
    <p>Pokazuję klientowi, czym myję i konserwuję, jakim pistoletem i narzędziami pracuję. Po robocie każdy dostaje na telefon zdjęcia podwozia przed i po.</p>
    <p class="wl-podpis">Witold Poznański</p>
    <p class="wl-odz-t">Członek Polskiego Stowarzyszenia Korozyjnego i Europejskiej Federacji Korozyjnej. Firma z certyfikatem Rzetelna Firma.</p>
  </div>
</div></section>'''

def faq():
    it = ''.join(f'<details class="faq-it"{" open" if i == 0 else ""}><summary>{q}<span class="plus" aria-hidden="true"></span></summary><div class="faq-a"><p>{a}</p></div></details>' for i, (q, a) in enumerate(FAQ))
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    return f'''<section class="sek" id="faq"><div class="wrap faq-grid">
  <div>{H('Częste', 'pytania')}<p class="lead">Nie ma tu Twojego pytania? Zadzwoń – odpowiem od ręki.</p><a class="btn btn-gh btn-sm" href="tel:{TELH}">{TELI}{TEL}</a></div>
  <div class="faq-lista">{it}</div></div>
  <script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>
</section>'''

def kontakt(p, pelna=False):
    tag = 'h1' if pelna else 'h2'
    return f'''<section class="sek sek-kon" id="kontakt"><div class="wrap">
  <div class="kon-karta">
    <div class="kon-l">
      {H('Zostaw numer.', 'Resztą zajmę się&nbsp;ja.', tag, 'h2')}
      <p class="lead">Oddzwonię z ceną i najbliższym wolnym terminem. Ze względu na specyfikę pracy najlepiej po prostu zadzwoń.</p>
      <a class="kon-tel" href="tel:{TELH}">{TEL}</a>
      <div class="kon-dane"><p>{PIN}<span>{ADR1}, {ADR2}<br>Chrzanów-Kąty, od strony Libiąża</span></p><p>{SMS}<span><a href="mailto:{MAIL}">{MAIL}</a><br>Faktura VAT</span></p></div>
      <a class="link-r" href="{GMAPS}" target="_blank" rel="noopener">Wyznacz dojazd {ARR}</a>
    </div>
    <div class="kon-mapa" id="mapa" data-lat="{LAT}" data-lon="{LON}"><div class="mapa-ph">{img(p, 'zaklad', 'Budynek Zakładu Konserwacji Samochodowej', '(max-width: 900px) 100vw, 50vw')}</div></div>
  </div>
</div></section>'''

# ---------- strony ----------
LEAFLET = '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>'

def home():
    p = ''
    body = hero(p) + uslugi(p, skrot=True) + przedpo(p) + realizacje_karuzela(p) + gwarancje() + wlasciciel(p) + kontakt(p)
    return head(p, 'Konserwacja podwozia Chrzanów – Zakład Konserwacji Samochodowej, Witold Poznański',
                'Konserwacja podwozia w Chrzanowie: nowe, używane i starsze auta, na hali, środkami z 15-letnim okresem ochrony. Auto zastępcze gratis, zdjęcia przed i po. Tel. 501 199 501.', '', intro=True) \
        + header(p, True) + '<main>' + body + '</main>' + LEAFLET + footer(p)

def realizacje():
    p = '../'
    filtry = [('wszystkie', 'Wszystkie'), ('podwozia', 'Podwozia'), ('hala', 'Hala'), ('auta', 'Auta klientów')]
    fb = ''.join(f'<button data-f="{k}" aria-pressed="{"true" if i == 0 else "false"}">{t}</button>' for i, (k, t) in enumerate(filtry))
    items = ''.join(f'<figure class="m-it rv" data-c="{c}"><a href="{full(p, n)}" data-lb>{img(p, n, a, "(max-width: 700px) 100vw, (max-width: 1100px) 50vw, 33vw")}</a><figcaption>{a}</figcaption></figure>' for n, a, c in GALERIA)
    body = f'''<section class="pod-hero"><div class="wrap">{H('Zdjęcia z mojej hali.', 'Bez białych płytek.', 'h1', 'h1 h1-pod')}
<p class="lead">Wszystkie zdjęcia zrobiłem sam, w Zakładzie w Chrzanowie. Takie same dostajesz na telefon po konserwacji swojego auta.</p></div></section>
<section class="sek galeria"><div class="wrap"><div class="filtry" role="group" aria-label="Filtr zdjęć">{fb}</div><div class="mur">{items}</div></div></section>
<div class="lb" hidden><button class="lb-x" aria-label="Zamknij">×</button><img alt=""><p></p></div>''' + kontakt(p)
    return head(p, 'Realizacje – konserwacja podwozia Chrzanów | Auto Konserwacja', 'Zdjęcia podwozi po konserwacji i hali Zakładu Konserwacji Samochodowej w Chrzanowie.', 'realizacje/') \
        + header(p) + '<main class="pod">' + body + '</main>' + LEAFLET + footer(p)

def uslugi_str():
    p = '../'
    body = (f'<section class="pod-hero"><div class="wrap">{H("Usługi", "i sposób pracy", "h1", "h1 h1-pod")}<p class="lead">Najpierw oglądam podwozie na podnośniku, potem mówię, co trzeba zrobić. Cenę podaję z materiałem, na gotowo – bez dopłat za zawieszenie czy przewody.</p></div></section>'
            + uslugi(p) + gwarancje() + proces() + porownanie() + kontakt(p))
    return head(p, 'Usługi – konserwacja podwozia, profili i zawieszenia Chrzanów | Auto Konserwacja', 'Konserwacja podwozia, profili zamkniętych, progów i zawieszenia w Chrzanowie. Siedem etapów, na hali, 5–6 warstw środka. Auto zastępcze gratis.', 'uslugi/') \
        + header(p) + '<main class="pod">' + body + '</main>' + LEAFLET + footer(p)

def wycena_str():
    p = '../'
    body = wycena('h1') + faq()
    return head(p, 'Wycena konserwacji podwozia – Chrzanów | Auto Konserwacja', 'Wybierz auto i zakres – oddzwonię z ceną konserwacji podwozia z materiałem, na gotowo. Tel. 501 199 501.', 'wycena/') \
        + header(p) + '<main class="pod">' + body + '</main>' + footer(p)

def kontakt_str():
    p = '../'
    body = f'<section class="pod-hero"><div class="wrap">{H("Kontakt", "i dojazd", "h1", "h1 h1-pod")}<p class="lead">Zakład jest w Chrzanowie, od strony Libiąża – blisko z Trzebini, Jaworzna i Oświęcimia.</p></div></section>' + kontakt(p)
    return head(p, 'Kontakt i dojazd – konserwacja podwozia Chrzanów | Auto Konserwacja', 'Zakład Konserwacji Samochodowej, ul. Leśna 1a, Chrzanów (od strony Libiąża). Tel. 501 199 501. Auto zastępcze gratis.', 'kontakt/') \
        + header(p) + '<main class="pod">' + body + '</main>' + LEAFLET + footer(p)

def w(path, s):
    f = os.path.join(ROOT, path); os.makedirs(os.path.dirname(f), exist_ok=True)
    open(f, 'w', encoding='utf-8', newline='\n').write(s)

w('index.html', home()); w('realizacje/index.html', realizacje()); w('uslugi/index.html', uslugi_str()); w('wycena/index.html', wycena_str()); w('kontakt/index.html', kontakt_str())
w('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="7" fill="#0a1433"/><rect x="8" y="12" width="24" height="3.4" rx="1" fill="#e03e39" opacity=".45"/><rect x="8" y="17.6" width="24" height="3.4" rx="1" fill="#e03e39" opacity=".7"/><rect x="8" y="23.2" width="24" height="3.4" rx="1" fill="#e03e39"/><rect x="8" y="28.8" width="24" height="3.4" rx="1" fill="#f2f1ed"/></svg>')
w('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
w('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{BASE}{u}</loc></url>' for u in ['', 'uslugi/', 'realizacje/', 'wycena/', 'kontakt/']) + '</urlset>\n')
print('ok')
