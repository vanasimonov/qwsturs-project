"""
==============================================================================
          🎯 QWSTUR CROSSHAIR OVERLAY // by qwstur
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
import math
import webbrowser
import ctypes
from ctypes import wintypes
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
ACCENT_CYAN = "#06b6d4"

class CrosshairWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Crosshair")
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        # Transparent background color
        self.trans_color = "#000001"
        self.configure(bg=self.trans_color)
        self.wm_attributes("-transparentcolor", self.trans_color)

        # Fullscreen overlay centered
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        box_size = 200
        x = (sw - box_size) // 2
        y = (sh - box_size) // 2
        self.geometry(f"{box_size}x{box_size}+{x}+{y}")

        self.canvas = tk.Canvas(self, width=box_size, height=box_size, bg=self.trans_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Make click-through via WinAPI WS_EX_TRANSPARENT | WS_EX_LAYERED
        try:
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            GWL_EXSTYLE = -20
            WS_EX_LAYERED = 0x00080000
            WS_EX_TRANSPARENT = 0x00000020
            styles = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
            ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, styles | WS_EX_LAYERED | WS_EX_TRANSPARENT)
        except Exception:
            pass

class CrosshairOverlayApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🎯 QWSTUR CROSSHAIR OVERLAY // by qwstur")
        self.geometry("640x540")
        self.minsize(580, 500)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.style_var = tk.StringVar(value="Cross")
        self.color_var = tk.StringVar(value="#10b981") # Neon Green
        self.size_var = tk.IntVar(value=14)
        self.thickness_var = tk.IntVar(value=2)
        self.gap_var = tk.IntVar(value=4)
        self.dot_var = tk.BooleanVar(value=True)
        self.is_visible = True

        self.build_ui()
        self.overlay = CrosshairWindow(self)
        self.draw_crosshair()

        self.bind("<F6>", lambda e: self.toggle_visibility())

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

        t_lbl = tk.Label(h_left, text="🎯 QWSTUR CROSSHAIR OVERLAY // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Кастомный прицел поверх всех окон для шутеров (CS2, Rust, Fortnite, DayZ) // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Main Body
        body = tk.Frame(self, bg=BG_DARK, padx=16, pady=12)
        body.pack(fill="both", expand=True)

        # Preview & Toggle Bar
        top_row = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=10)
        top_row.pack(fill="x", pady=(0, 10))

        # Preview canvas
        self.preview_canvas = tk.Canvas(top_row, width=80, height=80, bg="#050508", highlightthickness=1, highlightbackground=BORDER_COLOR)
        self.preview_canvas.pack(side="left", padx=(0, 14))

        prv_info = tk.Frame(top_row, bg=BG_CARD)
        prv_info.pack(side="left", fill="both", expand=True)

        tk.Label(prv_info, text="СТАТУС ОВЕРЛЕЯ:", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w")
        self.status_lbl = tk.Label(prv_info, text="● Оверлей АКТИВЕН (Поверх экрана)", font=("Segoe UI", 10, "bold"), fg=ACCENT_GREEN, bg=BG_CARD)
        self.status_lbl.pack(anchor="w")
        tk.Label(prv_info, text="Хоткей [F6] — скрыть/показать прицел прямо во время игры", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(2, 0))

        self.tog_btn = tk.Button(top_row, text="👁️ Скрыть [F6]", font=("Segoe UI", 8, "bold"),
                                 bg=BG_SURFACE, fg=TEXT_MAIN, activebackground=BG_CARD,
                                 relief="flat", cursor="hand2", padx=12, pady=6,
                                 highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.toggle_visibility)
        self.tog_btn.pack(side="right")

        # Controls Grid
        ctrls = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=12)
        ctrls.pack(fill="both", expand=True)

        # Style Selector
        s_row = tk.Frame(ctrls, bg=BG_CARD)
        s_row.pack(fill="x", pady=4)
        tk.Label(s_row, text="Тип прицела:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD, width=15, anchor="w").pack(side="left")
        for st in ["Cross", "Dot", "Circle", "T-Shape"]:
            rb = tk.Radiobutton(s_row, text=st, variable=self.style_var, value=st, command=self.draw_crosshair,
                                font=("Segoe UI", 8), fg=TEXT_MAIN, bg=BG_CARD, selectcolor=BG_SURFACE, activebackground=BG_CARD)
            rb.pack(side="left", padx=8)

        # Color Selector
        c_row = tk.Frame(ctrls, bg=BG_CARD)
        c_row.pack(fill="x", pady=6)
        tk.Label(c_row, text="Цвет прицела:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD, width=15, anchor="w").pack(side="left")
        colors = [
            ("Неон Зеленый", "#10b981"),
            ("Неон Красный", "#ef4444"),
            ("Неон Циан", "#06b6d4"),
            ("Пурпурный", "#8b5cf6"),
            ("Желтый", "#eab308"),
            ("Белый", "#ffffff")
        ]
        for name, col in colors:
            btn = tk.Button(c_row, text=name, font=("Segoe UI", 7, "bold"), bg=col, fg="#000000" if col in ["#10b981", "#06b6d4", "#eab308", "#ffffff"] else "#ffffff",
                            relief="flat", cursor="hand2", padx=6, pady=2, command=lambda c=col: self.set_color(c))
            btn.pack(side="left", padx=3)

        # Size Slider
        sz_row = tk.Frame(ctrls, bg=BG_CARD)
        sz_row.pack(fill="x", pady=6)
        tk.Label(sz_row, text="Размер лучей:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD, width=15, anchor="w").pack(side="left")
        sz_scale = tk.Scale(sz_row, from_=4, to=40, variable=self.size_var, orient="horizontal", command=lambda v: self.draw_crosshair(),
                            bg=BG_CARD, fg=TEXT_MAIN, highlightthickness=0, troughcolor=BG_SURFACE)
        sz_scale.pack(side="left", fill="x", expand=True)

        # Thickness Slider
        th_row = tk.Frame(ctrls, bg=BG_CARD)
        th_row.pack(fill="x", pady=6)
        tk.Label(th_row, text="Толщина линий:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD, width=15, anchor="w").pack(side="left")
        th_scale = tk.Scale(th_row, from_=1, to=8, variable=self.thickness_var, orient="horizontal", command=lambda v: self.draw_crosshair(),
                            bg=BG_CARD, fg=TEXT_MAIN, highlightthickness=0, troughcolor=BG_SURFACE)
        th_scale.pack(side="left", fill="x", expand=True)

        # Gap Slider
        gp_row = tk.Frame(ctrls, bg=BG_CARD)
        gp_row.pack(fill="x", pady=6)
        tk.Label(gp_row, text="Зазор (Gap):", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD, width=15, anchor="w").pack(side="left")
        gp_scale = tk.Scale(gp_row, from_=0, to=25, variable=self.gap_var, orient="horizontal", command=lambda v: self.draw_crosshair(),
                            bg=BG_CARD, fg=TEXT_MAIN, highlightthickness=0, troughcolor=BG_SURFACE)
        gp_scale.pack(side="left", fill="x", expand=True)

        # Center dot checkbox
        dt_row = tk.Frame(ctrls, bg=BG_CARD)
        dt_row.pack(fill="x", pady=4)
        tk.Checkbutton(dt_row, text="Точка по центру (Center Dot)", variable=self.dot_var, command=self.draw_crosshair,
                       font=("Segoe UI", 8), fg=TEXT_MAIN, bg=BG_CARD, selectcolor=BG_SURFACE, activebackground=BG_CARD).pack(side="left", padx=15)

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=6)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))

        foot_hint = tk.Label(footer, text="Прозрачный фон / Не мешает мыши (Click-through)", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        foot_hint.pack(side="left", padx=16, pady=6)

    def set_color(self, c):
        self.color_var.set(c)
        self.draw_crosshair()

    def draw_crosshair(self):
        # Render on both overlay canvas and preview canvas
        self._render_on_canvas(self.overlay.canvas, 100, 100)
        self._render_on_canvas(self.preview_canvas, 40, 40)

    def _render_on_canvas(self, cv, cx, cy):
        cv.delete("all")

        st = self.style_var.get()
        col = self.color_var.get()
        sz = self.size_var.get()
        th = self.thickness_var.get()
        gap = self.gap_var.get()
        has_dot = self.dot_var.get()

        # Dot
        if has_dot:
            dr = max(1, th // 2 + 1)
            cv.create_oval(cx - dr, cy - dr, cx + dr, cy + dr, fill=col, outline=col)

        if st == "Dot":
            dr = max(2, sz // 3)
            cv.create_oval(cx - dr, cy - dr, cx + dr, cy + dr, fill=col, outline=col)

        elif st == "Cross":
            # Left
            cv.create_line(cx - gap - sz, cy, cx - gap, cy, fill=col, width=th)
            # Right
            cv.create_line(cx + gap, cy, cx + gap + sz, cy, fill=col, width=th)
            # Top
            cv.create_line(cx, cy - gap - sz, cx, cy - gap, fill=col, width=th)
            # Bottom
            cv.create_line(cx, cy + gap, cx, cy + gap + sz, fill=col, width=th)

        elif st == "T-Shape":
            # Left
            cv.create_line(cx - gap - sz, cy, cx - gap, cy, fill=col, width=th)
            # Right
            cv.create_line(cx + gap, cy, cx + gap + sz, cy, fill=col, width=th)
            # Bottom
            cv.create_line(cx, cy + gap, cx, cy + gap + sz, fill=col, width=th)

        elif st == "Circle":
            r = gap + sz // 2
            cv.create_oval(cx - r, cy - r, cx + r, cy + r, outline=col, width=th)

    def toggle_visibility(self):
        self.is_visible = not self.is_visible
        if self.is_visible:
            self.overlay.deiconify()
            self.status_lbl.config(text="● Оверлей АКТИВЕН (Поверх экрана)", fg=ACCENT_GREEN)
            self.tog_btn.config(text="👁️ Скрыть [F6]")
        else:
            self.overlay.withdraw()
            self.status_lbl.config(text="○ Оверлей СКРЫТ", fg=TEXT_MUTED)
            self.tog_btn.config(text="👁️ Показать [F6]")

if __name__ == "__main__":
    app = CrosshairOverlayApp()
    app.mainloop()
