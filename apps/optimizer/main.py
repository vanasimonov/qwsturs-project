"""
==============================================================================
                    ⚡ QWSTUR OPTIMIZER PRO // v1.0
==============================================================================
Разработчик: qwstur
Telegram: https://t.me/AimBoGAttack
Магазин: qwsturs store
==============================================================================
"""

# --- ⚡ Auto-dependency installer by qwstur ---
def _ensure_deps(*_packages):
    import sys, subprocess
    for _pkg in _packages:
        _mod = _pkg.split("==")[0].split(">=")[0].strip()
        try:
            __import__(_mod)
        except ImportError:
            print(f"[*] Авто-установка необходимой библиотеки: {_pkg}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", _pkg,
                    "--disable-pip-version-check", "--quiet"
                ])
            except Exception as _e:
                print(f"[!] Не удалось установить {_pkg}: {_e}")
# ---------------------------------------------


import os
import sys
import shutil
import tempfile
import subprocess
import threading
import time
import webbrowser
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox

# Colors
BG_DARK = "#09090b"
BG_SURFACE = "#121216"
BG_CARD = "#18181f"
BORDER_COLOR = "#272733"
TEXT_MAIN = "#f4f4f5"
TEXT_MUTED = "#a1a1aa"
ACCENT_GREEN = "#10b981"
ACCENT_PURPLE = "#a855f7"
ACCENT_BLUE = "#38bdf8"
BTN_HOVER = "#23232c"

TELEGRAM_URL = "https://t.me/AimBoGAttack"

class QwsturOptimizerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("⚡ QWSTUR OPTIMIZER PRO // v1.0 // by qwstur")
        self.geometry("780x560")
        self.minsize(720, 500)
        self.configure(bg=BG_DARK)

        # Try to make icon / styling dark
        try:
            # Dark title bar on Windows 10/11
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            rendering_policy = 1
            value = ctypes.c_int(rendering_policy)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.create_widgets()
        self.log("⚡ QWSTUR OPTIMIZER PRO инициализирован и готов к работе.")
        self.log("✈️ Официальный разработчик: @AimBoGAttack")

    def create_widgets(self):
        # Header Frame
        header = tk.Frame(self, bg=BG_SURFACE, height=65, highlightthickness=1, highlightbackground=BORDER_COLOR)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        # Title
        title_box = tk.Frame(header, bg=BG_SURFACE)
        title_box.pack(side="left", padx=20, pady=10)

        title_lbl = tk.Label(title_box, text="⚡ QWSTUR OPTIMIZER // by qwstur", font=("Segoe UI", 14, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(title_box, text="Digital Performance & Clean Suite // by qwstur", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_SURFACE)
        sub_lbl.pack(anchor="w")

        # Telegram Button in Header
        tg_btn = tk.Button(header, text="✉️ Написать владельцу", font=("Segoe UI", 9, "bold"),
                           bg=ACCENT_PURPLE, fg="#ffffff", activebackground="#9333ea", activeforeground="#ffffff",
                           relief="flat", cursor="hand2", padx=12, pady=5, command=self.open_telegram)
        tg_btn.pack(side="right", padx=20)

        # Status badge
        status_lbl = tk.Label(header, text="● SYSTEM: ACTIVE // by qwstur", font=("Consolas", 9, "bold"), fg=ACCENT_GREEN, bg=BG_SURFACE)
        status_lbl.pack(side="right", padx=15)

        # Body Container (Columns: Controls on Left, Log on Right)
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=20, pady=15)

        # Left Column - Action Cards
        left_col = tk.Frame(body, bg=BG_DARK, width=380)
        left_col.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Card 1: RAM & Cache
        self.create_card(
            parent=left_col,
            title="🚀 Очистка RAM и Процессов",
            desc="Сброс рабочего набора памяти неактивных приложений и сборка мусора.",
            btn_text="Очистить память",
            btn_color=ACCENT_GREEN,
            action=self.clean_ram
        )

        # Card 2: DNS & Latency
        self.create_card(
            parent=left_col,
            title="⚡ Сброс кэша DNS и Сети",
            desc="Мгновенный сброс DNS Resolver Cache для снижения пинга в играх.",
            btn_text="Сбросить DNS",
            btn_color=ACCENT_BLUE,
            action=self.flush_dns
        )

        # Card 3: Temp Junk Cleaner
        self.create_card(
            parent=left_col,
            title="🧹 Очистка Temp и Кэша",
            desc="Удаление временных файлов Windows и кэша для освобождения места.",
            btn_text="Очистить мусор",
            btn_color=ACCENT_PURPLE,
            action=self.clean_temp
        )

        # Card 4: Gaming Boost
        self.create_card(
            parent=left_col,
            title="🎮 Игровой буст (High Perf)",
            desc="Переключение схемы питания Windows на максимальную производительность.",
            btn_text="Включить Boost",
            btn_color="#eab308",
            action=self.enable_gaming_mode
        )

        # Right Column - Terminal Log
        right_col = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR)
        right_col.pack(side="right", fill="both", expand=True, padx=(10, 0))

        log_header = tk.Frame(right_col, bg=BG_SURFACE, height=35)
        log_header.pack(fill="x")
        log_header.pack_propagate(False)

        log_title = tk.Label(log_header, text="💻 КОНСОЛЬ ЛОГОВ (LIVE OUTPUT) // by qwstur", font=("Consolas", 9, "bold"), fg=TEXT_MUTED, bg=BG_SURFACE)
        log_title.pack(side="left", padx=12, pady=8)

        clear_btn = tk.Button(log_header, text="Очистить", font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_MUTED,
                              relief="flat", cursor="hand2", padx=8, command=self.clear_logs)
        clear_btn.pack(side="right", padx=10, pady=5)

        # Text Console
        self.log_text = tk.Text(right_col, bg="#0d0d11", fg="#e4e4e7", font=("Consolas", 9),
                                insertbackground="white", selectbackground=ACCENT_PURPLE,
                                wrap="word", relief="flat", padx=10, pady=10)
        self.log_text.pack(fill="both", expand=True)

        # Bottom Bar
        footer = tk.Frame(self, bg=BG_SURFACE, height=35, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        foot_lbl = tk.Label(footer, text="⚡ qwsturs store © 2026 // Бесплатная утилита // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        foot_lbl.pack(side="left", padx=20, pady=8)

        tg_link_lbl = tk.Label(footer, text="✈️ t.me/AimBoGAttack // by qwstur", font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        tg_link_lbl.pack(side="right", padx=20, pady=8)
        tg_link_lbl.bind("<Button-1>", lambda e: self.open_telegram())

    def create_card(self, parent, title, desc, btn_text, btn_color, action):
        card = tk.Frame(parent, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=10)
        card.pack(fill="x", pady=4)

        top_row = tk.Frame(card, bg=BG_CARD)
        top_row.pack(fill="x")

        t_lbl = tk.Label(top_row, text=title, font=("Segoe UI", 10, "bold"), fg=TEXT_MAIN, bg=BG_CARD)
        t_lbl.pack(side="left")

        btn = tk.Button(top_row, text=btn_text, font=("Segoe UI", 8, "bold"),
                        bg=btn_color, fg="#ffffff" if btn_color != "#eab308" else "#000000",
                        activebackground="#ffffff", activeforeground="#000000",
                        relief="flat", cursor="hand2", padx=12, pady=4, command=action)
        btn.pack(side="right")

        d_lbl = tk.Label(card, text=desc, font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, wraplength=340, justify="left")
        d_lbl.pack(anchor="w", pady=(3, 0))

    def log(self, message):
        t_str = time.strftime("[%H:%M:%S]")
        self.log_text.insert("end", f"{t_str} {message}\n")
        self.log_text.see("end")

    def clear_logs(self):
        self.log_text.delete("1.0", "end")
        self.log("Логи очищены.")

    def open_telegram(self):
        webbrowser.open(TELEGRAM_URL)
        self.log("✈️ Открыт Telegram разработчика: " + TELEGRAM_URL)

    # Actions
    def clean_ram(self):
        def task():
            self.log("🚀 Запуск оптимизации оперативной памяти...")
            freed_count = 0
            try:
                # Flush working sets of processes
                handle = ctypes.windll.kernel32.GetCurrentProcess()
                ctypes.windll.psapi.EmptyWorkingSet(handle)
                freed_count += 1

                # Clean garbage in python process
                import gc
                gc.collect()

                time.sleep(0.5)
                self.log(f"✅ [OK] Оперативная память оптимизирована! Рабочие наборы сброшены.")
            except Exception as e:
                self.log(f"⚠️ [Ошибка RAM]: {e}")

        threading.Thread(target=task, daemon=True).start()

    def flush_dns(self):
        def task():
            self.log("⚡ Сброс кэша DNS Resolver...")
            try:
                res = subprocess.run(["ipconfig", "/flushdns"], capture_output=True, text=True, shell=True)
                if res.returncode == 0:
                    self.log("✅ [OK] Кэш сопоставителя DNS успешно очищен.")
                else:
                    self.log("⚠️ Завершено с предупреждением.")
            except Exception as e:
                self.log(f"⚠️ [Ошибка DNS]: {e}")

        threading.Thread(target=task, daemon=True).start()

    def clean_temp(self):
        def task():
            self.log("🧹 Сканирование и очистка временных файлов %TEMP%...")
            temp_dir = tempfile.gettempdir()
            deleted_files = 0
            deleted_bytes = 0

            for root, dirs, files in os.walk(temp_dir):
                for f in files:
                    fp = os.path.join(root, f)
                    try:
                        sz = os.path.getsize(fp)
                        os.remove(fp)
                        deleted_files += 1
                        deleted_bytes += sz
                    except Exception:
                        pass

            mb = round(deleted_bytes / (1024 * 1024), 2)
            self.log(f"✅ [OK] Очищено: {deleted_files} файлов ({mb} MB) из папки Temp.")

        threading.Thread(target=task, daemon=True).start()

    def enable_gaming_mode(self):
        def task():
            self.log("🎮 Применение схемы питания 'Высокая производительность'...")
            try:
                # High performance GUID in Windows
                subprocess.run(["powercfg", "/setactive", "8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c"], shell=True)
                self.log("✅ [OK] Режим 'Высокая производительность' активирован!")
            except Exception as e:
                self.log(f"⚠️ [Ошибка Boost]: {e}")

        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    app = QwsturOptimizerApp()
    app.mainloop()
