"""
==============================================================================
            ⚡ QWSTUR PORT & PROCESS KILLER // v1.0
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
import subprocess
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
ACCENT_AMBER = "#f59e0b"

class PortKillerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ QWSTUR PORT & PROCESS KILLER // v1.0 // by qwstur")
        self.geometry("780x560")
        self.minsize(700, 480)
        self.configure(bg=BG_DARK)

        # Windows 10/11 Dark Titlebar
        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.ports_data = []
        self.build_ui()
        self.bind_keys()
        self.refresh_ports_async()

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

        t_lbl = tk.Label(h_left, text="⚡ PORT & PROCESS KILLER // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Освобождение занятых TCP-портов и завершение зависших процессов // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Top Quick Kill Box
        top_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=10)
        top_bar.pack(fill="x")

        tk.Label(top_bar, text="Быстрое освобождение порта:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_DARK).pack(side="left")

        self.port_entry = tk.Entry(top_bar, font=("Consolas", 10), bg=BG_CARD, fg=TEXT_MAIN,
                                   insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1,
                                   highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE, width=12)
        self.port_entry.pack(side="left", padx=(8, 8), ipady=3)
        self.port_entry.focus_set()

        kill_btn = tk.Button(top_bar, text="⚡ Убить процесс [Enter]", font=("Segoe UI", 8, "bold"),
                             bg=ACCENT_RED, fg="#ffffff", activebackground="#dc2626", activeforeground="#ffffff",
                             relief="flat", cursor="hand2", padx=12, pady=3, command=self.kill_entered_port)
        kill_btn.pack(side="left")

        refresh_btn = tk.Button(top_bar, text="🔄 Обновить [F5]", font=("Segoe UI", 8),
                                bg=BG_CARD, fg=TEXT_MAIN, activebackground=BG_SURFACE,
                                relief="flat", cursor="hand2", padx=10, pady=3,
                                highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.refresh_ports_async)
        refresh_btn.pack(side="right")

        # Search / Filter Bar
        search_bar = tk.Frame(self, bg=BG_DARK, padx=16)
        search_bar.pack(fill="x", pady=(0, 8))

        tk.Label(search_bar, text="Фильтр:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_DARK).pack(side="left")
        self.filter_var = tk.StringVar()
        self.filter_var.trace_add("write", lambda *args: self.apply_filter())
        self.filter_entry = tk.Entry(search_bar, textvariable=self.filter_var, font=("Segoe UI", 9),
                                     bg=BG_CARD, fg=TEXT_MAIN, insertbackground=TEXT_MAIN, relief="flat",
                                     highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        self.filter_entry.pack(side="left", fill="x", expand=True, padx=(8, 0), ipady=2)

        # Ports Table
        table_frame = tk.Frame(self, bg=BG_DARK, padx=16)
        table_frame.pack(fill="both", expand=True)

        cols = ("port", "pid", "name", "address", "state")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("port", text="Порт")
        self.tree.heading("pid", text="PID")
        self.tree.heading("name", text="Имя процесса")
        self.tree.heading("address", text="Локальный адрес")
        self.tree.heading("state", text="Состояние")

        self.tree.column("port", width=90, anchor="center")
        self.tree.column("pid", width=90, anchor="center")
        self.tree.column("name", width=220, anchor="w")
        self.tree.column("address", width=180, anchor="w")
        self.tree.column("state", width=110, anchor="center")

        # Styling ttk Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background=BG_CARD,
                        foreground=TEXT_MAIN,
                        fieldbackground=BG_CARD,
                        rowheight=26,
                        font=("Consolas", 9),
                        borderwidth=0)
        style.configure("Treeview.Heading",
                        background=BG_SURFACE,
                        foreground=TEXT_MUTED,
                        font=("Segoe UI", 8, "bold"),
                        relief="flat")
        style.map("Treeview",
                  background=[("selected", ACCENT_PURPLE)],
                  foreground=[("selected", "#ffffff")])
        style.map("Treeview.Heading",
                  background=[("active", BG_CARD)])

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action bar under table
        bot_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=8)
        bot_bar.pack(fill="x")

        kill_sel_btn = tk.Button(bot_bar, text="❌ Завершить выбранный процесс", font=("Segoe UI", 8, "bold"),
                                 bg=BG_CARD, fg=ACCENT_RED, activebackground=ACCENT_RED, activeforeground="#ffffff",
                                 relief="flat", cursor="hand2", padx=10, pady=4,
                                 highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.kill_selected_process)
        kill_sel_btn.pack(side="left")

        # Footer & Status Toast
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        self.status_lbl = tk.Label(footer, text="● Готов к работе // by qwstur", font=("Segoe UI", 8), fg=ACCENT_GREEN, bg=BG_SURFACE)
        self.status_lbl.pack(side="left", padx=16, pady=6)

        hint_lbl = tk.Label(footer, text="[F5] Обновить  |  [Esc] Сброс фильтра // by qwstur", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        hint_lbl.pack(side="right", padx=16, pady=6)

    def bind_keys(self):
        self.bind("<Return>", lambda e: self.on_enter_press())
        self.bind("<F5>", lambda e: self.refresh_ports_async())
        self.bind("<Escape>", lambda e: self.on_escape())

    def on_enter_press(self):
        val = self.port_entry.get().strip()
        if val:
            self.kill_entered_port()
        else:
            self.kill_selected_process()

    def on_escape(self):
        self.filter_var.set("")
        self.port_entry.delete(0, tk.END)
        self.set_status("● Фильтр очищен", ACCENT_GREEN)

    def set_status(self, text, color=TEXT_MAIN):
        self.status_lbl.config(text=text, fg=color)

    def show_toast(self, text, color=ACCENT_GREEN):
        self.set_status(text, color)
        self.after(3000, lambda: self.set_status("● Готов к работе", ACCENT_GREEN))

    def refresh_ports_async(self):
        self.set_status("⏳ Сканирование открытых TCP-портов...", ACCENT_AMBER)
        threading.Thread(target=self._fetch_ports_worker, daemon=True).start()

    def _fetch_ports_worker(self):
        # 1. Fetch processes map: PID -> Name
        pids_map = {}
        try:
            cmd_tasklist = "tasklist /FO CSV /NH"
            res_tl = subprocess.run(cmd_tasklist, shell=True, capture_output=True, text=True, errors="replace")
            for line in res_tl.stdout.splitlines():
                parts = [p.strip('"') for p in line.split('","')]
                if len(parts) >= 2:
                    name = parts[0]
                    pid_str = parts[1]
                    pids_map[pid_str] = name
        except Exception:
            pass

        # 2. Fetch netstat -ano -p tcp
        rows = []
        try:
            cmd = "netstat -ano -p tcp"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, errors="replace")
            for line in res.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 5 and parts[0].upper() == "TCP":
                    proto, local, foreign, state, pid = parts[0], parts[1], parts[2], parts[3], parts[4]
                    if state.upper() in ("LISTENING", "ESTABLISHED"):
                        # Extract port
                        port = local.split(":")[-1] if ":" in local else local
                        proc_name = pids_map.get(pid, "Системный / Unknown")
                        rows.append({
                            "port": port,
                            "pid": pid,
                            "name": proc_name,
                            "address": local,
                            "state": state
                        })
        except Exception as e:
            rows = []

        # Sort by port number if possible
        def port_key(item):
            try:
                return int(item["port"])
            except ValueError:
                return 999999
        rows.sort(key=port_key)

        self.ports_data = rows
        self.after(0, self.apply_filter)

    def apply_filter(self):
        q = self.filter_var.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.destroy_item(item) if hasattr(self.tree, 'destroy_item') else self.tree.delete(item)

        count = 0
        for item in self.ports_data:
            if not q or (q in item["port"] or q in item["pid"] or q in item["name"].lower() or q in item["address"].lower()):
                self.tree.insert("", "end", values=(item["port"], item["pid"], item["name"], item["address"], item["state"]))
                count += 1

        self.set_status(f"● Активных портов: {count}", ACCENT_GREEN)

    def kill_entered_port(self):
        val = self.port_entry.get().strip()
        if not val:
            self.show_toast("⚠️ Введите номер порта для завершения", ACCENT_AMBER)
            return

        target_pid = None
        target_name = "Unknown"
        for p in self.ports_data:
            if p["port"] == val:
                target_pid = p["pid"]
                target_name = p["name"]
                break

        if not target_pid:
            self.show_toast(f"✗ Порт :{val} не найден среди активных", ACCENT_RED)
            return

        self._terminate_pid(target_pid, target_name, val)

    def kill_selected_process(self):
        sel = self.tree.selection()
        if not sel:
            self.show_toast("⚠️ Выберите процесс из списка", ACCENT_AMBER)
            return
        vals = self.tree.item(sel[0])["values"]
        if vals:
            port, pid, name = vals[0], str(vals[1]), vals[2]
            self._terminate_pid(pid, name, port)

    def _terminate_pid(self, pid, name, port):
        if pid in ("0", "4"):
            self.show_toast(f"🛡️ PID {pid} защищен Windows (System kernel)", ACCENT_AMBER)
            return

        try:
            cmd = f"taskkill /PID {pid} /F"
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, errors="replace")
            if res.returncode == 0:
                self.show_toast(f"✓ Процесс {name} (PID: {pid}, порт :{port}) успешно убит!", ACCENT_GREEN)
                self.port_entry.delete(0, tk.END)
                self.refresh_ports_async()
            else:
                self.show_toast(f"✗ Ошибка: {res.stderr.strip() or 'Отказано в доступе'}", ACCENT_RED)
        except Exception as e:
            self.show_toast(f"✗ Ошибка завершения: {str(e)}", ACCENT_RED)

if __name__ == "__main__":
    app = PortKillerApp()
    app.mainloop()
