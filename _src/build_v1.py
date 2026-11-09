# -*- coding: utf-8 -*-
"""Generator dema: Zakład Konserwacji Samochodowej (Witold Poznański, Chrzanów). Uruchom: python _src/build.py"""
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

# ---------- obrazy ----------
def variants(name):
    out = []
    for f in os.listdir(IMG):
        m = re.fullmatch(re.escape(name) + r'-(\d+)\.webp', f)
        if m:
            w, h = Image.open(os.path.join(IMG, f)).size
            out.append((w, f, h))
    if not out: raise SystemExit('brak obrazu ' + name)
    seen, uniq = set(), []
    for w, f, h in sorted(out):
        if w not in seen: seen.add(w); uniq.append((w, f, h))
    return uniq

def img(p, name, alt, sizes='(max-width: 900px) 100vw, 50vw', lazy=True, cls=''):
    v = variants(name); big = v[-1]
    srcset = ', '.join(f'{p}img/{f} {w}w' for w, f, h in v)
    a = f'<img src="{p}img/{big[1]}" srcset="{srcset}" sizes="{sizes}" width="{big[0]}" height="{big[2]}" alt="{e(alt)}"'
    if cls: a += f' class="{cls}"'
    a += ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    return a + '>'

def full(p, name): return p + 'img/' + variants(name)[-1][1]

SV = lambda d, c='ico', w='1.7': f'<svg class="{c}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg>'
TELI = SV('M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2')
CHK = SV('M4 12.5l5 5L20 6.5', 'chk', '2')
ARR = SV('M5 12h14M13 6l6 6-6 6', 'ico arr')

def lines(*ls, tag='h2', cls='h2'):
    inner = ''.join(f'<span class="ln"><span class="ln-i"{" data-a" if i == len(ls) - 1 and len(ls) > 1 else ""}>{l}</span></span>' for i, l in enumerate(ls))
    return f'<{tag} class="{cls} lines">{inner}</{tag}>'

# ---------- szkielet ----------
NAV = [('Twoje auto', '#auta'), ('Jak pracuję', '#proces'), ('Realizacje', 'realizacje/'), ('Kontakt', 'kontakt/')]

def head(p, title, desc, path, intro=False):
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
<meta name="theme-color" content="#121416">
<link rel="icon" href="{p}favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Hubot+Sans:wght@500;700;800&family=Mona+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{p}assets/styles.css">
<script>{'try{if(sessionStorage.getItem("ak_intro"))document.documentElement.classList.remove("intro-on")}catch(e){}' if intro else ''}</script>
<script>{LICZNIK}</script>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"AutoRepair","name":"Zakład Konserwacji Samochodowej – Auto Konserwacja","founder":"Witold Poznański","telephone":"+48 501 199 501","email":MAIL,"url":BASE,"image":BASE+"img/hala-1-1600.webp","address":{"@type":"PostalAddress","streetAddress":"Leśna 1a","addressLocality":"Chrzanów","postalCode":"32-500","addressCountry":"PL"},"geo":{"@type":"GeoCoordinates","latitude":LAT,"longitude":LON},"areaServed":["Chrzanów","Libiąż","Trzebinia","Jaworzno","Oświęcim","Kraków"]}, ensure_ascii=False)}</script>
</head>
<body>
'''

def header(p, home=False):
    links = ''.join(f'<a href="{(p if not home else "") + h if not h.startswith("#") else ("" if home else p) + h}">{t}</a>' for t, h in NAV)
    return f'''<div class="kurtyna" aria-hidden="true"></div>
<div class="intro" aria-hidden="true"><div class="intro-in">
  <div class="intro-name"><span>AUTO</span><span>KONSERWACJA</span></div>
  <div class="intro-bar"><i></i><i></i><i></i><i></i><i></i><i></i></div>
  <div class="intro-meta">Chrzanów · od strony Libiąża</div>
</div></div>
<header class="top">
  <a class="logo" href="{p}" aria-label="Auto Konserwacja – strona główna">{LOGO}<span><b>Auto Konserwacja</b><small>Witold Poznański · Chrzanów</small></span></a>
  <nav class="menu" aria-label="Główne">{links}</nav>
  <a class="btn btn-tel" href="tel:{TELH}">{TELI}<span>{TEL}</span></a>
  <button class="burger" aria-label="Menu" aria-expanded="false"><i></i><i></i></button>
</header>
'''

LOGO = ('<svg class="sygnet" viewBox="0 0 40 40" aria-hidden="true"><rect x="1" y="1" width="38" height="38" rx="3" fill="none" stroke="currentColor" stroke-width="2"/>'
        '<rect class="w1" x="7" y="25" width="26" height="3"/><rect class="w2" x="7" y="20" width="26" height="3"/><rect class="w3" x="7" y="15" width="26" height="3"/>'
        '<rect x="7" y="30" width="26" height="3" fill="currentColor"/></svg>')

def footer(p):
    return f'''<footer class="stopka" id="kontakt-stopka">
  <div class="wrap stopka-grid">
    <div>
      <p class="stopka-h">Zadzwoń i umów termin</p>
      <a class="tel-xl" href="tel:{TELH}">{TEL}</a>
      <p class="muted">Ze względu na specyfikę pracy proszę zawsze o telefon. Jeśli akurat jestem pod autem, oddzwonię.</p>
    </div>
    <div class="stopka-kol">
      <p><b>Zakład Konserwacji Samochodowej</b><br>{ADR1}, {ADR2}<br>Chrzanów-Kąty, od strony Libiąża</p>
      <p><a href="mailto:{MAIL}">{MAIL}</a><br>Faktura VAT · Rzetelna Firma</p>
    </div>
    <div class="stopka-kol">
      <a href="{p}">Strona główna</a><a href="{p}#auta">Twoje auto</a><a href="{p}#proces">Jak pracuję</a><a href="{p}realizacje/">Realizacje</a><a href="{p}kontakt/">Kontakt i dojazd</a>
    </div>
  </div>
  <div class="wrap stopka-dol"><span class="marka-xl" aria-hidden="true">Auto Konserwacja</span>
  <p class="muted small">© 2026 Witold Poznański · Zdjęcia: własne, z zakładu · Projekt strony: Impulseo</p></div>
</footer>
<a class="sticky-tel" href="tel:{TELH}">{TELI}<span>Zadzwoń: {TEL}</span></a>
<script src="{p}assets/lenis.min.js"></script>
<script src="{p}assets/app.js"></script>
</body></html>
'''

# ---------- dane ----------
AUTA = [
    ('nowe', 'Nowe z salonu', 'przed-zakladem-1', 'Nowe auta z salonu, przed Zakładem',
     'Nowe auto: zabezpieczyć, zanim sól zrobi swoje',
     'Dealerzy coraz częściej sami sugerują konserwację – i mają rację. Blacha w nowych autach jest cienka, a pierwsze ognisko korozji to od razu niższa cena przy sprzedaży. Robię też nowe auta chińskich marek; mam do nich odpowiedni podnośnik i sprzęt.',
     ['Mycie podwozia profesjonalnym środkiem i suszenie', 'Konserwacja podwozia, progów i nadkoli', 'Profile zamknięte, bak, stalowe przewody hamulcowe', 'Zawieszenie: sanki i wahacze – bez dopłat', 'Zdjęcia przed i po na Twój telefon']),
    ('uzywane', 'Używane', 'hala-3', 'Auta na podnośnikach w hali Zakładu',
     'Używane auto: najpierw rdza, potem ochrona',
     'Po zimie na podwoziu zostaje sól drogowa – to ona robi ogniska rdzy i obniża wartość auta. Zanim położę cokolwiek, usuwam rdzę odrdzewiaczem, ręcznie i maszynowo, a skorodowane elementy piaskuję, gdy jest potrzeba i możliwość.',
     ['Usuwanie rdzy ręcznie i maszynowo', 'Piaskowanie skorodowanych elementów, gdy trzeba', 'Bloker rdzy i inhibitor korozji', 'Środek konserwujący nakładany pistoletem 5–6 razy', 'Wosk hydrofobowy na koniec']),
    ('starsze', 'Starsze i klasyki', 'zaklad', 'Zakład Konserwacji Samochodowej z klasycznym Mercedesem przed wejściem',
     'Starsze auto: zatrzymać korozję, zanim zje blachę',
     'W starszym aucie liczy się każdy element: sanki, wahacze, progi, profile zamknięte i stalowe przewody hamulcowe. Stosuję środek, który nie tylko chroni, ale zamyka i niszczy korozję i blokuje wodę. Podwozie przy okazji jest wyciszone.',
     ['Oględziny na podnośniku i zdjęcia stanu przed pracą', 'Piaskowanie i odrdzewianie ognisk korozji', 'Zabezpieczenie zawieszenia i jego podzespołów', 'Profile zamknięte i progi od środka', 'Pisemne zlecenie z wypisanymi środkami']),
    ('dostawcze', 'Dostawcze, pickupy, quady', 'hilux', 'Toyota Hilux przed Zakładem Konserwacji',
     'Pickupy, busy, maszyny i quady',
     'Konserwuję też podwozia aut dostawczych, pickupów, maszyn i urządzeń, a od niedawna również quadów. Hala i podnośniki pozwalają zrobić to porządnie, nie na kanale ani na trawie.',
     ['Auta dostawcze i pickupy na podnośniku', 'Maszyny i urządzenia', 'Quady – nowość w Zakładzie', 'Cena zawsze z materiałem, na gotowo', 'Faktura VAT']),
]

KROKI = [
    ('Mycie i suszenie', 'Całe podwozie i podzespoły myję profesjonalnym środkiem (m.in. FP2) pistoletem natryskowym. Potem suszę kompresorem i ręcznie, żeby nie został piasek, brud ani tłuszcz.'),
    ('Odtłuszczacz', 'Czysta, odtłuszczona blacha to warunek przyczepności. Bez tego nawet najlepszy środek odejdzie po pierwszej zimie.'),
    ('Odrdzewiacz i piaskowanie', 'Ogniska korozji usuwam odrdzewiaczem, ręcznie i maszynowo. Skorodowane elementy piaskuję, gdy jest potrzeba. Na koniec przedmuch kompresorem pod ciśnieniem.'),
    ('Bloker rdzy', 'Pierwsza warstwa ochronna. Zatrzymuje to, czego nie da się usunąć mechanicznie.'),
    ('Inhibitor korozji', 'Wnika w pory i spoiny, chroni tam, gdzie pędzel ani pistolet nie widzą.'),
    ('Środek konserwujący, 5–6 razy', 'Profesjonalna masa, nakładana maszynowo pistoletem 5–6 razy, czasem więcej. Odporna na kamienie i sól drogową, wycisza auto w czasie jazdy.'),
    ('Wosk hydrofobowy', 'Ostatnia warstwa odpycha wodę. Potem auto schnie na hali – dlatego nie oddaję go na drugi dzień.'),
]

POROWNANIE = [
    ('Gdzie', 'Na kanale albo na trawie', 'Hala z podnośnikami – widać każdy centymetr'),
    ('Środek', 'Bitex, „baranek”, środki z internetu – często rozcieńczone', 'Środki tylko do użytku profesjonalnego, według karty technicznej producenta'),
    ('Przygotowanie', 'Smarowanie po brudzie i rdzy', 'Mycie, suszenie, odtłuszczacz, odrdzewiacz, piaskowanie, gdy trzeba'),
    ('Warstwy', 'Jedna, „na oko”', 'Pistoletem 5–6 razy, czasem więcej – do skutku, bez braków'),
    ('Zawieszenie', 'Za dopłatą albo wcale', 'Sanki, wahacze, przewody hamulcowe – w cenie'),
    ('Czas', '7–10 dni czekania albo „na jutro”', 'Ok. 3–4 dni, od razu po przyjęciu auta. Schnie na hali'),
    ('Dowód', 'Trzeba uwierzyć na słowo', 'Zdjęcia przed i po na telefon, środki wpisane na zleceniu i gwarancji'),
]

ELEMENTY = ['Podwozie', 'Progi', 'Nadkola', 'Profile zamknięte', 'Sanki', 'Wahacze', 'Zawieszenie i podzespoły', 'Bak', 'Stalowe przewody hamulcowe']

FAQ = [
    ('Ile trwa konserwacja podwozia?', 'Około 3–4 dni. Biorę się za auto od razu po przyjęciu, nie trzymam go tygodnia w kolejce. Na drugi dzień go nie oddam, bo zabezpieczenie musi wyschnąć – auto stoi w tym czasie bezpiecznie na hali.'),
    ('Czym dojadę do domu, gdy auto zostaje w Zakładzie?', 'Moim autem. Na czas usługi daję bezpłatnie auto zastępcze: zostawiasz swoje, wracasz naszym.'),
    ('Czy nowe auto z salonu potrzebuje konserwacji?', 'Tak – blacha w nowych autach jest cienka, a fabryczne zabezpieczenie nie chroni wszystkiego. Korozja na nowym aucie to przede wszystkim utrata wartości przy sprzedaży.'),
    ('Ile kosztuje konserwacja podwozia?', 'Cenę podaję przez telefon, zawsze z materiałem i na gotowo – bez dopłat za zawieszenie czy przewody. Zależy od wielkości auta i jego stanu, dlatego proszę o krótką rozmowę.'),
    ('Skąd mam wiedzieć, co zostało zrobione?', 'Pokazuję środki do mycia i konserwacji oraz narzędzia, a na Twój telefon wysyłam zdjęcia podwozia przed i po. Środki wpisuję na pisemne zlecenie i gwarancję.'),
    ('Na jak długo wystarcza zabezpieczenie?', 'Używam środków z okresem ochrony 15 lat podanym przez producenta, nakładanych zgodnie z jego kartą technologiczną.'),
    ('Czy wystawiacie fakturę?', 'Tak, wystawiam faktury VAT. Zakład ma status Rzetelna Firma.'),
]

GALERIA = [
    ('podwozie-2', 'Podwozie po konserwacji – progi i podłużnice', 'podwozia'),
    ('hala-1', 'Hala Zakładu z podnośnikami', 'hala'),
    ('podwozie-1', 'Podwozie po konserwacji – tył i tłumik', 'podwozia'),
    ('przed-zakladem-1', 'Nowe auta po konserwacji, przed Zakładem', 'auta'),
    ('hala-3', 'Dwa auta na podnośnikach', 'hala'),
    ('podwozie-3', 'Zbliżenie: warstwa środka konserwującego', 'podwozia'),
    ('hilux', 'Toyota Hilux po wizycie w Zakładzie', 'auta'),
    ('hala-4', 'Stanowisko z kompresorami', 'hala'),
    ('podwozie-przed', 'Podwozie nowego auta przed konserwacją', 'podwozia'),
    ('przed-zakladem-2', 'Auta klientów pod Zakładem', 'auta'),
    ('hala-2', 'Podnośniki w hali', 'hala'),
    ('zaklad', 'Budynek Zakładu Konserwacji Samochodowej', 'auta'),
]

# ---------- sekcje ----------
def diagram():
    pas = ''.join(f'<rect class="w5 p{i}" x="40" y="{150 - 8 - i * 7}" width="520" height="7"/>' for i in range(6))
    return f'''<svg class="przekroj" viewBox="30 48 540 226" role="img" aria-label="Przekrój blachy podwozia z kolejnymi warstwami zabezpieczenia">
  <defs><pattern id="rdza" width="14" height="14" patternUnits="userSpaceOnUse"><circle cx="4" cy="4" r="3"/><circle cx="11" cy="10" r="2.2"/></pattern></defs>
  <rect class="blacha" x="40" y="150" width="520" height="34"/>
  <rect class="blacha-cien" x="40" y="184" width="520" height="6"/>
  <g class="brud"><path d="M40 150h520v-14c-30 6-60-8-95 0s-70 10-110 2-80-8-120 0-70 6-100 0-60-4-95 0z"/></g>
  <g class="tluszcz"><rect x="40" y="143" width="520" height="7"/></g>
  <g class="rdza"><rect x="80" y="146" width="90" height="10" fill="url(#rdza)"/><rect x="300" y="146" width="140" height="10" fill="url(#rdza)"/><rect x="490" y="146" width="50" height="10" fill="url(#rdza)"/></g>
  <rect class="w3" x="40" y="146" width="520" height="4"/>
  <rect class="w4" x="40" y="142" width="520" height="4"/>
  {pas}
  <rect class="w6" x="40" y="94" width="520" height="5"/>
  <g class="kropla"><path d="M300 66c0 0-10 13-10 20a10 10 0 0 0 20 0c0-7-10-20-10-20z"/></g>
  <g class="podpisy">
    <text class="t-blacha" x="44" y="212">BLACHA PODWOZIA</text>
    <text class="t3" x="560" y="214" text-anchor="end">bloker rdzy</text>
    <text class="t4" x="560" y="230" text-anchor="end">inhibitor korozji</text>
    <text class="t5" x="560" y="246" text-anchor="end">środek konserwujący ×5–6</text>
    <text class="t6" x="560" y="262" text-anchor="end">wosk hydrofobowy</text>
  </g>
</svg>'''

def sekcja_auta(p):
    tabs = ''.join(f'<button role="tab" id="tab-{k}" aria-controls="pan-{k}" aria-selected="{"true" if i == 0 else "false"}" data-k="{k}"><span>{t}</span></button>' for i, (k, t, *_) in enumerate(AUTA))
    pans = ''
    for i, (k, t, im, alt, h, txt, lst) in enumerate(AUTA):
        li = ''.join(f'<li>{CHK}{x}</li>' for x in lst)
        pans += f'''<div class="pan{' on' if i == 0 else ''}" role="tabpanel" id="pan-{k}" aria-labelledby="tab-{k}"{' hidden' if i else ''}>
  <figure class="pan-img">{img(p, im, alt, '(max-width: 900px) 100vw, 55vw')}</figure>
  <div class="pan-txt"><h3>{h}</h3><p>{txt}</p><ul class="lista">{li}</ul>
  <a class="btn btn-b" href="{p}kontakt/?auto={k}">Zapytaj o termin – {t.lower()}</a></div>
</div>'''
    return f'''<section class="auta" id="auta">
  <div class="wrap">
    <div class="sek-head"><p class="kicker">Konserwacja pod Twoje auto</p>{lines('Jakie auto', 'do mnie przywozisz?')}
    <p class="lead">Każde auto ma inny problem. Wybierz swoje, a pokażę, od czego zaczynam i co dostajesz w cenie.</p></div>
    <div class="taby" role="tablist" aria-label="Rodzaj auta">{tabs}<i class="taby-pasek" aria-hidden="true"></i></div>
    <div class="pany">{pans}</div>
  </div>
</section>'''

def sekcja_proces():
    kroki = ''.join(f'<li class="krok" data-s="{i + 1}"><span class="krok-n">{i + 1:02d}<small>/{len(KROKI):02d}</small></span><h3>{t}</h3><p>{d}</p></li>' for i, (t, d) in enumerate(KROKI))
    return f'''<section class="proces" id="proces">
  <div class="wrap proces-grid">
    <div class="proces-lewa">
      <div class="proces-sticky">
        <p class="kicker">Kolejność, której się trzymam</p>
        {lines('Siedem etapów.', 'Żadnego na skróty.')}
        <div class="diagram" data-step="0">{diagram()}</div>
        <p class="diagram-pod muted small">Schemat przekroju blachy – tak przybywa warstw na podwoziu Twojego auta.</p>
      </div>
    </div>
    <ol class="kroki">{kroki}</ol>
  </div>
</section>'''

def sekcja_porownanie():
    rows = ''.join(f'<tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in POROWNANIE)
    return f'''<section class="porown">
  <div class="wrap">
    <div class="sek-head"><p class="kicker">Zanim wybierzesz najtańszą ofertę</p>{lines('Czym to się różni', 'od bitexu na kanale?')}</div>
    <div class="tab-wrap rv"><table class="tabela">
      <thead><tr><th></th><th>Typowa „konserwacja”</th><th>W moim Zakładzie</th></tr></thead>
      <tbody>{rows}</tbody></table></div>
  </div>
</section>'''

def sekcja_elementy(p):
    el = ''.join(f'<li>{x}</li>' for x in ELEMENTY)
    return f'''<section class="elementy">
  <div class="stop" aria-hidden="true"><div class="stop-bg" style="background-image:url({full(p, 'podwozie-3')})"></div></div>
  <div class="wrap elementy-in">
    <p class="kicker">W cenie, bez dopłat</p>
    {lines('Zabezpieczam to,', 'za co inni chcą dopłat.')}
    <ul class="el-lista">{el}</ul>
  </div>
</section>'''

def sekcja_list(p):
    return f'''<section class="list">
  <div class="wrap list-grid">
    <figure class="list-img rv-img">{img(p, 'hala-1', 'Hala Zakładu Konserwacji Samochodowej w Chrzanowie', '(max-width: 900px) 100vw, 50vw')}<figcaption>Moja hala w Chrzanowie. Zdjęcia na tej stronie robiłem sam, w Zakładzie.</figcaption></figure>
    <div class="list-txt">
      <p class="kicker">Od właściciela</p>
      {lines('Samochody to moja', 'pasja i praca.')}
      <p>Nie robię na kanale ani na trawie, jak większość – tak nie da się tego zrobić fachowo. Pracuję na hali, na podnośnikach, środkami do użytku profesjonalnego.</p>
      <p>Wprowadziłem coś, czego wcześniej nikt tu nie robił: pokazuję klientowi, czym myję i konserwuję, jakim pistoletem i narzędziami pracuję. A po robocie każdy dostaje na telefon zdjęcia podwozia przed i po – widać stan i moją pracę.</p>
      <p>Cenę podaję zawsze z materiałem, na gotowo. Nie szukam klienta na jeden dzień, tylko na lata.</p>
      <p class="podpis">Witold Poznański</p>
      <ul class="odznaki">
        <li>Członek Polskiego Stowarzyszenia Korozyjnego</li>
        <li>Członek Europejskiej Federacji Korozyjnej</li>
        <li>Status Rzetelna Firma</li>
      </ul>
    </div>
  </div>
</section>'''

def sekcja_obietnice():
    ob = [('Auto zastępcze gratis', 'Zostawiasz swoje, wracasz moim. Nie musisz kombinować, z kim przyjedziesz i jak wrócisz.'),
          ('Zdjęcia na telefon', 'Przed i po. Widzisz stan podwozia i każdy element, który zabezpieczyłem.'),
          ('Gwarancja na piśmie', 'Pisemne zlecenie i gwarancja z wypisanymi środkami, których użyłem.'),
          ('Ok. 3–4 dni', 'Biorę auto od razu, bez tygodniowej kolejki. Schnie bezpiecznie na hali.')]
    li = ''.join(f'<li class="rv"><h3>{t}</h3><p>{d}</p></li>' for t, d in ob)
    return f'<section class="obietnice"><div class="wrap"><ul class="ob-lista">{li}</ul></div></section>'

def sekcja_galeria_skrot(p):
    sel = ['podwozie-1', 'przed-zakladem-1', 'hala-3', 'hilux', 'podwozie-2']
    items = ''.join(f'<a class="g-it rv-img" href="{p}realizacje/">{img(p, n, a, "(max-width: 900px) 70vw, 30vw")}</a>' for n, a, c in GALERIA if n in sel)
    return f'''<section class="gskrot">
  <div class="wrap sek-head sek-head-row"><div><p class="kicker">Realizacje</p>{lines('Moja praca,', 'nie zdjęcia z internetu.')}</div>
  <a class="btn btn-o" href="{p}realizacje/">Wszystkie zdjęcia {ARR}</a></div>
  <div class="g-tasma" data-tasma>{items}</div>
</section>'''

def sekcja_faq():
    it = ''.join(f'<details class="faq-it"><summary>{q}<span class="plus" aria-hidden="true"></span></summary><div class="faq-a"><p>{a}</p></div></details>' for q, a in FAQ)
    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    return f'''<section class="faq" id="faq">
  <div class="wrap faq-grid"><div><p class="kicker">Pytania</p>{lines('Zanim', 'zadzwonisz.')}<p class="lead">Na resztę odpowiem przez telefon: <a href="tel:{TELH}">{TEL}</a>.</p></div>
  <div class="faq-lista">{it}</div></div>
  <script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>
</section>'''

def sekcja_kontakt(p, pelna=False):
    opts = ''.join(f'<option value="{k}">{t}</option>' for k, t, *_ in AUTA)
    return f'''<section class="kontakt" id="kontakt">
  <div class="wrap kontakt-grid">
    <div class="kontakt-l">
      <p class="kicker">Termin ustalamy na bieżąco</p>
      {lines('Umów konserwację', 'swojego auta.', tag='h1' if pelna else 'h2', cls='h1' if pelna else 'h2')}
      <a class="tel-xl" href="tel:{TELH}">{TEL}</a>
      <p>Najlepiej zadzwoń – podam cenę z materiałem i najbliższy wolny termin. Jeśli nie odbieram, jestem pod autem: zostaw numer w formularzu, oddzwonię.</p>
      <p class="adres"><b>Zakład Konserwacji Samochodowej</b><br>{ADR1}, {ADR2} (Kąty)<br>Chrzanów, od strony Libiąża</p>
      <a class="btn btn-o" href="{GMAPS}" target="_blank" rel="noopener">Wyznacz dojazd {ARR}</a>
    </div>
    <form class="form" data-mail="{MAIL}" novalidate>
      <h3>Oddzwonię do Ciebie</h3>
      <label>Twoje auto<select name="auto" id="f-auto">{opts}</select></label>
      <div class="f2"><label>Marka i model<input name="model" placeholder="np. Toyota Yaris Cross" autocomplete="off"></label>
      <label>Rocznik<input name="rok" inputmode="numeric" maxlength="4" placeholder="np. 2024"></label></div>
      <div class="f2"><label>Imię<input name="imie" autocomplete="given-name" required></label>
      <label>Telefon<input name="tel" type="tel" autocomplete="tel" required></label></div>
      <label class="chk-l"><input type="checkbox" name="zastepcze" checked> Potrzebuję auta zastępczego na czas usługi</label>
      <button class="btn btn-b" type="submit">Proszę o telefon</button>
      <p class="form-msg" role="status"></p>
      <p class="muted small">Wysyłając, zgadzasz się na kontakt w sprawie wyceny. Dane trafiają tylko do Zakładu.</p>
    </form>
  </div>
  {'<div class="mapa" id="mapa" data-lat="%s" data-lon="%s"></div>' % (LAT, LON) if pelna else ''}
</section>'''

# ---------- strony ----------
def home():
    p = ''
    hero = f'''<section class="hero">
  <div class="hero-bg">{img(p, 'podwozie-2', 'Podwozie po konserwacji w Zakładzie w Chrzanowie', '100vw', lazy=False)}</div>
  <div class="hero-in wrap">
    <p class="hero-meta">Zakład Konserwacji Samochodowej · Chrzanów</p>
    {lines('Konserwacja podwozia', 'na hali, nie na kanale.', tag='h1', cls='h1')}
    <p class="hero-lead">Nowe auta z salonu, używane i starsze. Środki z 15-letnim okresem ochrony, zdjęcia przed i po na Twój telefon i bezpłatne auto zastępcze na czas usługi.</p>
    <div class="hero-cta"><a class="btn btn-b" href="tel:{TELH}">{TELI}<span>Zadzwoń: {TEL}</span></a><a class="btn btn-g" href="#auta">Wybierz swoje auto</a></div>
  </div>
  <ul class="hero-pas wrap" aria-label="W skrócie">
    <li><b>Auto zastępcze</b>bezpłatnie</li><li><b>Zdjęcia przed i po</b>na telefon</li><li><b>Gwarancja</b>i zlecenie na piśmie</li><li><b>Ok. 3–4 dni</b>bez kolejki</li>
  </ul>
</section>'''
    body = hero + sekcja_auta(p) + sekcja_proces() + sekcja_porownanie() + sekcja_elementy(p) + sekcja_list(p) + sekcja_obietnice() + sekcja_galeria_skrot(p) + sekcja_faq() + sekcja_kontakt(p)
    return head(p, 'Konserwacja podwozia Chrzanów – Zakład Konserwacji Samochodowej, Witold Poznański',
                'Konserwacja podwozia w Chrzanowie: nowe, używane i starsze auta, na hali, środkami z 15-letnim okresem ochrony. Auto zastępcze gratis, zdjęcia przed i po. Tel. 501 199 501.', '', intro=True) \
        + header(p, home=True) + '<main>' + body + '</main>' + footer(p)

def realizacje():
    p = '../'
    filtry = [('wszystkie', 'Wszystkie'), ('podwozia', 'Podwozia'), ('hala', 'Hala'), ('auta', 'Auta klientów')]
    fb = ''.join(f'<button data-f="{k}"{" aria-pressed=\"true\"" if i == 0 else " aria-pressed=\"false\""}>{t}</button>' for i, (k, t) in enumerate(filtry))
    items = ''.join(f'<figure class="m-it rv-img" data-c="{c}"><a href="{full(p, n)}" data-lb>{img(p, n, a, "(max-width: 700px) 100vw, (max-width: 1100px) 50vw, 33vw")}</a><figcaption>{a}</figcaption></figure>' for n, a, c in GALERIA)
    body = f'''<section class="pod-hero wrap"><p class="kicker">Realizacje</p>{lines('Zdjęcia z mojej hali.', 'Bez białych płytek.', tag='h1', cls='h1')}
<p class="lead">Wszystkie zdjęcia zrobiłem sam, w Zakładzie w Chrzanowie. Takie same dostajesz na telefon po konserwacji swojego auta.</p></section>
<section class="wrap galeria"><div class="filtry" role="group" aria-label="Filtr zdjęć">{fb}</div><div class="mur">{items}</div></section>
<div class="lb" hidden><button class="lb-x" aria-label="Zamknij">×</button><img alt=""><p></p></div>''' + sekcja_kontakt(p)
    return head(p, 'Realizacje – konserwacja podwozia Chrzanów | Auto Konserwacja', 'Zdjęcia podwozi po konserwacji i hali Zakładu Konserwacji Samochodowej w Chrzanowie.', 'realizacje/') \
        + header(p) + '<main class="pod">' + body + '</main>' + footer(p)

def kontakt():
    p = '../'
    body = sekcja_kontakt(p, pelna=True) + sekcja_faq()
    return head(p, 'Kontakt i dojazd – konserwacja podwozia Chrzanów | Auto Konserwacja', 'Zakład Konserwacji Samochodowej, ul. Leśna 1a, Chrzanów (od strony Libiąża). Tel. 501 199 501. Auto zastępcze gratis.', 'kontakt/') \
        + header(p) + '<main class="pod">' + body + '</main>' \
        + '<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"><script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>' + footer(p)

def w(path, s):
    full_ = os.path.join(ROOT, path); os.makedirs(os.path.dirname(full_), exist_ok=True)
    open(full_, 'w', encoding='utf-8', newline='\n').write(s)

w('index.html', home())
w('realizacje/index.html', realizacje())
w('kontakt/index.html', kontakt())
w('favicon.svg', '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40"><rect width="40" height="40" rx="6" fill="#121416"/><rect x="7" y="27" width="26" height="4" fill="#ece8df"/><rect x="7" y="21" width="26" height="4" fill="#c4913f"/><rect x="7" y="15" width="26" height="4" fill="#c4913f" opacity=".7"/><rect x="7" y="9" width="26" height="4" fill="#c4913f" opacity=".45"/></svg>')
w('robots.txt', f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
w('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{BASE}{u}</loc></url>' for u in ['', 'realizacje/', 'kontakt/']) + '</urlset>\n')
print('ok')
