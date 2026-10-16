"""
==============================================================================
             ⚡ QWSTUR BATCH FILE RENAMER // v1.0
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
from tkinter import ttk, filedialog, messagebox

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

class BatchRenamerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📁 QWSTUR BATCH FILE RENAMER // v1.0 // by qwstur")
        self.geometry("860x620")
        self.minsize(760, 520)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.current_folder = ""
        self.raw_files = []  # list of filenames
        self.preview_map = [] # [(old, new, is_changed, has_error)]

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

        t_lbl = tk.Label(h_left, text="📁 BATCH FILE RENAMER // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Пакетное переименование файлов с живым предпросмотром изменений // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Folder picker bar
        dir_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=10)
        dir_bar.pack(fill="x")

        tk.Label(dir_bar, text="Папка:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_DARK).pack(side="left")
        self.dir_entry = tk.Entry(dir_bar, font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                                  relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=8, ipady=3)
        self.dir_entry.bind("<Return>", lambda e: self.load_folder(self.dir_entry.get().strip()))

        browse_btn = tk.Button(dir_bar, text="📁 Выбрать папку...", font=("Segoe UI", 8, "bold"),
                               bg=ACCENT_PURPLE, fg="#ffffff", activebackground="#7c3aed",
                               relief="flat", cursor="hand2", padx=12, pady=3, command=self.browse_folder)
        browse_btn.pack(side="right")

        # Rules Configuration Card
        rules_card = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=10)
        rules_card.pack(fill="x", padx=16, pady=(0, 10))

        # Row 1: Find & Replace
        r1 = tk.Frame(rules_card, bg=BG_CARD)
        r1.pack(fill="x", pady=2)

        tk.Label(r1, text="Найти:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, width=8, anchor="w").pack(side="left")
        self.find_var = tk.StringVar()
        self.find_var.trace_add("write", lambda *args: self.compute_preview())
        e_find = tk.Entry(r1, textvariable=self.find_var, font=("Segoe UI", 9), bg=BG_SURFACE, fg=TEXT_MAIN,
                          insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR)
        e_find.pack(side="left", fill="x", expand=True, padx=(0, 12), ipady=2)

        tk.Label(r1, text="Заменить на:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, width=12, anchor="w").pack(side="left")
        self.replace_var = tk.StringVar()
        self.replace_var.trace_add("write", lambda *args: self.compute_preview())
        e_replace = tk.Entry(r1, textvariable=self.replace_var, font=("Segoe UI", 9), bg=BG_SURFACE, fg=TEXT_MAIN,
                             insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR)
        e_replace.pack(side="left", fill="x", expand=True, ipady=2)

        # Row 2: Prefix, Suffix, Numbering
        r2 = tk.Frame(rules_card, bg=BG_CARD)
        r2.pack(fill="x", pady=4)

        tk.Label(r2, text="Префикс:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, width=8, anchor="w").pack(side="left")
        self.prefix_var = tk.StringVar()
        self.prefix_var.trace_add("write", lambda *args: self.compute_preview())
        e_prefix = tk.Entry(r2, textvariable=self.prefix_var, font=("Segoe UI", 9), bg=BG_SURFACE, fg=TEXT_MAIN,
                            insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR)
        e_prefix.pack(side="left", fill="x", expand=True, padx=(0, 12), ipady=2)

        tk.Label(r2, text="Суффикс:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, width=12, anchor="w").pack(side="left")
        self.suffix_var = tk.StringVar()
        self.suffix_var.trace_add("write", lambda *args: self.compute_preview())
        e_suffix = tk.Entry(r2, textvariable=self.suffix_var, font=("Segoe UI", 9), bg=BG_SURFACE, fg=TEXT_MAIN,
                            insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR)
        e_suffix.pack(side="left", fill="x", expand=True, ipady=2)

        # Row 3: Options (Numbering, Case, Extension)
        r3 = tk.Frame(rules_card, bg=BG_CARD)
        r3.pack(fill="x", pady=(4, 0))

        self.num_var = tk.BooleanVar(value=False)
        cb_num = tk.Checkbutton(r3, text="Нумерация (001, 002...)", variable=self.num_var,
                                font=("Segoe UI", 8), fg=TEXT_MAIN, bg=BG_CARD, selectcolor=BG_SURFACE,
                                activebackground=BG_CARD, activeforeground=TEXT_MAIN, command=self.compute_preview)
        cb_num.pack(side="left", padx=(0, 16))

        tk.Label(r3, text="Регистр:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD).pack(side="left")
        self.case_var = tk.StringVar(value="none")
        for val, label in (("none", "Без изменений"), ("lower", "нижний"), ("upper", "ВЕРХНИЙ"), ("title", "С Заглавной")):
            rb = tk.Radiobutton(r3, text=label, variable=self.case_var, value=val,
                                font=("Segoe UI", 8), fg=TEXT_MAIN, bg=BG_CARD, selectcolor=BG_SURFACE,
                                activebackground=BG_CARD, activeforeground=TEXT_MAIN, command=self.compute_preview)
            rb.pack(side="left", padx=4)

        # Preview Table
        table_frame = tk.Frame(self, bg=BG_DARK, padx=16)
        table_frame.pack(fill="both", expand=True)

        cols = ("old", "new", "status")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("old", text="Исходное имя")
        self.tree.heading("new", text="Новое имя (Предпросмотр)")
        self.tree.heading("status", text="Статус")

        self.tree.column("old", width=340, anchor="w")
        self.tree.column("new", width=340, anchor="w")
        self.tree.column("status", width=120, anchor="center")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=BG_CARD, foreground=TEXT_MAIN, fieldbackground=BG_CARD, rowheight=24, font=("Consolas", 9), borderwidth=0)
        style.configure("Treeview.Heading", background=BG_SURFACE, foreground=TEXT_MUTED, font=("Segoe UI", 8, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", ACCENT_PURPLE)], foreground=[("selected", "#ffffff")])

        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Action bar
        act_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=8)
        act_bar.pack(fill="x")

        apply_btn = tk.Button(act_bar, text="⚡ Применить переименование [Enter]", font=("Segoe UI", 9, "bold"),
                              bg=ACCENT_GREEN, fg="#000000", activebackground="#059669", activeforeground="#ffffff",
                              relief="flat", cursor="hand2", padx=16, pady=5, command=self.apply_rename)
        apply_btn.pack(side="left")

        reset_btn = tk.Button(act_bar, text="🔄 Сбросить правила [Esc]", font=("Segoe UI", 8),
                              bg=BG_CARD, fg=TEXT_MUTED, activebackground=BG_SURFACE, relief="flat", cursor="hand2",
                              padx=12, pady=5, highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.reset_rules)
        reset_btn.pack(side="right")

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        self.status_lbl = tk.Label(footer, text="● Выберите папку для начала // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        self.status_lbl.pack(side="left", padx=16, pady=6)

        hint_lbl = tk.Label(footer, text="[Enter] Применить  |  [Esc] Сброс // by qwstur", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        hint_lbl.pack(side="right", padx=16, pady=6)

    def bind_keys(self):
        self.bind("<Return>", lambda e: self.apply_rename())
        self.bind("<Escape>", lambda e: self.reset_rules())

    def browse_folder(self):
        d = filedialog.askdirectory(title="Выберите папку с файлами")
        if d:
            self.load_folder(d)

    def load_folder(self, folder_path):
        if not os.path.isdir(folder_path):
            self.status_lbl.config(text="✗ Папка не существует", fg=ACCENT_RED)
            return

        self.current_folder = folder_path
        self.dir_entry.delete(0, tk.END)
        self.dir_entry.insert(0, folder_path)

        try:
            files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
            files.sort()
            self.raw_files = files
            self.compute_preview()
            self.status_lbl.config(text=f"● Загружено файлов: {len(files)}", fg=ACCENT_GREEN)
        except Exception as e:
            self.status_lbl.config(text=f"✗ Ошибка чтения папки: {e}", fg=ACCENT_RED)

    def compute_preview(self):
        find_str = self.find_var.get()
        replace_str = self.replace_var.get()
        prefix = self.prefix_var.get()
        suffix = self.suffix_var.get()
        is_num = self.num_var.get()
        case_mode = self.case_var.get()

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.preview_map = []
        new_names_set = set()
        changed_count = 0

        for idx, orig in enumerate(self.raw_files, start=1):
            name, ext = os.path.splitext(orig)

            # 1. Find & Replace
            if find_str:
                name = name.replace(find_str, replace_str)

            # 2. Case convert
            if case_mode == "lower":
                name = name.lower()
            elif case_mode == "upper":
                name = name.upper()
            elif case_mode == "title":
                name = name.title()

            # 3. Numbering
            if is_num:
                name = f"{name}_{idx:03d}"

            # 4. Prefix & Suffix
            if prefix:
                name = f"{prefix}{name}"
            if suffix:
                name = f"{name}{suffix}"

            new_full = name + ext
            is_changed = (orig != new_full)
            has_error = False
            status_text = "Без изменений"

            if is_changed:
                changed_count += 1
                status_text = "Изменится"

            if new_full in new_names_set:
                status_text = "⚠️ Конфликт имен!"
                has_error = True
            new_names_set.add(new_full)

            self.preview_map.append((orig, new_full, is_changed, has_error))
            self.tree.insert("", "end", values=(orig, new_full, status_text))

        if self.raw_files:
            self.status_lbl.config(text=f"● Файлов: {len(self.raw_files)} | Изменятся: {changed_count}", fg=ACCENT_GREEN)

    def apply_rename(self):
        if not self.current_folder or not self.preview_map:
            self.status_lbl.config(text="⚠️ Нет файлов для переименования", fg=ACCENT_CYAN)
            return

        to_rename = [item for item in self.preview_map if item[2]]
        if not to_rename:
            self.status_lbl.config(text="● Имена файлов не изменились", fg=ACCENT_GREEN)
            return

        # Check for errors
        if any(item[3] for item in self.preview_map):
            messagebox.showerror("Ошибка", "Обнаружены конфликты одинаковых имен файлов! Измените правила.")
            return

        success_count = 0
        error_count = 0

        for old_name, new_name, is_changed, _ in to_rename:
            old_path = os.path.join(self.current_folder, old_name)
            new_path = os.path.join(self.current_folder, new_name)
            try:
                os.rename(old_path, new_path)
                success_count += 1
            except Exception:
                error_count += 1

        self.reset_rules()
        self.load_folder(self.current_folder)
        self.status_lbl.config(text=f"✓ Успешно переименовано: {success_count} (Ошибок: {error_count})", fg=ACCENT_GREEN)

    def reset_rules(self):
        self.find_var.set("")
        self.replace_var.set("")
        self.prefix_var.set("")
        self.suffix_var.set("")
        self.num_var.set(False)
        self.case_var.set("none")
        self.compute_preview()

if __name__ == "__main__":
    app = BatchRenamerApp()
    app.mainloop()
