#!/usr/bin/env python3
"""Builds the static site for ресторант „Хитър Петър“.

    python3 build.py

Reads data/menu.json and writes every page to dist/ (a full static site you can
upload to any host) and artifact/ (the same pages, with index.html in the form a
claude.ai artifact expects). Edit the menu in data/menu.json, then run it again.
"""
import html, json, os, shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://hitarpetar.net/"  # canonical domain; change if the site moves

# Inquiries are delivered to the restaurant's inbox through Web3Forms (free; key is public-safe).
# Get the key at https://web3forms.com with hitarpetar1@abv.bg, paste it here, run build.py.
# While it is empty, the form falls back to preparing an e-mail the guest sends themselves.
FORM_ENDPOINT = "https://api.web3forms.com/submit"
FORM_KEY = os.environ.get("WEB3FORMS_KEY", "")

B = {
    "name": "Ресторант „Хитър Петър“",
    "short": "Хитър Петър",
    "street": "ул. „Васил Априлов“ 140",
    "city": "Пловдив",
    "phone_tel": "+35932968778",
    "phone_local": "032 968 778",
    "phone_intl": "+359 32 968 778",
    "email": "hitarpetar1@abv.bg",
    "hours": "10:00 – 01:00",
    "maps": "https://www.google.com/maps/place/Hitar+Petar+Restaurant/@42.1574788,24.7297703,17z/data=!4m5!3m4!1s0x14acd1b4fbeb6201:0xfad581c79826b5a5!8m2!3d42.1591569!4d24.7309455",
    "directions": "https://www.google.com/maps/dir/?api=1&destination=42.1591569%2C24.7309455",
    "lat": 42.1591569, "lng": 24.7309455,
    "facebook": "https://www.facebook.com/RestaurantHitarPetar",
    "instagram": "https://www.instagram.com/_hitarpetar/",
}
e = html.escape
MENU = json.load(open(os.path.join(ROOT, "data", "menu.json"), encoding="utf-8"))
COUNT = sum(len(g["items"]) for c in MENU["categories"] for g in c["groups"])

NAV = [("index.html", "Начало"), ("za-nas.html", "За нас"), ("menu.html", "Меню"),
       ("galeria.html", "Галерия"), ("sabitiya.html", "Събития"), ("kontakti.html", "Контакти")]

ICON_PHONE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'
FAVICON = ("data:image/svg+xml," + "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230B0C22'/%3E"
           "%3Ctext x='32' y='43' font-family='Georgia,serif' font-size='30' text-anchor='middle' fill='%23FFB373'%3E%D0%A5%D0%9F%3C/text%3E%3C/svg%3E")


ICON_ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICON_BACK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'
ICON_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M20 20l-4.2-4.2"/></svg>'


_LQ = {}


def lqip(name):
    """A 24px preview of the photo as a data URI; it sits blurred under the real image."""
    if name not in _LQ:
        import base64, io
        from PIL import Image
        im = Image.open(os.path.join(ROOT, "assets", "img", f"{name}-640.webp")).convert("RGB")
        im.thumbnail((24, 24))
        buf = io.BytesIO(); im.save(buf, "WEBP", quality=40)
        _LQ[name] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    return f'style="background-image:url({_LQ[name]})"'


def src(name, big):
    return f"assets/img/{name}-{big}.webp"


def img(name, alt, sizes, big=900, eager=False):
    w = 1400 if big == 1400 else 900
    h = round(w * (1000 / 1500 if big == 1400 else 599 / 900))
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="{src(name, big)}" srcset="assets/img/{name}-640.webp 640w, {src(name, big)} {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}" class="lz" {load}>')


def big_of(name):
    return 1400 if name.startswith("wedding") else 900


def pc(name, alt, cap, sizes="(max-width: 759px) 70vw, 30vw", lb=None, eager=False, cls=""):
    b = big_of(name)
    inner = f'<span class="pc-img lqip" {lqip(name)}>{img(name, alt, sizes, b, eager)}</span><span class="pc-cap">{e(cap)}</span>'
    if lb:
        return (f'<button type="button" class="pc {cls}" data-lb="{lb}" data-full="{src(name, b)}" data-cap="{e(cap)}" '
                f'aria-label="Отворете снимката: {e(alt)}">{inner}</button>')
    return f'<figure class="pc {cls}">{inner}</figure>'


def bulbs(n=18, cls=""):
    # Two sagging spans of wire with bulbs hung along them (plain geometry).
    pts = []
    for span in (0, 1):
        x0 = span * 720
        for i in range(n // 2):
            t = (i + .5) / (n // 2)
            x = x0 + 720 * t
            y = (1 - t) ** 2 * 6 + 2 * (1 - t) * t * 58 + t ** 2 * 6 if span == 0 else (1 - t) ** 2 * 10 + 2 * (1 - t) * t * 58 + t ** 2 * 6
            pts.append((x, y))
    b = "".join(f'<circle class="b" style="--i:{k}" cx="{x:.1f}" cy="{y + 7:.1f}" r="4.2"/>' for k, (x, y) in enumerate(pts))
    return (f'<svg class="bulbs {cls}" viewBox="0 0 1440 72" preserveAspectRatio="xMidYMin slice" aria-hidden="true" focusable="false">'
            f'<path class="wire" d="M0 6 Q360 58 720 10 Q1080 58 1440 6"/>{b}</svg>')


def eur(x):
    return f"{x} €"


def dish(it):
    if it.get("price_eur"):
        price = f'<span class="dish-price">{e(eur(it["price_eur"]))}<small>{e(it["price_bgn"])} лв.</small></span>'
    else:
        price = '<span class="dish-price" title="Цената не е посочена в текущото меню">—</span>'
    desc = f'<p class="dish-desc">{e(it["description"])}</p>' if it.get("description") else ""
    return (f'<li class="dish"><div class="dish-line"><span class="dish-name">{e(it["name"])}</span><span class="dish-dots" aria-hidden="true"></span>{price}</div>'
            f'{desc}<p class="dish-meta">{e(it["portion"])}</p></li>')


def header(active):
    links = "".join(f'<a href="{h}"{" aria-current=" + chr(34) + "page" + chr(34) if h == active else ""}>{e(t)}</a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Към съдържанието</a>
<header class="site-header{' home' if active == 'index.html' else ''}">
  <div class="wrap">
    <a class="brand neon" href="index.html" aria-label="{e(B["name"])}, начало">Хитър Петър</a>
    <nav class="nav" aria-label="Основна навигация">{links}<a class="plaque plaque--small" href="kontakti.html#zapitvane">Резервирайте маса</a></nav>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="drawer">Меню</button>
  </div>
</header>
<div class="drawer" id="drawer" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Навигация">
  <div class="drawer-top"><span class="neon" style="font-size:30px">Хитър Петър</span><button class="drawer-close" type="button">Затворете</button></div>
  <nav aria-label="Мобилна навигация">{links}</nav>
  <div class="drawer-foot">
    <a class="plaque" href="tel:{B["phone_tel"]}">{ICON_PHONE} Обадете се: {B["phone_local"]}</a>
    <p class="muted">{e(B["street"])}, {B["city"]} · всеки ден {B["hours"]}</p>
  </div>
</div>
<nav class="actionbar" aria-label="Бързи действия">
  <a class="plaque" href="tel:{B["phone_tel"]}">{ICON_PHONE} Обадете се</a>
  <a class="plaque plaque--cream" href="menu.html">Менюто</a>
</nav>'''


def footer():
    year = date.today().year
    nav = "".join(f'<a href="{h}">{e(t)}</a>' for h, t in NAV)
    return f'''<footer class="site-footer">
  <div class="wrap">
    <p class="foot-sign neon neon--dim" aria-hidden="true">Хитър Петър</p>
    <div class="foot-grid">
      <div><a class="foot-logo" href="index.html"><img src="assets/img/logo.png" width="280" height="140" alt="Логото на ресторант „Хитър Петър“: Хитър Петър, яхнал магаре" loading="lazy"></a>
        <p class="muted">Ресторант с лятна градина, зала и собствен паркинг в Пловдив.</p></div>
      <div><h2>Страници</h2>{nav}<a href="poveritelnost.html">Поверителност</a></div>
      <div><h2>Контакти</h2>
        <a href="{B["maps"]}" target="_blank" rel="noopener">{e(B["street"])}, {B["city"]}</a>
        <a href="tel:{B["phone_tel"]}" class="num">{B["phone_intl"]}</a>
        <a href="mailto:{B["email"]}">{B["email"]}</a></div>
      <div><h2>Всеки ден</h2>
        <p class="num">{B["hours"]}</p>
        <a href="{B["facebook"]}" target="_blank" rel="noopener">Facebook · обедно меню</a>
        <a href="{B["instagram"]}" target="_blank" rel="noopener">Instagram</a></div>
    </div>
    <div class="foot-legal"><span>© {year} {e(B["name"])}</span><span>Снимки: ресторант „Хитър Петър“</span></div>
  </div>
</footer>
<div class="callbox" id="callbox" hidden role="dialog" aria-modal="true" aria-labelledby="callbox-t">
  <div class="callbox-card">
    <button class="callbox-x" type="button" aria-label="Затворете"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
    <p class="callbox-t" id="callbox-t">Обадете ни се</p>
    <p class="callbox-n neon num">{B["phone_local"]}</p>
    <p class="callbox-i num">{B["phone_intl"]} · всеки ден {B["hours"]}</p>
    <p class="callbox-note">В прегледа на Claude телефонът не може да набира директно. На истинския сайт бутонът „Обадете се“ звъни веднага.</p>
    <div class="callbox-a"><a class="plaque callbox-dial" href="tel:{B["phone_tel"]}" data-native>{ICON_PHONE} Обадете се</a><button class="plaque plaque--cream" type="button" data-copy-text="{B["phone_intl"]}">Копирайте номера</button></div>
  </div>
</div>
<div class="lb" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Снимки">
  <div class="lb-top"><span class="lb-count num" aria-live="polite"></span><button class="lb-close" type="button">Затворете</button></div>
  <div class="lb-stage"><button class="round lb-prev" type="button" aria-label="Предишна снимка">{ICON_BACK}</button><button class="round lb-next" type="button" aria-label="Следваща снимка">{ICON_ARROW}</button></div>
  <div class="lb-bottom"><span class="lb-cap"></span><span class="muted">← → или плъзнете</span></div>
</div>'''


def schema():
    data = {
        "@context": "https://schema.org", "@type": "Restaurant",
        "name": "Ресторант „Хитър Петър“", "alternateName": "Hitar Petar Restaurant",
        "url": SITE_URL, "telephone": B["phone_intl"], "email": B["email"],
        "image": SITE_URL + "assets/img/facade-900.webp", "logo": SITE_URL + "assets/img/logo.png",
        "address": {"@type": "PostalAddress", "streetAddress": "ул. „Васил Априлов“ 140", "addressLocality": "Пловдив", "addressCountry": "BG"},
        "geo": {"@type": "GeoCoordinates", "latitude": B["lat"], "longitude": B["lng"]},
        "hasMap": B["maps"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], "opens": "10:00", "closes": "01:00"}],
        "hasMenu": SITE_URL + "menu.html", "acceptsReservations": "True", "currenciesAccepted": "EUR",
        "sameAs": [B["facebook"], B["instagram"]],
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def head(title, desc, path, extra="", artifact=False):
    url = SITE_URL + ("" if path == "index.html" else path)
    return f'''<title>{e(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:locale" content="bg_BG">
<meta property="og:site_name" content="Ресторант „Хитър Петър“">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE_URL}assets/img/garden-900.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B0C22">
<link rel="icon" href="{FAVICON}">
<link rel="preload" href="assets/fonts/marck-cyr.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/oranienbaum-cyr.woff2" as="font" type="font/woff2" crossorigin>
{GFONTS if artifact else ""}<link rel="stylesheet" href="assets/css/site.css">
{extra}'''


GFONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Marck+Script&family=Oranienbaum&family=Onest:wght@400;500&display=swap">\n'


def page(path, title, desc, body, extra_head="", bare=False, artifact=False):
    h = head(title, desc, path, extra_head, artifact)
    content = f'{header(path)}\n<main id="main">\n{body}\n</main>\n{footer()}\n<script src="assets/js/site.js" defer></script>'
    if bare:
        return h + "\n" + content + "\n"
    return (f'<!doctype html>\n<html lang="bg">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">\n{h}</head>\n<body>\n{content}\n</body>\n</html>\n')


def preview_items(c, n=6):
    items = [it for g in c["groups"] for it in g["items"]]
    feat = [it for it in items if it.get("featured")]
    rest = [it for it in items if not it.get("featured") and it.get("price_eur")]
    return (feat + rest)[:n]




# ---------------------------------------------------------------- Home
def home():
    cats = MENU["categories"]
    tabs, panels = [], []
    for i, c in enumerate(cats):
        tabs.append(f'<button class="tab" type="button" role="tab" id="tab-{c["id"]}" aria-controls="panel-{c["id"]}" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}">{e(c["title"])}</button>')
        panels.append(f'<div class="panel" role="tabpanel" id="panel-{c["id"]}" aria-labelledby="tab-{c["id"]}"{"" if i == 0 else " hidden"}>'
                      f'<ul class="dishes">{"".join(dish(it) for it in preview_items(c))}</ul></div>')
    rail = [("hall-wide", "Основната зала с полилеи и бели завеси", "Залата"),
            ("hall-lamps", "Ъгъл на залата с висящи лампи", "Вечер в залата"),
            ("terrace", "Терасата пред входа, зад палмите", "Терасата"),
            ("table-set", "Маса с карирана покривка и лавандула", "Масата е готова"),
            ("hall-columns", "Залата с колони и арки", "Залата"),
            ("facade-windows", "Покритата тераса с цветя", "Лятото"),
            ("detail-bread", "Хлебни пръчици в кошница", "Хлябът"),
            ("hall-tables", "Маси, подредени за гости", "За компания")]
    rail_html = "".join(pc(n, a, c, "(max-width: 759px) 70vw, 26vw", lb="hall") for n, a, c in rail)
    return f'''
<section class="hero" aria-labelledby="hero-title">
  {bulbs(18)}
  <div class="hero-stage wrap">
    {pc("terrace", "Терасата и входът, скрити зад палми", "Терасата", "18vw", eager=True, cls="float f1")}
    {pc("hall-evening", "Залата вечер с бели столове и карирани покривки", "Залата вечер", "18vw", eager=True, cls="float f2")}
    {pc("wedding-table", "Масата на младоженците с цветна украса", "Сватба", "18vw", eager=True, cls="float f3")}
    {pc("garden", "Лятната градина с палми и зелени чадъри", "Градината", "18vw", eager=True, cls="float f4")}
    <div class="sign-glow">
      <svg class="sign-svg" viewBox="0 0 1000 430" role="img" aria-label="Хитър Петър">
        <text class="tube" x="40" y="200">Хитър</text><text class="tube" x="250" y="400">Петър</text>
        <text class="draw l1" x="40" y="200">Хитър</text><text class="draw l2" x="250" y="400">Петър</text>
      </svg>
    </div>
    <div class="hero-lede">
      <h1 id="hero-title">Вкус, който събира. Атмосфера, която остава.</h1>
      <p class="hero-sub lead">Ресторант с лятна градина в Пловдив, на {e(B["street"])}. Скара, риба, агнешко и над 100 вида вино.</p>
      <div class="hero-actions">
        <a class="plaque" href="kontakti.html#zapitvane">Резервирайте маса</a>
        <a class="plaque plaque--cream" href="#menu">Разгледайте менюто</a>
      </div>
      <p class="hero-status"><span class="open-now" data-open-now>Всеки ден {B["hours"]}</span><a href="tel:{B["phone_tel"]}" class="num">{B["phone_intl"]}</a><span>Собствен паркинг</span></p>
    </div>
    <div class="hero-floats-m">
      {pc("terrace", "Терасата и входът, скрити зад палми", "Терасата", "45vw")}
      {pc("hall-evening", "Залата вечер", "Залата вечер", "45vw")}
    </div>
  </div>
</section>

<section class="garden" aria-labelledby="garden-title">
  <div class="wrap garden-grid">
    <div class="garden-copy reveal">
      <h2 id="garden-title" class="h-l">Зад стена <span class="neon neon--dim">от зеленина</span></h2>
      <blockquote>„Само на няколко крачки от шумната улица може да откриете пространството на неограничените желания.“</blockquote>
      <ul class="ticks"><li>Лятна градина със 120 места</li><li>Безплатен интернет и тиха музика за бизнес обяд</li><li>Петък и събота вие поръчвате музиката</li><li>Собствен паркинг</li></ul>
    </div>
    <div class="garden-pics reveal">
      {pc("garden", "Лятната градина с палми, зелени чадъри и маси под дърветата", "Лятната градина", "(max-width: 959px) 46vw, 32vw", lb="garden")}
      {pc("facade-windows", "Покритата тераса с цветя по прозорците", "Под стрехата", "(max-width: 959px) 46vw, 28vw", lb="garden")}
    </div>
  </div>
</section>

<section class="table" id="menu" aria-labelledby="menu-title">
  <div class="wrap">
    <div class="table-head">
      <h2 id="menu-title" class="h-l">Какво ще поръчате?</h2>
      <p class="lead">{COUNT} позиции: салати, предястия, скара, риба, телешко, агнешко, десерти и напитки. Цените са в евро и в лева.</p>
    </div>
    <div class="menu-card paper">
      <div class="menu-card-top"><span class="t">Меню</span><span class="s">ресторант „Хитър Петър“</span></div>
      <div class="tabs" role="tablist" aria-label="Категории в менюто">{"".join(tabs)}</div>
      {"".join(panels)}
      <div class="panel-foot"><span class="note">Обедното меню се сменя всеки ден и е във Facebook.</span><a class="plaque" href="menu.html">Цялото меню · {COUNT} позиции</a></div>
    </div>
  </div>
</section>

<section class="line-sec" aria-labelledby="hall-title">
  <div class="wrap line-head">
    <h2 id="hall-title" class="h-l">Залата и терасата</h2>
    <div class="line-ctrl"><button class="round" type="button" data-rail-prev aria-label="Предишни снимки">{ICON_BACK}</button><button class="round" type="button" data-rail-next aria-label="Следващи снимки">{ICON_ARROW}</button></div>
  </div>
  <div class="rail-wrap">{bulbs(24)}<div class="rail" aria-label="Снимки на залата и терасата">{rail_html}</div></div>
  <div class="wrap"><a class="link" href="galeria.html">Всички 23 снимки <span class="arr">→</span></a></div>
</section>

<section class="feast" data-scene="view" aria-labelledby="feast-title">
  <div class="feast-photo lqip" {lqip("wedding-chairs")}>{img("wedding-chairs", "Залата, подредена за сватба, със столове с праскови панделки и цветя", "100vw", 1400)}</div>
  <div class="wrap">
    <div class="feast-copy">
      <h2 id="feast-title" class="neon neon--dim">Сватби и тържества</h2>
      <p class="statement">Празникът ви, подреден до последната маса</p>
      <p class="lead muted">170 места в залата и 120 в градината. Украса според повода, оркестър или DJ, големи маси, богато меню и професионално обслужване.</p>
      <ul class="occasions"><li>Сватби</li><li>Рождени дни</li><li>Тържества</li><li>Бизнес обеди</li></ul>
      <div class="hero-actions" style="margin-top:4px"><a class="plaque" href="kontakti.html#sabitie">Организирайте вашето събитие</a><a class="plaque plaque--ghost" href="sabitiya.html">Вижте сватбите</a></div>
    </div>
    <div class="feast-cards">
      {pc("wedding-flowers", "Рози и свещи върху дантелена покривка", "Цветята", "26vw")}
      {pc("wedding-table", "Масата на младоженците", "Масата на младоженците", "26vw")}
    </div>
  </div>
</section>

<section class="visit" id="rezervacii" aria-labelledby="visit-title">
  <div class="wrap visit-grid">
    <div class="visit-photo">
      {pc("facade", "Фасадата с табелата „Хитър Петър“ и живия плет", "Тук сме", "(max-width: 1080px) 90vw, 38vw")}
      <p>Търсете червения покрив и табелата зад живия плет. Паркингът е наш, а градината е зад вратата.</p>
    </div>
    <div class="visit-side">
      <h2 id="visit-title" class="vh">Резервации и адрес</h2>
      <a class="phone-neon neon num" href="tel:{B["phone_tel"]}" aria-label="Резервации по телефона: {B["phone_intl"]}">{B["phone_local"]}</a>
      <div class="visit-row"><span class="open-now" data-open-now>Всеки ден {B["hours"]}</span><span class="muted num">Понеделник – неделя, {B["hours"]}</span></div>
      <div class="visit-actions"><a class="plaque" href="kontakti.html#zapitvane">Резервирайте маса</a><a class="plaque plaque--ghost" href="kontakti.html#zapitvane">Изпратете запитване</a></div>
      <a class="street" href="{B["directions"]}" target="_blank" rel="noopener">
        <span class="s2">ул. „Васил Априлов“ 140</span>
        <span class="s3">Пловдив · Упътване {ICON_ARROW}</span>
      </a>
    </div>
  </div>
</section>'''


# ---------------------------------------------------------------- Menu
def menu_page():
    navl = "".join(f'<a href="#{c["id"]}">{e(c["title"])}</a>' for c in MENU["categories"])
    sheets = []
    for c in MENU["categories"]:
        n = sum(len(g["items"]) for g in c["groups"])
        groups = "".join(f'<div class="menu-group">{"<h3>" + e(g["title"]) + "</h3>" if g["title"] else ""}<ul class="dishes">{"".join(dish(it) for it in g["items"])}</ul></div>' for g in c["groups"])
        sheets.append(f'<section class="menu-cat menu-card paper" id="{c["id"]}" aria-labelledby="h-{c["id"]}"><div class="menu-cat-head"><h2 id="h-{c["id"]}">{e(c["title"])}</h2><span class="script">{n} позиции</span></div>{groups}</section>')
    return f'''
<div class="page-head wrap">
  <h1 class="neon switch-on">Менюто</h1>
  <p class="statement">Всичко, което готвим</p>
  <p class="lead">{COUNT} позиции с грамаж и цена в евро и лева. Обедното меню се сменя всеки ден и се публикува във <a href="{B["facebook"]}" target="_blank" rel="noopener">Facebook</a>.</p>
</div>
<div class="menu-bar"><div class="wrap"><nav class="menu-nav" aria-label="Категории">{navl}</nav>
  <div class="menu-search">{ICON_SEARCH}<label class="vh" for="menu-q">Търсете в менюто</label><input id="menu-q" type="search" placeholder="Търсете ястие: сьомга, скара…" autocomplete="off"></div></div></div>
<div class="wrap menu-page">
  <div class="menu-sheets">{"".join(sheets)}</div>
  <p class="menu-empty" hidden>Няма ястие с такова име. Опитайте „сирене“, „агнешко“ или „ракия“.</p>
  <p class="menu-note" style="margin-top:40px">„—“ означава, че цената не е посочена в текущото меню; попитайте сервитьора. Резервации: <a href="tel:{B["phone_tel"]}">{B["phone_intl"]}</a>.</p>
</div>'''


# ---------------------------------------------------------------- About
def about():
    return f'''
<div class="page-head wrap">
  <h1 class="neon switch-on">За нас</h1>
  <p class="statement">Пространството на неограничените желания</p>
  <p class="lead">Ресторант на {e(B["street"])} в Пловдив: зала, лятна градина и собствен паркинг. Всеки ден от 10:00 до 01:00.</p>
</div>
<div class="wrap collage">
  {pc("garden", "Лятната градина с палми и зелени чадъри", "Градината", "(max-width: 759px) 90vw, 40vw", lb="about")}
  {pc("facade-windows", "Покритата тераса с цветя", "Под стрехата", "(max-width: 759px) 90vw, 32vw", lb="about")}
  {pc("detail-box", "Дървени сандъчета със слама и зелени растения", "Детайли", "(max-width: 759px) 90vw, 24vw", lb="about")}
</div>
<div class="wrap">
  <section class="split">
    <div class="media">{pc("hall-evening", "Залата вечер", "Залата вечер", "(max-width: 859px) 90vw, 46vw", lb="about")}</div>
    <div class="copy">
      <h2 class="h-m">Зад стена от зеленина</h2>
      <p class="lead">Само на няколко крачки от шумната улица, зад стена от зеленина, може да откриете пространството на неограничените желания. Желания, които са заповед за персонала и собствениците.</p>
      <p>Заведението посреща с интерес всяка идея, всяко желание или хрумване. Всеки петък и събота можете сами да поръчате музиката.</p>
    </div>
  </section>
  <section class="split rev">
    <div class="media">{pc("terrace", "Терасата с палми пред входа", "Лятната градина", "(max-width: 859px) 90vw, 46vw", lb="about")}</div>
    <div class="copy">
      <h2 class="h-m">Градина за топлите месеци</h2>
      <p class="lead">Лятната градина е място за разпускане през топлите месеци.</p>
      <ul class="ticks"><li>120 места на открито</li><li>Безплатен интернет, тиха музика и спокойствие за бизнес обяд или среща</li><li>Собствен паркинг</li></ul>
    </div>
  </section>
  <section class="split">
    <div class="media">{pc("hall-tables", "Маси в залата, подредени за гости", "Кухнята", "(max-width: 859px) 90vw, 46vw", lb="about")}</div>
    <div class="copy">
      <h2 class="h-m">Пилешко, свинско, телешко, агнешко</h2>
      <p>Пилешки, свински и телешки ястия, агнешки специалитети и авторски рецепти. Колекция от над 100 вида бяло и червено вино. Всеки ден различно обедно меню.</p>
      <div class="page-head-actions" style="margin-top:4px"><a class="plaque" href="menu.html">Разгледайте менюто</a><a class="plaque plaque--ghost" href="{B["facebook"]}" target="_blank" rel="noopener">Обедното меню</a></div>
    </div>
  </section>
  <section style="padding-block:clamp(48px,6vw,96px) clamp(96px,10vw,160px)">
    <div class="figures"><div><b class="num">170</b><span>места в залата</span></div><div><b class="num">120</b><span>места в градината</span></div><div><b class="num">100+</b><span>вида вино</span></div></div>
  </section>
</div>'''


# ---------------------------------------------------------------- Gallery
GAL = [
    ("Залата", "zala", [("hall-wide", "Основната зала с полилеи", "Залата"), ("hall-evening", "Залата вечер", "Вечер"), ("hall-lamps", "Ъгъл с висящи лампи", "Лампите"),
                       ("hall-columns", "Залата с колони и арки", "Колоните"), ("hall-tables", "Маси, подредени за гости", "Масите"), ("table-set", "Маса с лавандула", "Лавандула"),
                       ("detail-bread", "Хлебни пръчици в кошница", "Хлябът"), ("detail-box", "Дървени сандъчета със слама", "Детайли")]),
    ("Градината и терасата", "gradina", [("garden", "Лятната градина с палми и чадъри", "Градината"), ("terrace", "Терасата пред входа", "Терасата"), ("facade-windows", "Покритата тераса", "Под стрехата"), ("facade", "Фасадата с табелата", "Входът")]),
    ("Сватби и тържества", "svatbi", [("wedding-table", "Масата на младоженците", "Младоженците"), ("wedding-flowers", "Рози и свещи", "Цветята"), ("wedding-hall", "Залата, подредена за сватба", "Залата"),
                                     ("wedding-setting", "Подредена маса с номер", "Маса 9"), ("wedding-centre", "Цветна украса в центъра на залата", "Украсата"), ("wedding-window", "Маси до прозорците", "До прозорците"),
                                     ("wedding-chairs", "Столове с панделки", "Панделките"), ("wedding-booths", "Сепарета с бели калъфи", "Сепаретата"), ("wedding-long", "Дълга маса за гостите", "Гостите"),
                                     ("wedding-lounge", "Кът със сепаре и светлини", "Светлините"), ("wedding-bottles", "Подредени маси с напитки", "Наздраве")]),
]


def gallery():
    secs = "".join(
        f'<section class="gal-sec" id="{gid}" aria-labelledby="g-{gid}"><h2 id="g-{gid}" class="h-m">{e(t)}</h2><div class="gal">'
        + "".join(pc(n, a, c, "(max-width: 759px) 90vw, 30vw", lb="gal") for n, a, c in pics) + "</div></section>"
        for t, gid, pics in GAL)
    return f'''
<div class="page-head wrap">
  <h1 class="neon switch-on">Галерия</h1>
  <p class="statement">23 снимки от ресторанта</p>
  <p class="lead">Залата, лятната градина и сватби, подредени в „Хитър Петър“. Натиснете снимка, за да я разгледате на цял екран.</p>
</div>
<div class="wrap">{secs}</div>'''


# ---------------------------------------------------------------- Events
def events():
    return f'''
<div class="page-head wrap">
  <h1 class="neon switch-on">Събития</h1>
  <p class="statement">Сватби, рождени дни и тържества</p>
  <p class="lead">„Хитър Петър“ е известен с организирането на сватби, рождени дни и други тържества. Залата побира 170 гости, а лятната градина още 120.</p>
  <div class="page-head-actions"><a class="plaque" href="kontakti.html#sabitie">Организирайте вашето събитие</a><a class="plaque plaque--ghost" href="tel:{B["phone_tel"]}">{ICON_PHONE} {B["phone_local"]}</a></div>
</div>
<div class="big-photo lqip" {lqip("wedding-hall")}>{img("wedding-hall", "Залата, подредена за сватба", "100vw", 1400)}</div>
<div class="wrap">
  <section class="split">
    <div class="media">{pc("wedding-table", "Масата на младоженците с цветна арка", "Масата на младоженците", "(max-width: 859px) 90vw, 46vw", lb="ev")}</div>
    <div class="copy">
      <h2 class="h-m">Какво осигуряваме</h2>
      <ul class="ticks"><li>170 места в залата и 120 в градината</li><li>Големи маси и богато меню</li><li>Професионално обслужване</li><li>Украса според повода</li><li>Оркестър или DJ</li><li>Собствен паркинг за гостите</li></ul>
    </div>
  </section>
  <section class="split rev">
    <div class="media">{pc("wedding-centre", "Цветна украса в центъра на залата", "Украсата", "(max-width: 859px) 90vw, 46vw", lb="ev")}</div>
    <div class="copy">
      <h2 class="h-m">Предпочитано място от пловдивчани</h2>
      <p class="lead">Подходящ за различни поводи, с удобно местоположение и добра кухня. Много младоженци са празнували сватбите си тук със специални програми.</p>
      <ul class="occasions"><li>Сватби</li><li>Рождени дни</li><li>Тържества и празници</li><li>Бизнес обеди и срещи</li></ul>
    </div>
  </section>
</div>
<section class="line-sec" aria-labelledby="ev-rail">
  <div class="wrap line-head"><h2 id="ev-rail" class="h-l">Подредени сватби</h2>
    <div class="line-ctrl"><button class="round" type="button" data-rail-prev aria-label="Предишни снимки">{ICON_BACK}</button><button class="round" type="button" data-rail-next aria-label="Следващи снимки">{ICON_ARROW}</button></div></div>
  <div class="rail-wrap">{bulbs(24)}<div class="rail">{"".join(pc(n, a, c, "(max-width: 759px) 70vw, 26vw", lb="ev") for n, a, c in GAL[2][2])}</div></div>
</section>
<section class="visit"><div class="wrap" style="display:grid;gap:28px;justify-items:start">
  <p class="script neon neon--dim" style="font-size:clamp(40px,3vw + 20px,72px)">Разкажете ни за празника</p>
  <p class="lead muted" style="max-width:34em">Напишете датата, броя на гостите и повода. Ще се свържем с вас, за да уточним менюто, украсата и музиката.</p>
  <div class="page-head-actions" style="margin:0"><a class="plaque" href="kontakti.html#sabitie">Изпратете запитване</a><a class="plaque plaque--ghost" href="tel:{B["phone_tel"]}">Обадете се: {B["phone_local"]}</a></div>
</div></section>'''


# ---------------------------------------------------------------- Contact
def contact():
    return f'''
<div class="page-head wrap">
  <h1 class="neon switch-on">Контакти</h1>
  <p class="statement">Резервирайте маса</p>
  <p class="lead">Най-бързо е по телефона. За събития и големи групи попълнете запитването и го изпратете по имейл.</p>
</div>
<div class="wrap contact-grid" id="zapitvane">
  <div class="contact-side">
    <a class="phone-neon neon num" href="tel:{B["phone_tel"]}">{B["phone_local"]}</a>
    <div class="visit-actions"><a class="plaque" href="tel:{B["phone_tel"]}">{ICON_PHONE} Обадете се</a><button class="plaque plaque--ghost" type="button" data-copy-text="{B["phone_intl"]}">Копирайте номера</button></div>
    <div class="hours"><span class="open-now" data-open-now>Всеки ден {B["hours"]}</span><a href="mailto:{B["email"]}" class="muted">{B["email"]}</a><span class="muted"><a href="{B["facebook"]}" target="_blank" rel="noopener">Facebook</a> · <a href="{B["instagram"]}" target="_blank" rel="noopener">Instagram</a></span></div>
    <a class="street" href="{B["directions"]}" target="_blank" rel="noopener"><span class="s2" style="font-size:clamp(40px,3vw + 14px,64px)">ул. „Васил Априлов“ 140</span><span class="s3">Пловдив · Упътване {ICON_ARROW}</span></a>
  </div>
  <div class="pad paper" id="sabitie">
    <div class="pad-head"><h2>Запитване</h2><p id="inq-help">{"Запитването отива директно при ресторанта. Това още не е потвърдена резервация: мястото е запазено, след като ресторантът ви се обади." if FORM_KEY else "Това не е потвърдена резервация. Формулярът подготвя имейл до ресторанта; мястото е запазено, след като ресторантът ви потвърди."}</p></div>
    <form class="inq" id="inquiry" novalidate data-email="{B["email"]}"{(' data-endpoint="' + FORM_ENDPOINT + '" data-key="' + FORM_KEY + '"') if FORM_KEY else ""} aria-describedby="inq-help">
      <fieldset class="fld full"><legend>За какво питате</legend>
        <div class="seg"><input type="radio" name="type" id="t-table" value="Маса" checked><label for="t-table">Маса</label><input type="radio" name="type" id="t-event" value="Събитие"><label for="t-event">Събитие</label></div></fieldset>
      <div class="fld"><label for="f-date">Дата</label><input class="field" id="f-date" inputmode="numeric" placeholder="ДД.ММ.ГГГГ" autocomplete="off"><span class="err" id="f-date-err" aria-live="polite"></span></div>
      <div class="fld"><label for="f-time">Час <span class="opt">(по желание)</span></label><input class="field" id="f-time" inputmode="numeric" placeholder="19:30" autocomplete="off"><span class="err" id="f-time-err" aria-live="polite"></span></div>
      <div class="fld"><label for="f-guests">Брой гости</label><input class="field" id="f-guests" type="number" min="1" max="300" inputmode="numeric"><span class="err" id="f-guests-err" aria-live="polite"></span></div>
      <div class="fld"><label for="f-name">Име</label><input class="field" id="f-name" autocomplete="name"><span class="err" id="f-name-err" aria-live="polite"></span></div>
      <div class="fld"><label for="f-phone">Телефон</label><input class="field" id="f-phone" type="tel" autocomplete="tel"><span class="err" id="f-phone-err" aria-live="polite"></span></div>
      <div class="fld"><label for="f-email">Имейл <span class="opt">(по желание)</span></label><input class="field" id="f-email" type="email" autocomplete="email"><span class="err" id="f-email-err" aria-live="polite"></span></div>
      <div class="fld full"><label for="f-msg">Бележка <span class="opt">(по желание)</span></label><textarea class="field" id="f-msg" maxlength="1200" placeholder="Повод, място в залата или градината, специални желания"></textarea></div>
      <div class="hp" aria-hidden="true"><label for="f-web">Уебсайт</label><input id="f-web" name="botcheck" tabindex="-1" autocomplete="off"></div>
      <div class="full form-foot"><button class="plaque" type="submit">{"Изпратете запитването" if FORM_KEY else "Подгответе запитването"}</button><small>Нищо не се съхранява на сайта. <a href="poveritelnost.html">Поверителност</a></small></div>
    </form>
    <div class="inq-out" id="inq-out" hidden tabindex="-1" aria-live="polite">
      <h3>Готово за изпращане</h3>
      <p>Изпратете го от своя имейл до <strong>{B["email"]}</strong> или се обадете на <a href="tel:{B["phone_tel"]}">{B["phone_intl"]}</a>. Ще ви потвърдим дали има места.</p>
      <pre></pre>
      <div class="row"><a class="plaque" data-mailto href="mailto:{B["email"]}">Отворете в имейл</a><button class="plaque plaque--cream" type="button" data-copy style="box-shadow:inset 0 0 0 1.5px rgba(34,28,22,.4)">Копирайте текста</button></div>
      <p class="status-line" aria-live="polite"></p>
    </div>
    <div class="inq-out" id="inq-sent" hidden tabindex="-1" aria-live="polite">
      <h3>Запитването е изпратено</h3>
      <p>Получихме го. Ресторантът ще ви се обади на посочения телефон, за да потвърди дали има места. Ако е спешно, обадете се на <a href="tel:{B["phone_tel"]}">{B["phone_intl"]}</a>.</p>
    </div>
  </div>
</div>'''


def privacy():
    return f'''
<div class="page-head wrap">
  <h1 class="neon switch-on">Поверителност</h1>
  <p class="statement">Поверителност и бисквитки</p>
</div>
<div class="wrap"><div class="prose">
  <p>Този сайт не събира и не съхранява лични данни и не използва бисквитки за проследяване или реклама.</p>
  <h2>Формулярът за запитване</h2>
  <p>Формулярът на страницата „Контакти“ не изпраща данни към сървър. Той подготвя текст, който изпращате сами от своя имейл до {B["email"]} или копирате. Ресторантът получава само това, което изпратите.</p>
  <h2>Шрифтове и външни връзки</h2>
  <p>Шрифтовете се зареждат от сайта, а при нужда и от Google Fonts. Връзките към Google Maps, Facebook и Instagram водят към външни сайтове със собствени правила за поверителност.</p>
  <h2>Въпроси</h2>
  <p>Пишете на <a href="mailto:{B["email"]}">{B["email"]}</a> или се обадете на <a href="tel:{B["phone_tel"]}">{B["phone_intl"]}</a>.</p>
</div></div>'''


PAGES = [
    ("index.html", "Ресторант „Хитър Петър“, Пловдив", "Ресторант с лятна градина на ул. „Васил Априлов“ 140 в Пловдив. Скара, риба, агнешко, над 100 вида вино. Сватби и тържества. Всеки ден 10:00–01:00.", home, True),
    ("menu.html", "Меню | Ресторант „Хитър Петър“, Пловдив", f"Пълното меню на ресторант „Хитър Петър“: {COUNT} позиции с грамажи и цени в евро и лева. Салати, скара, риба, агнешко, десерти и напитки.", menu_page, False),
    ("za-nas.html", "За нас | Ресторант „Хитър Петър“, Пловдив", "Ресторант зад стена от зеленина в Пловдив: зала със 170 места, лятна градина със 120 места, собствен паркинг и над 100 вида вино.", about, False),
    ("galeria.html", "Галерия | Ресторант „Хитър Петър“, Пловдив", "Снимки на залата, лятната градина и сватбите в ресторант „Хитър Петър“ в Пловдив.", gallery, False),
    ("sabitiya.html", "Сватби и тържества | Ресторант „Хитър Петър“, Пловдив", "Сватби, рождени дни и тържества в Пловдив: 170 места в залата, 120 в градината, украса, оркестър или DJ.", events, False),
    ("kontakti.html", "Контакти и резервации | Ресторант „Хитър Петър“, Пловдив", "Резервации на 032 968 778. Ул. „Васил Априлов“ 140, Пловдив. Всеки ден 10:00–01:00.", contact, False),
    ("poveritelnost.html", "Поверителност | Ресторант „Хитър Петър“", "Как сайтът на ресторант „Хитър Петър“ се отнася към личните данни.", privacy, False),
]


CSP = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; "
       "connect-src 'self' https://api.web3forms.com; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests")
HEADERS = [
    ("Content-Security-Policy", CSP),
    ("Strict-Transport-Security", "max-age=31536000; includeSubDomains"),
    ("X-Content-Type-Options", "nosniff"),
    ("X-Frame-Options", "DENY"),
    ("Referrer-Policy", "strict-origin-when-cross-origin"),
    ("Permissions-Policy", "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()"),
    ("Cross-Origin-Opener-Policy", "same-origin"),
]


def write_security(d):
    """Security headers for the hosting: .htaccess (Apache, most Bulgarian shared hosting) and _headers (Netlify, Cloudflare Pages)."""
    ht = ["# Security headers and HTTPS for ресторант „Хитър Петър“", "Options -Indexes", "ServerSignature Off", "",
          "<IfModule mod_rewrite.c>", "RewriteEngine On", "RewriteCond %{HTTPS} !=on", "RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]",
          "RewriteRule (^|/)\\.(?!well-known/) - [F]", "</IfModule>", "", "<IfModule mod_headers.c>"]
    ht += [f'Header always set {k} "{v}"' for k, v in HEADERS]
    ht += ["Header always unset X-Powered-By", "</IfModule>", "",
           "<IfModule mod_expires.c>", "ExpiresActive On", 'ExpiresByType image/webp "access plus 1 year"', 'ExpiresByType font/woff2 "access plus 1 year"',
           'ExpiresByType text/css "access plus 1 week"', 'ExpiresByType application/javascript "access plus 1 week"', "</IfModule>", ""]
    open(os.path.join(d, ".htaccess"), "w").write("\n".join(ht))
    open(os.path.join(d, "_headers"), "w").write("/*\n" + "".join(f"  {k}: {v}\n" for k, v in HEADERS))
    wk = os.path.join(d, ".well-known"); os.makedirs(wk, exist_ok=True)
    open(os.path.join(wk, "security.txt"), "w").write(f"Contact: mailto:{B['email']}\nPreferred-Languages: bg, en\nExpires: {date.today().year + 1}-12-31T00:00:00.000Z\n")


def main():
    for out in ("dist", "artifact"):
        d = os.path.join(ROOT, out)
        if os.path.exists(d):
            shutil.rmtree(d)
        shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(d, "assets"))
    for path, title, desc, fn, is_home in PAGES:
        body = fn()
        extra = schema() if is_home else ""
        full = page(path, title, desc, body, extra)
        open(os.path.join(ROOT, "dist", path), "w", encoding="utf-8").write(full)
        art = page(path, title, desc, body, extra, bare=is_home, artifact=True)
        open(os.path.join(ROOT, "artifact", path), "w", encoding="utf-8").write(art)
    urls = "".join(f"<url><loc>{SITE_URL}{'' if p == 'index.html' else p}</loc></url>" for p, *_ in PAGES)
    sm = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'
    rb = f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n"
    write_security(os.path.join(ROOT, "dist"))
    for out in ("dist", "artifact"):
        open(os.path.join(ROOT, out, "sitemap.xml"), "w").write(sm)
        open(os.path.join(ROOT, out, "robots.txt"), "w").write(rb)
    print(f"Built {len(PAGES)} pages, {COUNT} menu items.")


if __name__ == "__main__":
    main()
