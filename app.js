// ==============================================================================
//                    ⚡ QWSTURS STORE - CORE JAVASCRIPT
// ==============================================================================

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const productsGrid = document.getElementById("products-grid");
  const searchInput = document.getElementById("search-input");
  const filterTabs = document.querySelectorAll(".minimal-tab");
  const emptyState = document.getElementById("empty-state");
  const emptyTitle = document.getElementById("empty-title");
  const emptyDesc = document.getElementById("empty-desc");
  const productModal = document.getElementById("product-modal");
  const modalCloseBtn = document.getElementById("modal-close-btn");
  const modalBody = document.getElementById("modal-body");
  const toast = document.getElementById("toast");
  const toastMessage = document.getElementById("toast-message");

  let activeCategory = "all";
  let searchQuery = "";

  // 1. Scroll-Reveal Observer (Анимация плавного появления при листании)
  const scrollObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, {
    threshold: 0.08,
    rootMargin: "0px 0px -40px 0px"
  });

  function initScrollAnimations() {
    document.querySelectorAll(".scroll-reveal").forEach(el => {
      scrollObserver.observe(el);
    });
  }

  // Initial trigger for elements already in viewport
  setTimeout(() => {
    initScrollAnimations();
  }, 50);

  // 2. Typewriter Effect (Печатающийся текст с эмодзи)
  const typewriterTextEl = document.getElementById("typewriter-text");
  const phrases = [
    "💎 приватный софт и индивидуальные билды.",
    "🎁 бесплатные программы и утилиты от qwstur.",
    "⚡ скрипты, боты и оптимизация под ключ.",
    "✈️ прямой контакт в Telegram: @AimBoGAttack."
  ];

  let phraseIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typingDelay = 65;

  function typeWriter() {
    if (!typewriterTextEl) return;

    const currentPhrase = phrases[phraseIndex];

    if (isDeleting) {
      typewriterTextEl.textContent = currentPhrase.substring(0, charIndex - 1);
      charIndex--;
      typingDelay = 30;
    } else {
      typewriterTextEl.textContent = currentPhrase.substring(0, charIndex + 1);
      charIndex++;
      typingDelay = 65;
    }

    if (!isDeleting && charIndex === currentPhrase.length) {
      typingDelay = 2000;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      typingDelay = 400;
    }

    setTimeout(typeWriter, typingDelay);
  }

  typeWriter();

  // Helper: Telegram link
  function getTelegramLink(product) {
    const isFree = product.type === "free";
    const msg = isFree
      ? `Привет, qwstur! Хочу получить бесплатную программу: ${product.title}`
      : `Здравствуйте! Интересует заказ софта: ${product.title}`;
    return `https://t.me/${TELEGRAM_USERNAME}?text=${encodeURIComponent(msg)}`;
  }

  // 3. Render Cards
  function renderProducts() {
    const hasProducts = products && products.length > 0;

    if (!hasProducts) {
      productsGrid.innerHTML = "";
      emptyState.classList.remove("hidden");
      emptyTitle.textContent = "Каталог обновляется";
      emptyDesc.textContent = "Товары и бесплатные программы скоро появятся здесь. Напиши напрямую в Telegram, если нужен софт под заказ или хочешь предложить программу.";
      return;
    }

    const filtered = products.filter(product => {
      const matchesCategory = 
        activeCategory === "all" || 
        product.category === activeCategory || 
        (activeCategory === "free" && product.type === "free") ||
        (activeCategory === "private" && product.type === "private");

      const query = searchQuery.toLowerCase().trim();
      const matchesSearch = 
        !query ||
        product.title.toLowerCase().includes(query) ||
        product.shortDescription.toLowerCase().includes(query) ||
        (product.tags && product.tags.some(tag => tag.toLowerCase().includes(query)));

      return matchesCategory && matchesSearch;
    });

    productsGrid.innerHTML = "";

    if (filtered.length === 0) {
      emptyState.classList.remove("hidden");
      emptyTitle.textContent = "Ничего не найдено 🔍";
      emptyDesc.textContent = "По твоему поисковому запросу нет результатов. Попробуй сбросить фильтры.";
    } else {
      emptyState.classList.add("hidden");
      filtered.forEach((item, index) => {
        const card = createProductCard(item, index);
        productsGrid.appendChild(card);
      });
    }

    if (window.lucide) {
      lucide.createIcons();
    }

    // Re-observe newly created elements
    initScrollAnimations();
  }

  // 4. Create Spotlight Product Card
  function createProductCard(product, index) {
    const isFree = product.type === "free";
    const tgLink = getTelegramLink(product);
    const badgeEmoji = isFree ? "🎁" : "💎";

    const card = document.createElement("div");
    card.className = "spotlight-card scroll-reveal p-5 flex flex-col justify-between";
    card.style.transitionDelay = `${(index % 3) * 120}ms`;

    const tagsHtml = (product.tags || []).map(tag => `
      <span class="text-[11px] font-mono px-2 py-0.5 rounded bg-white/[0.04] text-neutral-400 border border-white/[0.05]">
        #${tag}
      </span>
    `).join("");

    const featuresHtml = (product.features || []).slice(0, 3).map(f => `
      <li class="flex items-center text-xs text-neutral-300 gap-2">
        <span class="text-[10px]">🔹</span>
        <span class="truncate">${f}</span>
      </li>
    `).join("");

    // Action button logic (Direct download or Telegram)
    let actionBtnHtml = "";
    if (product.downloadUrl) {
      actionBtnHtml = `
        <a href="${product.downloadUrl}" download class="btn-vercel-primary py-2 px-3 text-xs flex items-center justify-center gap-1.5">
          <span>📥</span>
          <span>Скачать ZIP</span>
        </a>
      `;
    } else {
      actionBtnHtml = `
        <a href="${tgLink}" target="_blank" rel="noopener noreferrer"
          class="${isFree ? 'btn-vercel-tg' : 'btn-vercel-primary'} py-2 px-3 text-xs flex items-center justify-center gap-1.5">
          <span>✈️</span>
          <span>${isFree ? 'В Telegram' : 'Заказать в TG'}</span>
        </a>
      `;
    }

    card.innerHTML = `
      <div>
        <div class="flex items-center justify-between gap-2 mb-3">
          <div class="flex items-center gap-2">
            <span class="text-[10px] font-mono tracking-wider px-2 py-0.5 rounded flex items-center gap-1 ${isFree ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-purple-500/10 text-purple-300 border border-purple-500/20'}">
              <span>${badgeEmoji}</span>
              <span>${product.badge || (isFree ? 'FREEWARE' : 'PRIVATE')}</span>
            </span>
            <span class="text-[11px] font-mono text-neutral-500">${product.version || 'v1.0'}</span>
          </div>
          <span class="text-[11px] font-mono text-emerald-400 flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            <span>${product.status || 'Active'}</span>
          </span>
        </div>

        <h3 class="text-base font-medium text-white mb-1.5">${product.title}</h3>
        <p class="text-xs text-neutral-400 mb-4 line-clamp-2 leading-relaxed">
          ${product.shortDescription}
        </p>

        <ul class="space-y-1.5 mb-4 py-2 border-y border-white/[0.06]">
          ${featuresHtml}
        </ul>

        <div class="flex flex-wrap gap-1.5 mb-5">
          ${tagsHtml}
        </div>
      </div>

      <div class="grid grid-cols-2 gap-2 pt-3 border-t border-white/[0.06]">
        <button onclick="window.openDetailsModal('${product.id}')"
          class="btn-vercel-secondary py-2 px-3 text-xs flex items-center justify-center gap-1.5">
          <span>ℹ️</span>
          <span>Детали</span>
        </button>
        ${actionBtnHtml}
      </div>
    `;

    // Make visible after mounting
    setTimeout(() => {
      card.classList.add("visible");
    }, 50);

    return card;
  }

  // 5. Modal Logic
  window.openDetailsModal = function(id) {
    const item = products.find(p => p.id === id);
    if (!item) return;

    const isFree = item.type === "free";
    const tgLink = getTelegramLink(item);

    const featuresHtml = (item.features || []).map(f => `
      <li class="flex items-start text-xs text-neutral-300 gap-2">
        <span class="text-[10px] mt-0.5">🔹</span>
        <span>${f}</span>
      </li>
    `).join("");

    let downloadActionHtml = "";
    if (item.downloadUrl) {
      downloadActionHtml = `
        <a href="${item.downloadUrl}" download 
          class="btn-vercel-primary px-4 py-2 text-xs flex items-center gap-1.5">
          <span>📥</span>
          <span>Скачать файл (.zip)</span>
        </a>
      `;
    }

    modalBody.innerHTML = `
      <div class="flex items-center justify-between mb-4">
        <span class="text-[10px] font-mono px-2 py-0.5 rounded flex items-center gap-1 ${isFree ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-purple-500/10 text-purple-300 border border-purple-500/20'}">
          <span>${isFree ? '🎁' : '💎'}</span>
          <span>${item.badge || (isFree ? 'FREE' : 'PRIVATE')}</span>
        </span>
        <span class="text-xs font-mono text-emerald-400">${item.status || '● Active'}</span>
      </div>

      <h2 class="text-xl font-medium text-white mb-2">${item.title}</h2>
      <p class="text-xs text-neutral-300 leading-relaxed mb-5 bg-white/[0.02] p-3 rounded-lg border border-white/[0.06]">
        ${item.fullDescription || item.shortDescription}
      </p>

      <div class="mb-5">
        <div class="text-[11px] font-mono text-neutral-400 uppercase tracking-wider mb-2">⚡ Возможности:</div>
        <ul class="space-y-2">
          ${featuresHtml}
        </ul>
      </div>

      <div class="pt-4 border-t border-white/[0.08] flex flex-wrap items-center justify-between gap-3">
        <div class="text-xs font-mono text-neutral-400 flex items-center gap-1">
          <span>✈️</span>
          <span>@${TELEGRAM_USERNAME}</span>
        </div>
        <div class="flex items-center gap-2">
          ${downloadActionHtml}
          <a href="${tgLink}" target="_blank" rel="noopener noreferrer"
            class="btn-vercel-tg px-4 py-2 text-xs flex items-center gap-1.5">
            <span>✈️</span>
            <span>${isFree ? 'Чат в Telegram' : 'Заказать в TG'}</span>
          </a>
        </div>
      </div>
    `;

    productModal.classList.add("active");
    document.body.style.overflow = "hidden";

    if (window.lucide) {
      lucide.createIcons();
    }
  };

  function closeModal() {
    productModal.classList.remove("active");
    document.body.style.overflow = "";
  }

  modalCloseBtn.addEventListener("click", closeModal);
  productModal.addEventListener("click", (e) => {
    if (e.target === productModal) closeModal();
  });

  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && productModal.classList.contains("active")) {
      closeModal();
    }
    if (e.key === "/" && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
    }
  });

  // 6. Tabs Filter Listener
  filterTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      filterTabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      activeCategory = tab.getAttribute("data-category");
      renderProducts();
    });
  });

  // 7. Search Input
  searchInput.addEventListener("input", (e) => {
    searchQuery = e.target.value;
    renderProducts();
  });

  // 8. Copy to clipboard
  window.copyContact = function() {
    navigator.clipboard.writeText(`https://t.me/${TELEGRAM_USERNAME}`).then(() => {
      if (!toast || !toastMessage) return;
      toastMessage.textContent = "Ссылка на Telegram @AimBoGAttack скопирована в буфер ✈️";
      toast.classList.remove("translate-y-20", "opacity-0");
      toast.classList.add("translate-y-0", "opacity-100");
      setTimeout(() => {
        toast.classList.add("translate-y-20", "opacity-0");
        toast.classList.remove("translate-y-0", "opacity-100");
      }, 2500);
    });
  };

  // Initial
  renderProducts();
});
