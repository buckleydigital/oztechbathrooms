#!/usr/bin/env python3
"""Generates the static OZTECH Bathrooms site pages into the repo root.

Run: python3 tools/build_site.py
Content edited in the admin is stored in Supabase and applied at runtime
by assets/js/cms.js, so regenerating pages does not lose admin edits
(unless the default text of an edited element changes).
"""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- Business details (placeholders flagged to the owner) ----
PHONE_DISPLAY = "0466 877 871"
PHONE_TEL = "+61466877871"
EMAIL = "info@oztechbathrooms.com.au"
YEAR = "2026"

# ---- Icons ----
ARROW = '<svg class="arrow" viewBox="0 0 18 10" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M0 5h17M13 1l4 4-4 4"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M1 3l4 4 4-4"/></svg>'
STAR = '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 1.5l2.6 5.5 6 .8-4.4 4.1 1.1 6-5.3-2.9-5.3 2.9 1.1-6L1.4 7.8l6-.8z"/></svg>'
STARS = '<span class="stars" role="img" aria-label="5 out of 5 stars">' + STAR * 5 + '</span>'
CHECK = '<svg viewBox="0 0 18 18" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><circle cx="9" cy="9" r="8.4"/><path d="M5.2 9.2l2.5 2.5 5-5.2"/></svg>'
PHONE = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M5.6 1.5H3A1.5 1.5 0 001.5 3c0 6.4 5.1 11.5 11.5 11.5A1.5 1.5 0 0014.5 13v-2.6l-3.2-1.1-1.5 1.5A8.6 8.6 0 015.2 6.2l1.5-1.5z"/></svg>'
MAIL = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><rect x="1.5" y="3" width="13" height="10"/><path d="M1.5 3.5L8 9l6.5-5.5"/></svg>'
PIN = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M8 15s5-4.6 5-8.5A5 5 0 003 6.5C3 10.4 8 15 8 15z"/><circle cx="8" cy="6.5" r="1.8"/></svg>'
FB = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M9.5 15V9h2l.4-2.4H9.5V5.2c0-.7.3-1.2 1.3-1.2H12V1.9a14 14 0 00-1.8-.1C8.4 1.8 7.2 2.9 7.2 4.9v1.7H5.2V9h2v6"/></svg>'
IG = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><rect x="1.8" y="1.8" width="12.4" height="12.4" rx="3.5"/><circle cx="8" cy="8" r="2.9"/><circle cx="11.9" cy="4.1" r=".5" fill="currentColor"/></svg>'
SHIELD = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M8 1.5l5.5 2v4.2c0 3.3-2.3 5.9-5.5 6.8-3.2-.9-5.5-3.5-5.5-6.8V3.5z"/><path d="M5.5 8l1.8 1.8L10.8 6"/></svg>'
DOC = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M3.5 1.5h6l3 3v10h-9z"/><path d="M9.5 1.5v3h3M5.5 8h5M5.5 10.5h5"/></svg>'

# Larger line icons for "sign" cards
ICONS = {
    "drop": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M10 2s5.5 6.2 5.5 10a5.5 5.5 0 01-11 0C4.5 8.2 10 2 10 2z"/></svg>',
    "tile": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><rect x="2.5" y="2.5" width="6.5" height="6.5"/><rect x="11" y="2.5" width="6.5" height="6.5" transform="rotate(8 14.25 5.75)"/><rect x="2.5" y="11" width="6.5" height="6.5"/><rect x="11" y="11" width="6.5" height="6.5"/></svg>',
    "mould": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><circle cx="6" cy="7" r="2"/><circle cx="13" cy="5.5" r="1.4"/><circle cx="12.5" cy="12.5" r="2.6"/><circle cx="5.5" cy="14" r="1.2"/></svg>',
    "wall": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M2.5 2.5h15v15h-15z"/><path d="M6 12c1.5-1 3 1 4.5 0s3-1 4 0M6 15c1.5-1 3 1 4.5 0s3-1 4 0"/></svg>',
    "grout": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M2.5 10h15M10 2.5v15"/><path d="M12 12.5l2 2.5M14.5 11.5l1.5 1.5" /></svg>',
    "nose": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M4 7c2-2 4 2 6 0s4-2 6 0M4 11c2-2 4 2 6 0s4-2 6 0M4 15c2-2 4 2 6 0s4-2 6 0"/></svg>',
    "ruler": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M2.5 13.5l11-11 4 4-11 11z"/><path d="M6 10l1.5 1.5M8.5 7.5L10 9M11 5l1.5 1.5"/></svg>',
    "quote": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M4.5 2.5h8l3 3v12h-11z"/><path d="M7 9h6M7 12h6M7 15h3.5"/></svg>',
    "team": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><circle cx="7" cy="7" r="2.6"/><circle cx="14" cy="8" r="2"/><path d="M2.5 16.5c.6-3 2.4-4.5 4.5-4.5s3.9 1.5 4.5 4.5M12 12.3c.6-.2 1.3-.3 2-.3 1.8 0 3 1.2 3.5 3.5"/></svg>',
    "clock": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><circle cx="10" cy="10" r="7.5"/><path d="M10 5.5V10l3 2"/></svg>',
    "spark": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M10 2.5v4M10 13.5v4M2.5 10h4M13.5 10h4M4.7 4.7l2.8 2.8M12.5 12.5l2.8 2.8M15.3 4.7l-2.8 2.8M7.5 12.5l-2.8 2.8"/></svg>',
    "shower": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M4 17.5V5a2.5 2.5 0 012.5-2.5h2A2.5 2.5 0 0111 5v.5"/><path d="M8 5.5h6M9 9v1M11 9v1.5M13 9v1"/></svg>',
    "glass": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><rect x="5" y="2.5" width="10" height="15"/><path d="M8 6l3-3M8 10l6-6"/></svg>',
    "tap": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M3 8.5h9a3 3 0 013 3V13"/><path d="M3 6.5v4M7 8.5V5.5M5 5.5h4M15 15.5v1"/></svg>',
    "vanity": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M2.5 9.5h15v6h-15zM10 9.5v6M7.5 12.5h.5M12 12.5h.5M7 9.5c0-1.5 1.3-2.5 3-2.5s3 1 3 2.5M10 4v3"/></svg>',
    "home": '<svg viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M2.5 9L10 2.5 17.5 9v8.5h-15z"/><path d="M8 17.5v-5h4v5"/></svg>',
}

SERVICES = [
    ("bathroom-renovations.html", "Bathroom Renovations", "Complete bathroom & ensuite renovations"),
    ("shower-renovations.html", "Shower Renovations", "Walk-in showers, screens & shower-over-bath"),
    ("leaking-showers.html", "Leaking Showers", "Leak diagnosis, re-waterproofing & rebuilds"),
    ("partial-renovations.html", "Partial Renovations", "Targeted updates without a full strip-out"),
]

REVIEWS = [
    ("Karen M", "From the first quote to the final clean-up, the team was professional and easy to deal with. Our ensuite went from dated 90s tiles to something that looks like a hotel bathroom, and they finished on the day they said they would."),
    ("David N", "They kept us updated every step and kept the mess to a minimum. The waterproofing and tiling are excellent, and the price matched the quote exactly."),
    ("Sophia P", "Great communication, tidy tradies and beautiful workmanship. They helped us pick fixtures that fit our budget and the space. I’d happily recommend them to anyone in Sydney looking at a bathroom reno."),
]


def img(name, alt, cls="", sizes="(max-width: 1024px) 100vw, 50vw", eager=False, pos=None):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy"'
    dims = 'width="924" height="2000"' if name != "14378" else 'width="1080" height="770"'
    style = f' style="object-position:{pos}"' if pos else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="assets/img/{name}-1600.webp" '
            f'srcset="assets/img/{name}-800.webp 800w, assets/img/{name}-1600.webp 1600w" '
            f'sizes="{sizes}" alt="{alt}" {dims} {loading} decoding="async"{style}>')


def head(title, desc, path):
    return f"""<!doctype html>
<html lang="en-AU" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0a0a0a">
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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..700&family=Hanken+Grotesk:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/css/styles.css">
<link rel="preload" as="image" href="assets/img/oztech-logo-480.webp" type="image/webp">
"""


def schema():
    data = {
        "@context": "https://schema.org",
        "@type": "HomeAndConstructionBusiness",
        "name": "OZTECH Bathrooms",
        "description": "Sydney bathroom renovation specialists: complete bathroom and ensuite renovations, shower renovations, leaking shower repairs and partial renovations.",
        "image": "assets/img/og-image.jpg",
        "logo": "assets/img/oztech-logo-960.png",
        "telephone": PHONE_TEL,
        "email": EMAIL,
        "address": {"@type": "PostalAddress", "addressLocality": "Sydney", "addressRegion": "NSW", "addressCountry": "AU"},
        "areaServed": {"@type": "City", "name": "Sydney"},
        "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s[1]}} for s in SERVICES],
    }
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>\n"


def header(active, has_form=True):
    quote = "get-a-quote.html"
    def cur(p):
        return ' aria-current="page"' if active == p else ""
    svc_active = active in [s[0] for s in SERVICES]
    menu = "".join(f'<li><a href="{f}"{cur(f)}>{n}{ARROW}</a></li>' for f, n, _ in SERVICES)
    dmenu = "".join(f'<li><a href="{f}">{n}</a></li>' for f, n, _ in SERVICES)
    home = "" if active == "index.html" else "index.html"
    return f"""</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="OZTECH Bathrooms home">
      <picture>
        <source srcset="assets/img/oztech-logo-480.webp 480w, assets/img/oztech-logo-960.webp 960w" sizes="210px" type="image/webp">
        <img src="assets/img/oztech-logo-480.png" alt="OZTECH Bathrooms" width="480" height="102" data-biz-img="logo">
      </picture>
    </a>
    <nav class="nav" aria-label="Primary">
      <ul class="nav__list">
        <li><a class="nav__link" href="index.html"{cur("index.html")}>Home</a></li>
        <li class="has-menu">
          <button class="nav__link" type="button" aria-expanded="false" aria-haspopup="true"{' aria-current="page"' if svc_active else ""}>Services {CHEV}</button>
          <ul class="menu">{menu}</ul>
        </li>
        <li><a class="nav__link" href="{home}#work">Our Work</a></li>
        <li><a class="nav__link" href="{home}#process">Process</a></li>
        <li><a class="nav__link" href="{home}#reviews">Reviews</a></li>
      </ul>
      <a class="btn btn--light header-cta" href="{quote}">Free Quote {ARROW}</a>
    </nav>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu"><span></span><span></span><span></span></button>
  </div>
</header>

<div class="drawer" id="drawer" aria-hidden="true">
  <ul class="drawer__list">
    <li><a href="index.html">Home</a></li>
    <li><span class="drawer__label">Services</span><ul class="drawer__sub">{dmenu}</ul></li>
    <li><a href="{home}#work">Our Work</a></li>
    <li><a href="{home}#process">Process</a></li>
    <li><a href="{home}#reviews">Reviews</a></li>
  </ul>
  <div class="drawer__foot">
    <a class="btn btn--light" href="{quote}">Request a Free Quote {ARROW}</a>
    <a class="btn btn--ghost" href="tel:{PHONE_TEL}" data-biz-href="tel">{PHONE} <span data-cms-skip>Call</span> <span data-biz="phone">{PHONE_DISPLAY}</span></a>
  </div>
</div>
"""


def footer(has_form=True):
    quote = "get-a-quote.html"
    svc = "".join(f'<li><a href="{f}">{n}</a></li>' for f, n, _ in SERVICES)
    return f"""
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="assets/img/oztech-logo-480.png" alt="OZTECH Bathrooms" width="480" height="102" loading="lazy" data-biz-img="logo">
        <p>Bathroom, ensuite and shower renovations for Sydney homes, designed with care, waterproofed properly and finished to a standard you'll notice every day.</p>
        <div class="footer-social" data-biz-social hidden>
          <a href="#" data-biz-link="facebook" data-biz-wrap hidden aria-label="Facebook" target="_blank" rel="noopener">{FB}</a>
          <a href="#" data-biz-link="instagram" data-biz-wrap hidden aria-label="Instagram" target="_blank" rel="noopener">{IG}</a>
        </div>
      </div>
      <div class="footer-col">
        <h3>Services</h3>
        <ul>{svc}</ul>
      </div>
      <div class="footer-col">
        <h3>Company</h3>
        <ul>
          <li><a href="index.html#work">Our Work</a></li>
          <li><a href="index.html#process">Our Process</a></li>
          <li><a href="index.html#reviews">Reviews</a></li>
          <li><a href="index.html#faq">FAQs</a></li>
          <li><a href="{quote}">Request a Quote</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h3>Contact</h3>
        <ul>
          <li><a href="tel:{PHONE_TEL}" data-biz-href="tel"><span data-biz="phone">{PHONE_DISPLAY}</span></a></li>
          <li><a href="mailto:{EMAIL}" data-biz-href="mailto"><span data-biz="email">{EMAIL}</span></a></li>
          <li><span data-biz="service_area">Greater Sydney, NSW</span></li>
          <li data-biz-wrap hidden><span data-biz="hours" data-biz-optional></span></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <div>
        <p>&copy; <span data-year>{YEAR}</span> <span data-biz="business_name">OZTECH Bathrooms</span>. Sydney, NSW. All rights reserved.</p>
        <p class="footer-legal"><span data-biz="licence" data-biz-optional data-biz-format="Contractor Licence No. {{}}" hidden></span><span data-biz="abn" data-biz-optional data-biz-format="ABN {{}}" hidden></span></p>
      </div>
      <ul>
        <li><a href="privacy-policy.html">Privacy Policy</a></li>
        <li><a href="terms.html">Terms of Use</a></li>
      </ul>
    </div>
  </div>
</footer>

<nav class="mobile-bar" aria-label="Quick contact">
  <a href="tel:{PHONE_TEL}" data-biz-href="tel">{PHONE} Call</a>
  <a href="{quote}">{DOC} Free Quote</a>
</nav>

<script src="assets/js/config.js" defer></script>
<script src="assets/js/cms.js" defer></script>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""


def service_options(selected=None):
    opts = ['<option value="" disabled' + (" selected" if not selected else "") + '>Select a service</option>']
    for _, n, _ in SERVICES:
        sel = " selected" if n == selected else ""
        opts.append(f'<option{sel}>{n}</option>')
    opts.append("<option>Not sure yet</option>")
    return "".join(opts)


def contact_section(selected=None, heading='Tell us about your project', bg="section--ink"):
    return f"""
<section class="section {bg}" id="quote" aria-labelledby="quote-title">
  <div class="wrap contact">
    <div class="reveal">
      <span class="eyebrow">Free, no-obligation quote</span>
      <h2 class="h2" id="quote-title">{heading}</h2>
      <p class="lead">Tell us a little about your space and what you'd like to achieve. We'll get back to you to arrange an on-site visit, then provide a clear, itemised quote. No pressure and no surprises.</p>
      <ul class="contact__details">
        <li><span>Call</span><a href="tel:{PHONE_TEL}" data-biz-href="tel" data-biz="phone">{PHONE_DISPLAY}</a></li>
        <li><span>Email</span><a href="mailto:{EMAIL}" data-biz-href="mailto" data-biz="email">{EMAIL}</a></li>
        <li><span>Area</span><p data-biz="service_area">Greater Sydney, NSW</p></li>
      </ul>
    </div>
    <form class="form reveal reveal-d2" data-lead-form="contact-form" data-phone="{PHONE_DISPLAY}" novalidate>
      <p class="form__title">Request your quote<small>We usually respond within one business day.</small></p>
      <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" type="text" autocomplete="name" placeholder="Your name" required></div>
      <div class="field"><label for="f-phone">Phone</label><input id="f-phone" name="phone" type="tel" autocomplete="tel" placeholder="04xx xxx xxx" required></div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="you@email.com" required></div>
      <div class="field"><label for="f-suburb">Suburb</label><input id="f-suburb" name="suburb" type="text" autocomplete="address-level2" placeholder="e.g. Ryde" required></div>
      <div class="field field--full"><label for="f-service">Service</label><select id="f-service" name="service" required>{service_options(selected)}</select></div>
      <div class="hp-field" aria-hidden="true"><label for="f-company">Company</label><input id="f-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
      <div class="field field--full"><label for="f-message">About your project</label><textarea id="f-message" name="message" placeholder="Room size, what you'd like changed, ideal timing…"></textarea></div>
      <button class="btn btn--dark" type="submit">Send enquiry {ARROW}</button>
      <p class="form__status" role="status" aria-live="polite"></p>
      <p class="form__note">By submitting this form you agree to us contacting you about your enquiry. See our <a href="privacy-policy.html">Privacy Policy</a>.</p>
    </form>
  </div>
</section>
"""


def review_card(name, text, delay=""):
    return f"""<figure class="review reveal {delay}">
        <span class="review__mark" aria-hidden="true">&ldquo;</span>
        {STARS}
        <blockquote>&ldquo;{text}&rdquo;</blockquote>
        <figcaption><span class="review__avatar" aria-hidden="true">{name[0]}</span><span><span class="review__name">{name}</span><span class="review__meta">Client &middot; Sydney</span></span></figcaption>
      </figure>"""


def faq(items, dark=False):
    out = [f'<div class="faq{" faq--dark" if dark else ""}">']
    for q, a in items:
        paras = "".join(f"<p>{p}</p>" for p in (a if isinstance(a, list) else [a]))
        out.append(f'<details class="reveal"><summary>{q}<i aria-hidden="true"></i></summary><div class="faq__a">{paras}</div></details>')
    out.append("</div>")
    return "\n".join(out)


def process(steps, light=False):
    s = "".join(f'<div class="step"><h3>{t}</h3><p>{d}</p></div>' for t, d in steps)
    return f'<div class="process{" process--light" if light else ""}">{s}</div>'


def write(fname, html):
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname)


# =====================================================================
# HOME
# =====================================================================
def home():
    services_cards = []
    svc_imgs = {
        "bathroom-renovations.html": ("14377", "Renovated bathroom with frameless walk-in shower, marble-look tiles and black and white mosaic floor", "50% 60%"),
        "shower-renovations.html": ("14374", "Shower over bath with frameless glass panel, brushed nickel rail shower and handmade-look white tiles", "50% 45%"),
        "leaking-showers.html": ("14375", "Bathroom stripped back and prepared ahead of re-waterproofing and retiling", "50% 45%"),
        "partial-renovations.html": ("14378", "Classic white subway-tiled bathroom with glass block windows and frameless bath screen", "50% 50%"),
    }
    blurbs = {
        "bathroom-renovations.html": "Full strip-out to final polish. Main bathrooms and ensuites rebuilt with new waterproofing, tiling, fixtures and finishes.",
        "shower-renovations.html": "Walk-in showers, frameless screens, recessed niches and shower-over-bath upgrades that change how the room feels.",
        "leaking-showers.html": "We find the source, strip back what's failed and rebuild with compliant waterproofing, fixed properly, not patched.",
        "partial-renovations.html": "New vanity, tapware, screen or tiles without the full strip-out. A considered refresh on a tighter budget or timeline.",
    }
    for i, (f, n, _) in enumerate(SERVICES):
        im, alt, pos = svc_imgs[f]
        services_cards.append(f"""<article class="service-card reveal reveal-d{i+1}">
        <div class="service-card__img">{img(im, alt, sizes="(max-width: 720px) 100vw, (max-width: 1180px) 50vw, 25vw", pos=pos)}</div>
        <span class="service-card__num">0{i+1}</span>
        <div class="service-card__body">
          <h3>{n}</h3>
          <p>{blurbs[f]}</p>
          <a class="text-link" href="{f}">Explore {ARROW}</a>
        </div>
        <a class="cover" href="{f}" aria-label="{n}" tabindex="-1"></a>
      </article>""")


    reviews = "\n      ".join(review_card(n, t, f"reveal-d{i+1}") for i, (n, t) in enumerate(REVIEWS))

    areas = ["Inner West", "Eastern Suburbs", "North Shore", "Northern Beaches", "Hills District", "Sutherland Shire", "St George", "Western Sydney", "Parramatta", "Sydney CBD &amp; surrounds"]
    area_html = "".join(f"<li>{a}</li>" for a in areas)

    faqs = [
        ("How much does a bathroom renovation cost in Sydney?", ["Every bathroom is different. The size of the room, the condition behind the tiles, plumbing changes and the fixtures you choose all affect the price. That's why we quote after seeing the space in person.", "After an on-site visit you'll receive a fixed, itemised quote so you know exactly what's included before any work begins."]),
        ("How long does a full bathroom renovation take?", "Timeframes depend on scope, but we give you a realistic schedule up front and keep you updated at every stage. Waterproofing needs proper curing time, and we never rush it, it's the part of a bathroom you can't see but rely on most."),
        ("Is waterproofing included?", "Yes. Waterproofing is included in every renovation that involves wet areas, and is carried out in line with Australian Standard AS 3740 for wet-area waterproofing."),
        ("Do I need to supply my own fixtures and tiles?", "You can, but you don't have to. We're happy to help you choose tiles, tapware, vanities and screens that suit your space, style and budget, or work with selections you've already made."),
        ("Can I use my bathroom during the renovation?", "For a full renovation the room will be out of action while we work. If it's your only bathroom, talk to us during the quote and we'll plan the schedule to keep the disruption as short as possible."),
        ("Do you clean up afterwards?", "Always. We protect floors and access paths during the job, keep the site tidy as we go and finish with a thorough clean, so your new bathroom is ready to use."),
    ]

    html = head("OZTECH Bathrooms | Bathroom Renovations Sydney",
                "OZTECH Bathrooms: premium bathroom, ensuite and shower renovations in Sydney. Leaking shower repairs, waterproofing and partial renovations. Fixed, itemised quotes.",
                "index.html")
    html += schema()
    html += header("index.html")
    html += f"""
<main id="main">

<!-- HERO -->
<section class="hero" aria-labelledby="hero-title">
  <div class="wrap">
    <div class="hero__copy">
      <span class="eyebrow reveal">Sydney Bathroom Renovation Specialists</span>
      <h1 class="display reveal reveal-d1" id="hero-title">Bathrooms,<br>built properly.</h1>
      <p class="lead reveal reveal-d2">OZTECH Bathrooms designs and builds bathroom, ensuite and shower renovations across Sydney, waterproofed right, finished beautifully and managed by one team from strip-out to final clean.</p>
      <div class="hero__actions reveal reveal-d3">
        <a class="btn btn--light" href="get-a-quote.html">Request a Free Quote {ARROW}</a>
        <a class="btn btn--ghost" href="#work">View Our Work</a>
      </div>
      <ul class="hero__meta reveal reveal-d4">
        <li>{SHIELD} Waterproofing to AS 3740</li>
        <li>{DOC} Fixed, itemised quotes</li>
        <li>{PIN} Servicing all of Sydney</li>
      </ul>
    </div>
    <div class="hero__media reveal reveal-d2">
      <span class="hero__outline" aria-hidden="true"></span>
      <div class="hero__frame">
        {img("14377", "Completed OZTECH bathroom renovation with frameless walk-in shower, marble-look wall tiles and black and white octagon mosaic floor", sizes="(max-width: 1024px) 90vw, 40vw", eager=True)}
      </div>
      <div class="hero__badge">
        {STARS}
        <strong>5.0 rated</strong>
        <span>by Sydney homeowners</span>
      </div>
    </div>
  </div>
</section>


<!-- INTRO -->
<section class="section section--light" aria-labelledby="intro-title">
  <div class="wrap intro">
    <div class="intro__media reveal">
      <div class="frame">{img("14374", "Renovated bathroom with frameless shower screen over bath, brushed nickel rail shower and heated towel rail", sizes="(max-width: 1024px) 100vw, 42vw")}</div>
      <span class="caption">Completed &middot; Sydney</span>
    </div>
    <div class="intro__copy">
      <span class="eyebrow reveal">About OZTECH</span>
      <h2 class="h2 reveal reveal-d1" id="intro-title">One team, from strip-out to final clean</h2>
      <p class="lead reveal reveal-d2">It's the room you start and finish every day in. We approach every renovation with the same care: honest advice at the start, meticulous preparation behind the walls, and precise finishing you can see and feel.</p>
      <p class="lead reveal reveal-d2">Whether it's a complete ensuite transformation, a new walk-in shower or fixing a leak properly, you deal with one team that takes ownership of the whole job.</p>
      <ul class="intro__points reveal reveal-d3">
        <li><strong>Fixed quotes</strong><span>Itemised and clear. The price you approve is the price you pay.</span></li>
        <li><strong>One team</strong><span>A single point of contact from first visit to final clean.</span></li>
        <li><strong>Done right</strong><span>Compliant waterproofing and careful prep beneath every tile.</span></li>
        <li><strong>Respectful sites</strong><span>Protected floors, tidy work areas and minimal disruption.</span></li>
      </ul>
      <a class="btn btn--dark reveal reveal-d4" href="get-a-quote.html">Book an On-Site Quote {ARROW}</a>
    </div>
  </div>
</section>

<!-- SERVICES -->
<section class="section" id="services" aria-labelledby="services-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow reveal">What we do</span>
        <h2 class="h2 reveal reveal-d1" id="services-title">We only do bathrooms</h2>
      </div>
      <p class="lead reveal reveal-d2">Focusing on one room means we know it inside out: the waterproofing, the drainage falls, the tiling details and the finishes that make a bathroom feel high-end.</p>
    </div>
    <div class="services">
      {"".join(services_cards)}
    </div>
  </div>
</section>

<!-- BEFORE / AFTER -->
<section class="section section--ink" id="work" aria-labelledby="ba-title">
  <div class="wrap ba">
    <div class="ba__copy">
      <span class="eyebrow reveal">Before &amp; after</span>
      <h2 class="h2 reveal reveal-d1" id="ba-title">Same room, new finish</h2>
      <p class="lead reveal reveal-d2">Drag the slider to see the difference. Tired tiles and worn grout replaced with crisp, handmade-look tiling, a new rail shower and a frameless screen, the layout stays, the feel is completely new.</p>
      <ul class="ba__list reveal reveal-d3">
        <li><b>01</b>Old tiles removed and walls prepared</li>
        <li><b>02</b>Wet areas re-waterproofed before tiling</li>
        <li><b>03</b>New tiling, tapware, rail shower and screen</li>
      </ul>
      <a class="text-link reveal reveal-d4" href="partial-renovations.html">See partial renovations {ARROW}</a>
    </div>
    <div class="compare reveal reveal-d2">
      {img("14376", "Before: bathroom with dated white tiles and worn grout", sizes="(max-width: 1024px) 100vw, 50vw")}
      {img("14374", "After: renovated bathroom with new handmade-look tiles, rail shower and frameless glass panel", cls="compare__after", sizes="(max-width: 1024px) 100vw, 50vw")}
      <span class="compare__tag compare__tag--before">Before</span>
      <span class="compare__tag compare__tag--after">After</span>
      <input type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after">
      <div class="compare__handle" aria-hidden="true"><span class="compare__knob"><svg viewBox="0 0 26 12" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M5 1L1 6l4 5M21 1l4 5-4 5M1 6h24"/></svg></span></div>
    </div>
  </div>
</section>

<!-- GALLERY -->
<section class="section section--paper" aria-labelledby="gallery-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow reveal">Our work</span>
        <h2 class="h2 reveal reveal-d1" id="gallery-title">Recent projects</h2>
      </div>
      <p class="lead reveal reveal-d2">Crisp tile lines, accurate falls to the waste, clean silicone and hardware set exactly where it should be. It's the detail you notice every day.</p>
    </div>
    <div class="gallery">
      <figure class="g-1 reveal">{img("14377", "Walk-in shower with frameless glass, marble-look tiles and octagon mosaic floor", sizes="(max-width: 720px) 50vw, 40vw")}<figcaption><span>Full renovation</span>Walk-in shower &amp; octagon mosaic floor</figcaption></figure>
      <figure class="g-2 reveal reveal-d1">{img("14378", "Classic white subway-tiled bathroom with glass block windows and frameless bath screen", sizes="(max-width: 720px) 100vw, 33vw")}<figcaption><span>Classic</span>Subway tiles &amp; glass block windows</figcaption></figure>
      <figure class="g-3 reveal reveal-d2">{img("14374", "Shower over bath with frameless panel and handmade-look tiles", sizes="(max-width: 720px) 50vw, 25vw")}<figcaption><span>Shower renovation</span>Shower over bath, frameless panel</figcaption></figure>
      <figure class="g-4 reveal reveal-d3">{img("14375", "Bathroom prepared and protected before retiling works", sizes="(max-width: 720px) 100vw, 33vw")}<figcaption><span>In progress</span>Prepared &amp; protected before works</figcaption></figure>
    </div>
  </div>
</section>

<!-- PROCESS -->
<section class="section" id="process" aria-labelledby="process-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow reveal">How it works</span>
        <h2 class="h2 reveal reveal-d1" id="process-title">Four steps, no surprises</h2>
      </div>
      <p class="lead reveal reveal-d2">No guesswork, no chasing tradespeople. You'll know what's happening, when it's happening and what it costs.</p>
    </div>
    {process([
        ("Consult &amp; measure", "We visit your home, look at the space, listen to what you want and check what's behind the existing finishes."),
        ("Design &amp; fixed quote", "You receive an itemised quote and we help you finalise tiles, fixtures and layout to suit your style and budget."),
        ("Build", "Strip-out, plumbing, electrical, waterproofing, tiling and fit-off, carried out in sequence with regular updates."),
        ("Handover", "A final walk-through together, a thorough clean, and a bathroom that's ready to use from day one."),
    ])}
  </div>
</section>

<!-- REVIEWS -->
<section class="section section--paper" id="reviews" aria-labelledby="reviews-title">
  <div class="wrap">
    <div class="section-head section-head--center">
      <div>
        <span class="eyebrow reveal">Client reviews</span>
        <h2 class="h2 reveal reveal-d1" id="reviews-title">What our clients say</h2>
      </div>
    </div>
    <div class="reviews">
      {reviews}
    </div>
    <div class="reviews-summary reveal">
      <strong>5.0</strong>{STARS}<span>Rated five stars by Sydney homeowners</span>
    </div>
  </div>
</section>

<!-- AREAS -->
<section class="section" aria-labelledby="areas-title">
  <div class="wrap areas">
    <div>
      <span class="eyebrow reveal">Service area</span>
      <h2 class="h2 reveal reveal-d1" id="areas-title">Working across Sydney</h2>
      <p class="lead reveal reveal-d2">Based in Sydney, we work with homeowners right across the metropolitan area, from apartments and terraces to family homes. Not sure if we cover your suburb? Just ask.</p>
    </div>
    <ul class="area-list reveal reveal-d2">{area_html}</ul>
  </div>
</section>

<!-- FAQ -->
<section class="section section--light" id="faq" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="section-head section-head--center">
      <div>
        <span class="eyebrow reveal">FAQs</span>
        <h2 class="h2 reveal reveal-d1" id="faq-title">Common questions</h2>
      </div>
    </div>
    {faq(faqs)}
  </div>
</section>

{contact_section()}
</main>
"""
    html += footer()
    write("index.html", html)


# =====================================================================
# SERVICE PAGES
# =====================================================================
def service_page(cfg):
    f = cfg["file"]
    others = [s for s in SERVICES if s[0] != f]
    related = "".join(f'<a href="{rf}" class="reveal reveal-d{i+1}"><small>{rd}</small><strong>{rn}{ARROW}</strong></a>' for i, (rf, rn, rd) in enumerate(others))
    checklist = "".join(f"<li>{CHECK}<div><strong>{t}</strong><span>{d}</span></div></li>" for t, d in cfg["included"])
    cards = "".join(f'<div class="sign reveal reveal-d{(i % 3) + 1}"><div class="sign__icon">{ICONS[ic]}</div><h3>{t}</h3><p>{d}</p></div>' for i, (ic, t, d) in enumerate(cfg["cards"]))
    rname, rtext = cfg["review"]
    m1, m2 = cfg["media"]

    breadcrumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "index.html"},
            {"@type": "ListItem", "position": 2, "name": cfg["name"], "item": f},
        ],
    }
    faq_schema = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": " ".join(a) if isinstance(a, list) else a}} for q, a in cfg["faqs"]],
    }

    html = head(cfg["title"], cfg["desc"], f)
    html += schema()
    html += '<script type="application/ld+json">' + json.dumps(breadcrumbs, ensure_ascii=False) + "</script>\n"
    html += '<script type="application/ld+json">' + json.dumps(faq_schema, ensure_ascii=False) + "</script>\n"
    html += header(f)
    html += f"""
<main id="main">

<section class="page-hero" aria-labelledby="page-title">
  <div class="wrap">
    <div>
      <ol class="crumbs reveal" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li>Services</li><li aria-current="page">{cfg["name"]}</li></ol>
      <span class="eyebrow reveal reveal-d1">{cfg["eyebrow"]}</span>
      <h1 class="display reveal reveal-d1" id="page-title" style="margin-top:28px">{cfg["h1"]}</h1>
      <p class="lead reveal reveal-d2">{cfg["lead"]}</p>
      <div class="hero__actions reveal reveal-d3">
        <a class="btn btn--light" href="get-a-quote.html?service={cfg["survey"]}">Request a Free Quote {ARROW}</a>
        <a class="btn btn--ghost" href="tel:{PHONE_TEL}" data-biz-href="tel">{PHONE} <span data-biz="phone">{PHONE_DISPLAY}</span></a>
      </div>
    </div>
    <div class="page-hero__media reveal reveal-d2">
      <span class="hero__outline" aria-hidden="true"></span>
      <div class="frame">{img(cfg["hero_img"][0], cfg["hero_img"][1], sizes="(max-width: 1024px) 90vw, 40vw", eager=True, pos=cfg["hero_img"][2])}</div>
    </div>
  </div>
</section>

<section class="section section--light" aria-labelledby="included-title">
  <div class="wrap detail">
    <div>
      <span class="eyebrow reveal">{cfg["inc_eyebrow"]}</span>
      <h2 class="h2 reveal reveal-d1" id="included-title">{cfg["inc_h2"]}</h2>
      {"".join(f'<p class="lead reveal reveal-d2">{p}</p>' for p in cfg["inc_copy"])}
    </div>
    <ul class="checklist reveal reveal-d2">{checklist}</ul>
  </div>
</section>

<section class="section section--ink" aria-labelledby="cards-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow reveal">{cfg["cards_eyebrow"]}</span>
        <h2 class="h2 reveal reveal-d1" id="cards-title">{cfg["cards_h2"]}</h2>
      </div>
      <p class="lead reveal reveal-d2">{cfg["cards_lead"]}</p>
    </div>
    <div class="signs">{cards}</div>
  </div>
</section>

<section class="section section--light" aria-labelledby="media-title">
  <div class="wrap detail detail--center">
    <div class="split-media">
      <figure class="reveal">{img(m1[0], m1[1], sizes="(max-width: 1024px) 50vw, 25vw", pos=m1[3])}<figcaption>{m1[2]}</figcaption></figure>
      <figure class="reveal reveal-d2">{img(m2[0], m2[1], sizes="(max-width: 1024px) 50vw, 25vw", pos=m2[3])}<figcaption>{m2[2]}</figcaption></figure>
    </div>
    <div>
      <span class="eyebrow reveal">{cfg["media_eyebrow"]}</span>
      <h2 class="h2 reveal reveal-d1" id="media-title">{cfg["media_h2"]}</h2>
      {"".join(f'<p class="lead reveal reveal-d2">{p}</p>' for p in cfg["media_copy"])}
      <div class="reveal reveal-d3" style="margin-top:40px"><a class="btn btn--dark" href="get-a-quote.html?service={cfg["survey"]}">Start Your Project {ARROW}</a></div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="process-title">
  <div class="wrap">
    <div class="section-head">
      <div>
        <span class="eyebrow reveal">Our process</span>
        <h2 class="h2 reveal reveal-d1" id="process-title">{cfg["process_h2"]}</h2>
      </div>
      <p class="lead reveal reveal-d2">{cfg["process_lead"]}</p>
    </div>
    {process(cfg["process"])}
  </div>
</section>

<section class="section section--paper" aria-label="Client review">
  <div class="wrap">
    <figure class="quote-band reveal">
      {STARS}
      <blockquote>&ldquo;{rtext}&rdquo;</blockquote>
      <figcaption><cite>{rname} &middot; Sydney</cite></figcaption>
    </figure>
  </div>
</section>

<section class="section section--light" aria-labelledby="faq-title">
  <div class="wrap">
    <div class="section-head section-head--center">
      <div>
        <span class="eyebrow reveal">FAQs</span>
        <h2 class="h2 reveal reveal-d1" id="faq-title">Frequently asked questions</h2>
      </div>
    </div>
    {faq(cfg["faqs"])}
  </div>
</section>

<section class="section section--light" style="padding-top:0" aria-labelledby="related-title">
  <div class="wrap">
    <h2 class="eyebrow reveal" id="related-title" style="margin-bottom:30px">Other services</h2>
    <div class="related">{related}</div>
  </div>
</section>

{contact_section(selected=cfg["name"], heading=cfg["contact_h2"])}
</main>
"""
    html += footer()
    write(f, html)


PAGES = [
    dict(
        file="bathroom-renovations.html",
        survey="bathroom",
        name="Bathroom Renovations",
        title="Bathroom Renovations Sydney | Complete Bathroom & Ensuite Renovations | OZTECH",
        desc="Complete bathroom and ensuite renovations across Sydney. Strip-out, waterproofing, tiling, plumbing and fit-off managed by one team with a fixed, itemised quote.",
        eyebrow="Complete bathroom &amp; ensuite renovations",
        h1="Bathroom renovations in Sydney",
        lead="A full renovation is the chance to get everything right: the layout, the waterproofing, the storage and the finishes. We manage the entire project, from the first measure to the final polish, so you get a bathroom that looks exceptional and is built to last.",
        hero_img=("14377", "Fully renovated bathroom with frameless walk-in shower, wall-hung mirror cabinet, white vanity and octagon mosaic floor", "50% 62%"),
        inc_eyebrow="What's included",
        inc_h2="What's included",
        inc_copy=[
            "A full bathroom renovation involves several trades working in the right order. We coordinate every stage so nothing falls through the gaps, and you have one point of contact the whole way through.",
            "Every quote is itemised, so you can see exactly what's included before work begins.",
        ],
        included=[
            ("Design guidance &amp; selections", "Help choosing a layout, tiles, vanity, tapware, screen and lighting that suit your space and budget."),
            ("Strip-out &amp; disposal", "Careful removal of the old bathroom, with floors and access paths protected throughout."),
            ("Plumbing &amp; electrical", "Rough-in and fit-off for new layouts, fixtures, lighting, exhaust fans and heated towel rails."),
            ("Waterproofing", "Wet-area waterproofing carried out to Australian Standard AS 3740 before a single tile goes down."),
            ("Floor &amp; wall tiling", "Precise setting-out, correct falls to the waste and clean, consistent grout lines."),
            ("Fit-off &amp; final clean", "Vanity, toilet, tapware, screen and accessories installed, then a thorough clean before handover."),
        ],
        cards_eyebrow="Why OZTECH",
        cards_h2="Why choose OZTECH",
        cards_lead="A great bathroom isn't just about looks. It's about how it works day to day, and how it holds up in ten years' time.",
        cards=[
            ("quote", "Fixed, itemised quotes", "Clear pricing up front. The price you approve is the price you pay."),
            ("drop", "Waterproofing first", "The most important part of any bathroom is the part you'll never see. We never cut corners on it."),
            ("ruler", "Precision tiling", "Careful setting-out means balanced cuts, straight lines and drainage falls that actually work."),
            ("team", "One point of contact", "No chasing multiple trades. One team takes ownership of your project from start to finish."),
            ("clock", "Realistic timelines", "An honest schedule at the start and regular updates as the job progresses."),
            ("home", "Respect for your home", "Protected floors, tidy work areas and a full clean before we hand back the keys."),
        ],
        media=(
            ("14377", "Renovated bathroom with frameless shower screen and black and white octagon mosaic floor", "After", "50% 70%"),
            ("14372", "Dated bathroom with gold-framed shower and old floor tiles before renovation", "Typical before", "50% 55%"),
        ),
        media_eyebrow="Transformations",
        media_h2="Before and after",
        media_copy=[
            "Framed shower cubicles, tired tiles and vanities that don't fit the space are some of the most common things we replace. With a well-planned layout, even a modest bathroom can feel open, bright and genuinely premium.",
            "Classic black and white, warm natural tones or a sleek modern finish. We'll help you land on a look that suits your home and stands the test of time.",
        ],
        process_h2="How your renovation works",
        process_lead="A clear sequence, regular updates and no surprises, so you always know where your project is up to.",
        process=[
            ("On-site consultation", "We measure the space, discuss how you use it and talk through ideas, layout options and budget."),
            ("Fixed quote &amp; selections", "You receive an itemised quote, then we help finalise tiles, fixtures and finishes."),
            ("Renovation", "Strip-out, rough-in, waterproofing, tiling and fit-off, completed in the right order and to standard."),
            ("Handover", "We walk through the finished bathroom with you, then clean up so it's ready to enjoy."),
        ],
        review=REVIEWS[0],
        faqs=[
            ("How much does a full bathroom renovation cost?", ["The cost depends on the size of the room, any layout or plumbing changes, the condition behind the existing finishes and the fixtures you choose.", "We provide a fixed, itemised quote after an on-site visit so you know exactly what's included."]),
            ("Can you change the layout of my bathroom?", "Often, yes. Moving a shower, toilet or vanity can make a big difference to how a room works. We'll look at the existing plumbing and structure on site and talk you through what's practical."),
            ("Do you renovate ensuites as well as main bathrooms?", "Yes. We renovate ensuites, main bathrooms and powder rooms. Smaller spaces benefit most from careful planning, and we'll help you make the most of every centimetre."),
            ("Will I need to choose all the fixtures myself?", "Only if you want to. We're happy to recommend tiles, tapware, vanities and screens that suit your space and budget, or work with selections you've already made."),
        ],
        contact_h2="Tell us about your bathroom",
    ),
    dict(
        file="shower-renovations.html",
        survey="shower",
        name="Shower Renovations",
        title="Shower Renovations Sydney | Walk-In Showers & Frameless Screens | OZTECH",
        desc="Shower renovations in Sydney: walk-in showers, frameless glass screens, shower-over-bath upgrades, niches and rail showers. Properly waterproofed and beautifully tiled.",
        eyebrow="Walk-in showers &amp; shower upgrades",
        h1="Shower renovations in Sydney",
        lead="Replace a cramped, framed cubicle or a tired shower-over-bath with something that feels open, modern and genuinely luxurious. We rebuild showers from the base up (waterproofing, falls, tiling, glass and tapware) so they look beautiful and drain perfectly.",
        hero_img=("14374", "Shower over bath with frameless glass panel, brushed nickel twin rail shower and handmade-look white wall tiles", "50% 45%"),
        inc_eyebrow="What we do",
        inc_h2="What we can do for your shower",
        inc_copy=[
            "A new shower can change the whole feel of a bathroom, without always needing to renovate the entire room.",
            "We'll help you choose the right configuration, glass and fixtures for your space, then build it properly from the base up.",
        ],
        included=[
            ("Walk-in &amp; open showers", "Frameless, open-plan showers with a single fixed panel for a clean, spacious look."),
            ("Shower-over-bath upgrades", "New tiling, rail showers and frameless bath screens that modernise the space."),
            ("Framed cubicle replacement", "Old aluminium-framed cubicles removed and replaced with a frameless design."),
            ("Recessed niches", "Built-in storage for shampoo and soap that sits flush with the wall. No more caddies."),
            ("Rail showers &amp; tapware", "Rain heads, hand showers and mixers in chrome, brushed nickel, matte black and more."),
            ("Waterproofing &amp; drainage", "A new waterproof membrane to AS 3740 with correct falls to a standard or linear drain."),
        ],
        cards_eyebrow="Options",
        cards_h2="Popular options",
        cards_lead="Every bathroom is different. Here are some of the most popular ways we transform a shower.",
        cards=[
            ("glass", "Frameless glass", "Clear, minimal glass panels and screens that make even a small room feel bigger."),
            ("shower", "Rain &amp; rail showers", "Overhead rain heads paired with handheld showers for comfort and easy cleaning."),
            ("tile", "Feature tiling", "Large-format, marble-look, handmade-style or mosaic, chosen to suit the room."),
            ("drop", "Linear drains", "A sleek strip drain allows a single floor fall and a seamless, step-free entry."),
            ("vanity", "Built-in niches", "Recessed shelving, tiled to line up perfectly with the surrounding wall."),
            ("spark", "Easy-clean finishes", "Smart tile and grout choices that keep your shower looking new for longer."),
        ],
        media=(
            ("14374", "Shower over bath after renovation with frameless glass panel and rail shower", "After", "50% 45%"),
            ("14377", "Frameless walk-in shower with marble-look tiles and twin rail shower", "Walk-in shower", "50% 45%"),
        ),
        media_eyebrow="Recent showers",
        media_h2="Frameless glass, clean tiling",
        media_copy=[
            "A frameless panel, a quality rail shower and well-chosen tiles can make a shower the standout feature of the room.",
            "Whether you want a walk-in shower with a single fixed panel or a refreshed shower-over-bath, we'll plan the layout, waterproofing and drainage so it looks good and works perfectly.",
        ],
        process_h2="How a shower renovation works",
        process_lead="A shower renovation is a focused project, but the steps behind the tiles matter just as much as in a full renovation.",
        process=[
            ("Assess &amp; advise", "We look at your current shower, the space available and what's achievable, then talk through options."),
            ("Quote &amp; select", "A fixed, itemised quote, plus help choosing glass, tapware, tiles and drainage."),
            ("Rebuild", "Strip-out, base preparation, waterproofing to AS 3740, tiling, glass and tapware installed."),
            ("Final check", "Water-tested, sealed, cleaned and ready for your first shower."),
        ],
        review=REVIEWS[1],
        faqs=[
            ("Can I convert my bath into a walk-in shower?", "In many bathrooms, yes. We'll check the space, plumbing and floor on site and let you know what's practical, including any changes needed to drainage."),
            ("What is a linear drain and do I need one?", "A linear drain is a long, slim drain that sits along one edge of the shower. It allows the floor to fall in one direction, which suits large-format tiles and step-free entries. It isn't essential, but it's a popular choice for a clean, modern look."),
            ("Can you replace just the shower without touching the rest of the bathroom?", "Often, yes. Depending on the layout, we can rebuild the shower area on its own. We'll take care to blend new work with the existing finishes as closely as possible, and let you know if a wider update would give a better result."),
            ("Is frameless glass hard to keep clean?", "Not at all. With fewer frames and tracks there are fewer places for grime to build up. A quick squeegee after showering keeps glass looking clear."),
        ],
        contact_h2="Tell us about your shower",
    ),
    dict(
        file="leaking-showers.html",
        survey="leaking",
        name="Leaking Showers",
        title="Leaking Shower Repairs Sydney | Re-Waterproofing & Shower Rebuilds | OZTECH",
        desc="Leaking shower repairs across Sydney. We find the source of the leak, remove failed waterproofing and rebuild your shower properly to Australian Standard AS 3740.",
        eyebrow="Leak repairs &amp; re-waterproofing",
        h1="Leaking shower repairs in Sydney",
        lead="A leaking shower rarely fixes itself, and the longer it goes, the more damage it can do to walls, floors and framing. We find where the water is getting through, remove what's failed and rebuild with compliant waterproofing, so the problem is solved rather than covered up.",
        hero_img=("14377", "Rebuilt shower with new waterproofing, marble-look tiles and frameless glass panel", "62% 38%"),
        inc_eyebrow="Our approach",
        inc_h2="Fixed properly, not patched over",
        inc_copy=[
            "Re-grouting or re-sealing can sometimes hide a leak for a while, but if the waterproof membrane underneath has failed, water will keep finding its way through.",
            "We'll be upfront about what's causing your leak and the right way to fix it, then do the work to a standard you won't need to think about again.",
        ],
        included=[
            ("Inspection &amp; diagnosis", "We assess the shower, surrounding walls and floor to understand where water is escaping."),
            ("Honest advice", "A clear explanation of what's failed and the options to fix it, with a fixed, itemised quote."),
            ("Strip-out of failed areas", "Removal of tiles, bedding and the old membrane back to a sound substrate."),
            ("Re-waterproofing", "A new waterproofing system installed to Australian Standard AS 3740, including corners, junctions and penetrations."),
            ("Retiling &amp; screen", "New tiles laid with correct falls to the waste, then the screen and fixtures refitted or replaced."),
            ("Making good", "Damaged adjacent areas (skirting, walls or flooring) repaired where needed so the finish is complete."),
        ],
        cards_eyebrow="Warning signs",
        cards_h2="Signs your shower is leaking",
        cards_lead="Leaks often start small and out of sight. If you notice any of these signs, it's worth having your shower checked sooner rather than later.",
        cards=[
            ("tile", "Loose or drummy tiles", "Tiles that sound hollow when tapped, move, crack or lift, especially on the shower floor."),
            ("grout", "Cracked or missing grout", "Grout that keeps crumbling, discolouring or cracking, even after it's been redone."),
            ("mould", "Mould &amp; mildew", "Persistent mould at the base of walls or in corners that returns soon after cleaning."),
            ("wall", "Stains on nearby walls", "Bubbling paint, water stains or damp patches on the other side of the shower wall."),
            ("home", "Swollen skirting or flooring", "Timber skirting, door frames, carpet or floorboards near the bathroom swelling or rotting."),
            ("nose", "Musty smell", "A damp, musty odour in or around the bathroom that won't go away."),
        ],
        media=(
            ("14372", "Older bathroom with aluminium-framed shower cubicle, a common source of leaks", "Typical older shower", "50% 50%"),
            ("14377", "Rebuilt shower area with new waterproofing, tiling and frameless glass", "Rebuilt properly", "50% 50%"),
        ),
        media_eyebrow="Why showers leak",
        media_h2="The problem is usually under the tiles",
        media_copy=[
            "In older bathrooms the waterproof membrane can break down over time, particularly at the junctions between walls and floor, around the waste and at the shower hob. Movement, poor falls and failed seals all add to the problem.",
            "Once water gets past the membrane, it can travel into walls, subfloors and neighbouring rooms. Rebuilding the shower with a new, compliant waterproofing system is the reliable long-term fix, and a chance to modernise the shower at the same time.",
        ],
        process_h2="How we fix a leaking shower",
        process_lead="We take the guesswork out of leaking showers with a clear, step-by-step approach.",
        process=[
            ("Inspect", "We check the shower, waste, junctions and surrounding areas for signs of water escaping."),
            ("Explain &amp; quote", "You'll get a clear explanation of the cause and a fixed, itemised quote to fix it properly."),
            ("Rebuild", "Failed areas removed, new waterproofing applied to AS 3740, then retiled with correct falls."),
            ("Test &amp; finish", "Water-tested, sealed, cleaned and back in use, with nearby damage made good."),
        ],
        review=REVIEWS[1],
        faqs=[
            ("Can a leaking shower be fixed without removing the tiles?", ["Sometimes a failed silicone joint or a damaged grout line is the culprit, and that can be repaired without retiling. But if the waterproof membrane underneath has failed, re-grouting or sealing over the top usually only delays the problem.", "We'll tell you honestly what's going on and what will actually fix it."]),
            ("How do I know if my shower is leaking?", "Common signs include loose or drummy tiles, cracked grout, recurring mould, stains or bubbling paint on nearby walls, swollen skirting boards and a musty smell. If you notice any of these, it's worth getting it checked."),
            ("Is a leaking shower urgent?", "It's best not to wait. Ongoing leaks can damage wall framing, subfloors and neighbouring rooms, and the cost of repair generally grows the longer water is getting through."),
            ("Can you upgrade the shower while fixing the leak?", "Absolutely. Because the shower is being rebuilt anyway, it's a great time to switch to a frameless screen, add a niche, change tiles or upgrade tapware."),
        ],
        contact_h2="Tell us about your shower",
    ),
    dict(
        file="partial-renovations.html",
        survey="partial",
        name="Partial Renovations",
        title="Partial Bathroom Renovations Sydney | Bathroom Updates & Refreshes | OZTECH",
        desc="Partial bathroom renovations in Sydney. Update tiles, vanities, tapware, screens and lighting without a full strip-out. A high-end refresh on a tighter budget or timeline.",
        eyebrow="Targeted bathroom updates",
        h1="Partial bathroom renovations in Sydney",
        lead="Not every bathroom needs to be gutted. If the bones are sound, a targeted update (new wall tiles, a vanity, tapware, a screen or lighting) can make the room feel new for a fraction of the disruption. We'll help you decide what to change, and what's worth keeping.",
        hero_img=("14374", "Bathroom after partial renovation with new wall tiles, rail shower and frameless glass panel", "50% 45%"),
        inc_eyebrow="What we can update",
        inc_h2="Change what matters, keep what works",
        inc_copy=[
            "A partial renovation focuses on the elements that make the biggest difference. Done well, it can transform the look and feel of a bathroom, without the time and cost of a complete rebuild.",
            "We'll give you honest advice on what's in good condition and what should be replaced, so you're spending where it counts.",
        ],
        included=[
            ("Wall retiling", "New wall tiles in the shower or bath area to completely change the look of the room."),
            ("Vanity &amp; mirror upgrades", "A new vanity, basin, mirror or shaving cabinet for better storage and a fresh feel."),
            ("Tapware &amp; shower heads", "Modern mixers, rail showers and spouts in the finish of your choice."),
            ("Frameless screens", "Replace dated framed screens or shower curtains with clear, frameless glass."),
            ("Toilets &amp; accessories", "New toilet suites, towel rails, heated rails, toilet roll holders and robe hooks."),
            ("Lighting &amp; ventilation", "Updated lighting and exhaust fans for a brighter, fresher bathroom."),
        ],
        cards_eyebrow="Is a partial reno right for you?",
        cards_h2="When a partial renovation makes sense",
        cards_lead="A partial renovation is often the best value option, but only when the conditions are right. Here's when it makes sense.",
        cards=[
            ("drop", "No signs of leaks", "The existing waterproofing is performing, with no drummy tiles, damp or stains nearby."),
            ("home", "The layout works", "You're happy with where the shower, toilet and vanity sit, and don't need to move plumbing."),
            ("tile", "Floors are sound", "Floor tiles are in good condition and a style you can work with or happily keep."),
            ("clock", "You need it done sooner", "A focused scope means less time with your bathroom out of action."),
            ("quote", "Budget matters", "Spend on the changes you'll notice most, without paying for a full strip-out."),
            ("spark", "Preparing to sell or lease", "A fresh, modern bathroom can make a big difference to how a property presents."),
        ],
        media=(
            ("14376", "Bathroom before partial renovation with dated white wall tiles", "Before", "50% 55%"),
            ("14374", "Same bathroom after partial renovation with new wall tiles, rail shower and frameless panel", "After", "50% 55%"),
        ),
        media_eyebrow="Before &amp; after",
        media_h2="Same layout, new finish",
        media_copy=[
            "In this Sydney bathroom the layout and floor stayed as they were. New handmade-look wall tiles, a brushed nickel rail shower and a frameless panel completely changed the feel of the room.",
            "Where tiles are removed in wet areas, we re-waterproof before retiling, so a partial renovation is still built to last.",
        ],
        process_h2="How a partial renovation works",
        process_lead="Smaller scope doesn't mean lower standards. Every partial renovation gets the same care and attention to detail.",
        process=[
            ("Walk-through", "We look at your bathroom together and talk about what you'd like to change, and what can stay."),
            ("Scope &amp; quote", "A clear, fixed quote for exactly the work agreed, with help selecting new fixtures and finishes."),
            ("Update", "Careful removal, any required waterproofing, then tiling, installation and fit-off."),
            ("Reveal", "A final clean and walk-through of your refreshed bathroom."),
        ],
        review=REVIEWS[2],
        faqs=[
            ("What's the difference between a partial and a full renovation?", "A full renovation strips the bathroom back completely and rebuilds everything. A partial renovation updates selected elements (for example wall tiles, vanity, tapware or screen) while keeping things that are in good condition, such as the floor or layout."),
            ("Can you match new tiles to my existing ones?", "Exact matches can be hard to find, particularly with older tiles. Often a better result comes from choosing a complementary tile that works with what's staying. We'll talk through the options with you."),
            ("Will I still need waterproofing?", "If we're removing tiles in a wet area such as a shower or over a bath, yes. We re-waterproof those areas before retiling. It's an essential step that we never skip."),
            ("What if you find a problem once work starts?", "If we uncover something unexpected, like a failed membrane or water damage, we'll stop, show you, and talk through the options before going any further. Nothing extra happens without your approval."),
        ],
        contact_h2="Tell us about your bathroom",
    ),
]


# =====================================================================
# LEGAL
# =====================================================================
def legal_page(fname, name, title, desc, intro, sections):
    toc = "".join(f'<li><a href="#{sid}">{h}</a></li>' for sid, h, _ in sections)
    body = "".join(f'<h2 id="{sid}">{h}</h2>{content}' for sid, h, content in sections)
    html = head(title, desc, fname)
    html += header(fname, has_form=False)
    html += f"""
<main id="main">
<section class="page-hero page-hero--text" aria-labelledby="page-title">
  <div class="wrap">
    <div>
      <ol class="crumbs reveal" aria-label="Breadcrumb"><li><a href="index.html">Home</a></li><li aria-current="page">{name}</li></ol>
      <span class="eyebrow reveal reveal-d1">Legal</span>
      <h1 class="display reveal reveal-d1" id="page-title" style="margin-top:28px">{name}</h1>
      <p class="lead reveal reveal-d2" style="margin-bottom:0">{intro}</p>
    </div>
  </div>
</section>
<section class="section section--light">
  <div class="wrap legal">
    <aside class="legal__toc" aria-label="On this page"><p>On this page</p><ol>{toc}</ol></aside>
    <article class="prose">
      <span class="legal__updated">Last updated: 8 November 2026</span>
      {body}
    </article>
  </div>
</section>
</main>
"""
    html += footer(has_form=False)
    write(fname, html)


CONTACT_BLOCK = f"""<p><strong data-biz="business_name">OZTECH Bathrooms</strong><br>Sydney, NSW, Australia<br>Phone: <a href="tel:{PHONE_TEL}" data-biz-href="tel" data-biz="phone">{PHONE_DISPLAY}</a><br>Email: <a href="mailto:{EMAIL}" data-biz-href="mailto" data-biz="email">{EMAIL}</a></p>"""

PRIVACY = [
    ("overview", "Overview", """<p>OZTECH Bathrooms (&ldquo;OZTECH&rdquo;, &ldquo;we&rdquo;, &ldquo;us&rdquo; or &ldquo;our&rdquo;) respects your privacy. This Privacy Policy explains how we collect, use, store and disclose your personal information when you visit our website, contact us, request a quote or engage us to carry out work.</p>
<p>We handle personal information in accordance with the <em>Privacy Act 1988</em> (Cth) and the Australian Privacy Principles (APPs), to the extent they apply to our business. By using our website or providing us with your personal information, you agree to it being handled as described in this policy.</p>"""),
    ("collect", "Information we collect", """<p>The personal information we collect depends on how you interact with us. It may include:</p>
<ul>
<li>your name, phone number, email address and postal or site address;</li>
<li>details about your property and project, including photos, measurements and preferences you share with us;</li>
<li>information you provide in enquiries, quote requests, emails, phone calls or messages;</li>
<li>billing and payment details needed to invoice and receive payment for our services;</li>
<li>feedback and reviews you choose to provide; and</li>
<li>technical information about your visit to our website, such as your browser type, device, pages viewed and approximate location, collected through cookies and similar technologies.</li>
</ul>
<p>We do not intentionally collect sensitive information (such as health information). Please do not send us sensitive information unless it is necessary for us to provide our services.</p>"""),
    ("how", "How we collect it", """<p>We collect personal information directly from you wherever reasonably practicable, for example, when you fill in our quote form, phone or email us, meet us on site or engage us to complete work. We may also collect information from third parties such as builders, real estate agents, strata managers or other people you have authorised to deal with us on your behalf.</p>
<p>When you submit a quote request or enquiry through our website, the details you enter are stored securely by our website hosting and database provider and sent to us by email through our email delivery provider, so we can respond to you.</p>"""),
    ("use", "How we use your information", """<p>We use personal information to:</p>
<ul>
<li>respond to your enquiries and provide quotes;</li>
<li>arrange site visits, plan, schedule and carry out renovation work;</li>
<li>communicate with you about your project, including progress updates;</li>
<li>issue invoices, process payments and keep business records;</li>
<li>manage warranties, defects and after-care;</li>
<li>improve our website, services and customer experience;</li>
<li>comply with our legal and regulatory obligations; and</li>
<li>with your consent, send you occasional information about our services. You can opt out at any time.</li>
</ul>"""),
    ("disclose", "Disclosure to third parties", """<p>We do not sell your personal information. We may disclose it to:</p>
<ul>
<li>tradespeople, contractors and suppliers who help us deliver your project (for example plumbers, electricians, glaziers and product suppliers);</li>
<li>certifiers, insurers and government authorities where required for your project or by law;</li>
<li>service providers who support our business, such as accounting, IT, website hosting and email providers; and</li>
<li>professional advisers, such as lawyers and accountants.</li>
</ul>
<p>We only share what is reasonably necessary, and we expect those parties to handle your information appropriately. Some of our service providers (for example cloud email or hosting services) may store data outside Australia. Where this occurs, we take reasonable steps to ensure your information is protected.</p>"""),
    ("photos", "Project photos", """<p>We may photograph our work before, during and after a project for quality records and to show examples of our work on our website and social media. We take care not to include personal items, people or identifying details such as street numbers in photos we publish. If you would prefer that photos of your project are not published, just let us know.</p>"""),
    ("cookies", "Cookies &amp; analytics", """<p>Our website may use cookies and similar technologies to make the site work, remember your preferences and understand how visitors use it. We may use third-party services, such as web analytics or font providers, which may collect technical information like your IP address and browser details.</p>
<p>You can set your browser to refuse or delete cookies. Some parts of the website may not work as intended if you do.</p>"""),
    ("security", "Storage &amp; security", """<p>We take reasonable steps to protect personal information from misuse, interference, loss, unauthorised access, modification and disclosure. When information is no longer needed for any purpose for which it may be used or disclosed, and we are not required by law to keep it, we take reasonable steps to destroy or de-identify it.</p>
<p>No method of transmitting information over the internet is completely secure, so we cannot guarantee the security of information you send to us online.</p>"""),
    ("access", "Access &amp; correction", """<p>You can ask to access the personal information we hold about you, or ask us to correct it if you believe it is inaccurate, out of date or incomplete. Please contact us using the details below. We will respond within a reasonable time and may need to verify your identity first. In limited circumstances permitted by law we may decline a request, and if so we will explain why.</p>"""),
    ("complaints", "Complaints", """<p>If you have a concern about how we have handled your personal information, please contact us first so we can try to resolve it. If you are not satisfied with our response, you may contact the Office of the Australian Information Commissioner (OAIC) at <a href="https://www.oaic.gov.au" rel="noopener" target="_blank">www.oaic.gov.au</a>.</p>"""),
    ("changes", "Changes to this policy", """<p>We may update this Privacy Policy from time to time. The current version will always be available on this page, with the date it was last updated shown at the top.</p>"""),
    ("contact", "Contact us", "<p>For privacy questions, access requests or complaints, please contact:</p>" + CONTACT_BLOCK),
]

TERMS = [
    ("acceptance", "Acceptance of these terms", """<p>These Terms of Use apply to your use of the OZTECH Bathrooms website (the &ldquo;website&rdquo;). By accessing or using the website, you agree to these terms. If you do not agree, please do not use the website.</p>
<p>These terms govern the website only. Any renovation or repair work we carry out for you will be governed by a separate written quote and contract, which will take precedence over anything on this website.</p>"""),
    ("info", "Website information", """<p>The content on this website is general information about our business and services. While we take care to keep it accurate and current, we do not warrant that it is complete, accurate or up to date, and it may change without notice.</p>
<p>Information on this website is not professional advice for your specific situation. Every bathroom is different, so please contact us so we can assess your project in person.</p>"""),
    ("quotes", "Quotes &amp; pricing", """<p>Nothing on this website is an offer to carry out work at a particular price. Any price, estimate or timeframe is only binding once it is set out in a written quote or contract issued by OZTECH Bathrooms following an assessment of your project. Quotes are valid for the period stated on them.</p>"""),
    ("images", "Images &amp; examples", """<p>Photos on this website show examples of bathrooms and work stages. Finished results depend on the specific space, products and selections for each project, and products shown may vary in colour, finish or availability.</p>"""),
    ("ip", "Intellectual property", """<p>Unless otherwise indicated, all content on this website (including text, photographs, graphics, logos and the OZTECH Bathrooms name and branding) is owned by or licensed to OZTECH Bathrooms and is protected by Australian and international intellectual property laws.</p>
<p>You may view and print pages for your own personal, non-commercial use. You must not copy, reproduce, republish, modify or distribute any content without our prior written permission.</p>"""),
    ("use", "Acceptable use", """<p>You agree not to:</p>
<ul>
<li>use the website in any way that breaches any law or the rights of any person;</li>
<li>submit false, misleading or offensive information through the website;</li>
<li>attempt to gain unauthorised access to the website, its servers or any connected systems; or</li>
<li>introduce viruses, malicious code or anything else that may damage or interfere with the website.</li>
</ul>"""),
    ("links", "Third-party links", """<p>The website may contain links to third-party websites. These are provided for convenience only. We do not control and are not responsible for the content, availability or privacy practices of those websites.</p>"""),
    ("liability", "Limitation of liability", """<p>Nothing in these terms excludes, restricts or modifies any consumer guarantee, right or remedy you may have under the <em>Australian Consumer Law</em> or any other law that cannot be excluded.</p>
<p>Subject to that, and to the maximum extent permitted by law, OZTECH Bathrooms is not liable for any loss or damage (including indirect or consequential loss) arising from your use of, or reliance on, this website or its content, or from the website being unavailable.</p>"""),
    ("privacy", "Privacy", """<p>Our handling of personal information is described in our <a href="privacy-policy.html">Privacy Policy</a>.</p>"""),
    ("law", "Governing law", """<p>These terms are governed by the laws of New South Wales, Australia. You submit to the non-exclusive jurisdiction of the courts of New South Wales.</p>"""),
    ("changes", "Changes to these terms", """<p>We may update these Terms of Use at any time by publishing a revised version on this page. Your continued use of the website after any change means you accept the updated terms.</p>"""),
    ("contact", "Contact us", "<p>If you have any questions about these terms, please contact:</p>" + CONTACT_BLOCK),
]


# =====================================================================
# GET A QUOTE (step-by-step survey)
# =====================================================================
SVC_ICONS = {
    "bathroom": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M3 12h18v2a5 5 0 01-5 5H8a5 5 0 01-5-5z"/><path d="M5 12V5.5A2.5 2.5 0 017.5 3 2.5 2.5 0 0110 5.5M7 19l-1 2M17 19l1 2"/></svg>',
    "shower": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M4 21V6a3 3 0 013-3h1a3 3 0 013 3v1"/><path d="M8 7h6M9 11v1M11.5 11v1.5M14 11v1M10 15v1M13 15v1"/></svg>',
    "leaking": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M12 3s6 6.8 6 11a6 6 0 01-12 0c0-4.2 6-11 6-11z"/><path d="M9.5 15a2.5 2.5 0 002.5 2.5"/></svg>',
    "partial": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><rect x="3" y="3" width="8" height="8"/><rect x="13" y="3" width="8" height="8"/><rect x="3" y="13" width="8" height="8"/><path d="M13 17h8M17 13v8"/></svg>',
    "ensuite": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M5 21V4a1 1 0 011-1h12a1 1 0 011 1v17"/><path d="M3 21h18M15 12h1"/></svg>',
    "other": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 114 2c-.9.6-1.5 1.1-1.5 2.2M12 16.5v.5"/></svg>',
}
TIME_ICONS = {
    "asap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M13 2L5 13.5h6L10 22l8-11.5h-6z"/></svg>',
    "month": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4M8 13.5h2"/></svg>',
    "quarter": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4M8 13.5h2M12 13.5h2M16 13.5h.5M8 17h2"/></svg>',
    "half": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>',
    "research": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5L21 21"/></svg>',
}
DONE_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.1" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
BACK = '<svg viewBox="0 0 16 10" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M16 5H1M5 1L1 5l4 4"/></svg>'
TICK = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><path d="M2.5 6.2l2.3 2.3 4.7-4.9"/></svg>'

SURVEY_SERVICES = [
    ("bathroom", "Full bathroom renovation", "Complete strip-out and rebuild"),
    ("ensuite", "Ensuite renovation", "Upgrade your private bathroom"),
    ("shower", "Shower renovation", "Walk-in shower, screen or shower-over-bath"),
    ("leaking", "Leaking shower repair", "Find the leak and fix it properly"),
    ("partial", "Partial renovation", "New tiles, vanity, tapware or screen"),
    ("other", "Not sure yet", "Talk it through with us"),
]
SURVEY_TIMES = [
    ("asap", "As soon as possible", "Ready to go now"),
    ("month", "Within the next month", ""),
    ("quarter", "In 1 to 3 months", ""),
    ("half", "In 3 to 6 months", ""),
    ("research", "Just researching for now", "Planning ahead"),
]


def option(key, label, sub, icon):
    sub_html = f'<span class="option__sub">{sub}</span>' if sub else ""
    return (f'<button type="button" class="option" data-key="{key}"><span class="option__icon">{icon}</span>'
            f'<span><span class="option__label">{label}</span>{sub_html}</span><span class="option__check">{TICK}</span></button>')


def quote_page():
    svc = "".join(option(k, l, s, SVC_ICONS[k]) for k, l, s in SURVEY_SERVICES)
    tm = "".join(option(k, l, s, TIME_ICONS[k]) for k, l, s in SURVEY_TIMES)
    html = head("Get a Free Quote | OZTECH Bathrooms Sydney",
                "Get a free, no-obligation quote for your bathroom renovation, shower renovation or leaking shower repair in Sydney. Takes less than a minute.",
                "get-a-quote.html")
    html += header("get-a-quote.html")
    html += f"""
<main id="main">
<section class="quote-page" aria-labelledby="quote-title">
  <div class="wrap">
    <div class="quote-intro">
      <span class="eyebrow">Takes about 30 seconds</span>
      <h1 class="h2" id="quote-title">Get a free quote</h1>
    </div>

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
        <h2 class="survey__q" id="q3" tabindex="-1">Where should we send your quote?</h2>
        <p class="survey__hint">We'll be in touch within one business day to arrange a free on-site visit.</p>
        <form class="form" id="survey-form" novalidate>
          <div class="field"><label for="s-name">Full name</label><input id="s-name" name="name" type="text" autocomplete="name" placeholder="Your name" required minlength="2"></div>
          <div class="field"><label for="s-email">Email</label><input id="s-email" name="email" type="email" autocomplete="email" placeholder="you@email.com" required></div>
          <div class="field"><label for="s-phone">Phone</label><input id="s-phone" name="phone" type="tel" autocomplete="tel" placeholder="04xx xxx xxx" required minlength="8"></div>
          <div class="field"><label for="s-postcode">Postcode</label><input id="s-postcode" name="postcode" type="text" inputmode="numeric" autocomplete="postal-code" placeholder="e.g. 2000" required pattern="[0-9]{{4}}" maxlength="4"></div>
          <div class="hp-field" aria-hidden="true"><label for="s-company">Company</label><input id="s-company" name="company" type="text" tabindex="-1" autocomplete="off"></div>
          <button class="btn btn--dark" type="submit">Get My Free Quote {ARROW}</button>
          <p class="form__status" role="status" aria-live="polite"></p>
          <p class="form__note">Your details are only used to respond to your enquiry. See our <a href="privacy-policy.html">Privacy Policy</a>.</p>
        </form>
      </div>

      <div class="survey__step survey__done" aria-labelledby="q4">
        <div class="survey__done-icon">{DONE_ICON}</div>
        <h2 class="survey__q" id="q4" tabindex="-1">Thank you, we&rsquo;ve got it.</h2>
        <p>We'll review your details and be in touch within one business day to arrange your free on-site quote.</p>
        <div class="hero__actions">
          <a class="btn btn--dark" href="tel:{PHONE_TEL}" data-biz-href="tel">{PHONE} <span data-biz="phone">{PHONE_DISPLAY}</span></a>
          <a class="btn btn--ghost-dark" href="index.html">Back to Home</a>
        </div>
      </div>
    </div>

    <ul class="quote-trust">
      <li>{DOC} Fixed, itemised quotes</li>
      <li>{SHIELD} Waterproofing to AS 3740</li>
      <li>{PIN} Servicing all of Sydney</li>
    </ul>
  </div>
</section>
</main>
"""
    html += footer().replace('<script src="assets/js/main.js" defer></script>',
                             '<script src="assets/js/main.js" defer></script>\n<script src="assets/js/quote.js" defer></script>')
    write("get-a-quote.html", html)


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
