/* Frankie Velvet and the Tendertones — the Official Archive
   Small progressive enhancements. Nothing here is required for the pages to read. */

(function () {
  "use strict";

  /* ---------------------------------------------------------------- player */
  var player = document.querySelector("[data-player]");
  if (player) {
    var audio = player.querySelector("audio");
    var buttons = Array.prototype.slice.call(player.querySelectorAll(".trk"));
    var nowEl = player.querySelector("[data-now]");
    var stateEl = player.querySelector("[data-state]");
    var current = -1;

    function label(i) {
      var b = buttons[i];
      return b ? b.getAttribute("data-title") : "";
    }

    function setState(msg) {
      if (stateEl) stateEl.textContent = msg;
    }

    function select(i) {
      buttons.forEach(function (b, n) {
        b.setAttribute("aria-current", n === i ? "true" : "false");
      });
      current = i;
      if (nowEl) nowEl.textContent = label(i);
    }

    function play(i) {
      var src = buttons[i].getAttribute("data-src");
      if (!src) {
        select(i);
        setState("Not yet digitised — reel held at Preston.");
        return;
      }
      select(i);
      if (audio.getAttribute("src") !== src) audio.setAttribute("src", src);
      setState("Playing");
      var p = audio.play();
      if (p && p.catch) {
        p.catch(function () {
          setState("Not yet digitised — reel held at Preston.");
        });
      }
    }

    buttons.forEach(function (b, i) {
      b.addEventListener("click", function () {
        if (i === current && !audio.paused) {
          audio.pause();
          setState("Paused");
        } else {
          play(i);
        }
      });
    });

    audio.addEventListener("ended", function () {
      if (current + 1 < buttons.length) play(current + 1);
      else setState("End of side two.");
    });
    audio.addEventListener("error", function () {
      setState("Not yet digitised — reel held at Preston.");
    });
    audio.addEventListener("pause", function () {
      if (!audio.ended && audio.currentTime > 0) setState("Paused");
    });

    if (buttons.length) select(0);
  }

  /* -------------------------------------------------------------- lightbox */
  var plates = document.querySelectorAll("[data-zoom]");
  if (plates.length) {
    var box = document.createElement("div");
    box.className = "lightbox";
    box.setAttribute("hidden", "");
    box.innerHTML =
      '<button class="lightbox__x" aria-label="Close">&times;</button>' +
      '<figure><img alt=""><figcaption></figcaption></figure>';
    document.body.appendChild(box);

    var lbImg = box.querySelector("img");
    var lbCap = box.querySelector("figcaption");
    var lastFocus = null;

    function open(src, cap, alt) {
      lastFocus = document.activeElement;
      lbImg.setAttribute("src", src);
      lbImg.setAttribute("alt", alt || "");
      lbCap.textContent = cap || "";
      box.hidden = false;
      document.body.style.overflow = "hidden";
      box.querySelector(".lightbox__x").focus();
    }
    function close() {
      box.hidden = true;
      lbImg.removeAttribute("src");
      document.body.style.overflow = "";
      if (lastFocus) lastFocus.focus();
    }

    Array.prototype.forEach.call(plates, function (el) {
      el.style.cursor = "zoom-in";
      el.setAttribute("tabindex", "0");
      el.setAttribute("role", "button");
      function fire() {
        var img = el.querySelector("img");
        var cap = el.querySelector("figcaption");
        if (img) open(img.getAttribute("src"), cap ? cap.textContent : "", img.alt);
      }
      el.addEventListener("click", fire);
      el.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fire(); }
      });
    });

    box.addEventListener("click", function (e) {
      if (e.target === box || e.target.classList.contains("lightbox__x")) close();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !box.hidden) close();
    });
  }

  /* ------------------------------------------------- discography filtering */
  var filterBar = document.querySelector("[data-filter]");
  if (filterBar) {
    var items = document.querySelectorAll("[data-kind]");
    filterBar.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-show]");
      if (!b) return;
      var want = b.getAttribute("data-show");
      Array.prototype.forEach.call(filterBar.querySelectorAll("button"), function (x) {
        x.setAttribute("aria-pressed", x === b ? "true" : "false");
      });
      Array.prototype.forEach.call(items, function (it) {
        it.hidden = !(want === "all" || it.getAttribute("data-kind") === want);
      });
    });
  }
})();
