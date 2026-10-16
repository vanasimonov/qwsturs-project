"""
==============================================================================
            ⚡ QWSTUR SECURE PASS & TOKEN GENERATOR // v1.0
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
import math
import string
import secrets
import uuid
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

class PassGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔑 QWSTUR SECURE PASS & TOKEN GENERATOR // v1.0 // by qwstur")
        self.geometry("740x580")
        self.minsize(680, 520)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.build_ui()
        self.bind_keys()
        self.generate()

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

        t_lbl = tk.Label(h_left, text="🔑 SECURE PASS & TOKEN GENERATOR // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Криптографический генератор паролей, API-токенов, UUID и PIN на базе модуля secrets // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Result Display Box (Big)
        res_card = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=16, pady=14)
        res_card.pack(fill="x", padx=16, pady=12)

        self.res_entry = tk.Entry(res_card, font=("Consolas", 14, "bold"), bg=BG_SURFACE, fg=ACCENT_CYAN,
                                  insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1,
                                  highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        self.res_entry.pack(fill="x", ipady=6)

        # Strength Bar & Metrics
        st_row = tk.Frame(res_card, bg=BG_CARD)
        st_row.pack(fill="x", pady=(8, 0))

        self.entropy_lbl = tk.Label(st_row, text="Энтропия: 0 бит", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD)
        self.entropy_lbl.pack(side="left")

        self.strength_badge = tk.Label(st_row, text="● Надежный", font=("Segoe UI", 8, "bold"),
                                       bg=BG_SURFACE, fg=ACCENT_GREEN, padx=8, pady=2)
        self.strength_badge.pack(side="right")

        # Action Buttons for Result
        act_row = tk.Frame(res_card, bg=BG_CARD)
        act_row.pack(fill="x", pady=(10, 0))

        gen_btn = tk.Button(act_row, text="⚡ Сгенерировать новый [Enter]", font=("Segoe UI", 9, "bold"),
                            bg=ACCENT_PURPLE, fg="#ffffff", activebackground="#7c3aed",
                            relief="flat", cursor="hand2", padx=14, pady=5, command=self.generate)
        gen_btn.pack(side="left")

        copy_btn = tk.Button(act_row, text="📋 Скопировать в буфер [Ctrl+C]", font=("Segoe UI", 9, "bold"),
                             bg=BG_SURFACE, fg=TEXT_MAIN, activebackground=BG_DARK,
                             relief="flat", cursor="hand2", padx=14, pady=5,
                             highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.copy_result)
        copy_btn.pack(side="left", padx=8)

        # Options Card
        opt_card = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=16, pady=12)
        opt_card.pack(fill="x", padx=16, pady=(0, 10))

        # Mode selector
        tk.Label(opt_card, text="Тип генерации:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w", pady=(0, 4))
        self.type_var = tk.StringVar(value="password")
        type_row = tk.Frame(opt_card, bg=BG_CARD)
        type_row.pack(fill="x", pady=(0, 8))

        modes = [
            ("password", "Пароль"),
            ("token_hex", "Hex Токен"),
            ("token_url", "URL Safe Token"),
            ("uuid4", "UUID v4"),
            ("pin", "PIN-код")
        ]
        for val, title in modes:
            rb = tk.Radiobutton(type_row, text=title, variable=self.type_var, value=val,
                                font=("Segoe UI", 8, "bold"), fg=TEXT_MAIN, bg=BG_CARD, selectcolor=BG_SURFACE,
                                activebackground=BG_CARD, activeforeground=TEXT_MAIN, command=self.generate)
            rb.pack(side="left", padx=(0, 12))

        # Length Slider
        len_row = tk.Frame(opt_card, bg=BG_CARD)
        len_row.pack(fill="x", pady=4)

        tk.Label(len_row, text="Длина символов:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, width=14, anchor="w").pack(side="left")
        self.len_var = tk.IntVar(value=20)
        self.len_scale = ttk.Scale(len_row, from_=6, to=64, variable=self.len_var, orient="horizontal", command=lambda v: self.on_len_change())
        self.len_scale.pack(side="left", fill="x", expand=True, padx=8)

        self.len_val_lbl = tk.Label(len_row, text="20", font=("Consolas", 10, "bold"), fg=ACCENT_CYAN, bg=BG_CARD, width=4)
        self.len_val_lbl.pack(side="left")

        # Checkboxes for charset
        cb_row = tk.Frame(opt_card, bg=BG_CARD)
        cb_row.pack(fill="x", pady=(6, 0))

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.no_ambig = tk.BooleanVar(value=False)

        cbs = [
            ("A-Z (Заглавные)", self.use_upper),
            ("a-z (Строчные)", self.use_lower),
            ("0-9 (Цифры)", self.use_digits),
            ("!@#$ (Символы)", self.use_symbols),
            ("Без похожих (0, O, l, 1)", self.no_ambig)
        ]
        for title, var in cbs:
            cb = tk.Checkbutton(cb_row, text=title, variable=var,
                                font=("Segoe UI", 8), fg=TEXT_MAIN, bg=BG_CARD, selectcolor=BG_SURFACE,
                                activebackground=BG_CARD, activeforeground=TEXT_MAIN, command=self.generate)
            cb.pack(side="left", padx=(0, 10))

        # Batch Generator Frame
        batch_card = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=16, pady=10)
        batch_card.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        b_top = tk.Frame(batch_card, bg=BG_CARD)
        b_top.pack(fill="x", pady=(0, 6))

        tk.Label(b_top, text="Пакетная генерация (список паролей):", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD).pack(side="left")

        b5_btn = tk.Button(b_top, text="+5 шт // by qwstur", font=("Segoe UI", 8), bg=BG_SURFACE, fg=TEXT_MAIN,
                          relief="flat", cursor="hand2", padx=8, pady=1, command=lambda: self.generate_batch(5))
        b5_btn.pack(side="left", padx=(10, 4))

        b10_btn = tk.Button(b_top, text="+10 шт // by qwstur", font=("Segoe UI", 8), bg=BG_SURFACE, fg=TEXT_MAIN,
                           relief="flat", cursor="hand2", padx=8, pady=1, command=lambda: self.generate_batch(10))
        b10_btn.pack(side="left", padx=4)

        copy_all_btn = tk.Button(b_top, text="📋 Скопировать весь список", font=("Segoe UI", 8),
                                 bg=BG_SURFACE, fg=ACCENT_CYAN, relief="flat", cursor="hand2", padx=8, pady=1,
                                 command=self.copy_batch)
        copy_all_btn.pack(side="right")

        self.batch_text = tk.Text(batch_card, height=4, font=("Consolas", 9), bg=BG_SURFACE, fg=TEXT_MAIN,
                                  insertbackground=TEXT_MAIN, relief="flat", padx=8, pady=6)
        self.batch_text.pack(fill="both", expand=True)

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        self.status_lbl = tk.Label(footer, text="● Готов // by qwstur", font=("Segoe UI", 8), fg=ACCENT_GREEN, bg=BG_SURFACE)
        self.status_lbl.pack(side="left", padx=16, pady=6)

        hint_lbl = tk.Label(footer, text="[Enter / Space] Сгенерировать  |  [Ctrl+C] Копировать // by qwstur", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        hint_lbl.pack(side="right", padx=16, pady=6)

    def bind_keys(self):
        self.bind("<Return>", lambda e: self.generate())
        self.bind("<space>", lambda e: self.generate() if self.focus_get() != self.res_entry and self.focus_get() != self.batch_text else None)
        self.bind("<Control-c>", lambda e: self.copy_result())

    def on_len_change(self):
        v = self.len_var.get()
        self.len_val_lbl.config(text=str(v))
        self.generate()

    def generate(self):
        mode = self.type_var.get()
        length = self.len_var.get()

        if mode == "uuid4":
            result = str(uuid.uuid4())
            entropy = 122
        elif mode == "token_hex":
            result = secrets.token_hex(length // 2)
            entropy = (length // 2) * 8
        elif mode == "token_url":
            result = secrets.token_urlsafe(length)[:length]
            entropy = length * 6
        elif mode == "pin":
            result = "".join(secrets.choice(string.digits) for _ in range(length))
            entropy = length * 3.32
        else: # password
            charset = ""
            if self.use_upper.get():
                charset += string.ascii_uppercase
            if self.use_lower.get():
                charset += string.ascii_lowercase
            if self.use_digits.get():
                charset += string.digits
            if self.use_symbols.get():
                charset += "!@#$%^&*()-_=+[]{}<>:?"

            if self.no_ambig.get():
                for ch in "0O1lI":
                    charset = charset.replace(ch, "")

            if not charset:
                charset = string.ascii_letters + string.digits

            result = "".join(secrets.choice(charset) for _ in range(length))
            entropy = length * math.log2(len(charset))

        self.res_entry.delete(0, tk.END)
        self.res_entry.insert(0, result)

        # Update Entropy and Badge
        self.entropy_lbl.config(text=f"Энтропия: {entropy:.1f} бит | Длина: {len(result)} симв.")
        if entropy < 40:
            self.strength_badge.config(text="● Слабый // by qwstur", fg=ACCENT_RED, bg=BG_SURFACE)
        elif entropy < 65:
            self.strength_badge.config(text="● Средний // by qwstur", fg=ACCENT_AMBER, bg=BG_SURFACE)
        elif entropy < 90:
            self.strength_badge.config(text="● Высокий // by qwstur", fg=ACCENT_GREEN, bg=BG_SURFACE)
        else:
            self.strength_badge.config(text="● Максимальный (Crypto Grade) // by qwstur", fg=ACCENT_CYAN, bg=BG_SURFACE)

        self.status_lbl.config(text="✓ Новый пароль сгенерирован", fg=ACCENT_GREEN)

    def generate_batch(self, count):
        items = []
        old_val = self.res_entry.get()
        for _ in range(count):
            self.generate()
            items.append(self.res_entry.get())
        self.res_entry.delete(0, tk.END)
        self.res_entry.insert(0, old_val)

        self.batch_text.delete("1.0", tk.END)
        self.batch_text.insert("1.0", "\n".join(items))
        self.status_lbl.config(text=f"✓ Сгенерирован список из {count} элементов", fg=ACCENT_GREEN)

    def copy_result(self):
        txt = self.res_entry.get()
        if txt:
            self.clipboard_clear()
            self.clipboard_append(txt)
            self.show_toast("✓ Скопировано в буфер обмена!")

    def copy_batch(self):
        txt = self.batch_text.get("1.0", tk.END).strip()
        if txt:
            self.clipboard_clear()
            self.clipboard_append(txt)
            self.show_toast("✓ Весь список скопирован в буфер!")

    def show_toast(self, text):
        self.status_lbl.config(text=text, fg=ACCENT_GREEN)

if __name__ == "__main__":
    app = PassGeneratorApp()
    app.mainloop()
