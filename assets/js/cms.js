/* OZTECH Bathrooms: content runtime
 *
 * The HTML on each page holds the default content. This script loads the
 * admin's saved overrides from Supabase (copy, images, links, hidden
 * sections, SEO, business information and custom sections) and applies
 * them over the defaults. If Supabase can't be reached the defaults stay.
 *
 * Inside the admin page editor (?cms-edit=1 in a same-origin iframe) it
 * also makes the page editable and talks to the admin via postMessage.
 */
(function () {
  "use strict";

  var CFG = window.OZTECH_CONFIG || {};
  var EDIT = /[?&]cms-edit=1\b/.test(location.search) && window.parent !== window;
  var PAGE = pageName();
  var CACHE_KEY = "oztech-cms:v1:" + PAGE;

  function pageName() {
    var f = location.pathname.split("/").pop() || "index.html";
    f = f.replace(/\.html?$/i, "");
    return f || "index";
  }

  /* ---------- Helpers ---------- */
  function hash(str) {
    var h = 0x811c9dc5;
    for (var i = 0; i < str.length; i++) {
      h ^= str.charCodeAt(i);
      h = (h + ((h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24))) >>> 0;
    }
    return h.toString(36);
  }
  function norm(s) { return String(s || "").replace(/\s+/g, " ").trim(); }
  function esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  // Escape, then allow *italic* and line breaks.
  function fmt(s) {
    return esc(s).replace(/\*([^*\n]+)\*/g, "<em>$1</em>").replace(/\n/g, "<br>");
  }
  function paras(s) {
    return String(s || "").split(/\n\s*\n/).map(function (p) { return p.trim(); })
      .filter(Boolean).map(function (p) { return "<p>" + fmt(p) + "</p>"; }).join("");
  }
  function safeUrl(u) {
    u = String(u || "").trim();
    if (!u) return "";
    if (/^(javascript|data|vbscript):/i.test(u)) return "";
    return u;
  }
  function sanitize(html) {
    var tpl = document.createElement("template");
    tpl.innerHTML = String(html || "");
    var bad = tpl.content.querySelectorAll("script,style,iframe,object,embed,link,meta,form,input,textarea,select,button");
    bad.forEach(function (n) { n.remove(); });
    tpl.content.querySelectorAll("*").forEach(function (n) {
      Array.prototype.slice.call(n.attributes).forEach(function (a) {
        var name = a.name.toLowerCase();
        if (name.indexOf("on") === 0) n.removeAttribute(a.name);
        if ((name === "href" || name === "src" || name === "xlink:href") && !safeUrl(a.value)) n.removeAttribute(a.name);
        if (name === "contenteditable" || name === "data-cms-k") n.removeAttribute(a.name);
      });
    });
    return tpl.innerHTML;
  }

  /* ---------- Index editable content on the pristine DOM ---------- */
  var SKIP = { SCRIPT: 1, STYLE: 1, SVG: 1, OPTION: 1, SELECT: 1, TEXTAREA: 1, INPUT: 1, NOSCRIPT: 1, TEMPLATE: 1, PICTURE: 1, SOURCE: 1 };
  var texts = [];   // {key, el, original}
  var images = [];  // {key, el, src, srcset, sizes, alt, sources}
  var counts = {};

  function isGlobal(el) {
    return el.matches("header.site-header, footer.site-footer, .drawer, .mobile-bar");
  }
  function hasDirectText(el) {
    for (var n = el.firstChild; n; n = n.nextSibling) {
      if (n.nodeType === 3 && n.nodeValue.trim()) return true;
    }
    return false;
  }
  function skip(el) {
    if (SKIP[el.tagName.toUpperCase()]) return true;
    return el.hasAttribute("data-biz") || el.hasAttribute("data-cms-skip") || el.hasAttribute("data-cms-custom") ||
      el.classList.contains("stars") || el.hasAttribute("data-year");
  }
  function nextKey(base) {
    counts[base] = (counts[base] || 0);
    return base + "." + counts[base]++;
  }
  function indexImages(root, scope) {
    root.querySelectorAll("img").forEach(function (img) {
      if (img.closest("[data-biz-img],[data-cms-custom],[data-cms-skip]")) return;
      var src = img.getAttribute("src") || "";
      var pic = img.parentElement && img.parentElement.tagName === "PICTURE" ? img.parentElement : null;
      images.push({
        key: nextKey(scope + ":img:" + hash(src)),
        el: img, src: src,
        srcset: img.getAttribute("srcset"), sizes: img.getAttribute("sizes"),
        alt: img.getAttribute("alt") || "",
        sources: pic ? Array.prototype.slice.call(pic.querySelectorAll("source")) : []
      });
    });
  }
  function walk(el, scope) {
    for (var c = el.firstElementChild; c; c = c.nextElementSibling) {
      if (skip(c)) continue;
      var s = isGlobal(c) ? "g" : scope;
      if (hasDirectText(c)) {
        texts.push({ key: nextKey(s + ":" + hash(c.tagName + "|" + norm(c.innerHTML))), el: c, original: c.innerHTML });
      } else {
        walk(c, s);
      }
    }
  }
  walk(document.body, PAGE);
  // Images: global chrome first, then page body, for stable ordering.
  document.querySelectorAll("header.site-header, footer.site-footer, .drawer, .mobile-bar").forEach(function (r) { indexImages(r, "g"); });
  var mainEl = document.querySelector("main");
  if (mainEl) indexImages(mainEl, PAGE);

  var builtInSections = mainEl ? Array.prototype.slice.call(mainEl.children).filter(function (n) { return n.tagName === "SECTION"; }) : [];
  builtInSections.forEach(function (s, i) { s.setAttribute("data-cms-index", i); });

  var metaDesc = document.querySelector('meta[name="description"]');
  var defaults = { title: document.title, description: metaDesc ? metaDesc.getAttribute("content") : "" };

  // Remember default business info (from the HTML) for fallbacks.
  var bizDefaults = {};
  document.querySelectorAll("[data-biz]").forEach(function (el) {
    var f = el.getAttribute("data-biz");
    if (!(f in bizDefaults)) bizDefaults[f] = el.getAttribute("data-biz-default") != null ? el.getAttribute("data-biz-default") : el.textContent;
  });

  /* ---------- Apply ---------- */
  function applyContent(c) {
    c = c || {};
    texts.forEach(function (t) {
      var v = c[t.key];
      var html = v != null ? sanitize(v) : t.original;
      if (t.el.innerHTML !== html) t.el.innerHTML = html;
      var a = t.el.tagName === "A" ? t.el : t.el.closest("a");
      if (a) {
        if (!a.hasAttribute("data-cms-href-default")) a.setAttribute("data-cms-href-default", a.getAttribute("href") || "");
        var h = c[t.key + "@href"];
        var url = h != null ? safeUrl(h) : a.getAttribute("data-cms-href-default");
        if (url) a.setAttribute("href", url);
      }
    });
    images.forEach(function (im) {
      var v = c[im.key];
      if (v) {
        im.el.src = safeUrl(v);
        im.el.removeAttribute("srcset");
        im.el.removeAttribute("sizes");
        im.sources.forEach(function (s) { s.remove(); });
      } else if (im.el.getAttribute("src") !== im.src) {
        im.el.src = im.src;
        if (im.srcset) im.el.setAttribute("srcset", im.srcset);
        if (im.sizes) im.el.setAttribute("sizes", im.sizes);
      }
      var alt = c[im.key + "@alt"];
      im.el.alt = alt != null ? alt : im.alt;
    });
    builtInSections.forEach(function (s, i) {
      var hidden = c["hide:" + PAGE + ":" + i] === "1";
      if (EDIT) s.classList.toggle("cms-hidden-section", hidden);
      else s.style.display = hidden ? "none" : "";
    });
    var t = c["seo:" + PAGE + ":title"], d = c["seo:" + PAGE + ":description"];
    document.title = t || defaults.title;
    if (metaDesc) metaDesc.setAttribute("content", d || defaults.description);
    applyBiz(c);
  }

  function telHref(phone) {
    var d = String(phone || "").replace(/[^\d+]/g, "");
    if (/^0\d{9}$/.test(d)) d = "+61" + d.slice(1);
    return "tel:" + d;
  }

  function applyBiz(c) {
    function get(f) {
      var v = c["biz." + f];
      return v != null && String(v).trim() !== "" ? String(v).trim() : null;
    }
    document.querySelectorAll("[data-biz]").forEach(function (el) {
      var f = el.getAttribute("data-biz");
      var v = get(f);
      var optional = el.hasAttribute("data-biz-optional");
      var wrap = el.closest("[data-biz-wrap]") || el;
      if (v == null) {
        if (optional) { wrap.hidden = true; return; }
        v = bizDefaults[f];
      }
      wrap.hidden = false;
      var format = el.getAttribute("data-biz-format");
      el.textContent = format ? format.replace("{}", v) : v;
    });
    var phone = get("phone") || bizDefaults.phone;
    var email = get("email") || bizDefaults.email;
    document.querySelectorAll('[data-biz-href="tel"]').forEach(function (a) { if (phone) a.href = telHref(phone); });
    document.querySelectorAll('[data-biz-href="mailto"]').forEach(function (a) { if (email) a.href = "mailto:" + email; });
    document.querySelectorAll("[data-biz-link]").forEach(function (a) {
      var v = get(a.getAttribute("data-biz-link"));
      var wrap = a.closest("[data-biz-wrap]") || a;
      if (v && safeUrl(v)) { a.href = safeUrl(v); wrap.hidden = false; } else { wrap.hidden = true; }
    });
    var anyLink = Array.prototype.some.call(document.querySelectorAll("[data-biz-link]"), function (a) { return !(a.closest("[data-biz-wrap]") || a).hidden; });
    document.querySelectorAll("[data-biz-social]").forEach(function (el) { el.hidden = !anyLink; });
    var logo = get("logo");
    document.querySelectorAll("[data-biz-img='logo']").forEach(function (img) {
      if (!img.hasAttribute("data-default-src")) img.setAttribute("data-default-src", img.getAttribute("src"));
      if (logo) {
        img.src = safeUrl(logo);
        var pic = img.parentElement && img.parentElement.tagName === "PICTURE" ? img.parentElement : null;
        if (pic) pic.querySelectorAll("source").forEach(function (s) { s.remove(); });
      }
    });
    document.querySelectorAll('script[type="application/ld+json"]').forEach(function (s) {
      try {
        var data = JSON.parse(s.textContent);
        if (data && data["@type"] === "HomeAndConstructionBusiness") {
          data.telephone = telHref(phone).slice(4);
          data.email = email;
          if (get("business_name")) data.name = get("business_name");
          s.textContent = JSON.stringify(data);
        }
      } catch (e) { /* ignore */ }
    });
    document.querySelectorAll("form[data-lead-form]").forEach(function (f) { f.setAttribute("data-phone", phone || ""); });
  }

  /* ---------- Custom sections ---------- */
  var THEMES = { light: "section--light", paper: "section--paper", dark: "section--dark", ink: "section--dark" };
  function head(d, center) {
    var h = "";
    if (d.eyebrow) h += '<span class="eyebrow">' + esc(d.eyebrow) + "</span>";
    if (d.heading) h += '<h2 class="h2">' + fmt(d.heading) + "</h2>";
    return h ? '<div class="cms-head' + (center ? " cms-head--center" : "") + '">' + h + "</div>" : "";
  }
  function button(d, theme) {
    var url = safeUrl(d.button_url);
    if (!d.button_label || !url) return "";
    var cls = "btn";
    return '<div class="cms-actions"><a class="' + cls + '" href="' + esc(url) + '">' + esc(d.button_label) +
      ' <svg class="arrow" viewBox="0 0 18 10" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true"><path d="M0 5h17M13 1l4 4-4 4"/></svg></a></div>';
  }
  function img(url, alt, cls) {
    url = safeUrl(url);
    return url ? '<img class="' + (cls || "") + '" src="' + esc(url) + '" alt="' + esc(alt || "") + '" loading="lazy" decoding="async">' : "";
  }
  function featureCols(n) { return n === 4 ? 2 : Math.max(1, Math.min(n, 3)); }
  function renderSection(s) {
    var d = s.data || {};
    var theme = d.theme || (s.type === "cta" ? "dark" : "light");
    var el = document.createElement("section");
    el.setAttribute("data-cms-custom", s.id);
    var inner = "";
    switch (s.type) {
      case "text":
        el.className = "section cms-section " + (THEMES[theme] || "");
        inner = '<div class="wrap cms-text' + (d.align === "center" ? " cms-text--center" : "") + '">' +
          head(d, d.align === "center") + '<div class="cms-body">' + paras(d.body) + "</div>" + button(d, theme) + "</div>";
        break;
      case "image_text":
        el.className = "section cms-section " + (THEMES[theme] || "");
        inner = '<div class="wrap cms-split' + (d.image_side === "right" ? " cms-split--right" : "") + '">' +
          '<div class="cms-split__media">' + img(d.image, d.image_alt) + "</div>" +
          '<div class="cms-split__copy">' + head(d) + '<div class="cms-body">' + paras(d.body) + "</div>" + button(d, theme) + "</div></div>";
        break;
      case "gallery":
        el.className = "section cms-section " + (THEMES[theme] || "");
        inner = '<div class="wrap">' + head(d, true) + (d.intro ? '<div class="cms-body cms-body--center">' + paras(d.intro) + "</div>" : "") +
          '<div class="cms-gallery">' + (d.images || []).filter(function (i) { return i && safeUrl(i.url); }).map(function (i) {
            return "<figure>" + img(i.url, i.alt || i.caption) + (i.caption ? "<figcaption>" + esc(i.caption) + "</figcaption>" : "") + "</figure>";
          }).join("") + "</div></div>";
        break;
      case "features":
        el.className = "section cms-section " + (THEMES[theme] || "");
        inner = '<div class="wrap">' + head(d, true) + (d.intro ? '<div class="cms-body cms-body--center">' + paras(d.intro) + "</div>" : "") +
          '<div class="cms-features" style="--cols:' + featureCols((d.items || []).filter(function (i) { return i && (i.title || i.text); }).length) + '">' + (d.items || []).filter(function (i) { return i && (i.title || i.text); }).map(function (i, n) {
            return '<div class="cms-feature"><span class="cms-feature__num">' + (n < 9 ? "0" : "") + (n + 1) + "</span><h3>" + esc(i.title) + "</h3><p>" + esc(i.text) + "</p></div>";
          }).join("") + "</div></div>";
        break;
      case "before_after":
        el.className = "section cms-section " + (THEMES[theme] || "");
        var pairs = (d.pairs || []).filter(function (p) { return p && safeUrl(p.before) && safeUrl(p.after); });
        inner = '<div class="wrap">' + head(d, true) + (d.intro ? '<div class="cms-body cms-body--center">' + paras(d.intro) + "</div>" : "") +
          '<div class="ba-grid' + (pairs.length === 1 ? " ba-grid--single" : "") + '">' + pairs.map(function (p) {
            return '<figure class="ba-item"><div class="compare">' +
              img(p.before, "Before: " + (p.caption || "bathroom"), "compare__before") +
              img(p.after, "After: " + (p.caption || "bathroom"), "compare__after") +
              '<span class="compare__tag compare__tag--before">Before</span><span class="compare__tag compare__tag--after">After</span>' +
              '<input type="range" min="0" max="100" value="50" aria-label="Drag to compare before and after">' +
              '<span class="compare__handle" aria-hidden="true"><span class="compare__knob"><svg viewBox="0 0 26 12" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 1L1 6l4 5M21 1l4 5-4 5M1 6h24"/></svg></span></span>' +
              "</div>" + (p.caption ? "<figcaption>" + esc(p.caption) + "</figcaption>" : "") + "</figure>";
          }).join("") + "</div>" + button(d, theme) + "</div>";
        break;
      case "cta":
        el.className = "cta-band cms-section";
        inner = (safeUrl(d.image) ? '<div class="cta-band__bg" aria-hidden="true">' + img(d.image, "") + "</div>" : "") +
          '<div class="wrap">' + (d.eyebrow ? '<span class="eyebrow">' + esc(d.eyebrow) + "</span>" : "") +
          (d.heading ? '<h2 class="h2">' + fmt(d.heading) + "</h2>" : "") +
          (d.body ? '<p class="lead">' + fmt(d.body) + "</p>" : "") + button(d, "dark") + "</div>";
        break;
      default:
        return null;
    }
    el.innerHTML = inner;
    return el;
  }
  function renderSections(list) {
    if (!mainEl) return;
    mainEl.querySelectorAll("[data-cms-custom]").forEach(function (n) { n.remove(); });
    var groups = {};
    (list || []).forEach(function (s) { (groups[s.after_section] = groups[s.after_section] || []).push(s); });
    Object.keys(groups).forEach(function (k) {
      var idx = Math.min(parseInt(k, 10) || 0, builtInSections.length - 1);
      var anchor = builtInSections[idx];
      if (!anchor) return;
      var ref = anchor.nextSibling;
      // keep any non-section siblings directly after the anchor (e.g. marquee strip)
      while (ref && ref.nodeType === 1 && ref.tagName !== "SECTION" && !ref.hasAttribute("data-cms-custom") && ref.classList.contains("strip")) ref = ref.nextSibling;
      groups[k].forEach(function (s) {
        var node = renderSection(s);
        if (node) mainEl.insertBefore(node, ref);
      });
    });
  }

  function apply(payload) {
    if (!payload) return;
    applyContent(payload.content || {});
    renderSections(payload.sections || []);
    document.dispatchEvent(new CustomEvent("cms:applied"));
  }

  /* ---------- Load ---------- */
  var cached = null;
  if (!EDIT) {
    try { cached = JSON.parse(localStorage.getItem(CACHE_KEY) || "null"); } catch (e) { cached = null; }
    if (cached) apply(cached);
  }

  function load() {
    if (!CFG.supabaseUrl || !CFG.supabaseKey) return Promise.resolve(null);
    return fetch(CFG.supabaseUrl + "/rest/v1/rpc/get_page", {
      method: "POST",
      headers: { "Content-Type": "application/json", apikey: CFG.supabaseKey },
      body: JSON.stringify({ p_page: PAGE }),
      cache: "no-store"
    }).then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; });
  }

  var ready = load().then(function (payload) {
    if (payload) {
      var str = JSON.stringify(payload);
      if (!cached || JSON.stringify(cached) !== str) apply(payload);
      if (!EDIT) { try { localStorage.setItem(CACHE_KEY, str); } catch (e) { /* ignore */ } }
    }
    return payload;
  });

  window.OZTECH_CMS = { page: PAGE, ready: ready, apply: apply };

  /* ---------- Edit mode (inside the admin) ---------- */
  if (!EDIT) return;

  var parentOrigin = location.origin;
  function post(msg) { window.parent.postMessage(msg, parentOrigin); }

  var style = document.createElement("style");
  style.textContent =
    ".cms-editing .reveal{opacity:1!important;transform:none!important}" +
    ".cms-editing [data-cms-k]{outline:1px dashed transparent;outline-offset:3px;cursor:text;transition:outline-color .2s}" +
    ".cms-editing [data-cms-k]:hover{outline-color:rgba(59,130,246,.7)}" +
    ".cms-editing [data-cms-k]:focus{outline:2px solid #3b82f6;outline-offset:3px}" +
    ".cms-editing img[data-cms-k]{cursor:pointer}" +
    ".cms-editing img[data-cms-k]:hover{outline:3px solid #3b82f6;outline-offset:-3px}" +
    ".cms-editing [data-biz]{outline:1px dashed rgba(234,179,8,.6);outline-offset:3px;cursor:help}" +
    ".cms-editing .cms-hidden-section{opacity:.25;filter:grayscale(1)}" +
    ".cms-editing [data-cms-custom]{outline:2px dashed rgba(16,185,129,.6);outline-offset:-6px}" +
    ".cms-editing .compare input{pointer-events:none}" +
    ".cms-editing *::before,.cms-editing *::after{pointer-events:none!important}" +
    ".cms-editing a.cover{display:none!important}" +
    ".cms-editing .hero__frame img,.cms-editing .page-hero__media img{transform:none!important}" +
    ".cms-editing .mobile-bar{position:static}" +
    "";
  document.head.appendChild(style);
  document.documentElement.classList.add("cms-editing");

  ready.then(function () {
    document.querySelectorAll(".reveal,.step").forEach(function (e) { e.classList.add("is-visible"); });
    document.querySelectorAll("details").forEach(function (d) { d.open = true; });
    // Show both images of the before/after slider side by side is not possible; keep at 50%.

    texts.forEach(function (t) {
      var el = t.el;
      el.setAttribute("data-cms-k", t.key);
      el.contentEditable = "true";
      el.spellcheck = true;
      el.addEventListener("focus", function () {
        var a = el.tagName === "A" ? el : el.closest("a");
        post({ type: "cms:select", kind: "text", key: t.key, original: t.original, href: a ? a.getAttribute("href") : null, defaultHref: a ? a.getAttribute("data-cms-href-default") : null });
      });
      el.addEventListener("input", function () {
        post({ type: "cms:change", key: t.key, value: el.innerHTML, original: t.original });
      });
      el.addEventListener("keydown", function (e) {
        // Single-line elements: Enter = finish editing
        if (e.key === "Enter" && !e.shiftKey && /^(H\d|A|SPAN|STRONG|SUMMARY|LABEL|BUTTON|EM|B|SMALL|CITE|FIGCAPTION|LI)$/.test(el.tagName)) {
          e.preventDefault(); el.blur();
        }
      });
      el.addEventListener("paste", function (e) {
        e.preventDefault();
        var text = (e.clipboardData || window.clipboardData).getData("text/plain");
        document.execCommand("insertText", false, text);
      });
    });

    images.forEach(function (im) {
      im.el.setAttribute("data-cms-k", im.key);
      im.el.addEventListener("click", function (e) {
        e.preventDefault(); e.stopPropagation();
        post({ type: "cms:select", kind: "image", key: im.key, src: im.el.currentSrc || im.el.src, alt: im.el.alt, defaultSrc: im.src });
      });
    });

    document.querySelectorAll("[data-biz],[data-biz-img]").forEach(function (el) {
      el.addEventListener("click", function (e) { e.preventDefault(); e.stopPropagation(); post({ type: "cms:select", kind: "biz" }); });
    });
    document.querySelectorAll("[data-cms-custom]").forEach(function (el) {
      el.addEventListener("click", function (e) { e.preventDefault(); post({ type: "cms:select", kind: "custom", id: el.getAttribute("data-cms-custom") }); }, true);
    });

    // Block navigation and form submits while editing.
    document.addEventListener("click", function (e) {
      var a = e.target.closest("a, summary, button");
      if (a) e.preventDefault();
    }, true);
    document.addEventListener("submit", function (e) { e.preventDefault(); }, true);

    post({
      type: "cms:ready",
      page: PAGE,
      sections: builtInSections.map(function (s, i) { return { index: i, name: sectionName(s, i) }; })
    });
  });

  function sectionName(s, i) {
    var n = s.getAttribute("data-section-name");
    if (n) return n;
    var lb = s.getAttribute("aria-labelledby");
    var h = lb && document.getElementById(lb);
    var txt = h ? h.innerHTML.replace(/<br\s*\/?>/gi, " ").replace(/<[^>]+>/g, "") : "";
    var tmp = document.createElement("textarea"); tmp.innerHTML = txt;
    return norm(tmp.value || s.getAttribute("aria-label") || "Section " + (i + 1));
  }

  window.addEventListener("message", function (e) {
    if (e.origin !== parentOrigin || !e.data || typeof e.data !== "object") return;
    var m = e.data;
    if (m.type === "cms:set-image") {
      var im = images.filter(function (x) { return x.key === m.key; })[0];
      if (!im) return;
      if (m.src) {
        im.el.src = m.src; im.el.removeAttribute("srcset"); im.el.removeAttribute("sizes");
        im.sources.forEach(function (s) { s.remove(); });
      }
      if (m.alt != null) im.el.alt = m.alt;
    } else if (m.type === "cms:set-href") {
      var t = texts.filter(function (x) { return x.key === m.key; })[0];
      if (!t) return;
      var a = t.el.tagName === "A" ? t.el : t.el.closest("a");
      if (a) a.setAttribute("href", m.href);
    } else if (m.type === "cms:set-html") {
      var tx = texts.filter(function (x) { return x.key === m.key; })[0];
      if (tx) tx.el.innerHTML = sanitize(m.html);
    } else if (m.type === "cms:toggle-section") {
      var s = builtInSections[m.index];
      if (s) s.classList.toggle("cms-hidden-section", !!m.hidden);
    } else if (m.type === "cms:scroll-to-section") {
      var sec = builtInSections[m.index];
      if (sec) sec.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
})();
