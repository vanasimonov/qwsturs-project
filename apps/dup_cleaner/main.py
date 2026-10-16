"""
==============================================================================
            ⚡ QWSTUR DUPLICATE FILE FINDER // v1.0
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
import hashlib
import threading
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
ACCENT_AMBER = "#f59e0b"
ACCENT_CYAN = "#06b6d4"

class DupCleanerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧹 QWSTUR DUPLICATE FILE FINDER // v1.0 // by qwstur")
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

        self.is_scanning = False
        self.duplicates = {} # hash -> [list of full paths]
        self.file_items = [] # list of (item_id, path, is_duplicate)

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

        t_lbl = tk.Label(h_left, text="🧹 DUPLICATE FILE FINDER // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Двухэтапный скоростной поиск и очистка дубликатов файлов по SHA-256 // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Top Folder Bar
        top_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=10)
        top_bar.pack(fill="x")

        tk.Label(top_bar, text="Папка для сканирования:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_DARK).pack(side="left")
        self.dir_entry = tk.Entry(top_bar, font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                                  relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=8, ipady=3)
        self.dir_entry.insert(0, os.path.expanduser("~\\Downloads"))

        browse_btn = tk.Button(top_bar, text="📁 Обзор...", font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_MAIN,
                               relief="flat", cursor="hand2", padx=10, pady=2,
                               highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.browse_dir)
        browse_btn.pack(side="left", padx=(0, 8))

        self.scan_btn = tk.Button(top_bar, text="⚡ Начать поиск [Enter]", font=("Segoe UI", 9, "bold"),
                                  bg=ACCENT_PURPLE, fg="#ffffff", activebackground="#7c3aed",
                                  relief="flat", cursor="hand2", padx=14, pady=3, command=self.toggle_scan)
        self.scan_btn.pack(side="right")

        # Summary Bar
        self.sum_bar = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=16, pady=8)
        self.sum_bar.pack(fill="x", padx=16, pady=(0, 10))

        self.sum_lbl = tk.Label(self.sum_bar, text="● Нажмите 'Начать поиск' для сканирования папки", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_CARD)
        self.sum_lbl.pack(side="left")

        sel_all_btn = tk.Button(self.sum_bar, text="☑️ Выбрать все копии (кроме оригинала)", font=("Segoe UI", 8),
                                bg=BG_SURFACE, fg=ACCENT_CYAN, relief="flat", cursor="hand2", padx=8, pady=2,
                                command=self.select_all_copies)
        sel_all_btn.pack(side="right")

        # Results Tree
        table_frame = tk.Frame(self, bg=BG_DARK, padx=16)
        table_frame.pack(fill="both", expand=True)

        cols = ("group", "name", "size", "path")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="extended")
        self.tree.heading("group", text="Группа")
        self.tree.heading("name", text="Имя файла")
        self.tree.heading("size", text="Размер")
        self.tree.heading("path", text="Полный путь")

        self.tree.column("group", width=80, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("size", width=100, anchor="center")
        self.tree.column("path", width=420, anchor="w")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=BG_CARD, foreground=TEXT_MAIN, fieldbackground=BG_CARD, rowheight=24, font=("Consolas", 9), borderwidth=0)
        style.configure("Treeview.Heading", background=BG_SURFACE, foreground=TEXT_MUTED, font=("Segoe UI", 8, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", ACCENT_PURPLE)], foreground=[("selected", "#ffffff")])

        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Action bar under tree
        act_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=8)
        act_bar.pack(fill="x")

        del_btn = tk.Button(act_bar, text="🗑️ Удалить выбранные файлы", font=("Segoe UI", 9, "bold"),
                            bg=ACCENT_RED, fg="#ffffff", activebackground="#dc2626", activeforeground="#ffffff",
                            relief="flat", cursor="hand2", padx=14, pady=4, command=self.delete_selected)
        del_btn.pack(side="left")

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

        hint_lbl = tk.Label(footer, text="[Enter] Поиск  |  [Esc] Отмена // by qwstur", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        hint_lbl.pack(side="right", padx=16, pady=6)

    def bind_keys(self):
        self.bind("<Return>", lambda e: self.toggle_scan())
        self.bind("<Escape>", lambda e: self.cancel_scan())

    def browse_dir(self):
        d = filedialog.askdirectory(title="Выберите папку для поиска дубликатов")
        if d:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, d)

    def toggle_scan(self):
        if self.is_scanning:
            self.cancel_scan()
        else:
            self.start_scan()

    def start_scan(self):
        folder = self.dir_entry.get().strip()
        if not os.path.isdir(folder):
            messagebox.showerror("Ошибка", "Выбранная папка не существует!")
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.is_scanning = True
        self.scan_btn.config(text="🛑 Остановить [Esc]", bg=ACCENT_RED, fg="#ffffff")
        self.status_lbl.config(text="⏳ Этап 1: Индексация файлов по размеру...", fg=ACCENT_AMBER)

        threading.Thread(target=self._scan_worker, args=(folder,), daemon=True).start()

    def cancel_scan(self):
        self.is_scanning = False
        self.scan_btn.config(text="⚡ Начать поиск [Enter]", bg=ACCENT_PURPLE, fg="#ffffff")
        self.status_lbl.config(text="🛑 Сканирование прервано", fg=ACCENT_RED)

    def _scan_worker(self, folder):
        size_map = {} # size -> [paths]
        total_files = 0

        # Step 1: Walk & group by size
        for root, dirs, files in os.walk(folder):
            if not self.is_scanning:
                return
            for f in files:
                p = os.path.join(root, f)
                try:
                    s = os.path.getsize(p)
                    if s > 0:
                        size_map.setdefault(s, []).append(p)
                        total_files += 1
                except Exception:
                    pass

        # Step 2: Candidates with same size
        candidates = {s: paths for s, paths in size_map.items() if len(paths) > 1}
        self.after(0, lambda: self.status_lbl.config(text=f"⏳ Этап 2: Вычисление хэшей для {len(candidates)} групп совпадений...", fg=ACCENT_CYAN))

        dups = {} # hash -> [paths]
        group_idx = 1
        wasted_bytes = 0

        for sz, paths in candidates.items():
            if not self.is_scanning:
                return
            sub_hashes = {}
            for p in paths:
                h = self._get_file_hash(p)
                if h:
                    sub_hashes.setdefault(h, []).append(p)

            for h, match_list in sub_hashes.items():
                if len(match_list) > 1:
                    dups[h] = match_list
                    wasted_bytes += sz * (len(match_list) - 1)

        self.duplicates = dups
        self.is_scanning = False
        self.after(0, lambda: self._render_results(dups, wasted_bytes))

    def _get_file_hash(self, path):
        try:
            hasher = hashlib.sha256()
            with open(path, "rb") as f:
                while chunk := f.read(65536):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return None

    def _render_results(self, dups, wasted_bytes):
        self.scan_btn.config(text="⚡ Начать поиск [Enter]", bg=ACCENT_PURPLE, fg="#ffffff")

        wasted_mb = wasted_bytes / (1024**2)
        total_dup_files = sum(len(v) - 1 for v in dups.values())

        group_num = 1
        for h, paths in dups.items():
            try:
                sz_str = f"{os.path.getsize(paths[0]) / 1024:.1f} КБ"
            except Exception:
                sz_str = "Unknown"

            for idx, p in enumerate(paths):
                tag = f"Группа #{group_num}" if idx == 0 else "   ↳ Копия"
                name = os.path.basename(p)
                self.tree.insert("", "end", values=(tag, name, sz_str, p))
            group_num += 1

        self.sum_lbl.config(
            text=f"✓ Найдено дубликатов: {total_dup_files} | Потрачено впустую: {wasted_mb:.1f} МБ",
            fg=ACCENT_GREEN if total_dup_files > 0 else TEXT_MUTED
        )
        self.status_lbl.config(text="● Сканирование завершено", fg=ACCENT_GREEN)

    def select_all_copies(self):
        to_select = []
        for item in self.tree.get_children():
            vals = self.tree.item(item)["values"]
            if vals and "Копия" in str(vals[0]):
                to_select.append(item)
        self.tree.selection_set(to_select)
        self.status_lbl.config(text=f"● Выбрано копий: {len(to_select)}", fg=ACCENT_CYAN)

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("Инфо", "Выберите файлы для удаления")
            return

        paths_to_delete = [self.tree.item(item)["values"][3] for item in sel]
        confirm = messagebox.askyesno("Подтверждение", f"Вы уверены, что хотите удалить {len(paths_to_delete)} выбранных файлов безвозвратно?")
        if not confirm:
            return

        deleted = 0
        for p in paths_to_delete:
            try:
                os.remove(p)
                deleted += 1
            except Exception:
                pass

        for item in sel:
            self.tree.delete(item)

        self.status_lbl.config(text=f"✓ Удалено файлов: {deleted}", fg=ACCENT_GREEN)

if __name__ == "__main__":
    app = DupCleanerApp()
    app.mainloop()
