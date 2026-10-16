"""
==============================================================================
       ⚡ QWSTUR GAMER AUTO-CLICKER & MACRO // by qwstur
==============================================================================
Разработчик: qwstur | Магазин: qwsturs store
Telegram: https://t.me/AimBoGAttack
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
import time
import random
import threading
import webbrowser
import ctypes
from ctypes import wintypes
import tkinter as tk
from tkinter import ttk, messagebox

BG_DARK = "#09090b"
BG_SURFACE = "#121217"
BG_CARD = "#18181f"
BORDER_COLOR = "#27272a"
TEXT_MAIN = "#f4f4f5"
TEXT_MUTED = "#a1a1aa"
ACCENT_PURPLE = "#8b5cf6"
ACCENT_GREEN = "#10b981"
ACCENT_RED = "#ef4444"
ACCENT_AMBER = "#f59e0b"
ACCENT_CYAN = "#06b6d4"

# WinAPI Mouse Events
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010
MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040

class AutoClickerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ QWSTUR GAMER AUTO-CLICKER // by qwstur")
        self.geometry("640x520")
        self.minsize(580, 480)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.is_running = False
        self.click_count = 0
        self.btn_var = tk.StringVar(value="LEFT") # LEFT, RIGHT, MIDDLE
        self.interval_ms_var = tk.IntVar(value=50) # 50ms = 20 CPS
        self.humanize_var = tk.BooleanVar(value=True)

        self.build_ui()

        # Keyboard hook for F7 toggle
        self.bind("<F7>", lambda e: self.toggle_clicking())
        self.start_hotkey_listener()

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG_SURFACE, height=60, highlightthickness=1, highlightbackground=BORDER_COLOR)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        owner_btn = tk.Button(header, text="💬 Написать владельцу", font=("Segoe UI", 8, "bold"),
                              bg=ACCENT_PURPLE, fg="#ffffff", activebackground="#7c3aed", activeforeground="#ffffff",
                              relief="flat", cursor="hand2", padx=10, pady=3,
                              command=lambda: webbrowser.open("https://t.me/AimBoGAttack"))
        owner_btn.pack(side="right", padx=16)

        h_left = tk.Frame(header, bg=BG_SURFACE)
        h_left.pack(side="left", padx=16, pady=8)

        t_lbl = tk.Label(h_left, text="⚡ GAMER AUTO-CLICKER & MACRO // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Высокоточный кликер для фарма, гринда и шутеров с защитой от античита // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Stats Hero Bar
        stats_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=10)
        stats_bar.pack(fill="x")

        stats_card = tk.Frame(stats_bar, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=16, pady=12)
        stats_card.pack(fill="x")

        # Status & Counter
        s_left = tk.Frame(stats_card, bg=BG_CARD)
        s_left.pack(side="left", fill="both", expand=True)

        self.state_lbl = tk.Label(s_left, text="СТАТУС: ОСТАНОВЛЕН (Нажмите F7)", font=("Consolas", 9, "bold"), fg=TEXT_MUTED, bg=BG_CARD)
        self.state_lbl.pack(anchor="w")

        self.count_lbl = tk.Label(s_left, text="Всего кликов: 0", font=("Segoe UI", 16, "bold"), fg=ACCENT_CYAN, bg=BG_CARD)
        self.count_lbl.pack(anchor="w")

        # Master Start / Stop Button
        self.start_btn = tk.Button(stats_card, text="▶ СТАРТ [F7]", font=("Segoe UI", 11, "bold"),
                                   bg=ACCENT_GREEN, fg="#000000", activebackground="#34d399", activeforeground="#000000",
                                   relief="flat", cursor="hand2", padx=20, pady=10, command=self.toggle_clicking)
        self.start_btn.pack(side="right")

        # Settings Container
        body = tk.Frame(self, bg=BG_DARK, padx=16, pady=6)
        body.pack(fill="both", expand=True)

        card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=16, pady=14)
        card.pack(fill="both", expand=True)

        # Mouse Button Choice
        b_row = tk.Frame(card, bg=BG_CARD)
        b_row.pack(fill="x", pady=6)
        tk.Label(b_row, text="Клавиша мыши:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD, width=18, anchor="w").pack(side="left")

        for name, val in [("Левая (ЛКМ)", "LEFT"), ("Правая (ПКМ)", "RIGHT"), ("Средняя (СКМ)", "MIDDLE")]:
            rb = tk.Radiobutton(b_row, text=name, variable=self.btn_var, value=val,
                                font=("Segoe UI", 8), fg=TEXT_MAIN, bg=BG_CARD, selectcolor=BG_SURFACE, activebackground=BG_CARD)
            rb.pack(side="left", padx=8)

        # Interval Slider
        i_row = tk.Frame(card, bg=BG_CARD)
        i_row.pack(fill="x", pady=8)
        tk.Label(i_row, text="Интервал клика (ms):", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD, width=18, anchor="w").pack(side="left")
        
        scale = tk.Scale(i_row, from_=5, to=500, variable=self.interval_ms_var, orient="horizontal", command=self.update_cps_preview,
                         bg=BG_CARD, fg=TEXT_MAIN, highlightthickness=0, troughcolor=BG_SURFACE)
        scale.pack(side="left", fill="x", expand=True, padx=6)

        self.cps_lbl = tk.Label(i_row, text="~20 CPS", font=("Consolas", 9, "bold"), fg=ACCENT_AMBER, bg=BG_CARD, width=8)
        self.cps_lbl.pack(side="right")

        # Quick Presets
        p_row = tk.Frame(card, bg=BG_CARD)
        p_row.pack(fill="x", pady=6)
        tk.Label(p_row, text="Быстрые пресеты:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD, width=18, anchor="w").pack(side="left")

        presets = [
            ("Максимум (~50 CPS)", 20),
            ("Пистолет CS2 (12 CPS)", 80),
            ("Фарм кликер (5 CPS)", 200),
            ("1 клик в секунду", 1000)
        ]
        for name, ms in presets:
            btn = tk.Button(p_row, text=name, font=("Segoe UI", 7), bg=BG_SURFACE, fg=TEXT_MUTED, activebackground=BG_CARD,
                            relief="flat", cursor="hand2", padx=6, pady=2, command=lambda m=ms: self.set_preset(m))
            btn.pack(side="left", padx=3)

        # Anti-Cheat Humanizer Mode
        h_row = tk.Frame(card, bg=BG_CARD)
        h_row.pack(fill="x", pady=10)
        tk.Checkbutton(h_row, text="🛡️ Режим Humanize (Рандомизация задержки ±15% для обхода анти-автокликеров)",
                       variable=self.humanize_var, font=("Segoe UI", 8, "bold"), fg=ACCENT_GREEN, bg=BG_CARD,
                       selectcolor=BG_SURFACE, activebackground=BG_CARD).pack(anchor="w")

        # Hotkey Info banner
        info_box = tk.Frame(card, bg=BG_SURFACE, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=12, pady=8)
        info_box.pack(fill="x", pady=(10, 0))
        tk.Label(info_box, text="⚡ ГОРЯЧАЯ КЛАВИША: [F7] — старт и мгновенная остановка прямо в игре.", font=("Consolas", 8, "bold"), fg=ACCENT_PURPLE, bg=BG_SURFACE).pack(anchor="w")

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=6)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))

        foot_hint = tk.Label(footer, text="WinAPI mouse_event / Минимальная задержка", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        foot_hint.pack(side="left", padx=16, pady=6)

    def set_preset(self, ms):
        self.interval_ms_var.set(ms)
        self.update_cps_preview(ms)

    def update_cps_preview(self, val):
        ms = int(val)
        if ms > 0:
            cps = round(1000.0 / ms, 1)
            self.cps_lbl.config(text=f"~{cps} CPS")

    def toggle_clicking(self):
        self.is_running = not self.is_running
        if self.is_running:
            self.state_lbl.config(text="● СТАТУС: АКТИВЕН / КЛИКАЕТ", fg=ACCENT_GREEN)
            self.start_btn.config(text="⏹ СТОП [F7]", bg=ACCENT_RED, fg="#ffffff")
            threading.Thread(target=self._click_loop, daemon=True).start()
        else:
            self.state_lbl.config(text="СТАТУС: ОСТАНОВЛЕН (Нажмите F7)", fg=TEXT_MUTED)
            self.start_btn.config(text="▶ СТАРТ [F7]", bg=ACCENT_GREEN, fg="#000000")

    def _click_loop(self):
        while self.is_running:
            btn = self.btn_var.get()
            if btn == "LEFT":
                down, up = MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
            elif btn == "RIGHT":
                down, up = MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
            else:
                down, up = MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP

            # Perform click via WinAPI
            ctypes.windll.user32.mouse_event(down, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(up, 0, 0, 0, 0)

            self.click_count += 1
            if self.click_count % 5 == 0:
                self.after(0, lambda c=self.click_count: self.count_lbl.config(text=f"Всего кликов: {c}"))

            interval = self.interval_ms_var.get() / 1000.0
            if self.humanize_var.get():
                jitter = (random.random() * 0.3 - 0.15) * interval
                interval = max(0.002, interval + jitter)

            time.sleep(interval)

    def start_hotkey_listener(self):
        # Global background listener for F7 via GetAsyncKeyState
        def listener():
            VK_F7 = 0x76
            was_pressed = False
            while True:
                state = ctypes.windll.user32.GetAsyncKeyState(VK_F7)
                is_pressed = bool(state & 0x8000)
                if is_pressed and not was_pressed:
                    self.after(0, self.toggle_clicking)
                was_pressed = is_pressed
                time.sleep(0.05)

        threading.Thread(target=listener, daemon=True).start()

if __name__ == "__main__":
    app = AutoClickerApp()
    app.mainloop()
