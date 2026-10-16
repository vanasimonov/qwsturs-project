# ⚡ qwsturs store

> Официальный сайт-витрина для **qwstur** с Dark Tech Glassmorphism дизайном, разделом приватных заказов и каталогом из **10 самых полезных десктопных утилит на Python**.

---

## 🚀 Как запустить сайт

1. Перейди в папку: `C:\Users\Admin\Desktop\python\проекты\qwsturs dhop`
2. Просто дважды кликни на файл **`index.html`**, и сайт откроется в твоем браузере (Chrome, Edge, Opera, Firefox).
3. Или можно запустить локальный сервер в PowerShell:
   ```powershell
   python -m http.server 8000
   ```
   и открыть в браузере: `http://localhost:8000`

---

## 🎮 GAMER EDITION: 5 топовых утилит для геймеров (CS2, Rust, Valorant, Apex)

1. **⚡ QWSTUR GAME FPS & RAM BOOSTER** (`qwstur-fps-booster-v1.0.zip`)
   * Принудительный сброс неактивной RAM через WinAPI `EmptyWorkingSet`, очистка кэша DNS Resolver, удаление Temp и переход на план Ultimate Power в 1 клик.
2. **🎯 QWSTUR CROSSHAIR OVERLAY** (`qwstur-crosshair-overlay-v1.0.zip`)
   * Прозрачный оверлей с кастомным прицелом поверх всех окон (`WS_EX_TRANSPARENT`), 4 типа (Dot, Cross, Circle, T-Shape), неоновые расцветки и хоткей [F6].
3. **⚡ QWSTUR GAMER AUTO-CLICKER & MACRO** (`qwstur-auto-clicker-v1.0.zip`)
   * Высокоскоростной автокликер (до 50+ CPS) на WinAPI `mouse_event` с защитой от античита (Humanize ±15%), поддержкой ЛКМ/ПКМ/СКМ и хоткеем [F7].
4. **🖱️ QWSTUR SENSITIVITY & DPI CONVERTER** (`qwstur-sens-converter-v1.0.zip`)
   * Точный пересчет чувствительности мыши между CS2, Valorant, Apex, Rust, Fortnite, R6 с вычислением eDPI и см/360°.
5. **📡 QWSTUR GAMER PING & PACKET LOSS HUD** (`qwstur-ping-hud-v1.0.zip`)
   * Плавающий поверх экрана HUD для непрерывного мониторинга пинга и джиттера до серверов Valve EU, Riot Games, Discord Voice с предупреждением о Packet Drop.

---

## ⚡ 10 десктопных системных утилит на Python (Готовы к работе, 0 сек запуска, оффлайн)

Все утилиты написаны на стандартной библиотеке Python (`tkinter`, `ctypes`, `subprocess`, `hashlib`, `winreg`, `secrets`, `http.server`), не требуют сторонних pip-пакетов, имеют кнопку «💬 Написать владельцу» и фирменный брендинг `// by qwstur`:

1. **⚡ QWSTUR PORT & PROCESS KILLER** (`qwstur-port-killer-v1.0.zip`)
   * Освобождение занятых TCP-портов (3000, 8000, 8080) и завершение зависших процессов по Enter.
2. **📋 QWSTUR CLIPSTACK HISTORY** (`qwstur-clipstack-v1.0.zip`)
   * Фоновый менеджер истории буфера обмена (до 100 записей) с мгновенным поиском и предпросмотром.
3. **🛡️ QWSTUR HASH & CHECKSUM VERIFIER** (`qwstur-hash-verifier-v1.0.zip`)
   * Расчет хэшей файлов и текста (MD5, SHA-1, SHA-256, SHA-512) и автоматическая проверка контрольной суммы.
4. **📁 QWSTUR BATCH FILE RENAMER** (`qwstur-batch-renamer-v1.0.zip`)
   * Пакетное переименование файлов (поиск/замена, префиксы, суффиксы, нумерация 001, регистр) с живой таблицей предпросмотра.
5. **⏱️ QWSTUR SMART SLEEP & SHUTDOWN TIMER** (`qwstur-sleep-timer-v1.0.zip`)
   * Таймер выключения, перезагрузки, сна и блокировки ПК с пресетами (+15м, +30м, +1ч), отменой (Esc) и звуковым предупреждением.
6. **🔑 QWSTUR SECURE PASS & TOKEN GENERATOR** (`qwstur-pass-generator-v1.0.zip`)
   * Криптографический генератор паролей, API-токенов, UUIDv4 и PIN на модуле secrets с замером энтропии и пакетным экспортом.
7. **📊 QWSTUR MINI HUD SYSTEM MONITOR** (`qwstur-mini-monitor-v1.0.zip`)
   * Компактный плавающий телеметрический виджет: CPU %, RAM (ГБ), Диск C:, аптайм Windows с режимом поверх окон (T).
8. **🌐 QWSTUR QUICK HTTP & STATIC SERVER** (`qwstur-quick-server-v1.0.zip`)
   * Локальный веб-сервер в 1 клик для раздачи файлов и сайтов с автоопределением LAN IP для входа с телефона и логом запросов.
9. **🧹 QWSTUR DUPLICATE FILE FINDER** (`qwstur-dup-cleaner-v1.0.zip`)
   * Скоростной двухэтапный поиск одинаковых файлов-дубликатов по размеру и SHA-256 с безопасным удалением.
10. **🚀 QWSTUR AUTOSTART & STARTUP MANAGER** (`qwstur-autostart-manager-v1.0.zip`)
    * Сканирование реестра HKCU/HKLM и папки Автозагрузки для ускорения старта системы и открытия файлов в Проводнике.

Исходный код всех 15 программ находится в каталоге:
`C:\Users\Admin\Desktop\python\проекты\qwsturs dhop\apps\`

---

## 📂 Структура проекта

* `index.html` — Главная страница магазина (адаптивная верстка, стили, шапка, поиск, модальные окна).
* `style.css` — Эстетика Dark Tech (глубокий темный фон, стеклянные карточки glassmorphism, неоновые акценты).
* `app.js` — Логика сайта (фильтрация категорий, живой поиск, генерация карточек, модальные окна, тосты).
* `products.js` — **База товаров и программ**. Все карточки и прямые ссылки на скачивание ZIP хранятся тут.
* `apps/` — Исходный Python-код и батники всех 10 утилит.
* `*.zip` — Готовые к скачиванию релизные архивы для пользователей сайта.

---

## 🔗 Контакты
* **Telegram:** [@AimBoGAttack](https://t.me/AimBoGAttack)
* **Владелец:** qwstur
