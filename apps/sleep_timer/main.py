"""
==============================================================================
            ⚡ QWSTUR SYSTEM SLEEP & SHUTDOWN TIMER // v1.0
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
import webbrowser
import time
import subprocess
import threading
import ctypes
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

class SleepTimerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⏱️ QWSTUR SYSTEM SLEEP & SHUTDOWN TIMER // v1.0 // by qwstur")
        self.geometry("640x520")
        self.minsize(580, 460)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.remaining_seconds = 0
        self.is_running = False
        self.warned_beep = False

        self.build_ui()
        self.bind_keys()

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

        t_lbl = tk.Label(h_left, text="⏱️ SYSTEM SLEEP & SHUTDOWN TIMER // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Таймер выключения, перезагрузки и гибернации ПК // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Action Type Selection
        act_card = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=10)
        act_card.pack(fill="x", padx=16, pady=12)

        tk.Label(act_card, text="Действие по таймеру:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w", pady=(0, 6))

        self.action_var = tk.StringVar(value="shutdown")
        actions = [
            ("shutdown", "🛑 Выключение ПК"),
            ("restart", "🔄 Перезагрузка"),
            ("sleep", "💤 Спящий режим"),
            ("lock", "🔒 Блокировка системы")
        ]
        a_row = tk.Frame(act_card, bg=BG_CARD)
        a_row.pack(fill="x")
        for val, title in actions:
            rb = tk.Radiobutton(a_row, text=title, variable=self.action_var, value=val,
                                font=("Segoe UI", 8, "bold"), fg=TEXT_MAIN, bg=BG_CARD, selectcolor=BG_SURFACE,
                                activebackground=BG_CARD, activeforeground=TEXT_MAIN)
            rb.pack(side="left", padx=(0, 14))

        # Presets Bar
        preset_frame = tk.Frame(self, bg=BG_DARK, padx=16)
        preset_frame.pack(fill="x", pady=(0, 8))

        tk.Label(preset_frame, text="Быстрые пресеты:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_DARK).pack(side="left", padx=(0, 8))
        for mins, lbl in ((15, "+15м"), (30, "+30м"), (45, "+45м"), (60, "+1ч"), (120, "+2ч")):
            btn = tk.Button(preset_frame, text=lbl, font=("Consolas", 8, "bold"),
                            bg=BG_CARD, fg=TEXT_MAIN, activebackground=ACCENT_PURPLE, activeforeground="#ffffff",
                            relief="flat", cursor="hand2", padx=8, pady=2,
                            highlightthickness=1, highlightbackground=BORDER_COLOR, command=lambda m=mins: self.add_minutes(m))
            btn.pack(side="left", padx=3)

        # Custom minutes input
        custom_frame = tk.Frame(self, bg=BG_DARK, padx=16)
        custom_frame.pack(fill="x", pady=(0, 12))

        tk.Label(custom_frame, text="Или введите минуты:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_DARK).pack(side="left")
        self.mins_entry = tk.Entry(custom_frame, font=("Consolas", 10), bg=BG_CARD, fg=TEXT_MAIN,
                                   insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1,
                                   highlightbackground=BORDER_COLOR, width=10)
        self.mins_entry.insert(0, "30")
        self.mins_entry.pack(side="left", padx=8, ipady=2)

        set_btn = tk.Button(custom_frame, text="Установить", font=("Segoe UI", 8),
                            bg=BG_SURFACE, fg=TEXT_MAIN, activebackground=BG_CARD,
                            relief="flat", cursor="hand2", padx=8, pady=2,
                            highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.apply_custom_minutes)
        set_btn.pack(side="left")

        # Big Countdown Display Card
        timer_card = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=20, pady=20)
        timer_card.pack(fill="both", expand=True, padx=16, pady=(0, 12))

        self.timer_label = tk.Label(timer_card, text="00:30:00", font=("Consolas", 42, "bold"),
                                    fg=ACCENT_CYAN, bg=BG_CARD)
        self.timer_label.pack(expand=True)

        self.action_preview_lbl = tk.Label(timer_card, text="● Таймер остановлен", font=("Segoe UI", 9),
                                           fg=TEXT_MUTED, bg=BG_CARD)
        self.action_preview_lbl.pack(pady=(0, 10))

        # Control Buttons
        btn_box = tk.Frame(timer_card, bg=BG_CARD)
        btn_box.pack()

        self.start_btn = tk.Button(btn_box, text="⚡ Запустить таймер [Enter]", font=("Segoe UI", 9, "bold"),
                                   bg=ACCENT_GREEN, fg="#000000", activebackground="#059669", activeforeground="#ffffff",
                                   relief="flat", cursor="hand2", padx=16, pady=6, command=self.start_timer)
        self.start_btn.pack(side="left", padx=6)

        self.stop_btn = tk.Button(btn_box, text="🛑 Отменить таймер [Esc]", font=("Segoe UI", 9, "bold"),
                                  bg=ACCENT_RED, fg="#ffffff", activebackground="#dc2626", activeforeground="#ffffff",
                                  relief="flat", cursor="hand2", padx=16, pady=6, command=self.stop_timer)
        self.stop_btn.pack(side="left", padx=6)

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        self.status_lbl = tk.Label(footer, text="● Готов // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        self.status_lbl.pack(side="left", padx=16, pady=6)

        hint_lbl = tk.Label(footer, text="[Enter] Старт  |  [Esc] Отмена // by qwstur", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        hint_lbl.pack(side="right", padx=16, pady=6)

        self.remaining_seconds = 30 * 60
        self.update_display()

    def bind_keys(self):
        self.bind("<Return>", lambda e: self.start_timer())
        self.bind("<Escape>", lambda e: self.stop_timer())

    def add_minutes(self, mins):
        if self.is_running:
            self.remaining_seconds += mins * 60
        else:
            self.remaining_seconds = mins * 60
        self.update_display()

    def apply_custom_minutes(self):
        val = self.mins_entry.get().strip()
        try:
            mins = int(val)
            if mins <= 0:
                raise ValueError
            self.remaining_seconds = mins * 60
            self.update_display()
            self.status_lbl.config(text=f"● Установлено: {mins} мин", fg=ACCENT_GREEN)
        except ValueError:
            self.status_lbl.config(text="✗ Введите положительное число минут", fg=ACCENT_RED)

    def update_display(self):
        hrs = self.remaining_seconds // 3600
        mins = (self.remaining_seconds % 3600) // 60
        secs = self.remaining_seconds % 60
        self.timer_label.config(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")

    def start_timer(self):
        if self.remaining_seconds <= 0:
            self.status_lbl.config(text="⚠️ Укажите время таймера больше 0", fg=ACCENT_AMBER)
            return

        if self.is_running:
            return

        self.is_running = True
        self.warned_beep = False
        act = self.action_var.get()
        act_names = {"shutdown": "Выключение ПК", "restart": "Перезагрузка ПК", "sleep": "Спящий режим", "lock": "Блокировка системы"}
        self.action_preview_lbl.config(text=f"⏳ Таймер активен // {act_names.get(act)}", fg=ACCENT_PURPLE)
        self.status_lbl.config(text="● Отсчет запущен", fg=ACCENT_GREEN)
        self.tick()

    def stop_timer(self):
        if not self.is_running and self.remaining_seconds == 0:
            return

        self.is_running = False
        # Cancel any Windows shutdown command
        try:
            subprocess.run("shutdown /a", shell=True, capture_output=True)
        except Exception:
            pass

        self.action_preview_lbl.config(text="● Таймер остановлен", fg=TEXT_MUTED)
        self.status_lbl.config(text="🛑 Таймер отменен", fg=ACCENT_RED)

    def tick(self):
        if not self.is_running:
            return

        if self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            self.update_display()

            # Beep warning at 60 seconds
            if self.remaining_seconds == 60 and not self.warned_beep:
                self.warned_beep = True
                try:
                    ctypes.windll.user32.MessageBeep(0xFFFFFFFF)
                except Exception:
                    pass

            self.after(1000, self.tick)
        else:
            self.is_running = False
            self.execute_action()

    def execute_action(self):
        act = self.action_var.get()
        self.status_lbl.config(text="⚡ Выполнение действия...", fg=ACCENT_AMBER)
        try:
            if act == "shutdown":
                subprocess.run("shutdown /s /t 0", shell=True)
            elif act == "restart":
                subprocess.run("shutdown /r /t 0", shell=True)
            elif act == "sleep":
                subprocess.run("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)
            elif act == "lock":
                subprocess.run("rundll32.exe user32.dll,LockWorkStation", shell=True)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось выполнить действие: {e}")

if __name__ == "__main__":
    app = SleepTimerApp()
    app.mainloop()
