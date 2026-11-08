/* OZTECH Bathrooms — site interactions */
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

  /* Services dropdown — click support for touch & keyboard */
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

  /* Quote form — opens the visitor's email client with the enquiry pre-filled.
     To use a form service instead (Formspree, Netlify Forms, etc.), set the
     form's action/method and remove the data-mailto attribute. */
  document.querySelectorAll("form[data-mailto]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      var data = new FormData(form);
      var lines = [
        "Name: " + (data.get("name") || ""),
        "Phone: " + (data.get("phone") || ""),
        "Email: " + (data.get("email") || ""),
        "Suburb: " + (data.get("suburb") || ""),
        "Service: " + (data.get("service") || ""),
        "",
        (data.get("message") || "")
      ];
      var subject = "Quote request — " + (data.get("service") || "Bathroom renovation") + " — " + (data.get("suburb") || "Sydney");
      var href = "mailto:" + form.getAttribute("data-mailto") +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      window.location.href = href;
      var status = form.querySelector(".form__status");
      if (status) {
        status.textContent = "Thanks, " + (data.get("name") || "there") + ". Your email app should now open with your enquiry ready to send.";
        status.classList.add("is-visible");
      }
    });
  });

  /* Footer year */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
