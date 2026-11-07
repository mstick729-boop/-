/* Хитър Петър · interactions. No library.
   Motion keeps working under prefers-reduced-motion through opacity, glow and clip;
   only movement (parallax, slides, swings) is swapped for fades. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");
  /* Every page opens at the top (unless the link points to a section) */
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  var toTop = function () { if (!location.hash) window.scrollTo(0, 0); };
  toTop(); window.addEventListener("pageshow", toTop); window.addEventListener("load", toTop);
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* Header turns solid after the first screen starts to scroll */
  var header = $(".site-header");
  if (header) {
    var hs = function () { header.classList.toggle("is-scrolled", window.scrollY > 40); };
    hs(); window.addEventListener("scroll", hs, { passive: true });
  }

  /* Drawer */
  var drawer = $("#drawer"), toggle = $(".menu-toggle"), lastFocus = null;
  var setDrawer = function (open) {
    drawer.classList.toggle("is-open", open);
    drawer.setAttribute("aria-hidden", open ? "false" : "true");
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.style.overflow = open ? "hidden" : "";
    if (open) { lastFocus = document.activeElement; setTimeout(function () { $(".drawer-close").focus(); }, 80); }
    else if (lastFocus) lastFocus.focus();
  };
  if (drawer && toggle) {
    toggle.addEventListener("click", function () { setDrawer(true); });
    $(".drawer-close").addEventListener("click", function () { setDrawer(false); });
    drawer.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setDrawer(false);
      if (e.key === "Tab") {
        var f = $$("a,button", drawer), a = f[0], z = f[f.length - 1];
        if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); }
      }
    });
    $$("nav a", drawer).forEach(function (a) { a.addEventListener("click", function () { setDrawer(false); }); });
  }

  /* Open now: every day 10:00–01:00, Plovdiv time */
  var openNow = function () { $$("[data-open-now]").forEach(function (el) {
    try {
      var p = new Intl.DateTimeFormat("en-GB", { timeZone: "Europe/Sofia", hour: "2-digit", minute: "2-digit", hourCycle: "h23" }).formatToParts(new Date());
      var h = +p.find(function (x) { return x.type === "hour"; }).value, m = +p.find(function (x) { return x.type === "minute"; }).value;
      var t = h * 60 + m;
      var state = t >= 600 && t < 1320 ? "open" : (t >= 1320 || t < 60) ? "late" : "closed";
      el.dataset.state = state;
      el.textContent = state === "closed" ? "Затворено · отваряме в 10:00" : "Отворено сега, до 01:00";
    } catch (e) {}
  }); };
  openNow(); setInterval(openNow, 30000);
  document.addEventListener("visibilitychange", function () { if (!document.hidden) openNow(); });

  /* Scroll progress (0..1) for sticky scenes: the wall of greenery, the feast photo */
  var scenes = $$("[data-scene]");
  if (scenes.length) {
    var tick = false;
    var update = function () {
      tick = false;
      var vh = window.innerHeight;
      scenes.forEach(function (s) {
        var r = s.getBoundingClientRect(), p;
        if (s.dataset.scene === "sticky") p = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height - vh)));
        else p = Math.min(1, Math.max(0, (vh - r.top) / (vh + r.height)));
        s.style.setProperty("--p", p.toFixed(3));
      });
    };
    update();
    window.addEventListener("scroll", function () { if (!tick) { tick = true; requestAnimationFrame(update); } }, { passive: true });
    window.addEventListener("resize", update);
  }

  /* Hero postcards lean toward the pointer (full motion only) */
  var cards = $(".cards");
  if (cards && fine && !reduce) {
    var hero = $(".hero");
    hero.addEventListener("pointermove", function (e) {
      var x = e.clientX / window.innerWidth - .5, y = e.clientY / window.innerHeight - .5;
      cards.style.translate = (x * 18).toFixed(1) + "px " + (y * 14).toFixed(1) + "px";
    });
    hero.addEventListener("pointerleave", function () { cards.style.translate = "0 0"; });
    cards.style.transition = "translate 600ms cubic-bezier(0.23, 1, 0.32, 1)";
  }

  /* Things that light up or swing in once when they arrive */
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        var t = en.target;
        if (t.classList.contains("neon--dim")) t.classList.add("is-lit");
        if (t.classList.contains("rail")) {
          $$(".pc", t).forEach(function (pc, i) { setTimeout(function () { pc.classList.remove("swing-wait"); }, 90 * i); });
        }
        io.unobserve(t);
      });
    }, { threshold: .25 });
    $$(".neon--dim").forEach(function (el) { io.observe(el); });
    $$(".rail").forEach(function (rail) {
      if (rail.getBoundingClientRect().top > window.innerHeight) {
        $$(".pc", rail).forEach(function (pc) { pc.classList.add("swing-wait"); });
        io.observe(rail);
      }
    });
  } else {
    $$(".neon--dim").forEach(function (el) { el.classList.add("is-lit"); });
  }

  /* Postcard rail: buttons and drag */
  $$(".rail").forEach(function (rail) {
    var step = function (dir) { var c = rail.querySelector(".pc"); rail.scrollBy({ left: dir * (c ? c.offsetWidth + 30 : 320), behavior: reduce ? "auto" : "smooth" }); };
    var sec = rail.closest("section");
    var prev = sec && sec.querySelector("[data-rail-prev]"), next = sec && sec.querySelector("[data-rail-next]");
    if (prev) prev.addEventListener("click", function () { step(-1); });
    if (next) next.addEventListener("click", function () { step(1); });
    if (!fine) return;
    var down = false, sx = 0, sl = 0, moved = false;
    rail.addEventListener("pointerdown", function (e) { if (e.pointerType !== "mouse") return; down = true; moved = false; sx = e.clientX; sl = rail.scrollLeft; });
    window.addEventListener("pointermove", function (e) { if (!down) return; var dx = e.clientX - sx; if (Math.abs(dx) > 4) { moved = true; rail.classList.add("is-drag"); } rail.scrollLeft = sl - dx; });
    window.addEventListener("pointerup", function () { if (!down) return; down = false; setTimeout(function () { rail.classList.remove("is-drag"); }, 0); });
    rail.addEventListener("click", function (e) { if (moved) { e.stopPropagation(); e.preventDefault(); moved = false; } }, true);
  });

  /* Menu card tabs */
  var tabs = $$(".tab");
  if (tabs.length) {
    var choose = function (tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab, panel = document.getElementById(t.getAttribute("aria-controls"));
        t.setAttribute("aria-selected", on ? "true" : "false"); t.tabIndex = on ? 0 : -1;
        panel.hidden = !on;
        if (on) { panel.classList.remove("is-in"); void panel.offsetWidth; panel.classList.add("is-in"); }
      });
      if (focus) tab.focus();
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { choose(t); });
      t.addEventListener("keydown", function (e) {
        var n = null;
        if (e.key === "ArrowRight" || e.key === "ArrowDown") n = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowLeft" || e.key === "ArrowUp") n = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === "Home") n = tabs[0]; if (e.key === "End") n = tabs[tabs.length - 1];
        if (n) { e.preventDefault(); choose(n, true); }
      });
    });
  }

  /* Full menu: active category and search */
  var mnav = $(".menu-nav");
  if (mnav) {
    var links = $$("a", mnav), cats = links.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var active = function () {
      var y = window.innerHeight * .35, cur = null;
      cats.forEach(function (c) { if (c && !c.hidden && c.getBoundingClientRect().top < y) cur = c.id; });
      if (!cur) { var f = cats.filter(function (c) { return c && !c.hidden; })[0]; cur = f && f.id; }
      links.forEach(function (a) {
        var on = a.getAttribute("href") === "#" + cur;
        if (on !== a.classList.contains("is-active")) {
          a.classList.toggle("is-active", on);
          if (on) { a.setAttribute("aria-current", "true"); var nr = mnav.getBoundingClientRect(), ar = a.getBoundingClientRect(); if (ar.left < nr.left || ar.right > nr.right) mnav.scrollBy({ left: ar.left - nr.left - 16, behavior: "auto" }); }
          else a.removeAttribute("aria-current");
        }
      });
    };
    var mt = false;
    window.addEventListener("scroll", function () { if (!mt) { mt = true; requestAnimationFrame(function () { mt = false; active(); }); } }, { passive: true });
    active();
    var q = $("#menu-q"), empty = $(".menu-empty");
    var norm = function (s) { return s.toLowerCase().replace(/[„“”"'«»]/g, "").replace(/\s+/g, " ").trim(); };
    if (q) q.addEventListener("input", function () {
      var v = norm(q.value), total = 0;
      $$(".menu-cat").forEach(function (cat) {
        var cn = 0;
        $$(".menu-group", cat).forEach(function (g) {
          var gn = 0;
          $$(".dish", g).forEach(function (d) { var hit = !v || norm(d.textContent).indexOf(v) > -1; d.hidden = !hit; if (hit) gn++; });
          g.hidden = gn === 0; cn += gn;
        });
        cat.hidden = cn === 0; total += cn;
      });
      links.forEach(function (a, i) { a.hidden = cats[i] ? cats[i].hidden : false; });
      empty.hidden = total !== 0;
      active();
    });
  }

  /* Lightbox for postcards */
  var lb = $("#lightbox");
  if (lb) {
    var img = null, cnt = $(".lb-count", lb), cap = $(".lb-cap", lb), items = [], idx = 0, opener = null;
    var show = function (i) {
      if (!img) { img = document.createElement("img"); img.alt = ""; $(".lb-stage", lb).prepend(img); }
      idx = (i + items.length) % items.length;
      var it = items[idx]; img.classList.remove("is-ready");
      var pre = new Image();
      pre.onload = function () { img.src = it.src; img.alt = it.alt; requestAnimationFrame(function () { img.classList.add("is-ready"); }); };
      pre.src = it.src;
      cnt.textContent = (idx + 1) + " / " + items.length; cap.textContent = it.cap || "";
    };
    var open = function (t) {
      var group = t.getAttribute("data-lb"), all = $$('[data-lb="' + group + '"]');
      items = all.map(function (el) { return { src: el.getAttribute("data-full"), alt: el.querySelector("img").alt, cap: el.getAttribute("data-cap") }; });
      opener = t; lb.hidden = false; document.body.style.overflow = "hidden";
      requestAnimationFrame(function () { lb.classList.add("is-open"); });
      show(all.indexOf(t)); $(".lb-close", lb).focus();
    };
    var close = function () {
      lb.classList.remove("is-open"); document.body.style.overflow = "";
      setTimeout(function () { lb.hidden = true; if (img) img.classList.remove("is-ready"); }, 260);
      if (opener) opener.focus();
    };
    document.addEventListener("click", function (e) { var t = e.target.closest("[data-lb]"); if (t) { e.preventDefault(); open(t); } });
    $(".lb-close", lb).addEventListener("click", close);
    $(".lb-prev", lb).addEventListener("click", function () { show(idx - 1); });
    $(".lb-next", lb).addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb || e.target.classList.contains("lb-stage")) close(); });
    document.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") close(); if (e.key === "ArrowRight") show(idx + 1); if (e.key === "ArrowLeft") show(idx - 1);
      if (e.key === "Tab") { var f = $$("button", lb), a = f[0], z = f[f.length - 1]; if (e.shiftKey && document.activeElement === a) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a.focus(); } }
    });
    var sx = null, st = 0;
    lb.addEventListener("pointerdown", function (e) { if (e.pointerType !== "mouse") { sx = e.clientX; st = Date.now(); } });
    lb.addEventListener("pointerup", function (e) { if (sx === null) return; var dx = e.clientX - sx, v = Math.abs(dx) / Math.max(1, Date.now() - st); if (Math.abs(dx) > 60 || v > .11) show(idx + (dx < 0 ? 1 : -1)); sx = null; });
  }

  /* Inquiry pad: validates and prepares an e-mail. Nothing is stored or sent here. */
  var form = $("#inquiry");
  if (form) {
    var out = $("#inq-out"), pre = $("pre", out), mail = $("[data-mailto]", out), copy = $("[data-copy]", out), status = $(".status-line", out), EMAIL = form.getAttribute("data-email");
    var today = new Date(); today.setHours(0, 0, 0, 0);
    var started = Date.now();
    if (location.hash === "#sabitie") { var ev = $("#t-event"); if (ev) ev.checked = true; }
    var setErr = function (el, msg) { el.setAttribute("aria-invalid", msg ? "true" : "false"); var b = document.getElementById(el.id + "-err"); if (b) b.textContent = msg || ""; return !msg; };
    var parseDate = function (s) { var m = /^\s*(\d{1,2})[.\/-](\d{1,2})[.\/-](\d{4})\s*$/.exec(s); if (!m) return null; var d = new Date(+m[3], +m[2] - 1, +m[1]); return d.getDate() === +m[1] && d.getMonth() === +m[2] - 1 ? d : null; };
    var rules = {
      "f-date": function (v) { var d = parseDate(v); if (!d) return "Напишете дата във формат ДД.ММ.ГГГГ, например 24.12.2026."; return d < today ? "Изберете дата от днес нататък." : ""; },
      "f-time": function (v) { if (!v.trim()) return ""; var m = /^(\d{1,2})[:.](\d{2})$/.exec(v.trim()); if (!m || +m[1] > 23 || +m[2] > 59) return "Напишете час във формат ЧЧ:ММ, например 19:30."; var t = +m[1] * 60 + +m[2]; return t >= 600 || t <= 30 ? "" : "Работим от 10:00 до 01:00."; },
      "f-guests": function (v) { var n = parseInt(v, 10); return n >= 1 && n <= 300 ? "" : "Напишете брой гости от 1 до 300."; },
      "f-name": function (v) { return v.trim().length >= 2 ? "" : "Напишете името си."; },
      "f-phone": function (v) { return /^[+\d][\d\s()-]{6,}$/.test(v.trim()) ? "" : "Напишете телефон за връзка, например 0888 123 456."; },
      "f-email": function (v) { return !v.trim() || /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? "" : "Проверете имейл адреса."; }
    };
    Object.keys(rules).forEach(function (id) { var el = document.getElementById(id); el.addEventListener("blur", function () { if (el.value) setErr(el, rules[id](el.value)); }); });
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if ($(".hp input", form).value) return;
      var bad = null;
      Object.keys(rules).forEach(function (id) { var el = document.getElementById(id); if (!setErr(el, rules[id](el.value)) && !bad) bad = el; });
      if (bad) { bad.focus(); return; }
      /* Basic abuse limits: a human needs a few seconds to fill the pad, and a new inquiry waits 30 s */
      if (Date.now() - started < 3000) return;
      var last = 0; try { last = +sessionStorage.getItem("hp-inq") || 0; } catch (er) {}
      if (Date.now() - last < 30000) { out.hidden = false; status.textContent = "Току-що изпратихте запитване. Изчакайте малко, преди да пратите ново."; return; }
      var v = function (id) { return document.getElementById(id).value.trim(); };
      var type = $('input[name="type"]:checked', form).value;
      var lines = ["Запитване от сайта: " + type, "", "Име: " + v("f-name"), "Телефон: " + v("f-phone")];
      if (v("f-email")) lines.push("Имейл: " + v("f-email"));
      lines.push("Дата: " + v("f-date") + (v("f-time") ? ", " + v("f-time") + " ч." : ""), "Брой гости: " + v("f-guests"));
      if (v("f-msg")) lines.push("", "Бележка: " + v("f-msg"));
      lines.push("", "Моля, потвърдете по телефона дали има свободни места.");
      var body = lines.join("\n");
      var subject = type + " за " + v("f-date") + ", " + v("f-guests") + " гости";
      var endpoint = form.getAttribute("data-endpoint"), key = form.getAttribute("data-key");
      var btn = $('button[type="submit"]', form);
      var prepare = function (note) {
        pre.textContent = body;
        mail.href = "mailto:" + EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
        try { sessionStorage.setItem("hp-inq", String(Date.now())); } catch (er) {}
        out.hidden = false; out.classList.remove("is-in"); void out.offsetWidth; out.classList.add("is-in");
        status.textContent = note || ""; out.focus();
      };
      if (endpoint && key) {
        btn.disabled = true; var label = btn.textContent; btn.textContent = "Изпращаме…";
        fetch(endpoint, { method: "POST", headers: { "Content-Type": "application/json", Accept: "application/json" },
          body: JSON.stringify({ access_key: key, subject: "Сайт: " + subject, from_name: "Сайт „Хитър Петър“", name: v("f-name"), phone: v("f-phone"), email: v("f-email") || undefined, message: body, botcheck: "" }) })
          .then(function (r) { return r.json().then(function (d) { if (!r.ok || !d.success) throw new Error(d.message || r.status); }); })
          .then(function () {
            try { sessionStorage.setItem("hp-inq", String(Date.now())); } catch (er) {}
            form.hidden = true; var sent = $("#inq-sent"); sent.hidden = false; sent.focus();
          })
          .catch(function () { prepare("Не успяхме да изпратим запитването автоматично. Изпратете този текст по имейл или се обадете."); })
          .then(function () { btn.disabled = false; btn.textContent = label; });
        return;
      }
      prepare();

    });
    copy.addEventListener("click", function () {
      var done = function () { status.textContent = "Текстът е копиран. Поставете го в имейл до " + EMAIL + "."; };
      var fb = function () { var r = document.createRange(); r.selectNodeContents(pre); var s = getSelection(); s.removeAllRanges(); s.addRange(r); status.textContent = "Текстът е маркиран. Копирайте го с Ctrl+C."; };
      try { navigator.clipboard.writeText(pre.textContent).then(done, fb); } catch (er) { fb(); }
    });
  }
  $$("[data-copy-text]").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.getAttribute("data-copy-text"), l = b.innerHTML;
      try { navigator.clipboard.writeText(t).then(function () { b.textContent = "Копирано"; setTimeout(function () { b.innerHTML = l; }, 1600); }, function () {}); } catch (e) {}
    });
  });
  /* Photos fade in over their blurred preview, and every lazy photo is fetched once the page is idle */
  $$("img.lz").forEach(function (im) {
    var done = function () { im.classList.add("is-loaded"); };
    if (im.complete && im.naturalWidth) done(); else { im.addEventListener("load", done); im.addEventListener("error", done); }
  });
  window.addEventListener("load", function () {
    var go = function () { $$('img[loading="lazy"]').forEach(function (im) { im.loading = "eager"; }); };
    if ("requestIdleCallback" in window) requestIdleCallback(go, { timeout: 1500 }); else setTimeout(go, 800);
  });

  /* Sections that rise softly into place once */
  var rv = $$(".reveal");
  if (rv.length && "IntersectionObserver" in window) {
    var ro = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.remove("is-waiting"); ro.unobserve(en.target); } }); }, { threshold: .15 });
    rv.forEach(function (el) { if (el.getBoundingClientRect().top > window.innerHeight * .9) { el.classList.add("is-waiting"); ro.observe(el); } });
  }

  /* Hero postcards drift a little with the pointer */
  var floats = $$(".float");
  if (floats.length && fine && !reduce) {
    var hero2 = $(".hero");
    hero2.addEventListener("pointermove", function (e) {
      var x = e.clientX / window.innerWidth - .5, y = e.clientY / window.innerHeight - .5;
      floats.forEach(function (f, i) { var d = (i % 2 ? 1 : -1) * (10 + i * 4); f.style.translate = (x * d).toFixed(1) + "px " + (y * d).toFixed(1) + "px"; });
    });
    hero2.addEventListener("pointerleave", function () { floats.forEach(function (f) { f.style.translate = "0 0"; }); });
  }
  /* Phone links: on a computer, and inside an embedded preview where tel: cannot dial, show the number in a box */
  var callbox = $("#callbox");
  if (callbox) {
    var desktop = fine && !("ontouchstart" in window && navigator.maxTouchPoints > 0);
    var framed = false; try { framed = window.self !== window.top; } catch (e) { framed = true; }
    if (desktop) document.documentElement.classList.add("is-desktop");
    if (framed) document.documentElement.classList.add("is-framed");
    var cbOpener = null;
    var openCall = function () {
      cbOpener = document.activeElement; callbox.hidden = false; document.body.style.overflow = "hidden";
      requestAnimationFrame(function () { callbox.classList.add("is-open"); });
      $(".callbox-x", callbox).focus();
    };
    var closeCall = function () {
      callbox.classList.remove("is-open"); document.body.style.overflow = "";
      setTimeout(function () { callbox.hidden = true; }, 230);
      if (cbOpener && cbOpener.focus) cbOpener.focus();
    };
    document.addEventListener("click", function (e) {
      var a = e.target.closest('a[href^="tel:"]');
      if (!a || a.hasAttribute("data-native") && !framed) return;
      if (desktop || framed) {
        if (a.hasAttribute("data-native") && framed && !desktop) {
          /* Inside the preview on a phone: try the dialer through the top window, the box stays open as a fallback */
          try { window.top.location.href = a.href; } catch (er) {}
          return;
        }
        e.preventDefault(); openCall();
      }
    });
    $(".callbox-x", callbox).addEventListener("click", closeCall);
    document.addEventListener("keydown", function (e) {
      if (callbox.hidden) return;
      if (e.key === "Escape") closeCall();
      if (e.key === "Tab") { var f = $$("button, a", callbox).filter(function (x) { return x.offsetParent; }), a1 = f[0], z = f[f.length - 1]; if (e.shiftKey && document.activeElement === a1) { e.preventDefault(); z.focus(); } else if (!e.shiftKey && document.activeElement === z) { e.preventDefault(); a1.focus(); } }
    });
  }

  /* iOS: block pinch and double-tap zoom */
  document.addEventListener("gesturestart", function (e) { e.preventDefault(); });
  var lastTouch = 0;
  document.addEventListener("touchend", function (e) { var now = Date.now(); if (now - lastTouch < 300 && !e.target.closest("a, button, input, textarea, select, label")) e.preventDefault(); lastTouch = now; }, { passive: false });
})();
