"""
==============================================================================
       🖱️ QWSTUR SENSITIVITY & DPI CONVERTER // by qwstur
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
ACCENT_CYAN = "#06b6d4"
ACCENT_AMBER = "#f59e0b"

# Game yaw coefficients relative to Source / CS2 (yaw = 0.022)
GAMES = {
    "Counter-Strike 2 / Source": {"yaw": 0.022, "ratio": 1.0},
    "Valorant": {"yaw": 0.07, "ratio": 0.022 / 0.07}, # ~0.314285
    "Apex Legends": {"yaw": 0.022, "ratio": 1.0},
    "Overwatch 2": {"yaw": 0.0066, "ratio": 0.022 / 0.0066}, # ~3.3333
    "Rust": {"yaw": 0.11, "ratio": 0.022 / 0.11}, # 0.2
    "Fortnite (X/Y)": {"yaw": 0.00555, "ratio": 0.022 / 0.00555}, # ~3.96
    "Rainbow Six Siege": {"yaw": 0.00572, "ratio": 0.022 / 0.00572},
    "Roblox": {"yaw": 0.0785, "ratio": 0.022 / 0.0785}
}

class SensConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🖱️ QWSTUR SENSITIVITY & DPI CONVERTER // by qwstur")
        self.geometry("760x540")
        self.minsize(700, 480)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.from_game_var = tk.StringVar(value="Counter-Strike 2 / Source")
        self.sens_var = tk.StringVar(value="1.5")
        self.dpi_var = tk.StringVar(value="800")

        self.result_labels = {}
        self.build_ui()
        self.recalculate()

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

        t_lbl = tk.Label(h_left, text="🖱️ SENSITIVITY & DPI CONVERTER // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Точный конвертер чувствительности мыши, eDPI и см/360° между всеми играми // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Top Input Card
        top_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=10)
        top_bar.pack(fill="x")

        in_card = tk.Frame(top_bar, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=16, pady=12)
        in_card.pack(fill="x")

        grid_box = tk.Frame(in_card, bg=BG_CARD)
        grid_box.pack(fill="x")

        # From Game
        c1 = tk.Frame(grid_box, bg=BG_CARD)
        c1.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(c1, text="Исходная игра:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w")
        game_cb = ttk.Combobox(c1, textvariable=self.from_game_var, values=list(GAMES.keys()), state="readonly", font=("Segoe UI", 9))
        game_cb.pack(fill="x", pady=(4, 0))
        game_cb.bind("<<ComboboxSelected>>", lambda e: self.recalculate())

        # Sensitivity Value
        c2 = tk.Frame(grid_box, bg=BG_CARD)
        c2.pack(side="left", fill="x", expand=True, padx=10)
        tk.Label(c2, text="Чувствительность (Sens):", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w")
        sens_entry = tk.Entry(c2, textvariable=self.sens_var, font=("Segoe UI", 9), bg=BG_SURFACE, fg=ACCENT_CYAN,
                              relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        sens_entry.pack(fill="x", pady=(4, 0), ipady=3)
        sens_entry.bind("<KeyRelease>", lambda e: self.recalculate())

        # Mouse DPI
        c3 = tk.Frame(grid_box, bg=BG_CARD)
        c3.pack(side="left", fill="x", expand=True, padx=(10, 0))
        tk.Label(c3, text="DPI Мыши:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w")
        dpi_entry = tk.Entry(c3, textvariable=self.dpi_var, font=("Segoe UI", 9), bg=BG_SURFACE, fg=ACCENT_GREEN,
                             relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        dpi_entry.pack(fill="x", pady=(4, 0), ipady=3)
        dpi_entry.bind("<KeyRelease>", lambda e: self.recalculate())

        # Physics Metrics Summary Card
        m_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=2)
        m_bar.pack(fill="x")

        m_card = tk.Frame(m_bar, bg=BG_SURFACE, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=8)
        m_card.pack(fill="x")

        self.edpi_lbl = tk.Label(m_card, text="eDPI: 1200", font=("Consolas", 10, "bold"), fg=ACCENT_GREEN, bg=BG_SURFACE)
        self.edpi_lbl.pack(side="left", padx=10)

        self.cm360_lbl = tk.Label(m_card, text="Разворот на 360°: 34.6 см", font=("Consolas", 10, "bold"), fg=ACCENT_CYAN, bg=BG_SURFACE)
        self.cm360_lbl.pack(side="left", padx=20)

        self.speed_tier_lbl = tk.Label(m_card, text="Стиль: Сбалансированный / Средний", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_SURFACE)
        self.speed_tier_lbl.pack(side="right", padx=10)

        # Converted Games List
        body = tk.Frame(self, bg=BG_DARK, padx=16, pady=8)
        body.pack(fill="both", expand=True)

        list_card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=10)
        list_card.pack(fill="both", expand=True)

        tk.Label(list_card, text="КОНВЕРТИРОВАННАЯ ЧУВСТВИТЕЛЬНОСТЬ ДЛЯ ДРУГИХ ИГР:", font=("Consolas", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD).pack(anchor="w", pady=(0, 6))

        # Rows container
        for game_name in GAMES.keys():
            row = tk.Frame(list_card, bg=BG_SURFACE, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=10, pady=5)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=game_name, font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE, width=28, anchor="w").pack(side="left")

            val_lbl = tk.Label(row, text="--", font=("Consolas", 10, "bold"), fg=ACCENT_PURPLE, bg=BG_SURFACE, width=14, anchor="w")
            val_lbl.pack(side="left", padx=10)
            self.result_labels[game_name] = val_lbl

            copy_btn = tk.Button(row, text="📋 Скопировать", font=("Segoe UI", 7), bg=BG_CARD, fg=TEXT_MUTED,
                                 activebackground=BG_DARK, relief="flat", cursor="hand2", padx=8, pady=2,
                                 command=lambda gn=game_name: self.copy_sens(gn))
            copy_btn.pack(side="right")

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=6)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))

        foot_hint = tk.Label(footer, text="Математически точный расчет угловой скорости (Yaw)", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        foot_hint.pack(side="left", padx=16, pady=6)

    def recalculate(self):
        try:
            cur_game = self.from_game_var.get()
            sens = float(self.sens_var.get().replace(",", "."))
            dpi = float(self.dpi_var.get().replace(",", "."))
            if sens <= 0 or dpi <= 0:
                return

            # Convert current game sens to base Source sens
            source_sens = sens / GAMES[cur_game]["ratio"]

            # Calculate cm/360: (360 * 2.54) / (dpi * source_sens * 0.022)
            cm_360 = (360 * 2.54) / (dpi * source_sens * 0.022)
            edpi = dpi * sens

            self.edpi_lbl.config(text=f"eDPI: {edpi:.0f}")
            self.cm360_lbl.config(text=f"Разворот на 360°: {cm_360:.1f} см")

            if cm_360 > 45:
                tier = "Очень низкая (Low Sens) / Идеально для тактических шутеров"
            elif cm_360 > 28:
                tier = "Сбалансированная (Medium Sens) / Золотой стандарт"
            else:
                tier = "Высокая (High Sens) / Быстрые развороты"
            self.speed_tier_lbl.config(text=f"Стиль: {tier}")

            for game_name, data in GAMES.items():
                target_sens = source_sens * data["ratio"]
                self.result_labels[game_name].config(text=f"{target_sens:.4f}")

        except Exception:
            pass

    def copy_sens(self, game_name):
        val = self.result_labels[game_name].cget("text")
        self.clipboard_clear()
        self.clipboard_append(val)
        messagebox.showinfo("Скопировано", f"Чувствительность для {game_name} ({val}) скопирована в буфер обмена!")

if __name__ == "__main__":
    app = SensConverterApp()
    app.mainloop()
