/* OZTECH Bathrooms: admin dashboard */
(function () {
  "use strict";

  var CFG = window.OZTECH_CONFIG;
  var sb = window.supabase.createClient(CFG.supabaseUrl, CFG.supabaseKey, {
    auth: { persistSession: true, autoRefreshToken: true, detectSessionInUrl: true }
  });
  var BUCKET = CFG.mediaBucket || "site-media";

  var PAGES = [
    { id: "index", name: "Home" },
    { id: "bathroom-renovations", name: "Bathroom Renovations" },
    { id: "shower-renovations", name: "Shower Renovations" },
    { id: "leaking-showers", name: "Leaking Showers" },
    { id: "partial-renovations", name: "Partial Renovations" },
    { id: "get-a-quote", name: "Get a Quote" },
    { id: "privacy-policy", name: "Privacy Policy" },
    { id: "terms", name: "Terms of Use" }
  ];
  var STATUSES = ["new", "contacted", "quoted", "won", "lost"];

  /* ---------- Utils ---------- */
  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function esc(s) {
    return String(s == null ? "" : s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  }
  function norm(s) { return String(s || "").replace(/\s+/g, " ").trim(); }
  function pageUrl(id) { return "../" + id + ".html"; }
  function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function fmtDate(iso) {
    var d = new Date(iso);
    return d.toLocaleDateString("en-AU", { day: "numeric", month: "short", year: "numeric" }) + ", " +
      d.toLocaleTimeString("en-AU", { hour: "numeric", minute: "2-digit" });
  }
  var ICON_OK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 8.5l3 3 7-7"/></svg>';
  var ICON_ERR = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="8" cy="8" r="6.5"/><path d="M8 4.5v4.5M8 11v.5"/></svg>';
  var ICON_IMG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="3.5" y="4.5" width="17" height="15"/><circle cx="9" cy="10" r="1.8"/><path d="M3.5 17l5-4.5 4 3.5 3-2.5 5 4"/></svg>';
  var ICON_UP = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M8 13V3M4 7l4-4 4 4"/></svg>';
  var ICON_DOWN = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M8 3v10M4 9l4 4 4-4"/></svg>';
  var ICON_TRASH = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M2.5 4h11M6 4V2.5h4V4M4 4l.7 9.5h6.6L12 4"/></svg>';
  var ICON_EYE = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5z"/><circle cx="8" cy="8" r="2"/></svg>';
  var ICON_LINK = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3"><path d="M6.5 9.5l3-3M7 4.5l1-1a2.8 2.8 0 014 4l-1 1M9 11.5l-1 1a2.8 2.8 0 01-4-4l1-1"/></svg>';

  function toast(msg, isError) {
    var t = document.createElement("div");
    t.className = "toast" + (isError ? " is-error" : "");
    t.innerHTML = (isError ? ICON_ERR : ICON_OK) + "<span>" + esc(msg) + "</span>";
    $("#toasts").appendChild(t);
    setTimeout(function () { t.style.opacity = "0"; t.style.transition = "opacity .3s"; }, isError ? 5000 : 2800);
    setTimeout(function () { t.remove(); }, isError ? 5400 : 3200);
  }
  function fail(err, fallback) {
    console.error(err);
    toast((err && err.message) || fallback || "Something went wrong.", true);
  }
  function busy(btn, on, label) {
    if (!btn) return;
    if (on) { btn.dataset.label = btn.innerHTML; btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>' + (label ? " " + esc(label) : ""); }
    else { btn.disabled = false; if (btn.dataset.label) btn.innerHTML = btn.dataset.label; }
  }
  function pageOptions(sel) {
    sel.innerHTML = PAGES.map(function (p) { return '<option value="' + p.id + '">' + esc(p.name) + "</option>"; }).join("");
  }

  /* ---------- Page structure (from the live HTML) ---------- */
  var pageInfoCache = {};
  function pageInfo(id) {
    if (pageInfoCache[id]) return pageInfoCache[id];
    pageInfoCache[id] = fetch(pageUrl(id), { cache: "no-store" }).then(function (r) { return r.text(); }).then(function (html) {
      var doc = new DOMParser().parseFromString(html, "text/html");
      var main = doc.querySelector("main");
      var sections = main ? Array.prototype.filter.call(main.children, function (n) { return n.tagName === "SECTION"; }) : [];
      var meta = doc.querySelector('meta[name="description"]');
      return {
        title: (doc.querySelector("title") || {}).textContent || "",
        description: meta ? meta.getAttribute("content") : "",
        sections: sections.map(function (s, i) {
          var lb = s.getAttribute("aria-labelledby");
          var h = lb && doc.getElementById(lb);
          var raw = h ? h.innerHTML.replace(/<br\s*\/?>/gi, " ").replace(/<[^>]+>/g, "") : "";
          var name = norm(new DOMParser().parseFromString(raw, "text/html").documentElement.textContent || s.getAttribute("aria-label") || "Section " + (i + 1));
          return { index: i, name: name };
        })
      };
    });
    return pageInfoCache[id];
  }

  /* =====================================================================
     AUTH
     ===================================================================== */
  var started = false;

  function showAuth(formId, msg, isError) {
    $("#app").hidden = true;
    $("#auth").hidden = false;
    $$("#auth form").forEach(function (f) { f.hidden = f.id !== formId; });
    var m = $("#" + formId + " .auth__msg");
    if (m) { m.hidden = !msg; m.textContent = msg || ""; m.classList.toggle("is-error", !!isError); }
    var first = $("#" + formId + " input");
    if (first) setTimeout(function () { first.focus(); }, 50);
  }

  function enterApp(session) {
    return sb.rpc("is_admin").then(function (res) {
      if (res.error) throw res.error;
      if (res.data !== true) {
        return sb.auth.signOut().then(function () {
          showAuth("login-form", "This account doesn't have admin access.", true);
        });
      }
      $("#who").textContent = session.user.email;
      $("#auth").hidden = true;
      $("#app").hidden = false;
      if (!started) { started = true; startApp(); }
    }).catch(function (err) {
      showAuth("login-form", "Couldn't verify admin access: " + (err.message || err), true);
    });
  }

  var recovering = /type=recovery/.test(location.hash);

  sb.auth.onAuthStateChange(function (event, session) {
    if (event === "PASSWORD_RECOVERY") { recovering = true; showAuth("newpass-form"); return; }
    if (event === "SIGNED_OUT") { started = false; showAuth("login-form"); }
    if (event === "SIGNED_IN" && session && !recovering && $("#app").hidden) enterApp(session);
  });

  sb.auth.getSession().then(function (res) {
    var session = res.data && res.data.session;
    if (recovering) { showAuth("newpass-form"); return; }
    if (session) enterApp(session); else showAuth("login-form");
  });

  $$("[data-auth-view]").forEach(function (b) {
    b.addEventListener("click", function () { showAuth(b.getAttribute("data-auth-view")); });
  });

  $("#login-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var btn = $("#login-form button[type=submit]");
    var email = $("#login-email").value.trim(), password = $("#login-password").value;
    if (!email || !password) { showAuth("login-form", "Enter your email and password.", true); return; }
    busy(btn, true, "Signing in");
    sb.auth.signInWithPassword({ email: email, password: password }).then(function (res) {
      busy(btn, false);
      if (res.error) { showAuth("login-form", res.error.message === "Invalid login credentials" ? "Incorrect email or password." : res.error.message, true); return; }
      enterApp(res.data.session);
    });
  });

  $("#forgot-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var btn = $("#forgot-form button[type=submit]");
    var email = $("#forgot-email").value.trim();
    if (!email) return;
    busy(btn, true, "Sending");
    sb.auth.resetPasswordForEmail(email, { redirectTo: location.origin + location.pathname }).then(function (res) {
      busy(btn, false);
      if (res.error) showAuth("forgot-form", res.error.message, true);
      else showAuth("forgot-form", "If that email belongs to an admin, a reset link is on its way.");
    });
  });

  $("#newpass-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var p1 = $("#new-password").value, p2 = $("#new-password2").value;
    if (p1.length < 10) { showAuth("newpass-form", "Use at least 10 characters.", true); return; }
    if (p1 !== p2) { showAuth("newpass-form", "Passwords don't match.", true); return; }
    var btn = $("#newpass-form button[type=submit]");
    busy(btn, true, "Saving");
    sb.auth.updateUser({ password: p1 }).then(function (res) {
      busy(btn, false);
      if (res.error) { showAuth("newpass-form", res.error.message, true); return; }
      recovering = false;
      history.replaceState(null, "", location.pathname);
      toast("Password updated.");
      sb.auth.getSession().then(function (r) { if (r.data.session) enterApp(r.data.session); else showAuth("login-form"); });
    });
  });

  $("#sign-out").addEventListener("click", function () {
    if (editor.dirty() && !confirm("You have unsaved page changes. Sign out anyway?")) return;
    sb.auth.signOut();
  });

  /* =====================================================================
     APP SHELL
     ===================================================================== */
  var inited = {};
  var current = null;

  function startApp() {
    pageOptions($("#editor-page"));
    pageOptions($("#sections-page"));
    var tab = (location.hash || "").replace("#", "");
    if (!$('[data-panel="' + tab + '"]')) tab = "leads";
    showTab(tab);
    leads.refreshCount();
  }

  function showTab(tab) {
    if (current === "editor" && tab !== "editor" && editor.dirty() && !confirm("You have unsaved page changes. Leave the editor anyway?")) return;
    current = tab;
    $$("[data-panel]").forEach(function (p) { p.hidden = p.getAttribute("data-panel") !== tab; });
    $$(".side__nav button").forEach(function (b) { b.classList.toggle("is-active", b.getAttribute("data-tab") === tab); });
    history.replaceState(null, "", "#" + tab);
    $("#app").classList.remove("side-open");
    var mod = MODULES[tab];
    if (mod && !inited[tab]) { inited[tab] = true; mod.init(); }
    else if (mod && mod.show) mod.show();
  }

  $$(".side__nav button").forEach(function (b) {
    b.addEventListener("click", function () { showTab(b.getAttribute("data-tab")); });
  });
  $("#side-toggle").addEventListener("click", function () { $("#app").classList.toggle("side-open"); });

  window.addEventListener("beforeunload", function (e) {
    if (editor.dirty()) { e.preventDefault(); e.returnValue = ""; }
  });

  /* ---------- Overlay / drawer / modal ---------- */
  function openLayer(el) { $("#overlay").classList.add("is-open"); el.classList.add("is-open"); }
  function closeLayer(el) {
    el.classList.remove("is-open");
    if (!$(".drawer.is-open, .modal.is-open")) $("#overlay").classList.remove("is-open");
    if (el._onClose) { var f = el._onClose; el._onClose = null; f(); }
  }
  $$("[data-close]").forEach(function (b) {
    b.addEventListener("click", function () { closeLayer(b.closest(".drawer, .modal")); });
  });
  $("#overlay").addEventListener("click", function () {
    var top = $(".modal.is-open") || $(".drawer.is-open");
    if (top) closeLayer(top);
  });
  $$(".modal").forEach(function (m) {
    m.addEventListener("click", function (e) { if (e.target === m) closeLayer(m); });
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var top = $(".modal.is-open") || $(".drawer.is-open");
    if (top) closeLayer(top);
  });

  /* =====================================================================
     CONTENT STORE
     ===================================================================== */
  function loadContent(prefixes) {
    var q = sb.from("site_content").select("key,value");
    if (prefixes) q = q.or(prefixes.map(function (p) { return "key.like." + p + "*"; }).join(","));
    return q.then(function (res) {
      if (res.error) throw res.error;
      var map = {};
      res.data.forEach(function (r) { map[r.key] = r.value; });
      return map;
    });
  }
  // changes: { key: value | null }  (null = delete override)
  function saveContent(changes) {
    var ups = [], dels = [];
    Object.keys(changes).forEach(function (k) {
      if (changes[k] === null) dels.push(k); else ups.push({ key: k, value: changes[k] });
    });
    var jobs = [];
    if (ups.length) jobs.push(sb.from("site_content").upsert(ups, { onConflict: "key" }));
    if (dels.length) jobs.push(sb.from("site_content").delete().in("key", dels));
    return Promise.all(jobs).then(function (results) {
      results.forEach(function (r) { if (r.error) throw r.error; });
    });
  }

  /* =====================================================================
     MEDIA (upload + picker)
     ===================================================================== */
  function slug(name) {
    return String(name || "image").toLowerCase().replace(/\.[a-z0-9]+$/, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40) || "image";
  }
  // Resize big photos and convert to WebP in the browser.
  function prepareImage(file) {
    if (!/^image\/(jpeg|png|webp)$/.test(file.type)) return Promise.resolve({ blob: file, ext: (file.name.split(".").pop() || "img").toLowerCase(), type: file.type });
    return new Promise(function (resolve) {
      var img = new Image();
      var url = URL.createObjectURL(file);
      img.onload = function () {
        var max = 2200;
        var scale = Math.min(1, max / Math.max(img.naturalWidth, img.naturalHeight));
        var w = Math.round(img.naturalWidth * scale), h = Math.round(img.naturalHeight * scale);
        var c = document.createElement("canvas");
        c.width = w; c.height = h;
        c.getContext("2d").drawImage(img, 0, 0, w, h);
        URL.revokeObjectURL(url);
        c.toBlob(function (blob) {
          if (!blob || (scale === 1 && file.type === "image/webp" && blob.size >= file.size)) resolve({ blob: file, ext: file.type.split("/")[1], type: file.type });
          else resolve({ blob: blob, ext: "webp", type: "image/webp" });
        }, "image/webp", 0.86);
      };
      img.onerror = function () { URL.revokeObjectURL(url); resolve({ blob: file, ext: "img", type: file.type }); };
      img.src = url;
    });
  }
  function upload(file) {
    if (file.size > 25 * 1024 * 1024) return Promise.reject(new Error(file.name + " is larger than 25MB."));
    return prepareImage(file).then(function (p) {
      if (p.blob.size > 10 * 1024 * 1024) throw new Error(file.name + " is still over 10MB after resizing.");
      var path = "uploads/" + Date.now() + "-" + slug(file.name) + "." + (p.ext === "jpeg" ? "jpg" : p.ext);
      return sb.storage.from(BUCKET).upload(path, p.blob, { contentType: p.type, cacheControl: "31536000", upsert: false }).then(function (res) {
        if (res.error) throw res.error;
        return publicUrl(path);
      });
    });
  }
  function publicUrl(path) { return sb.storage.from(BUCKET).getPublicUrl(path).data.publicUrl; }
  function listMedia() {
    return sb.storage.from(BUCKET).list("uploads", { limit: 1000, sortBy: { column: "created_at", order: "desc" } }).then(function (res) {
      if (res.error) throw res.error;
      return res.data.filter(function (f) { return f.id && f.name !== ".emptyFolderPlaceholder"; }).map(function (f) {
        return { name: f.name, path: "uploads/" + f.name, url: publicUrl("uploads/" + f.name), size: f.metadata && f.metadata.size };
      });
    });
  }
  function setupDrop(zone, input, onFiles) {
    input.addEventListener("change", function () { if (input.files.length) onFiles(Array.prototype.slice.call(input.files)); input.value = ""; });
    ["dragenter", "dragover"].forEach(function (ev) { zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.add("is-over"); }); });
    ["dragleave", "drop"].forEach(function (ev) { zone.addEventListener(ev, function (e) { e.preventDefault(); zone.classList.remove("is-over"); }); });
    zone.addEventListener("drop", function (e) {
      var files = Array.prototype.slice.call(e.dataTransfer.files || []).filter(function (f) { return /^image\//.test(f.type); });
      if (files.length) onFiles(files);
    });
  }

  var picker = (function () {
    var resolveFn = null;
    var modal = $("#picker-modal");
    function render() {
      var grid = $("#picker-grid");
      grid.innerHTML = '<div class="muted">Loading…</div>';
      listMedia().then(function (items) {
        $("#picker-empty").hidden = items.length > 0;
        grid.innerHTML = items.map(function (m) {
          return '<figure class="media-item is-pick" tabindex="0" data-url="' + esc(m.url) + '"><img src="' + esc(m.url) + '" alt="" loading="lazy"><figcaption>' + esc(m.name) + "</figcaption></figure>";
        }).join("");
      }).catch(function (err) { grid.innerHTML = ""; fail(err, "Couldn't load media."); });
    }
    $("#picker-grid").addEventListener("click", function (e) {
      var item = e.target.closest(".media-item");
      if (item) choose(item.getAttribute("data-url"));
    });
    $("#picker-grid").addEventListener("keydown", function (e) {
      var item = e.target.closest(".media-item");
      if (item && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); choose(item.getAttribute("data-url")); }
    });
    setupDrop($("#picker-drop"), $("#picker-input"), function (files) {
      var zone = $("#picker-drop strong");
      zone.textContent = "Uploading…";
      upload(files[0]).then(function (url) {
        zone.textContent = "Upload a new image";
        media.invalidate();
        choose(url);
      }).catch(function (err) { zone.textContent = "Upload a new image"; fail(err, "Upload failed."); });
    });
    function choose(url) {
      var f = resolveFn; resolveFn = null;
      closeLayer(modal);
      if (f) f(url);
    }
    return {
      open: function () {
        return new Promise(function (resolve) {
          resolveFn = resolve;
          modal._onClose = function () { if (resolveFn) { var f = resolveFn; resolveFn = null; f(null); } };
          render();
          openLayer(modal);
        });
      }
    };
  })();

  /* =====================================================================
     LEADS
     ===================================================================== */
  var leads = (function () {
    var all = [];
    var openId = null;

    function load() {
      return sb.from("leads").select("*").order("created_at", { ascending: false }).limit(2000).then(function (res) {
        if (res.error) throw res.error;
        all = res.data || [];
        render();
        updateCount();
      }).catch(function (err) { fail(err, "Couldn't load leads."); });
    }
    function updateCount() {
      var n = all.filter(function (l) { return l.status === "new"; }).length;
      $("#new-count").hidden = !n;
      $("#new-count").textContent = n;
    }
    function render() {
      var q = $("#leads-search").value.trim().toLowerCase();
      var st = $("#leads-status").value;
      var list = all.filter(function (l) {
        if (st && l.status !== st) return false;
        if (!q) return true;
        return [l.name, l.email, l.phone, l.postcode, l.suburb, l.service].join(" ").toLowerCase().indexOf(q) !== -1;
      });
      var now = Date.now();
      var month = new Date(); month.setDate(1); month.setHours(0, 0, 0, 0);
      $("#stat-new").textContent = all.filter(function (l) { return l.status === "new"; }).length;
      $("#stat-week").textContent = all.filter(function (l) { return now - new Date(l.created_at) < 7 * 864e5; }).length;
      $("#stat-month").textContent = all.filter(function (l) { return new Date(l.created_at) >= month; }).length;
      $("#stat-total").textContent = all.length;
      $("#leads-count").textContent = list.length + (list.length === 1 ? " lead" : " leads");
      $("#leads-empty").hidden = list.length > 0;
      $("#leads-body").innerHTML = list.map(function (l) {
        return '<tr data-id="' + l.id + '">' +
          '<td class="nowrap">' + esc(fmtDate(l.created_at)) + "</td>" +
          '<td><span class="name">' + esc(l.name) + '</span><span class="sub">' + esc(l.email) + "</span></td>" +
          "<td>" + esc(l.service || "-") + "</td>" +
          "<td>" + esc(l.timeframe || "-") + "</td>" +
          "<td>" + esc(l.postcode || l.suburb || "-") + "</td>" +
          '<td class="nowrap"><a href="tel:' + esc(String(l.phone).replace(/[^\d+]/g, "")) + '" data-stop>' + esc(l.phone) + "</a></td>" +
          '<td><select class="select" data-status aria-label="Status">' + STATUSES.map(function (s) {
            return '<option value="' + s + '"' + (s === l.status ? " selected" : "") + ">" + cap(s) + "</option>";
          }).join("") + "</select></td></tr>";
      }).join("");
    }
    function update(id, patch) {
      return sb.from("leads").update(patch).eq("id", id).then(function (res) {
        if (res.error) throw res.error;
        all.forEach(function (l) { if (l.id === id) Object.assign(l, patch); });
        updateCount();
      });
    }

    $("#leads-body").addEventListener("change", function (e) {
      if (!e.target.matches("[data-status]")) return;
      var id = e.target.closest("tr").getAttribute("data-id");
      update(id, { status: e.target.value }).then(function () { toast("Status updated."); render(); }).catch(function (err) { fail(err); });
    });
    $("#leads-body").addEventListener("click", function (e) {
      if (e.target.closest("[data-status], [data-stop]")) return;
      var tr = e.target.closest("tr");
      if (tr) open(tr.getAttribute("data-id"));
    });
    $("#leads-search").addEventListener("input", render);
    $("#leads-status").addEventListener("change", render);
    $("#leads-refresh").addEventListener("click", function () { load().then(function () { toast("Leads refreshed."); }); });
    $("#leads-export").addEventListener("click", function () {
      var cols = ["created_at", "status", "name", "email", "phone", "postcode", "suburb", "service", "timeframe", "message", "notes", "source", "page"];
      var csv = [cols.join(",")].concat(all.map(function (l) {
        return cols.map(function (c) { return '"' + String(l[c] == null ? "" : l[c]).replace(/"/g, '""') + '"'; }).join(",");
      })).join("\r\n");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob(["﻿" + csv], { type: "text/csv" }));
      a.download = "oztech-leads-" + new Date().toISOString().slice(0, 10) + ".csv";
      a.click();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
    });

    function open(id) {
      var l = all.filter(function (x) { return x.id === id; })[0];
      if (!l) return;
      openId = id;
      var tel = String(l.phone).replace(/[^\d+]/g, "");
      $("#lead-title").textContent = l.name;
      var rows = [
        ["Received", fmtDate(l.created_at)], ["Phone", '<a href="tel:' + esc(tel) + '">' + esc(l.phone) + "</a>", true],
        ["Email", '<a href="mailto:' + esc(l.email) + '">' + esc(l.email) + "</a>", true],
        ["Postcode", l.postcode], ["Suburb", l.suburb], ["Looking for", l.service], ["Timeframe", l.timeframe],
        ["Message", l.message], ["Form", l.source], ["Page", l.page], ["Email sent", l.email_sent ? "Yes" : "No"]
      ];
      $("#lead-body").innerHTML =
        '<div class="quick"><a class="btn" href="tel:' + esc(tel) + '">Call</a><a class="btn btn--ghost" href="mailto:' + esc(l.email) + '">Email</a></div>' +
        '<dl class="dl">' + rows.filter(function (r) { return r[1]; }).map(function (r) {
          return "<dt>" + r[0] + "</dt><dd>" + (r[2] ? r[1] : esc(r[1])) + "</dd>";
        }).join("") + "</dl>" +
        '<div class="form-section"><div class="field"><label for="lead-status">Status</label><select class="select" id="lead-status">' +
        STATUSES.map(function (s) { return '<option value="' + s + '"' + (s === l.status ? " selected" : "") + ">" + cap(s) + "</option>"; }).join("") +
        '</select></div><div class="field"><label for="lead-notes">Notes</label><textarea class="textarea" id="lead-notes" placeholder="Private notes about this lead">' + esc(l.notes || "") + "</textarea></div></div>";
      openLayer($("#lead-drawer"));
    }
    $("#lead-save").addEventListener("click", function () {
      var btn = this;
      busy(btn, true);
      update(openId, { status: $("#lead-status").value, notes: $("#lead-notes").value }).then(function () {
        busy(btn, false); toast("Lead saved."); render(); closeLayer($("#lead-drawer"));
      }).catch(function (err) { busy(btn, false); fail(err); });
    });
    $("#lead-delete").addEventListener("click", function () {
      if (!confirm("Delete this lead permanently?")) return;
      sb.from("leads").delete().eq("id", openId).then(function (res) {
        if (res.error) return fail(res.error);
        all = all.filter(function (l) { return l.id !== openId; });
        render(); updateCount(); closeLayer($("#lead-drawer")); toast("Lead deleted.");
      });
    });

    return {
      init: load, show: load,
      refreshCount: function () {
        sb.from("leads").select("id", { count: "exact", head: true }).eq("status", "new").then(function (res) {
          if (res.error) return;
          $("#new-count").hidden = !res.count;
          $("#new-count").textContent = res.count;
        });
      }
    };
  })();

  /* =====================================================================
     PAGE EDITOR
     ===================================================================== */
  var editor = (function () {
    var frame = $("#editor-frame");
    var page = "index";
    var changes = {};
    var hidden = {};
    var selection = null;

    function dirtyCount() { return Object.keys(changes).length; }
    function refreshBar() {
      var n = dirtyCount();
      $("#editor-save").disabled = !n;
      $("#editor-discard").disabled = !n;
      $("#editor-unsaved").hidden = !n;
      $("#editor-unsaved").textContent = n + (n === 1 ? " unsaved change" : " unsaved changes");
    }
    function setChange(key, value) { changes[key] = value; refreshBar(); }
    function post(msg) { if (frame.contentWindow) frame.contentWindow.postMessage(msg, location.origin); }

    function load(id) {
      page = id;
      changes = {};
      selection = null;
      refreshBar();
      inspectorIdle();
      $("#sec-list").innerHTML = '<p class="hint">Loading…</p>';
      $("#frame-loading").hidden = false;
      $("#editor-open").href = pageUrl(id);
      frame.src = pageUrl(id) + "?cms-edit=1&t=" + Date.now();
      loadContent(["hide:" + id + ":"]).then(function (map) {
        hidden = {};
        Object.keys(map).forEach(function (k) { if (map[k] === "1") hidden[k] = true; });
      }).catch(function () { hidden = {}; });
    }

    function inspectorIdle() {
      $("#insp-title").textContent = "Nothing selected";
      $("#insp-body").innerHTML = '<p class="hint">Click any text on the page to start typing. Click an image to replace it. Changes stay in draft until you press <b>Save changes</b>.</p>' +
        '<div class="legend"><span><i style="border-color:#3b82f6"></i>Editable text and images</span><span><i style="border-color:#eab308"></i>Business info (edit in Business info)</span><span><i style="border-color:#10b981"></i>Custom section (edit in Sections)</span></div>';
    }

    function inspectText(m) {
      $("#insp-title").textContent = "Text";
      var html = '<p class="hint">Type directly on the page. Use <b>Ctrl/Cmd + B</b> for bold and <b>Ctrl/Cmd + I</b> for italics.</p>';
      if (m.href != null) {
        html += '<div class="field"><label for="insp-href">' + ICON_LINK.replace("<svg", '<svg style="display:inline;width:13px;height:13px;vertical-align:-2px;margin-right:4px"') + 'Link goes to</label><input class="input" id="insp-href" value="' + esc(m.href) + '"><small>A page (e.g. get-a-quote.html), a section (#quote) or a full web address.</small></div>';
      }
      html += '<button class="btn btn--ghost btn--sm" type="button" id="insp-revert">Revert to original</button>';
      $("#insp-body").innerHTML = html;
      var href = $("#insp-href");
      if (href) href.addEventListener("input", function () {
        var v = href.value.trim();
        setChange(m.key + "@href", v && v !== m.defaultHref ? v : null);
        post({ type: "cms:set-href", key: m.key, href: v || m.defaultHref });
      });
      $("#insp-revert").addEventListener("click", function () {
        setChange(m.key, null);
        if (m.href != null) { setChange(m.key + "@href", null); post({ type: "cms:set-href", key: m.key, href: m.defaultHref }); }
        post({ type: "cms:set-html", key: m.key, html: m.original });
        toast("Reverted. Save to apply.");
      });
    }

    function inspectImage(m) {
      $("#insp-title").textContent = "Image";
      $("#insp-body").innerHTML =
        '<img class="thumb" id="insp-img" src="' + esc(m.src) + '" alt="">' +
        '<div style="display:flex;gap:8px;flex-wrap:wrap"><button class="btn btn--sm" type="button" id="insp-replace">Replace image</button>' +
        '<button class="btn btn--ghost btn--sm" type="button" id="insp-img-revert">Revert to original</button></div>' +
        '<div class="field"><label for="insp-alt">Description (alt text)</label><textarea class="textarea" id="insp-alt" style="min-height:70px">' + esc(m.alt) + '</textarea><small>Describes the image for Google and screen readers.</small></div>';
      $("#insp-replace").addEventListener("click", function () {
        picker.open().then(function (url) {
          if (!url) return;
          setChange(m.key, url);
          $("#insp-img").src = url;
          post({ type: "cms:set-image", key: m.key, src: url });
        });
      });
      $("#insp-img-revert").addEventListener("click", function () {
        setChange(m.key, null);
        setChange(m.key + "@alt", null);
        $("#insp-img").src = m.defaultSrc;
        post({ type: "cms:set-image", key: m.key, src: m.defaultSrc });
        toast("Reverted. Save to apply.");
      });
      $("#insp-alt").addEventListener("input", function () {
        setChange(m.key + "@alt", this.value);
        post({ type: "cms:set-image", key: m.key, alt: this.value });
      });
    }

    function renderSectionList(list) {
      $("#sec-list").innerHTML = list.map(function (s) {
        var k = "hide:" + page + ":" + s.index;
        var isHidden = k in changes ? changes[k] === "1" : !!hidden[k];
        return '<div class="sec-row' + (isHidden ? " is-hidden" : "") + '" data-index="' + s.index + '">' +
          '<label class="switch" title="Show on website"><input type="checkbox"' + (isHidden ? "" : " checked") + '><i></i></label>' +
          '<span class="name" title="Scroll to section">' + esc(s.name) + "</span></div>";
      }).join("") || '<p class="hint">No sections.</p>';
    }
    $("#sec-list").addEventListener("change", function (e) {
      var row = e.target.closest(".sec-row");
      if (!row) return;
      var i = +row.getAttribute("data-index");
      var k = "hide:" + page + ":" + i;
      var hide = !e.target.checked;
      var saved = !!hidden[k];
      setChange(k, hide === saved ? undefined : (hide ? "1" : null));
      if (changes[k] === undefined) { delete changes[k]; refreshBar(); }
      row.classList.toggle("is-hidden", hide);
      post({ type: "cms:toggle-section", index: i, hidden: hide });
    });
    $("#sec-list").addEventListener("click", function (e) {
      var n = e.target.closest(".name");
      if (n) post({ type: "cms:scroll-to-section", index: +n.closest(".sec-row").getAttribute("data-index") });
    });

    window.addEventListener("message", function (e) {
      if (e.origin !== location.origin || e.source !== frame.contentWindow || !e.data) return;
      var m = e.data;
      if (m.type === "cms:ready") {
        $("#frame-loading").hidden = true;
        renderSectionList(m.sections || []);
      } else if (m.type === "cms:change") {
        setChange(m.key, norm(m.value) === norm(m.original) ? null : m.value);
      } else if (m.type === "cms:select") {
        selection = m;
        if (m.kind === "text") inspectText(m);
        else if (m.kind === "image") inspectImage(m);
        else if (m.kind === "biz") {
          $("#insp-title").textContent = "Business info";
          $("#insp-body").innerHTML = '<p class="hint">Phone, email, service area, licence and logo are shared across the site.</p><button class="btn btn--sm" type="button" id="go-biz">Edit business info</button>';
          $("#go-biz").addEventListener("click", function () { showTab("business"); });
        } else if (m.kind === "custom") {
          $("#insp-title").textContent = "Custom section";
          $("#insp-body").innerHTML = '<p class="hint">This section was added in the Sections tab.</p><button class="btn btn--sm" type="button" id="go-sec">Edit in Sections</button>';
          $("#go-sec").addEventListener("click", function () { $("#sections-page").value = page; showTab("sections"); sections.load(); });
        }
      }
    });

    $("#editor-page").addEventListener("change", function () {
      var next = this.value;
      if (dirtyCount() && !confirm("Discard your unsaved changes on this page?")) { this.value = page; return; }
      load(next);
    });
    // Desktop preview renders the page at 1440px wide and scales it to fit.
    var DESKTOP = 1440;
    function fit() {
      var stage = $("#frame-stage");
      if (stage.classList.contains("is-mobile") || !stage.clientWidth) {
        frame.style.width = ""; frame.style.height = ""; frame.style.transform = "";
        return;
      }
      var scale = Math.min(1, stage.clientWidth / DESKTOP);
      frame.style.width = DESKTOP + "px";
      frame.style.height = (stage.clientHeight / scale) + "px";
      frame.style.transform = "scale(" + scale + ")";
    }
    window.addEventListener("resize", fit);
    $$(".seg button").forEach(function (b) {
      b.addEventListener("click", function () {
        $$(".seg button").forEach(function (x) { x.classList.toggle("is-active", x === b); });
        $("#frame-stage").classList.toggle("is-mobile", b.getAttribute("data-device") === "mobile");
        fit();
      });
    });
    $("#editor-discard").addEventListener("click", function () {
      if (!confirm("Discard all unsaved changes on this page?")) return;
      load(page);
    });
    $("#editor-save").addEventListener("click", function () {
      var btn = this;
      var pending = {};
      Object.keys(changes).forEach(function (k) { if (changes[k] !== undefined) pending[k] = changes[k]; });
      busy(btn, true, "Saving");
      saveContent(pending).then(function () {
        Object.keys(pending).forEach(function (k) {
          if (k.indexOf("hide:") === 0) { if (pending[k] === "1") hidden[k] = true; else delete hidden[k]; }
        });
        changes = {};
        busy(btn, false);
        refreshBar();
        toast("Changes saved and live on the website.");
      }).catch(function (err) { busy(btn, false); refreshBar(); fail(err, "Couldn't save changes."); });
    });

    return {
      init: function () { $("#editor-page").value = page; load(page); requestAnimationFrame(fit); },
      show: function () { requestAnimationFrame(fit); },
      dirty: function () { return dirtyCount() > 0; }
    };
  })();

  /* =====================================================================
     CUSTOM SECTIONS
     ===================================================================== */
  var TYPE_INFO = {
    text: { name: "Text block", desc: "Heading with paragraphs and an optional button.", icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M4 6h16M4 10h16M4 14h12M4 18h9"/></svg>' },
    image_text: { name: "Image and text", desc: "A photo beside a heading, text and button.", icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="3" y="5" width="9" height="14"/><path d="M15 8h6M15 12h6M15 16h4"/></svg>' },
    gallery: { name: "Gallery", desc: "A grid of project photos with captions.", icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="3" y="3" width="8" height="8"/><rect x="13" y="3" width="8" height="8"/><rect x="3" y="13" width="8" height="8"/><rect x="13" y="13" width="8" height="8"/></svg>' },
    features: { name: "Feature list", desc: "Numbered points, e.g. benefits or inclusions.", icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M9 6h12M9 12h12M9 18h12"/><path d="M4 5v2M3.5 11h1.5v2M3.5 17h1.5l-1.5 2h1.5"/></svg>' },
    cta: { name: "Call to action", desc: "A bold banner with a button, optional background photo.", icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="3" y="5" width="18" height="14"/><path d="M8 13h8M10 10h4"/></svg>' }
  };
  var THEME_FIELD = { name: "theme", label: "Background", type: "select", options: [["light", "White"], ["paper", "Off-white"], ["dark", "Black"], ["ink", "Charcoal"]] };
  var BUTTON_FIELDS = [
    { name: "button_label", label: "Button text", type: "text", half: true, placeholder: "e.g. Get a free quote" },
    { name: "button_url", label: "Button link", type: "text", half: true, placeholder: "get-a-quote.html" }
  ];
  var SCHEMAS = {
    text: [THEME_FIELD, { name: "align", label: "Alignment", type: "select", options: [["left", "Left"], ["center", "Centred"]] },
      { name: "eyebrow", label: "Small heading", type: "text" }, { name: "heading", label: "Heading", type: "text" },
      { name: "body", label: "Text", type: "textarea", help: "Leave a blank line between paragraphs." }].concat(BUTTON_FIELDS),
    image_text: [THEME_FIELD, { name: "image_side", label: "Image position", type: "select", options: [["left", "Image on the left"], ["right", "Image on the right"]] },
      { name: "image", label: "Image", type: "image" }, { name: "image_alt", label: "Image description", type: "text" },
      { name: "eyebrow", label: "Small heading", type: "text" }, { name: "heading", label: "Heading", type: "text" },
      { name: "body", label: "Text", type: "textarea", help: "Leave a blank line between paragraphs." }].concat(BUTTON_FIELDS),
    gallery: [THEME_FIELD, { name: "eyebrow", label: "Small heading", type: "text" }, { name: "heading", label: "Heading", type: "text" },
      { name: "intro", label: "Intro text", type: "textarea" },
      { name: "images", label: "Photos", type: "list", item: [{ name: "url", label: "Image", type: "image" }, { name: "caption", label: "Caption", type: "text" }], add: "Add photo" }],
    features: [THEME_FIELD, { name: "eyebrow", label: "Small heading", type: "text" }, { name: "heading", label: "Heading", type: "text" },
      { name: "intro", label: "Intro text", type: "textarea" },
      { name: "items", label: "Points", type: "list", item: [{ name: "title", label: "Title", type: "text" }, { name: "text", label: "Description", type: "textarea" }], add: "Add point" }],
    cta: [{ name: "eyebrow", label: "Small heading", type: "text" }, { name: "heading", label: "Heading", type: "text" },
      { name: "body", label: "Text", type: "textarea" }].concat(BUTTON_FIELDS).concat([{ name: "image", label: "Background photo (optional)", type: "image" }])
  };

  var uid = 0;
  function imageField(value, onChange) {
    var wrap = document.createElement("div");
    wrap.className = "img-field";
    function draw(v) {
      wrap.innerHTML = (v ? '<img src="' + esc(v) + '" alt="">' : '<span class="ph">' + ICON_IMG + "</span>") +
        '<div class="row"><button class="btn btn--sm" type="button" data-pick>' + (v ? "Change" : "Choose image") + "</button>" +
        (v ? '<button class="btn btn--ghost btn--sm" type="button" data-clear>Remove</button>' : "") + "</div>";
    }
    draw(value);
    wrap.addEventListener("click", function (e) {
      if (e.target.closest("[data-pick]")) picker.open().then(function (url) { if (url) { value = url; draw(url); onChange(url); } });
      if (e.target.closest("[data-clear]")) { value = ""; draw(""); onChange(""); }
    });
    return wrap;
  }
  function buildFields(container, schema, data) {
    var row = null;
    schema.forEach(function (f) {
      var id = "sf-" + (++uid);
      var field = document.createElement("div");
      field.className = "field";
      var label = '<label for="' + id + '">' + esc(f.label) + "</label>";
      var help = f.help ? "<small>" + esc(f.help) + "</small>" : "";
      var v = data[f.name];
      if (f.type === "text") {
        field.innerHTML = label + '<input class="input" id="' + id + '" value="' + esc(v || "") + '" placeholder="' + esc(f.placeholder || "") + '">' + help;
        field.querySelector("input").addEventListener("input", function () { data[f.name] = this.value; });
      } else if (f.type === "textarea") {
        field.innerHTML = label + '<textarea class="textarea" id="' + id + '">' + esc(v || "") + "</textarea>" + help;
        field.querySelector("textarea").addEventListener("input", function () { data[f.name] = this.value; });
      } else if (f.type === "select") {
        if (v == null) data[f.name] = v = f.options[0][0];
        field.innerHTML = label + '<select class="select" id="' + id + '">' + f.options.map(function (o) {
          return '<option value="' + o[0] + '"' + (o[0] === v ? " selected" : "") + ">" + esc(o[1]) + "</option>";
        }).join("") + "</select>" + help;
        field.querySelector("select").addEventListener("change", function () { data[f.name] = this.value; });
      } else if (f.type === "image") {
        field.innerHTML = '<span class="label">' + esc(f.label) + "</span>";
        field.appendChild(imageField(v || "", function (url) { data[f.name] = url; }));
      } else if (f.type === "list") {
        if (!Array.isArray(data[f.name])) data[f.name] = [];
        var list = data[f.name];
        field.innerHTML = '<span class="label">' + esc(f.label) + '</span><div class="list-items"></div><div><button class="btn btn--ghost btn--sm" type="button" data-add-item>' + esc(f.add) + "</button></div>";
        var box = field.querySelector(".list-items");
        var drawList = function () {
          box.innerHTML = "";
          list.forEach(function (item, i) {
            var el = document.createElement("div");
            el.className = "list-item";
            el.innerHTML = '<div class="list-item__bar"><span>' + (i + 1) + '</span><span class="row">' +
              '<button class="btn btn--ghost btn--icon btn--sm" type="button" data-up aria-label="Move up"' + (i === 0 ? " disabled" : "") + ">" + ICON_UP + "</button>" +
              '<button class="btn btn--ghost btn--icon btn--sm" type="button" data-down aria-label="Move down"' + (i === list.length - 1 ? " disabled" : "") + ">" + ICON_DOWN + "</button>" +
              '<button class="btn btn--danger btn--icon btn--sm" type="button" data-del aria-label="Remove">' + ICON_TRASH + "</button></span></div>";
            buildFields(el, f.item, item);
            el.querySelector("[data-up]").addEventListener("click", function () { list.splice(i - 1, 0, list.splice(i, 1)[0]); drawList(); });
            el.querySelector("[data-down]").addEventListener("click", function () { list.splice(i + 1, 0, list.splice(i, 1)[0]); drawList(); });
            el.querySelector("[data-del]").addEventListener("click", function () { list.splice(i, 1); drawList(); });
            box.appendChild(el);
          });
        };
        drawList();
        field.querySelector(":scope > div > [data-add-item]").addEventListener("click", function () { list.push({}); drawList(); });
      }
      if (f.half) {
        if (!row) { row = document.createElement("div"); row.className = "grid-2"; container.appendChild(row); row.appendChild(field); }
        else { row.appendChild(field); row = null; }
      } else {
        row = null;
        container.appendChild(field);
      }
    });
  }

  var sections = (function () {
    var items = [];
    var page = "index";
    var editing = null;

    function load() {
      page = $("#sections-page").value;
      var box = $("#sections-list");
      box.innerHTML = '<div class="empty">Loading…</div>';
      return Promise.all([
        sb.from("page_sections").select("*").eq("page", page).order("after_section").order("position").order("created_at"),
        pageInfo(page)
      ]).then(function (r) {
        if (r[0].error) throw r[0].error;
        items = r[0].data || [];
        render(r[1].sections);
      }).catch(function (err) { box.innerHTML = ""; fail(err, "Couldn't load sections."); });
    }
    function render(builtIn) {
      var box = $("#sections-list");
      if (!items.length) {
        box.innerHTML = '<div class="empty">' + TYPE_INFO.text.icon.replace("<svg", '<svg style="margin:0 auto 12px;width:36px;height:36px"') +
          'No custom sections on this page yet.<br><br><button class="btn" type="button" data-add>Add a section</button></div>';
        return;
      }
      var html = "";
      builtIn.forEach(function (b) {
        var group = items.filter(function (s) { return Math.min(s.after_section, builtIn.length - 1) === b.index; });
        if (!group.length) return;
        html += '<div class="group-title">After: ' + esc(b.name) + "</div>";
        group.forEach(function (s, i) {
          var d = s.data || {};
          var title = d.heading || d.eyebrow || TYPE_INFO[s.type].name;
          html += '<div class="sec-item" data-id="' + s.id + '"><span class="sec-item__icon">' + TYPE_INFO[s.type].icon + "</span>" +
            '<div class="sec-item__main"><strong>' + esc(title.replace(/\*/g, "")) + "</strong><span>" + TYPE_INFO[s.type].name + (s.published ? "" : " &middot; Hidden") + "</span></div>" +
            '<div class="sec-item__actions">' +
            '<label class="switch" title="Show on website"><input type="checkbox" data-pub' + (s.published ? " checked" : "") + "><i></i></label>" +
            '<button class="btn btn--ghost btn--icon btn--sm" type="button" data-move="-1" aria-label="Move up"' + (i === 0 ? " disabled" : "") + ">" + ICON_UP + "</button>" +
            '<button class="btn btn--ghost btn--icon btn--sm" type="button" data-move="1" aria-label="Move down"' + (i === group.length - 1 ? " disabled" : "") + ">" + ICON_DOWN + "</button>" +
            '<button class="btn btn--ghost btn--sm" type="button" data-edit>Edit</button>' +
            '<button class="btn btn--danger btn--icon btn--sm" type="button" data-del aria-label="Delete">' + ICON_TRASH + "</button></div></div>";
        });
      });
      html += '<div class="sec-item" style="justify-content:space-between"><span class="muted">Changes go live as soon as you save.</span><a class="btn btn--ghost btn--sm" href="' + pageUrl(page) + '" target="_blank" rel="noopener">' + ICON_EYE + " View page</a></div>";
      box.innerHTML = html;
    }

    $("#sections-list").addEventListener("click", function (e) {
      if (e.target.closest("[data-add]")) return openTypePicker();
      var row = e.target.closest(".sec-item[data-id]");
      if (!row) return;
      var s = items.filter(function (x) { return x.id === row.getAttribute("data-id"); })[0];
      if (!s) return;
      if (e.target.closest("[data-edit]")) openEditor(s.type, s);
      else if (e.target.closest("[data-del]")) {
        if (!confirm("Delete this section?")) return;
        sb.from("page_sections").delete().eq("id", s.id).then(function (res) {
          if (res.error) return fail(res.error);
          toast("Section deleted."); load();
        });
      } else if (e.target.closest("[data-move]")) {
        var dir = +e.target.closest("[data-move]").getAttribute("data-move");
        var group = items.filter(function (x) { return x.after_section === s.after_section; });
        var i = group.indexOf(s), j = i + dir;
        if (j < 0 || j >= group.length) return;
        group.splice(j, 0, group.splice(i, 1)[0]);
        Promise.all(group.map(function (x, n) { return sb.from("page_sections").update({ position: n }).eq("id", x.id); }))
          .then(function (rs) { rs.forEach(function (r) { if (r.error) throw r.error; }); load(); })
          .catch(function (err) { fail(err); });
      }
    });
    $("#sections-list").addEventListener("change", function (e) {
      if (!e.target.matches("[data-pub]")) return;
      var id = e.target.closest(".sec-item").getAttribute("data-id");
      sb.from("page_sections").update({ published: e.target.checked }).eq("id", id).then(function (res) {
        if (res.error) return fail(res.error);
        toast(e.target.checked ? "Section is now visible." : "Section hidden."); load();
      });
    });

    function openTypePicker() {
      $("#section-modal-title").textContent = "Add a section";
      $("#section-modal-foot").hidden = true;
      $("#section-modal-body").innerHTML = '<div class="types">' + Object.keys(TYPE_INFO).map(function (t) {
        return '<button class="type" type="button" data-type="' + t + '">' + TYPE_INFO[t].icon + "<strong>" + TYPE_INFO[t].name + "</strong><span>" + TYPE_INFO[t].desc + "</span></button>";
      }).join("") + "</div>";
      openLayer($("#section-modal"));
    }
    $("#section-modal-body").addEventListener("click", function (e) {
      var t = e.target.closest("[data-type]");
      if (t) openEditor(t.getAttribute("data-type"), null);
    });

    function openEditor(type, existing) {
      pageInfo(page).then(function (info) {
        editing = {
          id: existing ? existing.id : null,
          type: type,
          after_section: existing ? existing.after_section : Math.max(0, info.sections.length - 2),
          published: existing ? existing.published : true,
          data: JSON.parse(JSON.stringify(existing ? existing.data || {} : {}))
        };
        $("#section-modal-title").textContent = (existing ? "Edit " : "New ") + TYPE_INFO[type].name.toLowerCase();
        $("#section-modal-foot").hidden = false;
        var body = $("#section-modal-body");
        body.innerHTML = "";
        var place = document.createElement("div");
        place.className = "grid-2";
        place.innerHTML = '<div class="field"><label for="sec-after">Place after</label><select class="select" id="sec-after">' +
          info.sections.map(function (s) { return '<option value="' + s.index + '"' + (s.index === editing.after_section ? " selected" : "") + ">" + esc(s.name) + "</option>"; }).join("") +
          '</select></div><div class="field"><span class="label">Visibility</span><label class="switch" style="height:40px"><input type="checkbox" id="sec-pub"' + (editing.published ? " checked" : "") + "><i></i>Show on website</label></div>";
        body.appendChild(place);
        $("#sec-after").addEventListener("change", function () { editing.after_section = +this.value; });
        $("#sec-pub").addEventListener("change", function () { editing.published = this.checked; });
        var fields = document.createElement("div");
        fields.className = "form-section";
        buildFields(fields, SCHEMAS[type], editing.data);
        body.appendChild(fields);
        openLayer($("#section-modal"));
      });
    }

    $("#section-modal-save").addEventListener("click", function () {
      if (!editing) return;
      var btn = this;
      var d = editing.data;
      if (d.images) d.images = d.images.filter(function (i) { return i.url; });
      if (d.items) d.items = d.items.filter(function (i) { return i.title || i.text; });
      var row = { page: page, type: editing.type, after_section: editing.after_section, published: editing.published, data: d };
      var q;
      if (editing.id) q = sb.from("page_sections").update(row).eq("id", editing.id);
      else {
        var same = items.filter(function (x) { return x.after_section === editing.after_section; });
        row.position = same.length ? Math.max.apply(null, same.map(function (x) { return x.position; })) + 1 : 0;
        q = sb.from("page_sections").insert(row);
      }
      busy(btn, true, "Saving");
      q.then(function (res) {
        busy(btn, false);
        if (res.error) return fail(res.error);
        closeLayer($("#section-modal"));
        editing = null;
        toast("Section saved and live on the website.");
        load();
      });
    });

    $("#sections-page").addEventListener("change", load);
    $("#section-add").addEventListener("click", openTypePicker);

    return { init: load, show: load, load: load };
  })();

  /* =====================================================================
     BUSINESS INFO
     ===================================================================== */
  var business = (function () {
    var logo = "";
    function drawLogo() {
      var box = $("#biz-logo-field");
      box.innerHTML = "";
      var f = imageField(logo, function (url) { logo = url; });
      box.parentNode.replaceChild(f, box);
      f.id = "biz-logo-field";
    }
    function load() {
      loadContent(["biz."]).then(function (map) {
        $$("[data-biz-field]").forEach(function (inp) { inp.value = map["biz." + inp.getAttribute("data-biz-field")] || ""; });
        logo = map["biz.logo"] || "";
        drawLogo();
      }).catch(function (err) { fail(err, "Couldn't load business info."); });
    }
    $("#biz-save").addEventListener("click", function () {
      var btn = this;
      var email = $("#biz-email").value.trim();
      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { toast("Please enter a valid email address.", true); return; }
      var changes = { "biz.logo": logo };
      $$("[data-biz-field]").forEach(function (inp) { changes["biz." + inp.getAttribute("data-biz-field")] = inp.value.trim(); });
      busy(btn, true, "Saving");
      saveContent(changes).then(function () { busy(btn, false); toast("Business info saved."); })
        .catch(function (err) { busy(btn, false); fail(err); });
    });
    return { init: load, show: load };
  })();

  /* =====================================================================
     MEDIA LIBRARY
     ===================================================================== */
  var media = (function () {
    var stale = true;
    function load() {
      stale = false;
      var grid = $("#media-grid");
      grid.innerHTML = '<div class="muted">Loading…</div>';
      listMedia().then(function (items) {
        $("#media-empty").hidden = items.length > 0;
        grid.innerHTML = items.map(function (m) {
          return '<figure class="media-item" data-path="' + esc(m.path) + '" data-url="' + esc(m.url) + '"><img src="' + esc(m.url) + '" alt="" loading="lazy">' +
            "<figcaption>" + esc(m.name) + (m.size ? " &middot; " + Math.round(m.size / 1024) + " KB" : "") + "</figcaption>" +
            '<div class="actions"><button class="btn btn--icon btn--sm" type="button" data-copy aria-label="Copy link">' + ICON_LINK + "</button>" +
            '<button class="btn btn--icon btn--sm" type="button" data-del aria-label="Delete">' + ICON_TRASH + "</button></div></figure>";
        }).join("");
      }).catch(function (err) { grid.innerHTML = ""; fail(err, "Couldn't load media."); });
    }
    $("#media-grid").addEventListener("click", function (e) {
      var item = e.target.closest(".media-item");
      if (!item) return;
      if (e.target.closest("[data-copy]")) {
        navigator.clipboard.writeText(item.getAttribute("data-url")).then(function () { toast("Image link copied."); });
      } else if (e.target.closest("[data-del]")) {
        if (!confirm("Delete this image? If it's used on the website it will stop showing.")) return;
        sb.storage.from(BUCKET).remove([item.getAttribute("data-path")]).then(function (res) {
          if (res.error) return fail(res.error);
          toast("Image deleted."); load();
        });
      }
    });
    setupDrop($("#media-drop"), $("#media-input"), function (files) {
      var label = $("#media-drop strong");
      var done = 0;
      label.textContent = "Uploading 1 of " + files.length + "…";
      files.reduce(function (p, f) {
        return p.then(function () {
          return upload(f).then(function () { done++; label.textContent = "Uploading " + Math.min(done + 1, files.length) + " of " + files.length + "…"; })
            .catch(function (err) { fail(err, "Upload failed."); });
        });
      }, Promise.resolve()).then(function () {
        label.textContent = "Click to upload";
        if (done) toast(done + (done === 1 ? " image uploaded." : " images uploaded."));
        load();
      });
    });
    return { init: load, show: function () { if (stale) load(); }, invalidate: function () { stale = true; } };
  })();

  /* =====================================================================
     SEO
     ===================================================================== */
  var seo = (function () {
    var saved = {};
    function load() {
      var box = $("#seo-list");
      box.innerHTML = '<div class="empty">Loading…</div>';
      Promise.all([loadContent(["seo:"])].concat(PAGES.map(function (p) { return pageInfo(p.id); }))).then(function (r) {
        saved = r[0];
        box.innerHTML = PAGES.map(function (p, i) {
          var info = r[i + 1];
          var t = saved["seo:" + p.id + ":title"] || "", d = saved["seo:" + p.id + ":description"] || "";
          return '<div class="seo-row" data-page="' + p.id + '"><h3>' + esc(p.name) + '<a href="' + pageUrl(p.id) + '" target="_blank" rel="noopener">' + esc(p.id) + ".html</a></h3>" +
            '<div class="field"><label>Title</label><input class="input" data-k="title" maxlength="120" value="' + esc(t) + '" placeholder="' + esc(info.title) + '"><span class="counter"></span></div>' +
            '<div class="field"><label>Description</label><textarea class="textarea" data-k="description" maxlength="320" style="min-height:70px" placeholder="' + esc(info.description) + '">' + esc(d) + '</textarea><span class="counter"></span></div></div>';
        }).join("");
        $$("#seo-list [data-k]").forEach(counter);
      }).catch(function (err) { box.innerHTML = ""; fail(err, "Couldn't load SEO settings."); });
    }
    function counter(el) {
      var max = el.getAttribute("data-k") === "title" ? 60 : 160;
      var n = (el.value || el.placeholder).length;
      el.nextElementSibling.textContent = n + " / " + max + " recommended" + (el.value ? "" : " (default)");
    }
    $("#seo-list").addEventListener("input", function (e) { if (e.target.matches("[data-k]")) counter(e.target); });
    $("#seo-save").addEventListener("click", function () {
      var btn = this, changes = {};
      $$("#seo-list .seo-row").forEach(function (row) {
        $$("[data-k]", row).forEach(function (el) {
          var key = "seo:" + row.getAttribute("data-page") + ":" + el.getAttribute("data-k");
          var v = el.value.trim();
          if (v) changes[key] = v; else if (key in saved) changes[key] = null;
        });
      });
      busy(btn, true, "Saving");
      saveContent(changes).then(function () {
        busy(btn, false); toast("SEO settings saved.");
        Object.keys(changes).forEach(function (k) { if (changes[k] === null) delete saved[k]; else saved[k] = changes[k]; });
      }).catch(function (err) { busy(btn, false); fail(err); });
    });
    return { init: load };
  })();

  var MODULES = { leads: leads, editor: editor, sections: sections, business: business, media: media, seo: seo };
})();
