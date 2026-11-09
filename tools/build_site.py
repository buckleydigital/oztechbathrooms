#!/usr/bin/env python3
"""Generates the static OZTECH Bathrooms site pages into the repo root.

Run: python3 tools/build_site.py
Wording lives in tools/content.py. Images live in assets/img/slots/
(see IMAGE_SLOTS below; replace a slot's files to change an image).
Content edited in the admin is stored in Supabase and applied at runtime
by assets/js/cms.js.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import *  # noqa: F401,F403  (copy, services, reviews, FAQs, legal text)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUOTE = "get-a-quote.html"

# ---------------------------------------------------------------- icons
I_PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1z"/></svg>'
I_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
I_CLOSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'
I_CHEV = '<svg class="chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 4l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_UP = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 15l7-7 7 7" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_PLUS = '<svg class="plus" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v16M4 12h16" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
I_LEFT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_RIGHT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="11" fill="currentColor"/><path d="M7 12.5l3.2 3.2L17 9" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'
I_STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6-4.9-4.6 6.6-.8z"/></svg>'
STARS5 = '<span class="stars" role="img" aria-label="5 out of 5 stars">' + I_STAR * 5 + '</span>'
I_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M14 8.5V6.8c0-.8.2-1.3 1.4-1.3H17V2.6c-.3 0-1.2-.1-2.4-.1-2.4 0-4 1.4-4 4.1v1.9H8V12h2.6v9.5H14V12h2.7l.4-3.5z"/></svg>'
I_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.2" fill="currentColor"/></svg>'

# Solid icons for the "why" band
BIG = {
    "quote": '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="currentColor" d="M12 4h17l9 9v31H12z" opacity=".25"/><path fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round" d="M12 4h17l9 9v31H12zM29 4v9h9"/><path stroke="currentColor" stroke-width="3" stroke-linecap="round" d="M18 24h14M18 31h14M18 38h8"/></svg>',
    "team": '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="currentColor" d="M14 14a10 10 0 0120 0v2H14z"/><rect x="21" y="6" width="6" height="5" rx="1" fill="currentColor"/><circle cx="24" cy="21" r="7" fill="none" stroke="currentColor" stroke-width="3"/><path fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round" d="M9 44v-6a8 8 0 018-8h14a8 8 0 018 8v6zM18 30v14M30 30v14"/></svg>',
    "pin": '<svg viewBox="0 0 48 48" aria-hidden="true"><path fill="currentColor" d="M24 3a15 15 0 00-15 15c0 11 15 25 15 25s15-14 15-25A15 15 0 0024 3zm0 21a6 6 0 110-12 6 6 0 010 12z"/><ellipse cx="24" cy="44" rx="11" ry="2.5" fill="currentColor" opacity=".35"/></svg>',
}

# ---------------------------------------------------------------- images
# Each slot is a pair of files in assets/img/slots: <slot>-800.webp and <slot>-1600.webp.
IMAGE_SLOTS = {
    "home-hero": (16, 9), "band": (21, 9), "cost": (4, 5), "process": (4, 5), "choosing": (16, 10),
    "reviews-bg": (16, 9), "svc-bathroom": (16, 10), "svc-shower": (16, 10), "svc-leaking": (16, 10),
    "svc-partial": (16, 10), "svc-bathroom-2": (4, 5), "svc-shower-2": (4, 5), "svc-leaking-2": (4, 5),
    "svc-partial-2": (4, 5), **{f"strip-{i}": (1, 1) for i in range(1, 7)},
}
SVC_ICON = {"bathroom-renovations.html": "vanity", "shower-renovations.html": "shower",
            "leaking-showers.html": "drop", "partial-renovations.html": "tile"}
SVC_SLOT = {"bathroom-renovations.html": "svc-bathroom", "shower-renovations.html": "svc-shower",
            "leaking-showers.html": "svc-leaking", "partial-renovations.html": "svc-partial"}


def slot(name, alt="", sizes="100vw", eager=False, cls=""):
    aw, ah = IMAGE_SLOTS[name]
    w, h = 1600, round(1600 * ah / aw)
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="assets/img/slots/{name}-1600.webp" '
            f'srcset="assets/img/slots/{name}-800.webp 800w, assets/img/slots/{name}-1600.webp 1600w" '
            f'sizes="{sizes}" alt="{alt}" width="{w}" height="{h}" {loading} decoding="async">')


# ---------------------------------------------------------------- shared parts
def head(title, desc):
    return f"""<!doctype html>
<html lang="en-AU" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#fdfcf9">
<meta property="og:type" content="website">
<meta property="og:site_name" content="OZTECH Bathrooms">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/img/og-image.jpg">
<meta property="og:locale" content="en_AU">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="assets/css/styles.css">
"""


def schema():
    data = {
        "@context": "https://schema.org", "@type": "HomeAndConstructionBusiness", "name": "OZTECH Bathrooms",
        "description": "Sydney bathroom renovation specialists: complete bathroom and ensuite renovations, shower renovations, leaking shower repairs and partial renovations.",
        "image": "assets/img/og-image.jpg", "logo": "assets/img/oztech-logo-960.png",
        "telephone": PHONE_TEL, "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Sydney", "addressRegion": "NSW", "addressCountry": "AU"},
        "areaServed": {"@type": "City", "name": "Sydney"},
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}} for s in SERVICES],
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>\n"


def header(active):
    def cur(p):
        return ' aria-current="page"' if active == p else ""
    svc_active = active in [s[0] for s in SERVICES]
    menu = "".join(f'<li><a href="{f}"{cur(f)}>{n}</a></li>' for f, n, _ in SERVICES)
    home = "" if active == "index.html" else "index.html"
    svc_tabs = "".join(f'<li><a href="{f}"{cur(f)}><span class="svc-bar__icon">{ICONS[SVC_ICON[f]]}</span>{n}</a></li>' for f, n, _ in SERVICES)
    return f"""</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="header-inner">
    <a class="header-call" href="tel:{PHONE_TEL}" data-biz-href="tel" aria-label="Call OZTECH Bathrooms">{I_PHONE}</a>
    <a class="brand" href="index.html" aria-label="OZTECH Bathrooms home">
      <picture>
        <source srcset="assets/img/oztech-logo-480.webp 480w, assets/img/oztech-logo-960.webp 960w" sizes="220px" type="image/webp">
        <img src="assets/img/oztech-logo-480.png" alt="OZTECH Bathrooms" width="480" height="102" data-biz-img="logo">
      </picture>
    </a>
    <nav class="nav" aria-label="Primary">
      <ul>
        <li><a href="index.html"{cur("index.html")}>Home</a></li>
        <li class="has-menu">
          <button class="nav-link" type="button" aria-expanded="false" aria-haspopup="true"{' aria-current="page"' if svc_active else ""}>Renovations {I_CHEV}</button>
          <ul class="menu">{menu}</ul>
        </li>
        <li><a href="{home}#process">Our Process</a></li>
        <li><a href="{home}#reviews">Reviews</a></li>
        <li><a href="{home}#faq">FAQs</a></li>
      </ul>
    </nav>
    <div class="header-actions">
      <a class="header-phone" href="tel:{PHONE_TEL}" data-biz-href="tel">{I_PHONE}<span data-biz="phone">{PHONE_DISPLAY}</span></a>
      <a class="btn btn--sm" href="{QUOTE}">Get a Quote</a>
    </div>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu">{I_MENU}</button>
  </div>
</header>

<nav class="svc-bar" aria-label="Our services">
  <ul>{svc_tabs}</ul>
</nav>

<div class="drawer" id="drawer" aria-hidden="true">
  <div class="drawer-top"><span>Menu</span><button class="drawer-close" type="button" aria-label="Close menu">{I_CLOSE}</button></div>
  <p class="drawer-label">Our Services</p>
  <ul class="drawer-list drawer-list--svc">
    {"".join(f'<li><a href="{f}"><span class="svc-bar__icon">{ICONS[SVC_ICON[f]]}</span>{n}</a></li>' for f, n, _ in SERVICES)}
  </ul>
  <p class="drawer-label">More</p>
  <ul class="drawer-list">
    <li><a href="index.html">Home</a></li>
    <li><a href="{home}#process">Our Process</a></li>
    <li><a href="{home}#reviews">Reviews</a></li>
    <li><a href="{home}#faq">FAQs</a></li>
  </ul>
  <div class="drawer-foot">
    <a class="btn btn--block" href="{QUOTE}">Get a Free Quote</a>
    <a class="btn btn--outline btn--block" href="tel:{PHONE_TEL}" data-biz-href="tel">Call <span data-biz="phone">{PHONE_DISPLAY}</span></a>
  </div>
</div>
"""


def footer(extra_scripts=""):
    svc = "".join(f'<li><a href="{f}">{n}</a></li>' for f, n, _ in SERVICES)
    return f"""
<footer class="site-footer">
  <div class="wrap footer-grid">
    <div class="footer-brand">
      <img src="assets/img/oztech-logo-480.png" alt="OZTECH Bathrooms" width="480" height="102" loading="lazy" data-biz-img="logo">
      <p>Bathroom, ensuite and shower renovations across Sydney.</p>
      <div class="footer-social" data-biz-social hidden>
        <a href="#" data-biz-link="facebook" data-biz-wrap hidden aria-label="Facebook" target="_blank" rel="noopener">{I_FB}</a>
        <a href="#" data-biz-link="instagram" data-biz-wrap hidden aria-label="Instagram" target="_blank" rel="noopener">{I_IG}</a>
      </div>
    </div>
    <div>
      <h3>Quick Links</h3>
      <ul class="footer-links">
        <li><a href="index.html">Home</a></li>
        <li><a href="index.html#process">Our Process</a></li>
        <li><a href="index.html#reviews">Reviews</a></li>
        <li><a href="index.html#faq">FAQs</a></li>
        <li><a href="{QUOTE}">Get a Quote</a></li>
      </ul>
    </div>
    <div>
      <h3>Renovations</h3>
      <ul class="footer-links">{svc}</ul>
    </div>
    <div>
      <h3>Contact Details</h3>
      <ul class="footer-links">
        <li><a href="tel:{PHONE_TEL}" data-biz-href="tel"><span data-biz="phone">{PHONE_DISPLAY}</span></a></li>
        <li><a href="mailto:{EMAIL}" data-biz-href="mailto"><span data-biz="email">{EMAIL}</span></a></li>
        <li><span data-biz="service_area">Greater Sydney, NSW</span></li>
      </ul>
      <div class="footer-hours" data-biz-wrap hidden>
        <h3>Business Hours</h3>
        <p data-biz="hours" data-biz-optional></p>
      </div>
    </div>
    <div>
      <h3>Information</h3>
      <ul class="footer-links">
        <li><a href="terms.html">Terms of Use</a></li>
        <li><a href="privacy-policy.html">Privacy Policy</a></li>
      </ul>
      <ul class="footer-legal">
        <li data-biz-wrap hidden><span data-biz="abn" data-biz-optional data-biz-format="ABN {{}}"></span></li>
        <li data-biz-wrap hidden><span data-biz="licence" data-biz-optional data-biz-format="Builders Lic no. {{}}"></span></li>
      </ul>
    </div>
  </div>
  <div class="footer-bar">
    <div class="wrap">&copy; <span data-year>{YEAR}</span> All Rights Reserved | <span data-biz="business_name">OZTECH Bathrooms</span></div>
  </div>
</footer>

<a class="to-top" href="#main" aria-label="Back to top">{I_UP}</a>

<script src="assets/js/config.js" defer></script>
<script src="assets/js/cms.js" defer></script>
<script src="assets/js/main.js" defer></script>
{extra_scripts}</body>
</html>
"""


def faq_list(items):
    out = ['<div class="faq">']
    for q, a in items:
        paras = "".join(f"<p>{p}</p>" for p in (a if isinstance(a, list) else [a]))
        out.append(f'<details><summary><span>{q}</span><i aria-hidden="true">{I_CHEV}</i></summary><div class="faq-a">{paras}</div></details>')
    out.append("</div>")
    return "".join(out)


def steps_list(steps, numbered=True):
    out = ['<div class="steps">']
    for i, (t, d) in enumerate(steps, 1):
        label = f"{i}. {t}" if numbered else t
        out.append(f'<details><summary><span>{label}</span>{I_PLUS}</summary><p>{d}</p></details>')
    out.append("</div>")
    return "".join(out)


def review_card(name, text):
    return f"""<figure class="review-card">
        <figcaption><span class="avatar" aria-hidden="true">{name[0]}</span><span><strong>{name}</strong><small>Sydney client</small></span></figcaption>
        {STARS5}
        <blockquote>&ldquo;{text}&rdquo;</blockquote>
      </figure>"""


def write(fname, html):
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname)


# =====================================================================
# HOME
# =====================================================================
HOME_SERVICES = {
    "bathroom-renovations.html": "Full strip-out and rebuild of your bathroom or ensuite. We organise every trade.",
    "shower-renovations.html": "Walk-in showers, frameless screens, niches and shower-over-bath upgrades.",
    "leaking-showers.html": "We find the leak, strip back what's failed and rebuild it properly.",
    "partial-renovations.html": "New tiles, vanity, tapware or screen without a full strip-out.",
}
HOME_STEPS = [
    ("Free on-site consultation", "We come to you, measure up and talk through what you want, what's possible in the space and roughly what it will involve."),
    ("Design and quote", "You get an itemised quote with allowances for tiles and fixtures, plus help choosing finishes that suit your budget."),
    ("Trades coordination", "We book the plumber, electrician, waterproofer and tiler in the right order, so you're not chasing anyone."),
    ("Build", "Strip-out, rough-in, waterproofing, tiling and fit-off, with updates from us as each stage is finished."),
    ("Final walk-through", "We go over the finished bathroom with you, sort out anything that isn't right and leave the place clean."),
]


def home():
    strip = "".join(f'<li>{slot(f"strip-{i}", "", "(max-width: 720px) 40vw, 17vw")}</li>' for i in range(1, 7))
    svc_blocks = "".join(f"""<a class="svc-card" href="{f}">
          <span class="svc-card__img">{slot(SVC_SLOT[f], "", "(max-width: 640px) 100vw, (max-width: 1100px) 50vw, 25vw")}<span class="svc-card__icon">{ICONS[SVC_ICON[f]]}</span></span>
          <span class="svc-card__body">
            <strong>{n}</strong>
            <span>{HOME_SERVICES[f]}</span>
            <span class="btn btn--sm btn--block">View service</span>
          </span>
        </a>""" for f, n, _ in SERVICES)
    reviews = "".join(review_card(n, t) for n, t in REVIEWS)

    html = head("OZTECH Bathrooms | Bathroom Renovations Sydney",
                "OZTECH Bathrooms: bathroom, ensuite and shower renovations in Sydney. Leaking shower repairs, waterproofing and partial renovations. Fixed, itemised quotes.")
    html += schema()
    html += header("index.html")
    html += f"""
<main id="main">

<section class="hero" aria-labelledby="hero-title">
  {slot("home-hero", "Modern bathroom with a walk-in shower and large-format wall tiles", "100vw", eager=True, cls="hero-bg")}
  <div class="wrap hero-inner">
    <h1 id="hero-title">Bathroom Renovation Specialists in Sydney</h1>
    <p>We renovate bathrooms, ensuites and showers across Sydney. Waterproofing done properly, tiling done right, and one team on the job from strip-out to final clean.</p>
    <div class="actions">
      <a class="btn" href="{QUOTE}">Get a Free Quote</a>
      <a class="btn btn--outline-light" href="tel:{PHONE_TEL}" data-biz-href="tel">Call <span data-biz="phone">{PHONE_DISPLAY}</span></a>
    </div>
  </div>
</section>

<div class="strip" aria-hidden="true"><ul>{strip}</ul></div>

<section class="band band--charcoal why" aria-labelledby="why-title">
  <div class="wrap">
    <h2 id="why-title" class="center">Why Sydney homeowners choose OZTECH Bathrooms</h2>
    <ul class="why-grid">
      <li><span class="why-num">5.0</span><strong>Star client rating</strong></li>
      <li><span class="why-icon">{BIG["quote"]}</span><strong>Fixed, itemised quotes</strong></li>
      <li><span class="why-icon">{BIG["team"]}</span><strong>One team, start to finish</strong></li>
      <li><span class="why-icon">{BIG["pin"]}</span><strong>Sydney based</strong></li>
    </ul>
  </div>
</section>

<section class="band band--charcoal-2" id="services" aria-labelledby="services-title">
  <div class="wrap">
    <div class="intro intro--center">
      <h2 id="services-title">Our Services</h2>
      <p class="lead">Four ways we can help. Pick the one that fits your bathroom to see what's involved.</p>
    </div>
    <div class="svc-cards">{svc_blocks}</div>
    <div class="actions"><a class="btn btn--wide" href="{QUOTE}">Get a Quote</a></div>
  </div>
</section>

<div class="photo-band">{slot("band", "Bright modern bathroom with a freestanding bath and walk-in shower", "100vw")}</div>

<section class="band band--white" aria-labelledby="cost-title">
  <div class="wrap split">
    <div class="prose-block">
      <h2 id="cost-title" class="h-muted">Bathroom renovation cost <span class="accent">in Sydney</span></h2>
      <p>Every bathroom is different, so we don't publish a one-size-fits-all price. After a free visit to measure up, you get an itemised quote that shows exactly where the money goes, including allowances for tiles and fixtures.</p>
      <p class="sub">What changes the cost of a bathroom renovation:</p>
      <ul class="bullets">
        <li>The size and layout of the room</li>
        <li>Your choice of tiles, tapware, vanity and screen</li>
        <li>How much plumbing and electrical work is needed</li>
        <li>Moving the shower, toilet or vanity to a new spot</li>
        <li>The condition of the walls and floor once the old tiles are off</li>
        <li>Built-in storage and joinery</li>
      </ul>
      <p>We'll point out the big cost drivers and where you can save. If something changes once work starts, nothing extra goes ahead without your approval.</p>
      <a class="btn btn--wide" href="#services">Explore Renovation Options</a>
    </div>
    <div class="split-img">{slot("cost", "Wall-hung timber vanity with a round mirror and matte black tapware", "(max-width: 900px) 100vw, 40vw")}</div>
  </div>
</section>

<section class="band band--navy" id="process" aria-labelledby="process-title">
  <div class="wrap split split--top">
    <div class="split-img">{slot("process", "Modern vanity with a vessel basin and wall mixer", "(max-width: 900px) 100vw, 40vw")}</div>
    <div>
      <h2 id="process-title">Our renovation process, step by step</h2>
      <p class="lead">Every job follows the same steps, so you know what's happening and when, and the disruption to your home is kept short.</p>
      {steps_list(HOME_STEPS)}
    </div>
  </div>
</section>

<section class="band band--white tips" aria-labelledby="tips-title">
  <div class="wrap tips-grid">
    <div class="tips-img">{slot("choosing", "Double vanity with two round mirrors and marble-look tiles", "(max-width: 900px) 100vw, 50vw")}</div>
    <div class="tips-panel">
      <h2 id="tips-title">Choosing a bathroom renovator in Sydney</h2>
      <p>Before you pay a deposit, ask these questions:</p>
      <ul class="bullets">
        <li><strong>Are you licensed and insured?</strong> Ask for the builder's licence number and check it on the NSW Fair Trading website.</li>
        <li><strong>Is the quote itemised?</strong> A detailed quote shows what's included and makes it easy to compare.</li>
        <li><strong>Who does the waterproofing?</strong> Ask how the wet areas will be waterproofed and whether you'll get a certificate.</li>
        <li><strong>What do past clients say?</strong> Read reviews about communication, tidiness and finishing on time.</li>
      </ul>
      <p>We're happy to go through all of this with you before you commit to anything.</p>
      <a class="btn btn--block" href="{QUOTE}">Book a Free Quote</a>
    </div>
  </div>
</section>

<section class="reviews" id="reviews" aria-labelledby="reviews-title">
  {slot("reviews-bg", "", "100vw", cls="reviews-bg")}
  <div class="wrap reviews-inner">
    <h2 id="reviews-title" class="center">What our clients say</h2>
    <p class="lead center">Here's what some of our recent clients across Sydney have said about working with us.</p>
    <div class="review-box">
      <div class="rating">
        <strong>5.0 out of 5</strong>
        {STARS5}
        <span>Rated five stars by our clients</span>
      </div>
      <div class="carousel" data-carousel>
        <div class="carousel-track">{reviews}</div>
        <button class="carousel-btn prev" type="button" aria-label="Previous review">{I_LEFT}</button>
        <button class="carousel-btn next" type="button" aria-label="Next review">{I_RIGHT}</button>
      </div>
    </div>
    <div class="actions actions--stack">
      <a class="btn btn--block" href="{QUOTE}">Make an Enquiry</a>
    </div>
  </div>
</section>

<section class="band band--white statement" aria-labelledby="statement-title">
  <div class="wrap">
    <h2 id="statement-title">Tired bathroom, leaking shower or dated ensuite? <span class="accent">Sydney's bathroom renovation specialists can fix that.</span></h2>
  </div>
</section>

<section class="band band--white band--tight-top" id="faq" aria-labelledby="faq-title">
  <div class="wrap wrap--narrow">
    <h2 id="faq-title" class="center">Frequently Asked Questions</h2>
    {faq_list(HOME_FAQS)}
  </div>
</section>

</main>
"""
    html += footer()
    write("index.html", html)


# =====================================================================
# SERVICE PAGES
# =====================================================================
def service_page(cfg):
    f = cfg["file"]
    sl = SVC_SLOT[f]
    others = [s for s in SERVICES if s[0] != f]
    checklist = "".join(f'<li>{I_CHECK}<div><strong>{t}</strong><span>{d}</span></div></li>' for t, d in cfg["included"])
    cards = "".join(f'<li><span class="card-icon">{ICONS[ic]}</span><h3>{t}</h3><p>{d}</p></li>' for ic, t, d in cfg["cards"])
    related = "".join(f"""<a class="related-card" href="{rf}">{slot(SVC_SLOT[rf], "", "(max-width: 900px) 100vw, 30vw")}<span><strong>{rn}</strong><small>{rd}</small></span></a>""" for rf, rn, rd in others)
    rname, rtext = cfg["review"]
    h1 = cfg["h1"]
    breadcrumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "index.html"},
        {"@type": "ListItem", "position": 2, "name": cfg["name"], "item": f}]}
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a) if isinstance(a, list) else a}} for q, a in cfg["faqs"]]}

    html = head(cfg["title"], cfg["desc"])
    html += schema()
    html += '<script type="application/ld+json">' + json.dumps(breadcrumbs, ensure_ascii=False) + "</script>\n"
    html += '<script type="application/ld+json">' + json.dumps(faq_schema, ensure_ascii=False) + "</script>\n"
    html += header(f)
    html += f"""
<main id="main">

<section class="hero hero--page" aria-labelledby="page-title">
  {slot(sl, "", "100vw", eager=True, cls="hero-bg")}
  <div class="wrap hero-inner">
    <ol class="crumbs" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li aria-current="page">{cfg["name"]}</li></ol>
    <h1 id="page-title">{h1}</h1>
    <p>{cfg["lead"]}</p>
    <div class="actions">
      <a class="btn" href="{QUOTE}?service={cfg["survey"]}">Get a Free Quote</a>
      <a class="btn btn--outline-light" href="tel:{PHONE_TEL}" data-biz-href="tel">Call <span data-biz="phone">{PHONE_DISPLAY}</span></a>
    </div>
  </div>
</section>

<section class="band band--white" aria-labelledby="included-title">
  <div class="wrap split split--top">
    <div class="prose-block">
      <h2 id="included-title">{cfg["inc_h2"]}</h2>
      {"".join(f"<p>{p}</p>" for p in cfg["inc_copy"])}
      <a class="btn btn--wide" href="{QUOTE}?service={cfg["survey"]}">Get a Quote</a>
    </div>
    <ul class="checklist">{checklist}</ul>
  </div>
</section>

<section class="band band--charcoal" aria-labelledby="cards-title">
  <div class="wrap">
    <div class="intro intro--center">
      <h2 id="cards-title">{cfg["cards_h2"]}</h2>
      <p class="lead">{cfg["cards_lead"]}</p>
    </div>
    <ul class="card-grid">{cards}</ul>
  </div>
</section>

<section class="band band--white tips" aria-labelledby="media-title">
  <div class="wrap tips-grid">
    <div class="tips-img">{slot(sl + "-2", "", "(max-width: 900px) 100vw, 50vw")}</div>
    <div class="tips-panel">
      <h2 id="media-title">{cfg["media_h2"]}</h2>
      {"".join(f"<p>{p}</p>" for p in cfg["media_copy"])}
      <a class="btn btn--block" href="{QUOTE}?service={cfg["survey"]}">Book a Free Quote</a>
    </div>
  </div>
</section>

<section class="band band--navy" aria-labelledby="process-title">
  <div class="wrap wrap--narrow">
    <h2 id="process-title">{cfg["process_h2"]}</h2>
    <p class="lead">{cfg["process_lead"]}</p>
    {steps_list(cfg["process"])}
  </div>
</section>

<section class="reviews reviews--single" aria-label="Client review">
  {slot("reviews-bg", "", "100vw", cls="reviews-bg")}
  <div class="wrap reviews-inner">
    <div class="review-box review-box--single">
      {review_card(rname, rtext)}
    </div>
  </div>
</section>

<section class="band band--white" aria-labelledby="faq-title">
  <div class="wrap wrap--narrow">
    <h2 id="faq-title" class="center">Frequently Asked Questions</h2>
    {faq_list(cfg["faqs"])}
  </div>
</section>

<section class="band band--grey" aria-labelledby="related-title">
  <div class="wrap">
    <h2 id="related-title" class="center">Other renovation services</h2>
    <div class="related-grid">{related}</div>
  </div>
</section>

</main>
"""
    html += footer()
    write(f, html)


# =====================================================================
# GET A QUOTE
# =====================================================================
def option(key, label, sub, icon):
    sub_html = f'<span class="option__sub">{sub}</span>' if sub else ""
    return (f'<button type="button" class="option" data-key="{key}"><span class="option__icon">{icon}</span>'
            f'<span class="option__text"><span class="option__label">{label}</span>{sub_html}</span><span class="option__check">{TICK}</span></button>')


def quote_page():
    svc = "".join(option(k, l, s, SVC_ICONS[k]) for k, l, s in SURVEY_SERVICES)
    tm = "".join(option(k, l, s, TIME_ICONS[k]) for k, l, s in SURVEY_TIMES)
    html = head("Get a Free Quote | OZTECH Bathrooms Sydney",
                "Get a free, no-obligation quote for your bathroom renovation, shower renovation or leaking shower repair in Sydney. Takes less than a minute.")
    html += header(QUOTE)
    html += f"""
<main id="main">
<section class="page-title" aria-labelledby="quote-title">
  <div class="wrap">
    <h1 id="quote-title">Get a Free Quote</h1>
    <p>Answer three quick questions and we'll be in touch within one business day.</p>
  </div>
</section>
<section class="band band--grey quote-band">
  <div class="wrap wrap--narrow">
    <div class="survey" id="survey">
      <div class="survey__top">
        <button class="survey__back" type="button" hidden>{BACK} Back</button>
        <span class="survey__count" data-cms-skip aria-live="polite">Step <b>1</b> of 3</span>
      </div>
      <div class="survey__progress" aria-hidden="true"><span class="survey__bar"></span></div>

      <div class="survey__step is-active" data-field="service" role="group" aria-labelledby="q1">
        <h2 class="survey__q" id="q1" tabindex="-1">What are you looking for?</h2>
        <p class="survey__hint">Choose the option that best describes your project.</p>
        <div class="options">{svc}</div>
      </div>

      <div class="survey__step" data-field="timeframe" role="group" aria-labelledby="q2">
        <h2 class="survey__q" id="q2" tabindex="-1">How soon are you looking to get started?</h2>
        <p class="survey__hint">This helps us plan our schedule around you.</p>
        <div class="options options--list">{tm}</div>
      </div>

      <div class="survey__step" aria-labelledby="q3">
        <h2 class="survey__q" id="q3" tabindex="-1">How can we reach you?</h2>
        <p class="survey__hint">We'll be in touch within one business day to arrange a free on-site visit.</p>
        <form class="form" id="survey-form" novalidate>
          <div class="field"><label for="s-name">Full name</label><input id="s-name" name="name" type="text" autocomplete="name" placeholder="Your name" required minlength="2"></div>
          <div class="field"><label for="s-email">Email</label><input id="s-email" name="email" type="email" autocomplete="email" placeholder="you@email.com" required></div>
          <div class="field"><label for="s-phone">Phone</label><input id="s-phone" name="phone" type="tel" autocomplete="tel" placeholder="04xx xxx xxx" required minlength="8"></div>
          <div class="field"><label for="s-postcode">Postcode</label><input id="s-postcode" name="postcode" type="text" inputmode="numeric" autocomplete="postal-code" placeholder="e.g. 2000" required pattern="[0-9]{{4}}" maxlength="4"></div>
          <div class="hp-field" aria-hidden="true"><label for="s-hp">Leave this field empty</label><input id="s-hp" name="oz_hp" type="text" tabindex="-1" autocomplete="off" data-1p-ignore data-lpignore="true" data-form-type="other"></div>
          <button class="btn btn--block" type="submit">Get My Free Quote</button>
          <p class="form__status" role="status" aria-live="polite"></p>
          <p class="form__note">Your details are only used to respond to your enquiry. See our <a href="privacy-policy.html">Privacy Policy</a>.</p>
        </form>
      </div>

      <div class="survey__step survey__done" aria-labelledby="q4">
        <div class="survey__done-icon">{DONE_ICON}</div>
        <h2 class="survey__q" id="q4" tabindex="-1">Thanks, we&rsquo;ve got your details.</h2>
        <p>We'll review your details and be in touch within one business day to arrange your free on-site quote.</p>
        <div class="actions actions--center">
          <a class="btn" href="tel:{PHONE_TEL}" data-biz-href="tel">Call <span data-biz="phone">{PHONE_DISPLAY}</span></a>
          <a class="btn btn--outline" href="index.html">Back to Home</a>
        </div>
      </div>
    </div>
  </div>
</section>
</main>
"""
    html += footer('<script src="assets/js/quote.js" defer></script>\n')
    write(QUOTE, html)


# =====================================================================
# LEGAL
# =====================================================================
def legal_page(fname, name, title, desc, intro, sections):
    toc = "".join(f'<li><a href="#{sid}">{h}</a></li>' for sid, h, _ in sections)
    body = "".join(f'<h2 id="{sid}">{h}</h2>{content}' for sid, h, content in sections)
    html = head(title, desc)
    html += header(fname)
    html += f"""
<main id="main">
<section class="page-title" aria-labelledby="page-title">
  <div class="wrap">
    <h1 id="page-title">{name}</h1>
    <p>{intro}</p>
  </div>
</section>
<section class="band band--white">
  <div class="wrap legal">
    <aside class="legal__toc" aria-label="On this page"><p>On this page</p><ol>{toc}</ol></aside>
    <article class="prose">
      <p class="legal__updated">Last updated: 8 November 2026</p>
      {body}
    </article>
  </div>
</section>
</main>
"""
    html += footer()
    write(fname, html)


if __name__ == "__main__":
    home()
    quote_page()
    for p in PAGES:
        service_page(p)
    legal_page("privacy-policy.html", "Privacy Policy", "Privacy Policy | OZTECH Bathrooms Sydney",
               "How OZTECH Bathrooms collects, uses and protects your personal information, in line with the Privacy Act 1988 (Cth) and the Australian Privacy Principles.",
               "How we collect, use and protect your personal information.", PRIVACY)
    legal_page("terms.html", "Terms of Use", "Terms of Use | OZTECH Bathrooms Sydney",
               "The terms that apply to your use of the OZTECH Bathrooms website.",
               "The terms that apply when you use the OZTECH Bathrooms website.", TERMS)
