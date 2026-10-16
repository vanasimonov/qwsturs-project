"""
==============================================================================
                 📋 QWSTUR CLIPSTACK // v1.0
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
import threading
import time
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
ACCENT_CYAN = "#06b6d4"

class ClipstackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📋 QWSTUR CLIPSTACK // v1.0 // by qwstur")
        self.geometry("820x580")
        self.minsize(740, 480)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.history = []  # List of dicts: {"time": "12:00:00", "text": "...", "len": 12}
        self.last_clip = ""
        self.is_monitoring = True

        self.build_ui()
        self.bind_keys()
        self.start_clipboard_listener()

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

        t_lbl = tk.Label(h_left, text="📋 QWSTUR CLIPSTACK // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Менеджер истории буфера обмена с мгновенным поиском // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        clear_btn = tk.Button(header, text="🗑️ Очистить всю историю", font=("Segoe UI", 8),
                              bg=BG_CARD, fg=TEXT_MUTED, activebackground=ACCENT_RED, activeforeground="#ffffff",
                              relief="flat", cursor="hand2", padx=10, pady=4,
                              highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.clear_all)
        clear_btn.pack(side="right", padx=16)

        # Search Bar
        search_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=10)
        search_bar.pack(fill="x")

        tk.Label(search_bar, text="🔍 Поиск по истории:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_DARK).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.render_history())
        self.search_entry = tk.Entry(search_bar, textvariable=self.search_var, font=("Segoe UI", 9),
                                     bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat",
                                     highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(10, 0), ipady=3)
        self.search_entry.focus_set()

        # Split pane (Left list, Right preview)
        panes = tk.Frame(self, bg=BG_DARK, padx=16)
        panes.pack(fill="both", expand=True)

        left_frame = tk.Frame(panes, bg=BG_DARK, width=380)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        cols = ("time", "snippet", "len")
        self.tree = ttk.Treeview(left_frame, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("time", text="Время")
        self.tree.heading("snippet", text="Текст буфера")
        self.tree.heading("len", text="Симв.")

        self.tree.column("time", width=80, anchor="center")
        self.tree.column("snippet", width=220, anchor="w")
        self.tree.column("len", width=60, anchor="center")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=BG_CARD, foreground=TEXT_MAIN, fieldbackground=BG_CARD, rowheight=26, font=("Consolas", 9), borderwidth=0)
        style.configure("Treeview.Heading", background=BG_SURFACE, foreground=TEXT_MUTED, font=("Segoe UI", 8, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", ACCENT_PURPLE)], foreground=[("selected", "#ffffff")])

        tree_scroll = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")
        self.tree.bind("<<TreeviewSelect>>", self.on_select_item)

        # Right Preview Frame
        right_frame = tk.Frame(panes, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR)
        right_frame.pack(side="right", fill="both", expand=True, padx=(8, 0))

        preview_header = tk.Frame(right_frame, bg=BG_SURFACE, height=36, highlightthickness=1, highlightbackground=BORDER_COLOR)
        preview_header.pack(fill="x", side="top")
        preview_header.pack_propagate(False)

        tk.Label(preview_header, text="Предпросмотр фрагмента // by qwstur", font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_SURFACE).pack(side="left", padx=10, pady=8)

        self.copy_btn = tk.Button(preview_header, text="📋 Копировать [Enter]", font=("Segoe UI", 8, "bold"),
                                  bg=ACCENT_PURPLE, fg="#ffffff", activebackground="#7c3aed",
                                  relief="flat", cursor="hand2", padx=10, pady=2, command=self.copy_selected)
        self.copy_btn.pack(side="right", padx=10)

        self.preview_text = tk.Text(right_frame, bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                                    font=("Consolas", 10), wrap="word", relief="flat", padx=10, pady=10)
        self.preview_text.pack(fill="both", expand=True)

        # Action bar under list
        bot_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=8)
        bot_bar.pack(fill="x")

        del_btn = tk.Button(bot_bar, text="❌ Удалить выбранное [Del]", font=("Segoe UI", 8),
                            bg=BG_CARD, fg=TEXT_MUTED, activebackground=BG_SURFACE, relief="flat", cursor="hand2",
                            padx=10, pady=3, highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.delete_selected)
        del_btn.pack(side="left")

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        self.status_lbl = tk.Label(footer, text="● Мониторинг буфера активен // by qwstur", font=("Segoe UI", 8), fg=ACCENT_GREEN, bg=BG_SURFACE)
        self.status_lbl.pack(side="left", padx=16, pady=6)

        info_lbl = tk.Label(footer, text="[Enter] Копировать  |  [Esc] Сброс поиска  |  [Del] Удалить // by qwstur", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        info_lbl.pack(side="right", padx=16, pady=6)

    def bind_keys(self):
        self.bind("<Return>", lambda e: self.copy_selected())
        self.bind("<Escape>", lambda e: self.on_escape())
        self.bind("<Delete>", lambda e: self.delete_selected())

    def on_escape(self):
        self.search_var.set("")
        self.show_toast("● Поиск очищен", ACCENT_GREEN)

    def show_toast(self, text, color=ACCENT_GREEN):
        self.status_lbl.config(text=text, fg=color)
        self.after(2500, lambda: self.status_lbl.config(text="● Мониторинг буфера активен", fg=ACCENT_GREEN))

    def start_clipboard_listener(self):
        self._poll_clipboard()

    def _poll_clipboard(self):
        if not self.is_monitoring:
            return
        try:
            clip = self.clipboard_get()
            if clip and clip != self.last_clip:
                self.last_clip = clip
                t_now = time.strftime("%H:%M:%S")
                snippet = clip.strip().replace("\n", " ")
                if len(snippet) > 60:
                    snippet = snippet[:57] + "..."
                item = {
                    "time": t_now,
                    "text": clip,
                    "snippet": snippet,
                    "len": len(clip)
                }
                # Prepend, keep max 100
                self.history.insert(0, item)
                if len(self.history) > 100:
                    self.history.pop()
                self.render_history()
        except Exception:
            pass
        if self.is_monitoring:
            try:
                self._after_id = self.after(500, self._poll_clipboard)
            except Exception:
                pass

    def destroy(self):
        self.is_monitoring = False
        if hasattr(self, '_after_id'):
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
        super().destroy()

    def render_history(self):
        q = self.search_var.get().strip().lower()
        sel = self.tree.selection()
        current_idx = self.tree.index(sel[0]) if sel else -1

        for item in self.tree.get_children():
            self.tree.delete(item)

        for idx, entry in enumerate(self.history):
            if not q or (q in entry["text"].lower()):
                self.tree.insert("", "end", iid=str(idx), values=(entry["time"], entry["snippet"], entry["len"]))

        # Restore selection if possible
        if self.tree.get_children():
            to_select = self.tree.get_children()[0]
            self.tree.selection_set(to_select)
            self.on_select_item(None)

    def on_select_item(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        if idx < len(self.history):
            txt = self.history[idx]["text"]
            self.preview_text.delete("1.0", tk.END)
            self.preview_text.insert("1.0", txt)

    def copy_selected(self):
        sel = self.tree.selection()
        if not sel:
            self.show_toast("⚠️ Выберите элемент для копирования", ACCENT_CYAN)
            return
        idx = int(sel[0])
        if idx < len(self.history):
            txt = self.history[idx]["text"]
            self.clipboard_clear()
            self.clipboard_append(txt)
            self.last_clip = txt
            self.show_toast("✓ Скопировано в буфер обмена!", ACCENT_GREEN)

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            return
        idx = int(sel[0])
        if idx < len(self.history):
            self.history.pop(idx)
            self.preview_text.delete("1.0", tk.END)
            self.render_history()
            self.show_toast("🗑️ Запись удалена", ACCENT_MUTED)

    def clear_all(self):
        if not self.history:
            return
        self.history.clear()
        self.preview_text.delete("1.0", tk.END)
        self.render_history()
        self.show_toast("🗑️ Вся история очищена", ACCENT_MUTED)

if __name__ == "__main__":
    app = ClipstackApp()
    app.mainloop()
