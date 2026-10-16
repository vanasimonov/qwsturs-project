"""
==============================================================================
        📡 QWSTUR GAMER PING & PACKET LOSS HUD // by qwstur
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
import subprocess
import threading
import webbrowser
import ctypes
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
ACCENT_AMBER = "#f59e0b"
ACCENT_RED = "#ef4444"
ACCENT_CYAN = "#06b6d4"

TARGET_HUBS = [
    ("Valve EU (CS2)", "155.133.248.51"),
    ("Riot Games EU", "104.160.141.3"),
    ("Discord Voice", "router.discord.gg"),
    ("Cloudflare DNS", "1.1.1.1")
]

class PingHudApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📡 QWSTUR GAMER PING HUD // by qwstur")
        self.attributes("-topmost", True)
        self.overrideredirect(True) # Borderless floating HUD
        self.configure(bg=BG_DARK)

        # Size & position in top-right of screen
        sw = self.winfo_screenwidth()
        self.w = 280
        self.h = 240
        self.geometry(f"{self.w}x{self.h}+{sw - self.w - 30}+40")

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.hub_labels = {}
        self.hub_history = {name: [] for name, _ in TARGET_HUBS}
        self.is_monitoring = True

        self.build_ui()
        self.make_draggable()
        self.start_ping_thread()

    def build_ui(self):
        # Outer Border Box
        box = tk.Frame(self, bg=BG_DARK, highlightthickness=1, highlightbackground=ACCENT_PURPLE)
        box.pack(fill="both", expand=True)

        # Header Bar (Drag handle)
        header = tk.Frame(box, bg=BG_SURFACE, height=34, cursor="fleur")
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="📡 PING & JITTER HUD // by qwstur", font=("Segoe UI", 8, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE).pack(side="left", padx=8)

        # Close / Minimize buttons
        cls_btn = tk.Button(header, text="✕", font=("Segoe UI", 8), bg=BG_SURFACE, fg=TEXT_MUTED,
                            activebackground="#ef4444", activeforeground="#ffffff", relief="flat", cursor="hand2", padx=6, command=self.destroy)
        cls_btn.pack(side="right")

        owner_btn = tk.Button(header, text="✈️", font=("Segoe UI", 8), bg=BG_SURFACE, fg=ACCENT_PURPLE,
                              relief="flat", cursor="hand2", padx=4, command=lambda: webbrowser.open("https://t.me/AimBoGAttack"))
        owner_btn.pack(side="right")

        # Hubs Grid
        content = tk.Frame(box, bg=BG_DARK, padx=8, pady=6)
        content.pack(fill="both", expand=True)

        for name, host in TARGET_HUBS:
            row = tk.Frame(content, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=8, pady=4)
            row.pack(fill="x", pady=2)

            left = tk.Frame(row, bg=BG_CARD)
            left.pack(side="left", fill="both", expand=True)

            tk.Label(left, text=name, font=("Segoe UI", 8, "bold"), fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w")

            jitter_lbl = tk.Label(left, text="Jitter: ~0 ms", font=("Consolas", 7), fg=TEXT_MUTED, bg=BG_CARD)
            jitter_lbl.pack(anchor="w")

            val_lbl = tk.Label(row, text="Тест...", font=("Consolas", 9, "bold"), fg=TEXT_MUTED, bg=BG_CARD)
            val_lbl.pack(side="right")

            self.hub_labels[name] = (val_lbl, jitter_lbl)

        # Footer Status
        footer = tk.Frame(box, bg=BG_SURFACE, height=24)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        tk.Label(footer, text="⚡ Перетаскивай мышью по экрану", font=("Segoe UI", 7), fg=TEXT_MUTED, bg=BG_SURFACE).pack(side="left", padx=8, pady=2)
        
        tg_link = tk.Label(footer, text="by qwstur", font=("Segoe UI", 7, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        tg_link.pack(side="right", padx=8, pady=2)
        tg_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))

    def make_draggable(self):
        def start_move(event):
            self.x = event.x
            self.y = event.y

        def on_move(event):
            deltax = event.x - self.x
            deltay = event.y - self.y
            x = self.winfo_x() + deltax
            y = self.winfo_y() + deltay
            self.geometry(f"+{x}+{y}")

        self.bind("<ButtonPress-1>", start_move)
        self.bind("<B1-Motion>", on_move)

    def start_ping_thread(self):
        def worker():
            while self.is_monitoring:
                for name, host in TARGET_HUBS:
                    try:
                        res = subprocess.run(["ping", "-n", "1", "-w", "1000", host], capture_output=True, text=True)
                        out = res.stdout
                        if "Average =" in out or "Среднее =" in out:
                            part = out.split("Average =")[-1] if "Average =" in out else out.split("Среднее =")[-1]
                            ms = int(''.join(filter(str.isdigit, part)))
                        elif "time=" in out or "время=" in out:
                            line = [l for l in out.splitlines() if "time=" in l or "время=" in l][0]
                            time_part = line.split("time=")[-1].split("ms")[0] if "time=" in line else line.split("время=")[-1].split("мс")[0]
                            ms = int(''.join(filter(str.isdigit, time_part)))
                        else:
                            ms = -1

                        self.after(0, self.update_hub, name, ms)
                    except Exception:
                        self.after(0, self.update_hub, name, -1)
                time.sleep(1.8)

        threading.Thread(target=worker, daemon=True).start()

    def update_hub(self, name, ms):
        if name not in self.hub_labels:
            return
        val_lbl, jit_lbl = self.hub_labels[name]

        if ms >= 0:
            hist = self.hub_history[name]
            hist.append(ms)
            if len(hist) > 8:
                hist.pop(0)

            # Jitter = average difference between consecutive pings
            if len(hist) >= 2:
                diffs = [abs(hist[i] - hist[i-1]) for i in range(1, len(hist))]
                jitter = sum(diffs) / len(diffs)
            else:
                jitter = 0.0

            if ms < 35:
                color = ACCENT_GREEN
            elif ms < 75:
                color = ACCENT_AMBER
            else:
                color = ACCENT_RED

            val_lbl.config(text=f"{ms} ms", fg=color)
            jit_lbl.config(text=f"Джиттер: ±{jitter:.1f} ms", fg=TEXT_MUTED)
        else:
            val_lbl.config(text="Потери ✕", fg=ACCENT_RED)
            jit_lbl.config(text="Packet Drop", fg=ACCENT_RED)

if __name__ == "__main__":
    app = PingHudApp()
    app.mainloop()
