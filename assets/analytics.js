/* TrueMid Manufacturing - GA4 analytics + conversion tracking
   Self-contained. Loaded at the end of <body> on all 13 pages.
   - Loads GA4 only after cookie consent (GDPR)
   - Tracks: generate_lead, contact_click, quote_cta_click
   - Submits quote form via AJAX (no redirect to formspree.io)
   - Debug mode: append ?ga_debug=1 to any URL to feed GA4 DebugView
*/
(function () {
  'use strict';

  var GA_ID = 'G-CENSR6CBB0';
  var CONSENT_KEY = 'tm_cookie_consent';
  var FIRST_REF_KEY = 'tm_first_referrer';
  var EMAIL_FALLBACK = ' Please email bruce@truemidmanufacturing.com.';

  /* ---------- styles (injected, so existing style.css is untouched) ---------- */
  function injectCss() {
    var s = document.createElement('style');
    s.textContent =
      '.tm-cookie{position:fixed;left:0;right:0;bottom:0;z-index:10000;background:#111827;color:#F4F7FA;padding:1rem 1.25rem;box-shadow:0 -2px 16px rgba(0,0,0,.18)}' +
      '.tm-cookie-inner{max-width:1200px;margin:0 auto;display:flex;align-items:center;gap:1.25rem;flex-wrap:wrap}' +
      '.tm-cookie p{flex:1 1 460px;margin:0;font-size:.85rem;line-height:1.55;color:#E8ECF0;font-family:inherit}' +
      '.tm-cookie a{color:#85B7EB;text-decoration:underline}' +
      '.tm-cookie button{background:#F6821F;color:#fff;border:0;border-radius:8px;padding:.6rem 1.6rem;font-size:.9rem;font-weight:600;cursor:pointer;white-space:nowrap;font-family:inherit}' +
      '.tm-cookie button:hover{background:#d96f12}' +
      '.toast.error{background:#EF4444}' +
      '@media(max-width:600px){.tm-cookie-inner{flex-direction:column;align-items:stretch;gap:.75rem}.tm-cookie button{width:100%}}';
    document.head.appendChild(s);
  }

  /* ---------- helpers ---------- */
  function privacyHref() {
    var p = location.pathname;
    return (p.indexOf('/cases/') > -1 || p.indexOf('/blog/') > -1) ? '../privacy.html' : 'privacy.html';
  }

  function showToast(msg, type) {
    var t = document.getElementById('toast');
    if (!t) {
      t = document.createElement('div');
      t.id = 'toast';
      t.className = 'toast';
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.className = 'toast ' + (type === 'error' ? 'error' : 'success') + ' show';
    if (t._tmTimer) clearTimeout(t._tmTimer);
    t._tmTimer = setTimeout(function () { t.className = 'toast'; }, 5000);
  }

  function tmEvent(name, params) {
    if (!window.__tmGaLoaded || typeof window.gtag !== 'function') return;
    var p = params || {};
    p.source_page = location.pathname;
    p.transport_type = 'beacon';
    window.gtag('event', name, p);
  }

  /* ---------- GA4 loader ---------- */
  function loadGA() {
    if (window.__tmGaLoaded) return;
    window.__tmGaLoaded = true;

    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);

    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('set', { allow_google_signals: true });

    var ref = document.referrer || '';
    var stored = '';
    try { stored = sessionStorage.getItem(FIRST_REF_KEY) || ''; } catch (e) {}
    if (/formspree\.io/i.test(ref) && stored) ref = stored;

    var cfg = { send_page_view: true, cookie_expires: 15552000 };
    if (ref) cfg.page_referrer = ref;
    if (/[?&]ga_debug=1/.test(location.search)) cfg.debug_mode = true;

    window.gtag('config', GA_ID, cfg);
  }

  /* ---------- cookie consent ---------- */
  function hasConsent() {
    try { return localStorage.getItem(CONSENT_KEY) === 'accepted'; } catch (e) { return false; }
  }

  function showBanner() {
    if (document.getElementById('tmCookie')) return;
    var bar = document.createElement('div');
    bar.className = 'tm-cookie';
    bar.id = 'tmCookie';
    bar.innerHTML =
      '<div class="tm-cookie-inner">' +
      '<p>We use cookies to analyze site traffic and improve your experience. By continuing, you agree to our use of cookies. <a href="' + privacyHref() + '">Privacy Policy</a></p>' +
      '<button type="button" id="tmCookieAccept">Accept</button>' +
      '</div>';
    document.body.appendChild(bar);
    document.getElementById('tmCookieAccept').addEventListener('click', function () {
      try { localStorage.setItem(CONSENT_KEY, 'accepted'); } catch (e) {}
      bar.parentNode.removeChild(bar);
      loadGA();
      tmEvent('cookie_consent', { consent_action: 'accept' });
    });
  }

  /* ---------- click tracking (event delegation, no HTML changes) ---------- */
  function bindClicks() {
    document.addEventListener('click', function (e) {
      var el = e.target;
      var a = (el && el.closest) ? el.closest('a') : null;
      if (!a) return;
      var href = a.getAttribute('href') || '';
      if (/wa\.me|api\.whatsapp\.com/i.test(href)) {
        tmEvent('contact_click', { click_target: 'whatsapp' });
      } else if (/^mailto:/i.test(href)) {
        tmEvent('contact_click', { click_target: 'email' });
      } else if (/^tel:/i.test(href)) {
        tmEvent('contact_click', { click_target: 'phone' });
      } else if (/contact/i.test(href)) {
        tmEvent('quote_cta_click', { cta_text: (a.textContent || '').trim().slice(0, 100) });
      }
    }, true);
  }

  /* ---------- quote form: AJAX submit ---------- */
  function bindForm() {
    var form = document.getElementById('quoteForm');
    if (!form) return;

    var btn = form.querySelector('button[type="submit"]');
    var btnHtml = btn ? btn.innerHTML : null;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (form.getAttribute('data-submitting') === '1') return;
      form.setAttribute('data-submitting', '1');
      if (btn) { btn.disabled = true; btn.innerHTML = 'Sending...'; }

      var serviceEl = form.querySelector('#service');
      var service = (serviceEl && serviceEl.value) ? serviceEl.value : 'not specified';

      fetch(form.getAttribute('action'), {
        method: 'POST',
        body: new FormData(form),
        headers: { 'Accept': 'application/json' }
      }).then(function (res) {
        if (res.ok) {
          tmEvent('generate_lead', {
            service_type: service,
            form_location: 'homepage_contact'
          });
          showToast("Sent successfully! We'll reply within 24 hours.", 'success');
          form.reset();
        } else {
          return res.json().then(function (data) {
            var msg = (data && data.errors && data.errors[0] && data.errors[0].message)
              ? data.errors[0].message
              : 'Submission failed.' + EMAIL_FALLBACK;
            showToast(msg, 'error');
          }, function () {
            showToast('Submission failed.' + EMAIL_FALLBACK, 'error');
          });
        }
      }).catch(function () {
        showToast('Network error.' + EMAIL_FALLBACK, 'error');
      }).then(function () {
        form.setAttribute('data-submitting', '');
        if (btn) { btn.disabled = false; if (btnHtml !== null) btn.innerHTML = btnHtml; }
      });
    });
  }

  /* ---------- init ---------- */
  function init() {
    injectCss();
    bindClicks();
    bindForm();
    try {
      if (!sessionStorage.getItem(FIRST_REF_KEY)) {
        sessionStorage.setItem(FIRST_REF_KEY, document.referrer || '');
      }
    } catch (e) {}
    if (hasConsent()) loadGA(); else showBanner();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
