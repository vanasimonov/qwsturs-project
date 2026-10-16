"""
==============================================================================
            ⚡ QWSTUR AUTOSTART & STARTUP MANAGER // v1.0
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
import winreg
import subprocess
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

class AutostartManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🚀 QWSTUR AUTOSTART MANAGER // v1.0 // by qwstur")
        self.geometry("860x600")
        self.minsize(760, 500)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.startup_items = []

        self.build_ui()
        self.bind_keys()
        self.load_autostart_entries()

    def build_ui(self):
        # Header
        header = tk.Frame(self, bg=BG_SURFACE, height=60, highlightthickness=1, highlightbackground=BORDER_COLOR)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        owner_btn = tk.Button(header, text="💬 Написать владельцу", font=("Segoe UI", 8, "bold"),
                              bg=ACCENT_PURPLE, fg="#ffffff", activebackground="#7c3aed", activeforeground="#ffffff",
                              relief="flat", cursor="hand2", padx=10, pady=3,
                              command=lambda: webbrowser.open("https://t.me/AimBoGAttack"))
        owner_btn.pack(side="right", padx=(6, 16))

        ref_btn = tk.Button(header, text="🔄 Обновить [F5]", font=("Segoe UI", 8),
                            bg=BG_CARD, fg=TEXT_MAIN, activebackground=BG_SURFACE,
                            relief="flat", cursor="hand2", padx=10, pady=3,
                            highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.load_autostart_entries)
        ref_btn.pack(side="right", padx=(0, 6))

        h_left = tk.Frame(header, bg=BG_SURFACE)
        h_left.pack(side="left", padx=16, pady=8)

        t_lbl = tk.Label(h_left, text="🚀 AUTOSTART & STARTUP MANAGER // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Анализ и оптимизация программ автозагрузки Windows для ускорения старта ПК // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Search Bar
        search_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=10)
        search_bar.pack(fill="x")

        tk.Label(search_bar, text="Фильтр:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_DARK).pack(side="left")
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *args: self.apply_filter())
        self.filter_entry = tk.Entry(search_bar, textvariable=self.filter_var, font=("Segoe UI", 9),
                                     bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat",
                                     highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        self.filter_entry.pack(side="left", fill="x", expand=True, padx=(10, 0), ipady=3)

        # Table
        table_frame = tk.Frame(self, bg=BG_DARK, padx=16)
        table_frame.pack(fill="both", expand=True)

        cols = ("name", "source", "command")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")
        self.tree.heading("name", text="Название программы")
        self.tree.heading("source", text="Источник (Реестр / Папка)")
        self.tree.heading("command", text="Исполняемая команда / Путь")

        self.tree.column("name", width=220, anchor="w")
        self.tree.column("source", width=190, anchor="center")
        self.tree.column("command", width=420, anchor="w")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background=BG_CARD, foreground=TEXT_MAIN, fieldbackground=BG_CARD, rowheight=26, font=("Consolas", 9), borderwidth=0)
        style.configure("Treeview.Heading", background=BG_SURFACE, foreground=TEXT_MUTED, font=("Segoe UI", 8, "bold"), relief="flat")
        style.map("Treeview", background=[("selected", ACCENT_PURPLE)], foreground=[("selected", "#ffffff")])

        tree_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scroll.pack(side="right", fill="y")

        # Action bar under table
        act_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=8)
        act_bar.pack(fill="x")

        del_btn = tk.Button(act_bar, text="🗑️ Удалить из автозагрузки [Del]", font=("Segoe UI", 8, "bold"),
                            bg=BG_CARD, fg=ACCENT_RED, activebackground=ACCENT_RED, activeforeground="#ffffff",
                            relief="flat", cursor="hand2", padx=12, pady=4,
                            highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.delete_selected)
        del_btn.pack(side="left")

        open_loc_btn = tk.Button(act_bar, text="📁 Открыть в Проводнике [Enter]", font=("Segoe UI", 8),
                                 bg=BG_CARD, fg=TEXT_MAIN, activebackground=BG_SURFACE,
                                 relief="flat", cursor="hand2", padx=12, pady=4,
                                 highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.open_file_location)
        open_loc_btn.pack(side="left", padx=8)

        copy_cmd_btn = tk.Button(act_bar, text="📋 Скопировать путь", font=("Segoe UI", 8),
                                 bg=BG_CARD, fg=TEXT_MUTED, activebackground=BG_SURFACE,
                                 relief="flat", cursor="hand2", padx=10, pady=4,
                                 highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.copy_command)
        copy_cmd_btn.pack(side="left")

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        self.status_lbl = tk.Label(footer, text="● Загрузка... // by qwstur", font=("Segoe UI", 8), fg=ACCENT_GREEN, bg=BG_SURFACE)
        self.status_lbl.pack(side="left", padx=16, pady=6)

        hint_lbl = tk.Label(footer, text="[F5] Обновить  |  [Enter] Проводник  |  [Del] Удалить // by qwstur", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        hint_lbl.pack(side="right", padx=16, pady=6)

    def bind_keys(self):
        self.bind("<F5>", lambda e: self.load_autostart_entries())
        self.bind("<Return>", lambda e: self.open_file_location())
        self.bind("<Delete>", lambda e: self.delete_selected())
        self.bind("<Escape>", lambda e: self.filter_var.set(""))

    def load_autostart_entries(self):
        self.startup_items = []

        # 1. HKCU Run
        self._read_reg_key(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKCU\\Run (Пользователь)")

        # 2. HKLM Run
        self._read_reg_key(winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run", "HKLM\\Run (Все пользователи)")

        # 3. Startup Folder
        startup_dir = os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup")
        if os.path.isdir(startup_dir):
            for f in os.listdir(startup_dir):
                full_p = os.path.join(startup_dir, f)
                self.startup_items.append({
                    "name": f,
                    "source": "Startup Folder",
                    "command": full_p,
                    "type": "folder",
                    "path": full_p
                })

        self.apply_filter()

    def _read_reg_key(self, hkey, subkey, label):
        try:
            with winreg.OpenKey(hkey, subkey, 0, winreg.KEY_READ) as key:
                num_vals = winreg.QueryInfoKey(key)[1]
                for i in range(num_vals):
                    try:
                        name, val, _ = winreg.EnumValue(key, i)
                        self.startup_items.append({
                            "name": name,
                            "source": label,
                            "command": str(val),
                            "type": "registry",
                            "hkey": hkey,
                            "subkey": subkey
                        })
                    except Exception:
                        pass
        except Exception:
            pass

    def apply_filter(self):
        q = self.filter_var.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        count = 0
        for idx, entry in enumerate(self.startup_items):
            if not q or (q in entry["name"].lower() or q in entry["command"].lower() or q in entry["source"].lower()):
                self.tree.insert("", "end", iid=str(idx), values=(entry["name"], entry["source"], entry["command"]))
                count += 1

        self.status_lbl.config(text=f"● Элементов в автозагрузке: {count}", fg=ACCENT_GREEN)

    def get_selected_item(self):
        sel = self.tree.selection()
        if not sel:
            return None
        idx = int(sel[0])
        if idx < len(self.startup_items):
            return self.startup_items[idx]
        return None

    def open_file_location(self):
        item = self.get_selected_item()
        if not item:
            messagebox.showinfo("Инфо", "Выберите элемент из списка")
            return

        cmd = item["command"].strip('"').split('"')[0]
        # Clean flags
        cmd = cmd.split(" /")[0].split(" -")[0].strip()
        if os.path.exists(cmd):
            subprocess.run(f'explorer /select,"{cmd}"', shell=True)
        else:
            self.status_lbl.config(text="✗ Файл или путь не найден на диске", fg=ACCENT_RED)

    def copy_command(self):
        item = self.get_selected_item()
        if item:
            self.clipboard_clear()
            self.clipboard_append(item["command"])
            self.status_lbl.config(text="✓ Путь скопирован в буфер!", fg=ACCENT_GREEN)

    def delete_selected(self):
        item = self.get_selected_item()
        if not item:
            return

        name = item["name"]
        confirm = messagebox.askyesno("Подтверждение", f"Удалить '{name}' из автозагрузки Windows?")
        if not confirm:
            return

        try:
            if item["type"] == "folder":
                os.remove(item["path"])
            elif item["type"] == "registry":
                with winreg.OpenKey(item["hkey"], item["subkey"], 0, winreg.KEY_SET_VALUE) as key:
                    winreg.DeleteValue(key, name)

            self.load_autostart_entries()
            self.status_lbl.config(text=f"✓ '{name}' успешно удален из автозагрузки", fg=ACCENT_GREEN)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить: {e}\nВозможно, требуются права Администратора.")

if __name__ == "__main__":
    app = AutostartManagerApp()
    app.mainloop()
