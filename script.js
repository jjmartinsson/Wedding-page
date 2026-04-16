/* ============================================================
   Joel & Madeleine — Wedding Page Scripts
   ============================================================ */

// ── Countdown ──────────────────────────────────────────────
(function initCountdown() {
  // Wedding: 22 August 2026, 16:00 (local Swedish time = UTC+2 in summer)
  const weddingDate = new Date('2026-08-22T16:00:00+02:00');

  const elDays    = document.getElementById('cd-days');
  const elHours   = document.getElementById('cd-hours');
  const elMinutes = document.getElementById('cd-minutes');
  const elSeconds = document.getElementById('cd-seconds');

  function pad(n) { return String(Math.max(0, n)).padStart(2, '0'); }

  function tick() {
    const now  = new Date();
    const diff = weddingDate - now;

    if (diff <= 0) {
      elDays.textContent    = '00';
      elHours.textContent   = '00';
      elMinutes.textContent = '00';
      elSeconds.textContent = '00';

      const label = document.querySelector('.countdown-label');
      if (label) label.textContent = '♥ Idag är vår stora dag! ♥';
      return;
    }

    const days    = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours   = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

    elDays.textContent    = pad(days);
    elHours.textContent   = pad(hours);
    elMinutes.textContent = pad(minutes);
    elSeconds.textContent = pad(seconds);
  }

  tick();
  setInterval(tick, 1000);
}());

// ── Navbar: add .scrolled class on scroll ──────────────────
(function initNavbar() {
  const navbar = document.getElementById('navbar');
  if (!navbar) return;

  function onScroll() {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // run once on load
}());

// ── Scroll-triggered fade-in ───────────────────────────────
(function initFadeIn() {
  const elements = document.querySelectorAll('.fade-in');
  if (!elements.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry, i) => {
        if (entry.isIntersecting) {
          // Stagger siblings slightly
          const siblings = Array.from(entry.target.parentElement.querySelectorAll('.fade-in'));
          const idx = siblings.indexOf(entry.target);
          setTimeout(() => {
            entry.target.classList.add('visible');
          }, idx * 100);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  elements.forEach((el) => observer.observe(el));
}());

// ── Lightbox ───────────────────────────────────────────────
(function initLightbox() {
  const lb      = document.getElementById('lightbox');
  const lbImg   = document.getElementById('lb-img');
  const btnClose = lb.querySelector('.lb-close');
  const btnPrev  = lb.querySelector('.lb-prev');
  const btnNext  = lb.querySelector('.lb-next');

  const imgs = Array.from(document.querySelectorAll('.gallery-item img'));
  let current = 0;

  function open(idx) {
    current = (idx + imgs.length) % imgs.length;
    lbImg.src = imgs[current].src;
    lbImg.alt = imgs[current].alt;
    lb.classList.add('open');
    lb.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function close() {
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  imgs.forEach((img, i) => {
    img.parentElement.parentElement.style.cursor = 'pointer';
    img.parentElement.parentElement.addEventListener('click', () => open(i));
  });

  btnClose.addEventListener('click', close);
  btnPrev.addEventListener('click', (e) => { e.stopPropagation(); open(current - 1); });
  btnNext.addEventListener('click', (e) => { e.stopPropagation(); open(current + 1); });

  lb.addEventListener('click', (e) => {
    if (e.target === lb || e.target === lbImg.parentElement) close();
  });

  document.addEventListener('keydown', (e) => {
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape')    close();
    if (e.key === 'ArrowLeft') open(current - 1);
    if (e.key === 'ArrowRight') open(current + 1);
  });

  // Swipe support
  let touchStartX = 0;
  lb.addEventListener('touchstart', (e) => { touchStartX = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 50) open(dx < 0 ? current + 1 : current - 1);
  });
}());

// ── Smooth active nav link highlight ──────────────────────
(function initActiveNav() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-links a');
  if (!sections.length || !navLinks.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          navLinks.forEach((link) => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + entry.target.id) {
              link.classList.add('active');
            }
          });
        }
      });
    },
    { rootMargin: '-40% 0px -55% 0px' }
  );

  sections.forEach((sec) => observer.observe(sec));
}());
