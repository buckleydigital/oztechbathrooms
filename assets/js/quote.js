/* OZTECH Bathrooms: get-a-quote survey */
(function () {
  "use strict";
  var root = document.getElementById("survey");
  if (!root) return;

  var steps = Array.prototype.slice.call(root.querySelectorAll(".survey__step"));
  var QUESTIONS = 3;
  var bar = root.querySelector(".survey__bar");
  var back = root.querySelector(".survey__back");
  var count = root.querySelector(".survey__count");
  var form = document.getElementById("survey-form");
  var answers = {};
  var current = 0;

  function label(btn) {
    var l = btn.querySelector(".option__label");
    return (l ? l.textContent : btn.textContent).replace(/\s+/g, " ").trim();
  }

  function show(i, focus) {
    current = i;
    steps.forEach(function (s, j) { s.classList.toggle("is-active", j === i); });
    var done = i >= QUESTIONS;
    bar.style.width = done ? "100%" : Math.max(6, (i / QUESTIONS) * 100) + "%";
    back.hidden = i === 0 || done;
    count.hidden = done;
    if (!done) count.innerHTML = "Step <b>" + (i + 1) + "</b> of " + QUESTIONS;
    if (focus !== false) {
      var h = steps[i].querySelector(".survey__q");
      if (h) h.focus({ preventScroll: true });
      var top = root.getBoundingClientRect().top + window.scrollY - 110;
      if (window.scrollY > top) window.scrollTo({ top: top, behavior: "smooth" });
    }
  }

  steps.forEach(function (step, i) {
    var field = step.getAttribute("data-field");
    if (!field) return;
    step.querySelectorAll(".option").forEach(function (btn) {
      btn.addEventListener("click", function () {
        step.querySelectorAll(".option").forEach(function (b) {
          b.classList.remove("is-selected");
          b.setAttribute("aria-pressed", "false");
        });
        btn.classList.add("is-selected");
        btn.setAttribute("aria-pressed", "true");
        answers[field] = label(btn);
        setTimeout(function () { show(i + 1); }, 260);
      });
    });
  });

  back.addEventListener("click", function () { if (current > 0) show(current - 1); });

  // Pre-select the service when arriving from a service page (?service=leaking)
  var m = /[?&]service=([a-z-]+)/.exec(location.search);
  if (m) {
    var pre = root.querySelector('.survey__step[data-field="service"] .option[data-key="' + m[1] + '"]');
    if (pre) {
      pre.classList.add("is-selected");
      pre.setAttribute("aria-pressed", "true");
      answers.service = label(pre);
      show(1, false);
    }
  } else {
    show(0, false);
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var status = form.querySelector(".form__status");
    status.classList.remove("is-visible", "is-error");
    if (!form.checkValidity()) { form.reportValidity(); return; }
    if (!answers.service) { show(0); return; }
    if (!answers.timeframe) { show(1); return; }
    var data = new FormData(form);
    var btn = form.querySelector("button[type='submit']");
    btn.disabled = true;
    window.OZTECH_submitLead({
      source: "quote-survey",
      service: answers.service,
      timeframe: answers.timeframe,
      name: data.get("name"),
      email: data.get("email"),
      phone: data.get("phone"),
      postcode: data.get("postcode"),
      company: data.get("company")
    }).then(function () {
      form.reset();
      show(QUESTIONS);
    }).catch(function (err) {
      var phoneEl = document.querySelector("[data-biz='phone']");
      var phone = phoneEl ? phoneEl.textContent.trim() : "";
      status.textContent = err.message + (phone ? " You can also call us on " + phone + "." : "");
      status.classList.add("is-visible", "is-error");
    }).then(function () { btn.disabled = false; });
  });
})();
