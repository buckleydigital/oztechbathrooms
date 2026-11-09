"""Website content for OZTECH Bathrooms: copy, services, reviews, FAQs, legal text.

Edit wording here, then run: python3 tools/build_site.py
"""

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



HOME_FAQS = [        ("How much does a bathroom renovation cost in Sydney?", ["Every bathroom is different. The size of the room, the condition behind the tiles, plumbing changes and the fixtures you choose all affect the price. That's why we quote after seeing the space in person.", "After an on-site visit you'll receive a fixed, itemised quote so you know exactly what's included before any work begins."]),
    ("How long does a full bathroom renovation take?", "Timeframes depend on scope, but we give you a realistic schedule up front and keep you updated at every stage. Waterproofing needs proper curing time, and we never rush it. It's the part of a bathroom you can't see but rely on most."),
    ("Is waterproofing included?", "Yes. Waterproofing is included in every renovation that involves wet areas, and it's done before any tiling starts. We never skip it or cut corners on it."),
    ("Do I need to supply my own fixtures and tiles?", "You can, but you don't have to. We're happy to help you choose tiles, tapware, vanities and screens that suit your space, style and budget, or work with selections you've already made."),
    ("Can I use my bathroom during the renovation?", "For a full renovation the room will be out of action while we work. If it's your only bathroom, talk to us during the quote and we'll plan the schedule to keep the disruption as short as possible."),
    ("Do you clean up afterwards?", "Always. We protect floors and access paths during the job, keep the site tidy as we go and finish with a thorough clean, so your new bathroom is ready to use."),
]


PAGES = [
    dict(
        file="bathroom-renovations.html",
        survey="bathroom",
        name="Bathroom Renovations",
        title="Bathroom Renovations Sydney | Complete Bathroom & Ensuite Renovations | OZTECH",
        desc="Complete bathroom and ensuite renovations across Sydney. Strip-out, waterproofing, tiling, plumbing and fit-off managed by one team with a fixed, itemised quote.",
        eyebrow="Complete bathroom &amp; ensuite renovations",
        h1="Bathroom renovations in Sydney",
        lead="A full renovation is the chance to get everything right: the layout, the waterproofing, the storage and the finishes. We manage the entire project, from the first measure to the final polish, so the finished bathroom looks good and lasts.",
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
            ("Waterproofing", "Full wet-area waterproofing, done before a single tile goes down."),
            ("Floor &amp; wall tiling", "Precise setting-out, correct falls to the waste and clean, consistent grout lines."),
            ("Fit-off &amp; final clean", "Vanity, toilet, tapware, screen and accessories installed, then a thorough clean before handover."),
        ],
        cards_eyebrow="Why OZTECH",
        cards_h2="Why choose OZTECH",
        cards_lead="A good bathroom isn't just about looks. It needs to work day to day and still hold up in ten years' time.",
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
        media_eyebrow="Our work",
        media_h2="Before and after",
        media_copy=[
            "Framed shower cubicles, tired tiles and vanities that don't fit the space are some of the most common things we replace. With a well-planned layout, even a small bathroom can feel open and bright.",
            "Classic black and white, warm natural tones or a sleek modern finish. We'll help you choose a look that suits your home and won't date quickly.",
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
        desc="Shower renovations in Sydney: walk-in showers, frameless glass screens, shower-over-bath upgrades, niches and rail showers. Properly waterproofed and tiled.",
        eyebrow="Walk-in showers &amp; shower upgrades",
        h1="Shower renovations in Sydney",
        lead="Replace a cramped framed cubicle or a tired shower-over-bath with something open and easy to clean. We rebuild showers from the base up, including waterproofing, falls, tiling, glass and tapware, so they look good and drain properly.",
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
            ("Waterproofing &amp; drainage", "A new waterproof membrane with correct falls to a standard or linear drain."),
        ],
        cards_eyebrow="Options",
        cards_h2="Popular options",
        cards_lead="Every bathroom is different. These are the upgrades we're asked for most.",
        cards=[
            ("glass", "Frameless glass", "Clear, minimal glass panels and screens that make even a small room feel bigger."),
            ("shower", "Rain &amp; rail showers", "Overhead rain heads paired with handheld showers for comfort and easy cleaning."),
            ("tile", "Feature tiling", "Large-format, marble-look, handmade-style or mosaic, chosen to suit the room."),
            ("drop", "Linear drains", "A long strip drain allows a single floor fall and a step-free entry."),
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
            "A frameless panel, a good rail shower and the right tiles make a big difference to how a bathroom looks and works.",
            "Whether you want a walk-in shower with a single fixed panel or a refreshed shower-over-bath, we'll plan the layout, waterproofing and drainage so it looks good and works properly.",
        ],
        process_h2="How a shower renovation works",
        process_lead="A shower renovation is a focused project, but the steps behind the tiles matter just as much as in a full renovation.",
        process=[
            ("Assess &amp; advise", "We look at your current shower, the space available and what's achievable, then talk through options."),
            ("Quote &amp; select", "A fixed, itemised quote, plus help choosing glass, tapware, tiles and drainage."),
            ("Rebuild", "Strip-out, base preparation, waterproofing, tiling, glass and tapware installed."),
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
        desc="Leaking shower repairs across Sydney. We find the source of the leak, remove failed waterproofing and rebuild your shower properly.",
        eyebrow="Leak repairs &amp; re-waterproofing",
        h1="Leaking shower repairs in Sydney",
        lead="A leaking shower rarely fixes itself, and the longer it goes, the more damage it can do to walls, floors and framing. We find where the water is getting through, remove what's failed and rebuild with new waterproofing, so the problem is solved rather than covered up.",
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
            ("Re-waterproofing", "A new waterproofing system installed, including corners, junctions and penetrations."),
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
            "Once water gets past the membrane, it can travel into walls, subfloors and neighbouring rooms. Rebuilding the shower with a new waterproofing system is the reliable long-term fix, and a chance to modernise the shower at the same time.",
        ],
        process_h2="How we fix a leaking shower",
        process_lead="Here's how we deal with a leaking shower, step by step.",
        process=[
            ("Inspect", "We check the shower, waste, junctions and surrounding areas for signs of water escaping."),
            ("Explain &amp; quote", "You'll get a clear explanation of the cause and a fixed, itemised quote to fix it properly."),
            ("Rebuild", "Failed areas removed, new waterproofing applied, then retiled with correct falls."),
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
        desc="Partial bathroom renovations in Sydney. Update tiles, vanities, tapware, screens and lighting without a full strip-out. A practical option when the budget or timeframe is tighter.",
        eyebrow="Targeted bathroom updates",
        h1="Partial bathroom renovations in Sydney",
        lead="Not every bathroom needs to be gutted. If the bones are sound, a targeted update (new wall tiles, a vanity, tapware, a screen or lighting) can make the room feel new for a fraction of the disruption. We'll help you decide what to change, and what's worth keeping.",
        hero_img=("14374", "Bathroom after partial renovation with new wall tiles, rail shower and frameless glass panel", "50% 45%"),
        inc_eyebrow="What we can update",
        inc_h2="Change what matters, keep what works",
        inc_copy=[
            "A partial renovation focuses on the elements that make the biggest difference. Done well, it can change the look of a bathroom without the time and cost of a complete rebuild.",
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
            ("Handover", "A final clean and a walk-through of the finished work with you."),
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
    ("ensuite", "Ensuite renovation", "Bathroom off the main bedroom"),
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

