# OZTECH Bathrooms: Website

Static website for OZTECH Bathrooms, Sydney. No build step: open `index.html` or upload the folder to any static host.

## Pages
- `index.html`: Home
- `bathroom-renovations.html`, `shower-renovations.html`, `leaking-showers.html`, `partial-renovations.html`: Services
- `privacy-policy.html`, `terms.html`: Legal

Shared styles and scripts live in `assets/css/styles.css` and `assets/js/main.js`. Optimised images are in `assets/img/`.

## Before going live
- **Email:** replace the placeholder `info@oztechbathrooms.com.au` across all `.html` files if it isn't correct.
- **Contractor licence:** NSW requires your contractor licence number on advertising for residential building work: add it to the footer.
- **Quote form:** currently opens the visitor's email app pre-filled (sent to the address in the form's `data-mailto`). To receive submissions directly, connect a form service such as Formspree or Netlify Forms.
- **Legal pages:** general templates: have them reviewed for your business.
