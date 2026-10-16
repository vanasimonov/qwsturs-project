// ==============================================================================
//                    ⚡ QWSTURS STORE - БАЗА ТОВАРОВ И ПРОГРАММ
// ==============================================================================
// Владелец: qwstur | Сочно, аккуратно и для своих!
// Telegram: https://t.me/AimBoGAttack
// ==============================================================================

const TELEGRAM_USERNAME = "AimBoGAttack";

// Официальные релизы от qwstur (десктопный Python-софт и веб-утилиты)
const products = [
  // ============================================================================
  // 🎮 GAMER EDITION: ТОП-5 УТИЛИТ ДЛЯ ГЕЙМЕРОВ (CS2, RUST, VALORANT, APEX)
  // ============================================================================
  {
    id: "qwstur-fps-booster",
    title: "⚡ QWSTUR GAME FPS & RAM BOOSTER",
    type: "free",
    category: "gaming",
    badge: "FPS BOOST",
    icon: "zap",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-fps-booster-v1.0.zip",
    shortDescription: "Мгновенная очистка оперативной памяти, сброс кэша DNS Resolver, удаление мусора Temp и переключение на Ultimate Power в 1 клик.",
    fullDescription: "Фирменный игровой бустер на чистом Python для геймеров. Освобождает сотни мегабайт неиспользуемой оперативной памяти через WinAPI EmptyWorkingSet, сбрасывает сетевой кэш DNS для устранения дропов пакетов, очищает кэш Windows и переключает схему электропитания на максимальную производительность.",
    features: [
      "🚀 Принудительный сброс рабочих наборов RAM (Working Sets)",
      "⚡ Мгновенный flushdns для устранения фризов и рассинхронов в играх",
      "🧹 Очистка временных файлов и кэша из %TEMP%",
      "🎮 Активация плана электропитания Ultimate Performance",
      "📊 Счетчик освобожденной оперативной памяти в реальном времени",
      "🔒 100% безопасный открытый код на чистом Python"
    ],
    tags: ["Gaming", "FPS", "Boost", "RAM", "Optimizer", "Free", "Windows"],
    version: "v1.0.0",
    views: "4.5k"
  },
  {
    id: "qwstur-crosshair-overlay",
    title: "🎯 QWSTUR CROSSHAIR OVERLAY",
    type: "free",
    category: "gaming",
    badge: "GAMER HUD",
    icon: "crosshair",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-crosshair-overlay-v1.0.zip",
    shortDescription: "Кастомный прозрачный прицел поверх всех окон для хардкорных шутеров (CS2, Rust, Fortnite, DayZ) с хоткеем F6.",
    fullDescription: "Прозрачный экранный оверлей на чистом Python без нагрузки на систему. Рисует прицел поверх игры через WinAPI Layered & Transparent Window (не перехватывает клики мыши). Незаменим для стрельбы от бедра из снайперских винтовок и луков. Поддерживает типы прицела Dot, Cross, Circle, T-Shape, кастомные неоновые цвета и хоткей F6 для скрытия.",
    features: [
      "🎯 4 типа прицелов: Точка (Dot), Крест (Cross), Круг, T-образный",
      "🎨 Неоновые расцветки: Зеленый, Красный, Циан, Фиолетовый, Желтый, Белый",
      "⚡ Прозрачный click-through оверлей: мышь свободно управляет игрой",
      "⌨️ Хоткей [F6] для моментального скрытия или показа прицела",
      "📏 Полная настройка размера лучей, толщины линий и центральной точки",
      "🛡️ Не внедряется в память игры (External Overlay) — 100% безопасность"
    ],
    tags: ["Gaming", "Crosshair", "CS2", "Rust", "Overlay", "Free"],
    version: "v1.0.0",
    views: "5.2k"
  },
  {
    id: "qwstur-auto-clicker",
    title: "⚡ QWSTUR GAMER AUTO-CLICKER",
    type: "free",
    category: "gaming",
    badge: "AUTO CLICKER",
    icon: "gauge",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-auto-clicker-v1.0.zip",
    shortDescription: "Высокоточный кликер до 50+ CPS с защитой от античита (Humanize ±15%), выбором ЛКМ/ПКМ/СКМ и хоткеем F7.",
    fullDescription: "Геймерский автокликер на чистом Python с управлением через WinAPI mouse_event. Оснащен режимом Humanize (рандомизация интервала кликов для обхода защит от макросов), выбором кнопки мыши, готовыми пресетами под пистолеты CS2 и фарм-кликеры, а также глобальным хоткеем F7 для старта и остановки.",
    features: [
      "⚡ Скорость до 50+ кликов в секунду (CPS) с ультра-низкой задержкой",
      "🛡️ Режим Humanize (рандомизация задержки ±15% для обхода детектов)",
      "🖱️ Поддержка ЛКМ, ПКМ и СКМ (колесико мыши)",
      "⌨️ Глобальный хоткей [F7] для старта/стопа прямо во время матча",
      "📊 Счетчик совершенных кликов и калькулятор реального CPS",
      "🎮 Готовые пресеты: CS2 пистолеты, фарм в RPG, максимальная скорость"
    ],
    tags: ["Gaming", "AutoClicker", "Macro", "CPS", "Free", "Windows"],
    version: "v1.0.0",
    views: "4.8k"
  },
  {
    id: "qwstur-sens-converter",
    title: "🖱️ QWSTUR SENSITIVITY & DPI CONVERTER",
    type: "free",
    category: "gaming",
    badge: "AIM UTILITY",
    icon: "gamepad-2",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-sens-converter-v1.0.zip",
    shortDescription: "Математически точный конвертер чувствительности мыши, eDPI и см/360° между CS2, Valorant, Apex, Rust, Fortnite.",
    fullDescription: "Профессиональный конвертер сенсы для сохранения мышечной памяти при смене шутера. Рассчитывает точный угол поворота (Yaw) между движками Source, Unreal Engine и кастомными играми. Показывает eDPI, точное расстояние в сантиметрах для полного разворота на 360° и классифицирует стиль стрельбы (Low/Medium/High Sens).",
    features: [
      "🎯 Точная конвертация между CS2, Valorant, Apex, Overwatch 2, Rust, Fortnite, R6",
      "📐 Расчет реального расстояния cm/360° для разворота прицела",
      "📊 Мгновенный расчет eDPI (DPI × Сенса)",
      "📋 Копирование полученного значения для любой игры в 1 клик",
      "💡 Определение стиля прицеливания (тактический Low-sens / быстрый High-sens)",
      "💻 Чистый Python без интернета и рекламы"
    ],
    tags: ["Gaming", "Sensitivity", "Aim", "DPI", "CS2", "Valorant", "Free"],
    version: "v1.0.0",
    views: "3.9k"
  },
  {
    id: "qwstur-ping-hud",
    title: "📡 QWSTUR GAMER PING & PACKET LOSS HUD",
    type: "free",
    category: "gaming",
    badge: "PING HUD",
    icon: "activity",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-ping-hud-v1.0.zip",
    shortDescription: "Компактный плавающий оверлей-виджет для мониторинга пинга и джиттера до игровых серверов (Valve EU, Riot, Discord) в реальном времени.",
    fullDescription: "Микро-виджет, закрепляемый поверх всех окон в углу экрана. Позволяет контролировать стабильность интернет-соединения во время катки. Измеряет отклик до ключевых игровых датацентров (Франкфурт Valve, Riot Games EU, Discord Voice, Cloudflare), рассчитывает джиттер (стабильность задержки) и предупреждает о потере пакетов.",
    features: [
      "📡 Непрерывный замер пинга до серверов Valve EU (CS2), Riot Games, Discord",
      "📊 Автоматический расчет джиттера (вариации задержки в миллисекундах)",
      "🎨 Цветовая индикация качества соединения (Зеленый <35ms, Желтый, Красный)",
      "🖱️ Свободное перетаскивание виджета мышью в любое место монитора",
      "⚡ Нативное закрепление поверх всех окон (Always on Top)",
      "🛑 Мгновенное оповещение о Packet Drop и разрыве соединения"
    ],
    tags: ["Gaming", "Ping", "HUD", "Network", "CS2", "Latency", "Free"],
    version: "v1.0.0",
    views: "4.1k"
  },
  // ============================================================================
  // ⚡ ТОП-10 САМЫХ ПОЛЕЗНЫХ ДЕСКТОПНЫХ УТИЛИТ НА PYTHON (NEW 2026)
  // ============================================================================
  {
    id: "qwstur-port-killer",
    title: "⚡ QWSTUR PORT & PROCESS KILLER",
    type: "free",
    category: "tools",
    badge: "PORT KILLER",
    icon: "zap",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-port-killer-v1.0.zip",
    shortDescription: "Мгновенное освобождение занятых TCP-портов (3000, 8000, 8080) и принудительное завершение зависших процессов в 1 клик.",
    fullDescription: "Системная утилита на чистом Python для мгновенного поиска и завершения процессов, блокирующих сетевые TCP-порты. Показывает PID, имя процесса, локальный IP и статус подключения. Позволяет освободить любой порт по нажатию Enter без командной строки.",
    features: [
      "⚡ Мгновенное освобождение портов 3000, 8000, 8080, 5000 по нажатию Enter",
      "🔍 Индексация всех активных сетевых соединений TCP и PID",
      "🛑 Безопасное завершение зависших процессов через taskkill",
      "⌨️ Поддержка горячих клавиш (Enter для завершения, F5 для обновления, Esc)",
      "🛡️ Защита системных процессов Windows от случайного закрытия",
      "💻 Чистый Python, запуск 0 сек без сторонних библиотек"
    ],
    tags: ["Python", "PortKiller", "Windows", "Utility", "Free", "Network"],
    version: "v1.0.0",
    views: "2.8k"
  },
  {
    id: "qwstur-clipstack",
    title: "📋 QWSTUR CLIPSTACK HISTORY",
    type: "free",
    category: "tools",
    badge: "CLIPBOARD",
    icon: "clipboard-list",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-clipstack-v1.0.zip",
    shortDescription: "Легковесный менеджер истории буфера обмена с автозахватом текста, живым поиском, предпросмотром и горячими клавишами.",
    fullDescription: "Автоматически сохраняет до 100 фрагментов скопированного текста, ссылок и кода. Оснащен моментальным поиском без задержек, окном детального предпросмотра с подсчетом символов и горячими клавишами (Enter для повторного копирования, Del для удаления, Esc для сброса поиска).",
    features: [
      "📋 Фоновый автозахват истории буфера обмена до 100 записей",
      "🔍 Моментальный фильтр-поиск по тексту фрагментов на лету",
      "👁️ Панель детального предпросмотра фрагментов кода и ссылок",
      "⚡ Копирование выбранной записи обратно в буфер по клавише Enter",
      "🗑️ Очистка одиночных записей (Del) или всей истории в 1 клик",
      "🔒 100% приватность: данные хранятся только в памяти сессии"
    ],
    tags: ["Python", "Clipboard", "History", "Text", "Productivity", "Free"],
    version: "v1.0.0",
    views: "3.1k"
  },
  {
    id: "qwstur-hash-verifier",
    title: "🛡️ QWSTUR HASH & CHECKSUM VERIFIER",
    type: "free",
    category: "tools",
    badge: "CHECKSUM",
    icon: "shield-check",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-hash-verifier-v1.0.zip",
    shortDescription: "Расчет хэшей файлов и текста (MD5, SHA-1, SHA-256, SHA-512) с мгновенным автоматическим сравнением контрольной суммы.",
    fullDescription: "Многопоточный инструмент проверки целостности файлов и текста. Считает MD5, SHA-1, SHA-256 и SHA-512 на лету через буферизованные потоки, не подвешивая интерфейс даже на тяжелых файлах. Имеет поле автоматической сверки с эталонным хэшем с мгновенной цветовой индикацией (зеленый/красный).",
    features: [
      "🔒 Вычисление MD5, SHA-1, SHA-256 и SHA-512 в фоновом потоке",
      "⚡ Автоматическая верификация: вставьте эталонный хэш для сверки",
      "📊 Индикатор прогресса расчета для больших файлов",
      "📋 Копирование любого вычисленного хэша в 1 клик",
      "✍️ Режим расчета хэша для произвольного текстового ввода",
      "⌨️ Поддержка горячих клавиш (Ctrl+O для выбора файла, Esc для сброса)"
    ],
    tags: ["Python", "Hash", "SHA256", "MD5", "Security", "Verifier"],
    version: "v1.0.0",
    views: "2.5k"
  },
  {
    id: "qwstur-batch-renamer",
    title: "📁 QWSTUR BATCH FILE RENAMER",
    type: "free",
    category: "tools",
    badge: "RENAMER",
    icon: "folder",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-batch-renamer-v1.0.zip",
    shortDescription: "Пакетное переименование файлов с гибкими правилами (поиск/замена, префикс, суффикс, нумерация 001, регистр) и живым предпросмотром.",
    fullDescription: "Быстрый инструмент массового переименования файлов в папке. Поддерживает поиск и замену подстрок, добавление префиксов/суффиксов, автонумерацию с ведущими нулями и изменение регистра (нижний, ВЕРХНИЙ, С Заглавной). Интерактивная таблица отображает изменения до их применения с защитой от коллизий одинаковых имен.",
    features: [
      "👁️ Интерактивная таблица предпросмотра 'До / После' до применения",
      "🔍 Поиск и замена подстрок в именах файлов",
      "🔢 Автонумерация с ведущими нулями (001, 002, 003...)",
      "🔠 Преобразование регистра: нижний, ВЕРХНИЙ, С Заглавной",
      "🛡️ Валидация конфликтов одинаковых имен файлов",
      "⚡ Применение переименования в 1 клик по клавише Enter"
    ],
    tags: ["Python", "Batch", "Renamer", "Files", "Windows", "Tools"],
    version: "v1.0.0",
    views: "2.2k"
  },
  {
    id: "qwstur-sleep-timer",
    title: "⏱️ QWSTUR SMART SLEEP & SHUTDOWN TIMER",
    type: "free",
    category: "tools",
    badge: "POWER TIMER",
    icon: "clock",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-sleep-timer-v1.0.zip",
    shortDescription: "Удобный таймер выключения, перезагрузки, сна и блокировки ПК с быстрыми пресетами (+15м, +30м, +1ч) и звуковым предупреждением.",
    fullDescription: "Минималистичный таймер питания Windows. Позволяет задать выключение, перезапуск, спящий режим или блокировку системы по таймеру или точным пресетам. Большой контрастный HUD с обратным отсчетом времени, возможность мгновенной отмены по клавише Esc и звуковой сигнал за 60 секунд до срабатывания.",
    features: [
      "🛑 Выключение, 🔄 перезагрузка, 💤 сон и 🔒 блокировка ПК",
      "⚡ Быстрые пресеты в 1 клик: +15 мин, +30 мин, +45 мин, +1 час, +2 часа",
      "⏱️ Большой контрастный цифровой таймер обратного отсчета",
      "🔔 Звуковое системное предупреждение за 60 секунд до действия",
      "⌨️ Мгновенная отмена таймера по клавише Esc или кнопке",
      "🛡️ Полная совместимость со стандартным API shutdown.exe"
    ],
    tags: ["Python", "Shutdown", "Timer", "Sleep", "System", "Utility"],
    version: "v1.0.0",
    views: "3.4k"
  },
  {
    id: "qwstur-pass-generator",
    title: "🔑 QWSTUR SECURE PASS & TOKEN GENERATOR",
    type: "free",
    category: "tools",
    badge: "SECURITY",
    icon: "key",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-pass-generator-v1.0.zip",
    shortDescription: "Криптографический генератор паролей, API-токенов, UUIDv4 и PIN-кодов с расчетом энтропии и пакетной выгрузкой списка.",
    fullDescription: "Генератор стойких учетных данных на базе криптографически безопасного генератора secrets. Настройка длины от 6 до 64 символов, наборов знаков, исключение похожих символов (0/O, 1/l), расчет битовой энтропии Шеннона, а также пакетная генерация до 20 паролей в 1 клик.",
    features: [
      "🔐 Криптостойкая генерация паролей на модуле secrets",
      "🌐 Генерация Hex-токенов, URL-Safe ключей, UUIDv4 и PIN-кодов",
      "📊 Индикатор энтропии Шеннона в битах и шкала надежности",
      "🚫 Опция исключения визуально схожих символов (0, O, l, 1, I)",
      "📦 Пакетная генерация списка паролей (+5, +10) с экспортом",
      "📋 Быстрое копирование в буфер по Enter или Ctrl+C"
    ],
    tags: ["Python", "Password", "Generator", "Crypto", "Token", "Security"],
    version: "v1.0.0",
    views: "2.7k"
  },
  {
    id: "qwstur-mini-monitor",
    title: "📊 QWSTUR MINI HUD SYSTEM MONITOR",
    type: "free",
    category: "tools",
    badge: "HUD MONITOR",
    icon: "activity",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-mini-monitor-v1.0.zip",
    shortDescription: "Компактный плавающий виджет телеметрии ПК: мониторинг CPU %, памяти RAM, диска C: и аптайма Windows без нагрузки на систему.",
    fullDescription: "Ультралегкий аппаратный HUD с нативным чтением метрик Windows через WinAPI kernel32/dwmapi без сторонних библиотек. Практически нулевое потребление ресурсов (менее 0.05% CPU). Поддержка закрепления поверх всех окон (клавиша T) и темный кибер-интерфейс.",
    features: [
      "⚡ Живой замер загрузки процессора CPU % в реальном времени",
      "🧠 Мониторинг занятой и доступной оперативной памяти RAM (ГБ)",
      "💾 Индикатор свободного пространства системного диска C:",
      "⏱️ Точный счетчик непрерывной работы Windows (System Uptime)",
      "📌 Режим 'Поверх всех окон' (переключение по клавише T)",
      "🚀 0 сторонних зависимостей, нулевая нагрузка на ПК"
    ],
    tags: ["Python", "Monitor", "CPU", "RAM", "HUD", "Telemetry"],
    version: "v1.0.0",
    views: "2.9k"
  },
  {
    id: "qwstur-quick-server",
    title: "🌐 QWSTUR QUICK HTTP & STATIC SERVER",
    type: "free",
    category: "tools",
    badge: "HTTP SERVER",
    icon: "server",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-quick-server-v1.0.zip",
    shortDescription: "Локальный веб-сервер в 1 клик для раздачи файлов и тестирования сайтов. Автоопределение LAN IP для открытия с телефона.",
    fullDescription: "Многопоточный HTTP-сервер для мгновенного шаринга файлов в локальной сети или запуска HTML/JS проектов. Автоматически определяет внутренний IP адрес вашего ПК в Wi-Fi сети для подключения с телефона или планшета. Оснащен живым журналом входящих HTTP запросов в реальном времени.",
    features: [
      "🚀 Запуск локального HTTP сервера для любой папки в 1 клик",
      "📱 Автоматическое определение локального IP (LAN) для входа с телефона",
      "🌐 Быстрый переход в браузер и копирование готовой ссылки",
      "📜 Живая консоль входящих сетевых запросов и кодов ответа",
      "⚙️ Выбор любого свободного порта (8000, 3000, 8080, custom)",
      "⚡ Многопоточная обработка одновременных подключений"
    ],
    tags: ["Python", "Server", "HTTP", "LAN", "Share", "WebDev"],
    version: "v1.0.0",
    views: "2.6k"
  },
  {
    id: "qwstur-dup-cleaner",
    title: "🧹 QWSTUR DUPLICATE FILE FINDER",
    type: "free",
    category: "tools",
    badge: "STORAGE",
    icon: "trash-2",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-dup-cleaner-v1.0.zip",
    shortDescription: "Быстрый поиск и удаление одинаковых файлов-дубликатов по точному размеру и хэшу SHA-256 для освобождения места на диске.",
    fullDescription: "Двухэтапный скоростной сканер свободного места: на первом этапе мгновенно группирует файлы по байтовому размеру, на втором — вычисляет SHA-256 хэши только для реальных кандидатов. Отображает сэкономленное дисковое пространство, позволяет выделить только дубликаты и безопасно удалить их.",
    features: [
      "⚡ Сверхбыстрый двухэтапный алгоритм (размер + SHA-256)",
      "📊 Подсчет напрасно потраченного места на диске (МБ / ГБ)",
      "☑️ Автоматический выбор только копий (сохраняя оригинал)",
      "🗑️ Безопасное удаление выбранных дубликатов с подтверждением",
      "📁 Сканирование любых вложенных папок и каталогов загрузок",
      "⌨️ Управление горячими клавишами (Enter для старта, Esc для отмены)"
    ],
    tags: ["Python", "Duplicates", "Cleaner", "Storage", "Disk", "Tools"],
    version: "v1.0.0",
    views: "3.2k"
  },
  {
    id: "qwstur-autostart-manager",
    title: "🚀 QWSTUR AUTOSTART & STARTUP MANAGER",
    type: "free",
    category: "tools",
    badge: "STARTUP",
    icon: "rocket",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-autostart-manager-v1.0.zip",
    shortDescription: "Сканер программ в автозагрузке Windows (реестр HKCU/HKLM и папка Автозагрузки) для ускорения включения ПК.",
    fullDescription: "Оптимизатор автозапуска ПК. Считывает программы и службы из веток реестра Run и системной папки Автозагрузка. Позволяет в один клик открыть расположение исполняемого файла в Проводнике, скопировать команду запуска или удалить ненужные программы, тормозящие старт системы.",
    features: [
      "🔍 Сканирование реестра HKCU\\Run, HKLM\\Run и папки Startup",
      "📁 Быстрый переход к файлу программы в Проводнике Windows",
      "🗑️ Безопасное удаление лишних программ из автозапуска",
      "📋 Копирование пути и параметров запуска в буфер обмена",
      "⚡ Мгновенный фильтр по названию программы или пути",
      "🚀 Ускорение времени загрузки операционной системы"
    ],
    tags: ["Python", "Autostart", "Registry", "Speedup", "Windows", "Optimizer"],
    version: "v1.0.0",
    views: "2.4k"
  },

  // ============================================================================
  // 🔥 ПРЕДЫДУЩИЕ РЕЛИЗЫ И ИНСТРУМЕНТЫ ОТ QWSTUR
  // ============================================================================
  {
    id: "qwstur-optimizer-pro",
    title: "⚡ QWSTUR OPTIMIZER PRO",
    type: "free",
    category: "free",
    badge: "FREEWARE",
    icon: "zap",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-optimizer-v1.0.zip",
    shortDescription: "Мощная утилита от qwstur: глубокая очистка RAM, сброс кэша DNS Resolver, удаление мусора Temp и мгновенный буст FPS.",
    fullDescription: "Фирменный комбайн от qwstur в темном Cyber Dark стиле. Включает реальную очистку рабочих наборов оперативной памяти (RAM Working Set), мгновенный сброс DNS Resolver Cache для устранения лагов и сетевых задержек в играх, удаление временного мусора из %TEMP% и активацию режима максимальной производительности Windows в 1 клик.",
    features: [
      "🚀 Очистка RAM и сброс неактивных рабочих наборов",
      "⚡ Мгновенный сброс DNS Resolver Cache для стабильного пинга",
      "🧹 Глубокая очистка каталога временных файлов %TEMP%",
      "🎮 Активация схемы питания 'Высокая производительность'",
      "💻 Живая консоль логов с поминутным выводом операций",
      "🔒 100% безопасный и открытый Python-код"
    ],
    tags: ["Utility", "Python", "Optimizer", "Free", "Windows"],
    version: "v1.0.0",
    views: "1.4k"
  },
  {
    id: "qwstur-network-booster",
    title: "🚀 QWSTUR NETWORK BOOSTER",
    type: "free",
    category: "tools",
    badge: "PING BOOSTER",
    icon: "activity",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-network-booster-v1.0.zip",
    shortDescription: "Живой монитор пинга серверов (Cloudflare, Steam, Discord), оптимизация TCP Auto-Tuning и сброс стека Winsock.",
    fullDescription: "Профессиональная сетевая утилита для снижения задержек и стабилизации соединения. Проверяет отклик до ключевых серверов в реальном времени, оптимизирует настройки TCP/IP через Netsh, активирует RSS и сбрасывает стек сетевых каталогов Winsock.",
    features: [
      "📊 Замер пинга до Cloudflare, Google, Steam EU, Discord и Riot",
      "⚡ Оптимизация TCP AutoTuning Level и приемного буфера RSS",
      "🔄 Полный сброс сетевого каталога Winsock в 1 клик",
      "🛡️ Очистка локальной таблицы ARP и DNS кэша",
      "🎯 Идеально для CS2, Dota 2, Valorant, GTA 5 и Rust"
    ],
    tags: ["Network", "Ping", "Booster", "Gaming", "TCP"],
    version: "v1.0.0",
    views: "980"
  },
  {
    id: "qwstur-hwid-inspector",
    title: "🛡️ QWSTUR HWID INSPECTOR",
    type: "free",
    category: "tools",
    badge: "HARDWARE",
    icon: "shield",
    status: "● Релиз v1.0",
    downloadUrl: "qwstur-hwid-inspector-v1.0.zip",
    shortDescription: "Безопасный сканер серийных номеров железа: Motherboard, BIOS UUID, Disk Serial, MAC-адреса и видеокарты.",
    fullDescription: "Незаменимый софт для любого геймера и разработчика. Мгновенно считывает все серийные номера оборудования (Motherboard, BIOS Serial, GUID, Disk Serial, MAC). Позволяет в один клик скопировать индивидуальное значение или выгрузить полный профессиональный отчет.",
    features: [
      "🔍 Считывание серийных номеров материнской платы и BIOS",
      "🆔 Определение уникального системного UUID (GUID)",
      "💾 Определение серийного номера физического диска (PhysicalDrive)",
      "🌐 Считывание активного аппаратного MAC-адреса сети",
      "📋 Экспорт полного HWID отчета в буфер обмена в один клик"
    ],
    tags: ["Security", "HWID", "Hardware", "Scanner", "Tools"],
    version: "v1.0.0",
    views: "1.1k"
  },
  {
    id: "cleanlink-sanitizer",
    title: "🔗 CLEANLINK & TEXT SANITIZER",
    type: "free",
    category: "tools",
    badge: "WEB TOOL",
    icon: "link",
    status: "● Web HTML5",
    downloadUrl: "cleanlink-sanitizer.zip",
    shortDescription: "Очистка ссылок от UTM-меток, трекеров (fbclid, gclid, si), нормализация текста и конвертер регистра с транслитом.",
    fullDescription: "Мгновенный санитайзер ссылок и текста прямо в браузере. Вырезает любые трекинговые параметры (utm_*, fbclid, gclid, YouTube si=, ref), убирает мусорные пробелы, декодирует URI-кодировки и преобразует регистр (КэмелКейс, нижний, транслит).",
    features: [
      "🛡️ Удаление utm_*, fbclid, gclid, YouTube si, ref в 1 клик",
      "🧹 Нормализация пробелов и удаление неразрывных пробелов",
      "🔡 Транслитерация текста и преобразование в КэмелКейс",
      "⚡ Мгновенная реакция при вставке из буфера (Ctrl+V)",
      "📋 Быстрое копирование чистого результата"
    ],
    tags: ["WebTool", "Sanitizer", "UTM", "Text", "Free"],
    version: "v1.0.0",
    views: "2.1k"
  },
  {
    id: "image-webp-resizer",
    title: "🖼️ IMAGE TO WEBP & RESIZER",
    type: "free",
    category: "tools",
    badge: "CANVAS TOOL",
    icon: "image",
    status: "● Web HTML5",
    downloadUrl: "image-webp-resizer.zip",
    shortDescription: "Клиентский конвертер картинок в WebP/JPG через HTML5 Canvas. Пакетное сжатие, изменение разрешения и ZIP-выгрузка.",
    fullDescription: "Локальный конвертер изображений, работающий на 100% в браузере через HTML5 Canvas API. Никакие файлы не отправляются в интернет! Поддерживает Drag-and-drop, регулировку качества (1-100%), ограничение макс. ширины и скачивание всех результатов единым ZIP-архивом.",
    features: [
      "🎨 Пакетная конвертация PNG / JPG в компактный WebP",
      "📉 Экономия веса до 80% без видимой потери качества",
      "📐 Настраиваемый ресайз (Full HD, 2K, Превью)",
      "🔒 100% приватность: все вычисления в памяти твоего ПК",
      "📦 Выгрузка всех файлов в один клик через JSZip"
    ],
    tags: ["Canvas", "WebP", "Image", "Compression", "ZIP"],
    version: "v1.0.0",
    views: "1.8k"
  },
  {
    id: "quickdrop-scratchpad",
    title: "📝 QUICKDROP SCRATCHPAD",
    type: "free",
    category: "tools",
    badge: "SCRATCHPAD",
    icon: "file-text",
    status: "● Web HTML5",
    downloadUrl: "quickdrop-scratchpad.zip",
    shortDescription: "Ультралегкий моноширинный блокнот с мгновенным автосохранением в LocalStorage, 5 вкладками и экспортом в .md.",
    fullDescription: "Минималистичный блокнот без лишних рамок с темной палитрой #121212. Мгновенно сохраняет каждую букву в LocalStorage. Включает 5 независимых вкладок (Черновик, Задачи, Сниппеты, Идеи, Промпты), подсчет слов/символов и экспорт в Markdown с датой.",
    features: [
      "⚡ Мгновенное автосохранение в LocalStorage при вводе",
      "📑 5 независимых вкладок (Черновик, Задачи, Сниппеты)",
      "📊 Подсчет символов, слов и примерного времени чтения",
      "💾 Экспорт текста в файл .md с текущей датой",
      "⌨️ Горячие клавиши (Ctrl+Shift+C для копирования)"
    ],
    tags: ["Notes", "Scratchpad", "Markdown", "LocalStorage"],
    version: "v1.0.0",
    views: "1.6k"
  },
  {
    id: "json-inspector",
    title: "🔍 JSON INSPECTOR & FORMATTER",
    type: "free",
    category: "tools",
    badge: "DEV TOOL",
    icon: "code",
    status: "● Web HTML5",
    downloadUrl: "json-inspector.zip",
    shortDescription: "Мгновенная подсветка синтаксических ошибок в JSON, форматирование, минификация и авто-исправление кавычек.",
    fullDescription: "Профессиональный инструмент разработчика. Валидирует и форматирует JSON в реальном времени, вычисляет скорость парсинга, минифицирует код и автоматически исправляет одинарные кавычки и висячие запятые в один клик.",
    features: [
      "⚡ Моментальная подсветка синтаксических ошибок в коде",
      "🔧 Автоматический фикс одинарных кавычек и висячих запятых",
      "📦 Минификация и форматирование с отступами (Ctrl+Enter)",
      "🔤 Экранирование JSON строк в один клик",
      "📊 Статистика строк и размера структуры"
    ],
    tags: ["JSON", "DevTool", "Formatter", "Syntax", "Validator"],
    version: "v1.0.0",
    views: "2.3k"
  },
  {
    id: "base64-hash-lab",
    title: "⚡ BASE64 & HASH DEVLAB",
    type: "free",
    category: "tools",
    badge: "CRYPTO TOOL",
    icon: "hash",
    status: "● Web HTML5",
    downloadUrl: "base64-hash-lab.zip",
    shortDescription: "Двунаправленный конвертер Base64 (текст и файлы/картинки в Data URI) + генератор хэшей SHA-256, SHA-512, SHA-1.",
    fullDescription: "Криптографическая веб-лаборатория для кодирования и декодирования Base64 со встроенным URL-Safe режимом. Поддерживает перетаскивание любых файлов для получения Data URI и расчет хэшей SHA-256 / SHA-512 через нативный Web Crypto API без интернета.",
    features: [
      "🔄 Двунаправленное кодирование и декодирование Base64",
      "📁 Drag-and-drop файлов для мгновенного получения Data URI",
      "🔒 Генерация хэшей SHA-256, SHA-512, SHA-1 на лету",
      "🌐 Поддержка URL-Safe Base64 режима (-_)",
      "📋 Копирование любого значения в буфер в 1 клик"
    ],
    tags: ["Base64", "SHA256", "Crypto", "Hash", "DataURI"],
    version: "v1.0.0",
    views: "1.9k"
  },
  {
    id: "colorkit-studio",
    title: "🎨 COLORKIT & GRADIENT STUDIO",
    type: "free",
    category: "tools",
    badge: "DESIGN TOOL",
    icon: "palette",
    status: "● Web HTML5",
    downloadUrl: "colorkit-studio.zip",
    shortDescription: "Интерактивная палитра цветов (HEX, RGB, HSL, Tailwind), проверка контрастности WCAG и визуальный генератор CSS-градиентов.",
    fullDescription: "Удобный генератор цветов и градиентов для фронтендеров и дизайнеров. Конвертирует в HEX, RGB, HSL и Tailwind CSS класс, тестирует контрастность текста по стандарту WCAG 2.1 (AA/AAA) и генерирует чистый CSS код градиента.",
    features: [
      "🎨 Двусторонняя конвертация HEX, RGB, HSL и Tailwind классов",
      "👁️ Проверка доступности контрастности текста (WCAG AA/AAA)",
      "🌈 Визуальный конструктор двухцветных градиентов с углами",
      "🎲 Случайная генерация цвета по нажатию на [Пробел]",
      "📋 Экспорт чистого CSS кода градиента"
    ],
    tags: ["Color", "Gradient", "Tailwind", "WCAG", "CSS"],
    version: "v1.0.0",
    views: "1.7k"
  }
];
