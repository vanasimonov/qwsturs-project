"""
==============================================================================
            ⚡ QWSTUR MINI HUD SYSTEM MONITOR // v1.0
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
import ctypes
import threading
import tkinter as tk
from tkinter import ttk

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

# Windows API Structures for zero-dependency metrics
class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
    ]

class FILETIME(ctypes.Structure):
    _fields_ = [("dwLowDateTime", ctypes.c_ulong), ("dwHighDateTime", ctypes.c_ulong)]

class MiniMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📊 QWSTUR MINI HUD MONITOR // v1.0 // by qwstur")
        self.geometry("420x540")
        self.minsize(380, 480)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.prev_idle = 0
        self.prev_kernel = 0
        self.prev_user = 0
        self.is_monitoring = True
        self.always_on_top = False

        self.build_ui()
        self.bind_keys()
        self.update_metrics_loop()

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG_SURFACE, height=54, highlightthickness=1, highlightbackground=BORDER_COLOR)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)
        owner_btn = tk.Button(header, text="💬 Написать владельцу", font=("Segoe UI", 8, "bold"),
                              bg=ACCENT_PURPLE, fg="#ffffff", activebackground="#7c3aed", activeforeground="#ffffff",
                              relief="flat", cursor="hand2", padx=10, pady=3,
                              command=lambda: webbrowser.open("https://t.me/AimBoGAttack"))
        owner_btn.pack(side="right", padx=16)


        h_left = tk.Frame(header, bg=BG_SURFACE)
        h_left.pack(side="left", padx=14, pady=6)

        t_lbl = tk.Label(h_left, text="📊 MINI HUD MONITOR // by qwstur", font=("Segoe UI", 11, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Системный телеметрический HUD // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        self.top_btn = tk.Button(header, text="📌 Поверх всех", font=("Segoe UI", 8),
                                 bg=BG_CARD, fg=TEXT_MUTED, activebackground=BG_SURFACE,
                                 relief="flat", cursor="hand2", padx=8, pady=3,
                                 highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.toggle_pin)
        self.top_btn.pack(side="right", padx=14)

        # Body Container
        body = tk.Frame(self, bg=BG_DARK, padx=14, pady=10)
        body.pack(fill="both", expand=True)

        # 1. CPU Card
        self.cpu_card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=12, pady=10)
        self.cpu_card.pack(fill="x", pady=4)

        cpu_top = tk.Frame(self.cpu_card, bg=BG_CARD)
        cpu_top.pack(fill="x")
        tk.Label(cpu_top, text="⚡ НАГРУЗКА CPU", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD).pack(side="left")
        self.cpu_val_lbl = tk.Label(cpu_top, text="0%", font=("Consolas", 11, "bold"), fg=ACCENT_CYAN, bg=BG_CARD)
        self.cpu_val_lbl.pack(side="right")

        self.cpu_bar = ttk.Progressbar(self.cpu_card, mode="determinate")
        self.cpu_bar.pack(fill="x", pady=(6, 2))

        # 2. RAM Card
        self.ram_card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=12, pady=10)
        self.ram_card.pack(fill="x", pady=4)

        ram_top = tk.Frame(self.ram_card, bg=BG_CARD)
        ram_top.pack(fill="x")
        tk.Label(ram_top, text="🧠 ПАМЯТЬ RAM", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD).pack(side="left")
        self.ram_val_lbl = tk.Label(ram_top, text="0 / 0 ГБ (0%)", font=("Consolas", 10, "bold"), fg=ACCENT_PURPLE, bg=BG_CARD)
        self.ram_val_lbl.pack(side="right")

        self.ram_bar = ttk.Progressbar(self.ram_card, mode="determinate")
        self.ram_bar.pack(fill="x", pady=(6, 2))

        # 3. Disk C Card
        self.disk_card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=12, pady=10)
        self.disk_card.pack(fill="x", pady=4)

        disk_top = tk.Frame(self.disk_card, bg=BG_CARD)
        disk_top.pack(fill="x")
        tk.Label(disk_top, text="💾 ДИСК (C:)", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD).pack(side="left")
        self.disk_val_lbl = tk.Label(disk_top, text="0 / 0 ГБ", font=("Consolas", 10, "bold"), fg=ACCENT_GREEN, bg=BG_CARD)
        self.disk_val_lbl.pack(side="right")

        self.disk_bar = ttk.Progressbar(self.disk_card, mode="determinate")
        self.disk_bar.pack(fill="x", pady=(6, 2))

        # 4. System Uptime & Stats Card
        stats_card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=12, pady=10)
        stats_card.pack(fill="both", expand=True, pady=4)

        tk.Label(stats_card, text="⏱️ ВРЕМЯ РАБОТЫ (UPTIME)", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w")
        self.uptime_lbl = tk.Label(stats_card, text="0д 0ч 0м", font=("Consolas", 14, "bold"), fg=TEXT_MAIN, bg=BG_CARD)
        self.uptime_lbl.pack(anchor="w", pady=(2, 6))

        tk.Label(stats_card, text="⚙️ ПРОЦЕССЫ И ПОТОКИ", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w")
        self.procs_lbl = tk.Label(stats_card, text="Активных процессов: подсчет...", font=("Segoe UI", 9), fg=TEXT_MAIN, bg=BG_CARD)
        self.procs_lbl.pack(anchor="w", pady=(2, 0))

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=30, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        self.status_lbl = tk.Label(footer, text="● Мониторинг активен (1 Hz) // by qwstur", font=("Segoe UI", 8), fg=ACCENT_GREEN, bg=BG_SURFACE)
        self.status_lbl.pack(side="left", padx=14, pady=5)

        hint_lbl = tk.Label(footer, text="[T] Закрепить  |  [Esc] Закрыть // by qwstur", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        hint_lbl.pack(side="right", padx=14, pady=5)

    def bind_keys(self):
        self.bind("<t>", lambda e: self.toggle_pin())
        self.bind("<T>", lambda e: self.toggle_pin())
        self.bind("<Escape>", lambda e: self.destroy())

    def toggle_pin(self):
        self.always_on_top = not self.always_on_top
        self.wm_attributes("-topmost", self.always_on_top)
        if self.always_on_top:
            self.top_btn.config(text="📌 Закреплено // by qwstur", fg=ACCENT_CYAN, bg=BG_SURFACE)
        else:
            self.top_btn.config(text="📌 Поверх всех", fg=TEXT_MUTED, bg=BG_CARD)

    def get_cpu_load(self):
        idle = FILETIME()
        kernel = FILETIME()
        user = FILETIME()
        if ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idle), ctypes.byref(kernel), ctypes.byref(user)):
            i = (idle.dwHighDateTime << 32) + idle.dwLowDateTime
            k = (kernel.dwHighDateTime << 32) + kernel.dwLowDateTime
            u = (user.dwHighDateTime << 32) + user.dwLowDateTime

            if self.prev_kernel != 0:
                d_idle = i - self.prev_idle
                d_kernel = k - self.prev_kernel
                d_user = u - self.prev_user
                total = d_kernel + d_user
                if total > 0:
                    load = (1.0 - (d_idle / total)) * 100.0
                    self.prev_idle, self.prev_kernel, self.prev_user = i, k, u
                    return max(0.0, min(100.0, load))

            self.prev_idle, self.prev_kernel, self.prev_user = i, k, u
        return 0.0

    def get_ram_info(self):
        mem = MEMORYSTATUSEX()
        mem.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(mem)):
            total_gb = mem.ullTotalPhys / (1024**3)
            avail_gb = mem.ullAvailPhys / (1024**3)
            used_gb = total_gb - avail_gb
            pct = mem.dwMemoryLoad
            return used_gb, total_gb, pct
        return 0, 0, 0

    def get_disk_info(self):
        free_bytes = ctypes.c_ulonglong(0)
        total_bytes = ctypes.c_ulonglong(0)
        total_free_bytes = ctypes.c_ulonglong(0)
        if ctypes.windll.kernel32.GetDiskFreeSpaceExW("C:\\", ctypes.byref(free_bytes), ctypes.byref(total_bytes), ctypes.byref(total_free_bytes)):
            t_gb = total_bytes.value / (1024**3)
            f_gb = free_bytes.value / (1024**3)
            u_gb = t_gb - f_gb
            pct = (u_gb / t_gb) * 100 if t_gb > 0 else 0
            return u_gb, t_gb, pct
        return 0, 0, 0

    def get_uptime_str(self):
        uptime_ms = ctypes.windll.kernel32.GetTickCount64()
        sec = uptime_ms // 1000
        days = sec // 86400
        hours = (sec % 86400) // 3600
        mins = (sec % 3600) // 60
        secs = sec % 60
        return f"{days}д {hours:02d}ч {mins:02d}м {secs:02d}с"

    def update_metrics_loop(self):
        try:
            # CPU
            cpu_pct = self.get_cpu_load()
            self.cpu_val_lbl.config(text=f"{cpu_pct:.1f}%")
            self.cpu_bar["value"] = cpu_pct

            # RAM
            used_ram, total_ram, ram_pct = self.get_ram_info()
            self.ram_val_lbl.config(text=f"{used_ram:.1f} / {total_ram:.1f} ГБ ({ram_pct}%)")
            self.ram_bar["value"] = ram_pct

            # Disk
            used_disk, total_disk, disk_pct = self.get_disk_info()
            self.disk_val_lbl.config(text=f"{used_disk:.1f} / {total_disk:.1f} ГБ ({disk_pct:.0f}%)")
            self.disk_bar["value"] = disk_pct

            # Uptime
            self.uptime_lbl.config(text=self.get_uptime_str())
        except Exception:
            pass

        self.after(1000, self.update_metrics_loop)

if __name__ == "__main__":
    app = MiniMonitorApp()
    app.mainloop()
