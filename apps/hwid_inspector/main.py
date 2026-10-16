"""
==============================================================================
               ⚡ QWSTUR HWID & SERIAL INSPECTOR // v1.0
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
import subprocess
import threading
import time
import webbrowser
import ctypes
import tkinter as tk
from tkinter import ttk, messagebox

BG_DARK = "#09090b"
BG_SURFACE = "#121216"
BG_CARD = "#18181f"
BORDER_COLOR = "#272733"
TEXT_MAIN = "#f4f4f5"
TEXT_MUTED = "#a1a1aa"
ACCENT_GREEN = "#10b981"
ACCENT_PURPLE = "#a855f7"
ACCENT_BLUE = "#38bdf8"

class HwidInspectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ QWSTUR HWID & SYSTEM INSPECTOR // v1.0 // by qwstur")
        self.geometry("760x560")
        self.minsize(720, 520)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.hwid_data = {}
        self.create_ui()
        self.start_scan_thread()

    def create_ui(self):
        # Header
        header = tk.Frame(self, bg=BG_SURFACE, height=65, highlightthickness=1, highlightbackground=BORDER_COLOR)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tb = tk.Frame(header, bg=BG_SURFACE)
        tb.pack(side="left", padx=20, pady=10)

        t_lbl = tk.Label(tb, text="⚡ QWSTUR HWID INSPECTOR // by qwstur", font=("Segoe UI", 13, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(tb, text="Анализатор серийных номеров железа и компонентов // by qwstur", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        tg_btn = tk.Button(header, text="✉️ Написать владельцу", font=("Segoe UI", 9, "bold"),
                           bg=ACCENT_PURPLE, fg="#ffffff", activebackground="#9333ea", activeforeground="#ffffff",
                           relief="flat", cursor="hand2", padx=12, pady=5, command=self.open_tg)
        tg_btn.pack(side="right", padx=20)

        # Body
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=20, pady=15)

        # Toolbar
        toolbar = tk.Frame(body, bg=BG_DARK)
        toolbar.pack(fill="x", pady=(0, 10))

        self.status_lbl = tk.Label(toolbar, text="⏳ Сканирование железа...", font=("Consolas", 9), fg=ACCENT_GREEN, bg=BG_DARK)
        self.status_lbl.pack(side="left")

        copy_all_btn = tk.Button(toolbar, text="📋 Скопировать весь HWID отчет", font=("Segoe UI", 8, "bold"),
                                 bg=BG_CARD, fg=TEXT_MAIN, activebackground=BG_SURFACE, relief="flat", cursor="hand2",
                                 padx=10, pady=4, highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.copy_all)
        copy_all_btn.pack(side="right")

        rescan_btn = tk.Button(toolbar, text="🔄 Пересканировать", font=("Segoe UI", 8),
                               bg=BG_CARD, fg=TEXT_MUTED, activebackground=BG_SURFACE, relief="flat", cursor="hand2",
                               padx=10, pady=4, highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.start_scan_thread)
        rescan_btn.pack(side="right", padx=8)

        # Items container
        self.cards_frame = tk.Frame(body, bg=BG_DARK)
        self.cards_frame.pack(fill="both", expand=True)

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=35, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        foot_lbl = tk.Label(footer, text="⚡ qwsturs store © 2026 // Бесплатная утилита // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        foot_lbl.pack(side="left", padx=20, pady=8)

        tg_link = tk.Label(footer, text="✈️ t.me/AimBoGAttack // by qwstur", font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        tg_link.pack(side="right", padx=20, pady=8)
        tg_link.bind("<Button-1>", lambda e: self.open_tg())

    def open_tg(self):
        webbrowser.open("https://t.me/AimBoGAttack")

    def run_cmd(self, cmd):
        try:
            res = subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True, timeout=5)
            return res.stdout.strip()
        except Exception:
            return "Не определено"

    def start_scan_thread(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        self.status_lbl.config(text="⏳ Чтение серийных номеров...")

        def worker():
            data = {}
            # Motherboard
            mb = self.run_cmd("(Get-CimInstance Win32_BaseBoard).SerialNumber")
            data["Материнская плата (Motherboard)"] = mb if mb else "Default string / Защищено"

            # BIOS Serial & UUID
            bios = self.run_cmd("(Get-CimInstance Win32_BIOS).SerialNumber")
            data["BIOS Serial Number"] = bios if bios else "Default / To be filled"

            uuid = self.run_cmd("(Get-CimInstance Win32_ComputerSystemProduct).UUID")
            data["System UUID (GUID)"] = uuid if uuid else "Не определен"

            # CPU
            cpu = self.run_cmd("(Get-CimInstance Win32_Processor).Name")
            data["Процессор (CPU)"] = cpu if cpu else "Unknown CPU"

            # Disk
            disk = self.run_cmd("(Get-CimInstance Win32_DiskDrive | Select-Object -First 1).SerialNumber")
            data["Диск Serial (Drive 0)"] = disk.strip() if disk else "Drive Serial"

            # GPU
            gpu = self.run_cmd("(Get-CimInstance Win32_VideoController | Select-Object -First 1).Name")
            data["Видеокарта (GPU)"] = gpu if gpu else "Generic Display Adapter"

            # MAC
            mac = self.run_cmd("(Get-NetAdapter | Where-Object Status -eq 'Up' | Select-Object -First 1).MacAddress")
            data["MAC-Адрес сети"] = mac if mac else "00:00:00:00:00:00"

            self.hwid_data = data
            self.after(0, self.render_data)

        threading.Thread(target=worker, daemon=True).start()

    def render_data(self):
        self.status_lbl.config(text="● HWID успешно определен", fg=ACCENT_GREEN)

        for key, val in self.hwid_data.items():
            row = tk.Frame(self.cards_frame, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=8)
            row.pack(fill="x", pady=3)

            left_box = tk.Frame(row, bg=BG_CARD)
            left_box.pack(side="left", fill="x", expand=True)

            k_lbl = tk.Label(left_box, text=key, font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_CARD)
            k_lbl.pack(anchor="w")

            v_lbl = tk.Label(left_box, text=val, font=("Consolas", 10, "bold"), fg=TEXT_MAIN, bg=BG_CARD)
            v_lbl.pack(anchor="w")

            copy_btn = tk.Button(row, text="📋 Копия // by qwstur", font=("Segoe UI", 8), bg=BG_SURFACE, fg=TEXT_MAIN,
                                 activebackground=ACCENT_PURPLE, activeforeground="#ffffff", relief="flat", cursor="hand2",
                                 padx=8, pady=3, command=lambda v=val: self.copy_text(v))
            copy_btn.pack(side="right")

    def copy_text(self, text):
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Скопировано", f"Значение скопировано в буфер:\n{text}")

    def copy_all(self):
        if not self.hwid_data:
            return
        report = "=== ⚡ QWSTUR HWID INSPECTOR REPORT ===\n"
        for k, v in self.hwid_data.items():
            report += f"{k}: {v}\n"
        report += "======================================\n"
        report += "Разработчик: https://t.me/AimBoGAttack\n"
        self.clipboard_clear()
        self.clipboard_append(report)
        messagebox.showinfo("Скопировано", "Полный HWID отчет скопирован в буфер обмена!")

if __name__ == "__main__":
    app = HwidInspectorApp()
    app.mainloop()
