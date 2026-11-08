/* OZTECH Bathrooms - site interactions */
(function () {
  "use strict";

  var doc = document.documentElement;
  doc.classList.remove("no-js");

  window.addEventListener("load", function () { doc.classList.add("is-loaded"); });
  // In case load already fired / images are cached
  requestAnimationFrame(function () { setTimeout(function () { doc.classList.add("is-loaded"); }, 60); });

  /* Header state on scroll */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 24);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* Mobile drawer */
  var toggle = document.querySelector(".nav-toggle");
  var drawer = document.getElementById("drawer");
  function setNav(open) {
    document.body.classList.toggle("nav-open", open);
    if (toggle) {
      toggle.setAttribute("aria-expanded", String(open));
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    }
    if (drawer) drawer.setAttribute("aria-hidden", String(!open));
    if (header && open) header.classList.add("is-scrolled");
    if (!open) onScroll();
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      setNav(!document.body.classList.contains("nav-open"));
    });
  }
  if (drawer) {
    drawer.addEventListener("click", function (e) {
      if (e.target.closest("a")) setNav(false);
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      setNav(false);
      closeMenus();
    }
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth > 1024) setNav(false);
  });

  /* Services dropdown - click support for touch & keyboard */
  var menuBtns = document.querySelectorAll(".has-menu > .nav__link");
  function closeMenus() {
    document.querySelectorAll(".has-menu.is-open").forEach(function (m) {
      m.classList.remove("is-open");
      var b = m.querySelector(".nav__link");
      if (b) b.setAttribute("aria-expanded", "false");
    });
  }
  menuBtns.forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      e.preventDefault();
      var li = btn.parentElement;
      var open = !li.classList.contains("is-open");
      closeMenus();
      li.classList.toggle("is-open", open);
      btn.setAttribute("aria-expanded", String(open));
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-menu")) closeMenus();
  });

  /* Reveal on scroll */
  var reveals = document.querySelectorAll(".reveal, .step");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* Before / after comparison */
  document.querySelectorAll(".compare").forEach(function (cmp) {
    var range = cmp.querySelector("input[type='range']");
    if (!range) return;
    function set(v) { cmp.style.setProperty("--pos", v + "%"); }
    set(range.value);
    range.addEventListener("input", function () { set(range.value); });
  });

  /* Lead submission (Supabase edge function "submit-lead") */
  function submitLead(payload) {
    var cfg = window.OZTECH_CONFIG || {};
    payload.page = location.pathname;
    return fetch(cfg.supabaseUrl + "/functions/v1/submit-lead", {
      method: "POST",
      headers: { "Content-Type": "application/json", apikey: cfg.supabaseKey },
      body: JSON.stringify(payload)
    }).then(function (res) {
      return res.json().catch(function () { return {}; }).then(function (data) {
        if (!res.ok || !data.ok) throw new Error(data.error || "Something went wrong.");
        return data;
      });
    });
  }
  window.OZTECH_submitLead = submitLead;

  function phoneFallback(form) {
    var phone = (form && form.getAttribute("data-phone")) || "";
    return phone ? " You can also call us on " + phone + "." : "";
  }
  window.OZTECH_phoneFallback = phoneFallback;

  document.querySelectorAll("form[data-lead-form]").forEach(function (form) {
    form.setAttribute("novalidate", "");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = new FormData(form);
      var status = form.querySelector(".form__status");
      var btn = form.querySelector("button[type='submit']");
      var payload = {
        source: form.getAttribute("data-lead-form") || "contact-form",
        name: data.get("name"), phone: data.get("phone"), email: data.get("email"),
        suburb: data.get("suburb"), postcode: data.get("postcode"),
        service: data.get("service"), message: data.get("message"),
        company: data.get("company")
      };
      if (btn) btn.disabled = true;
      if (status) { status.classList.remove("is-visible", "is-error"); }
      submitLead(payload).then(function () {
        form.reset();
        if (status) {
          status.textContent = "Thanks, " + (payload.name || "there") + ". We've received your enquiry and will be in touch within one business day.";
          status.classList.add("is-visible");
        }
      }).catch(function (err) {
        if (status) {
          status.textContent = err.message + phoneFallback(form);
          status.classList.add("is-visible", "is-error");
        }
      }).then(function () { if (btn) btn.disabled = false; });
    });
  });

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
