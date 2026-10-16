"""
==============================================================================
            ⚡ QWSTUR QUICK HTTP & STATIC SHARE SERVER // v1.0
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
import socket
import threading
import webbrowser
import functools
import http.server
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

class LogHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, app_ref=None, directory=None, **kwargs):
        self.app_ref = app_ref
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format, *args):
        msg = format % args
        if self.app_ref:
            client_ip = self.client_address[0]
            t_now = time.strftime("%H:%M:%S")
            self.app_ref.add_log(f"[{t_now}] {client_ip} -> {msg}")

class QuickServerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🌐 QWSTUR QUICK HTTP & SHARE SERVER // v1.0 // by qwstur")
        self.geometry("780x580")
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

        self.server = None
        self.server_thread = None
        self.is_running = False
        self.lan_ip = self.detect_lan_ip()

        self.build_ui()
        self.bind_keys()

    def detect_lan_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"

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

        t_lbl = tk.Label(h_left, text="🌐 QUICK HTTP & SHARE SERVER // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Мгновенный запуск локального веб-сервера для раздачи файлов и тестирования сайтов // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Config Card
        cfg_card = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=16, pady=12)
        cfg_card.pack(fill="x", padx=16, pady=12)

        # Directory Row
        d_row = tk.Frame(cfg_card, bg=BG_CARD)
        d_row.pack(fill="x", pady=(0, 8))

        tk.Label(d_row, text="Каталог файлов:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD, width=14, anchor="w").pack(side="left")
        self.dir_entry = tk.Entry(d_row, font=("Segoe UI", 9), bg=BG_SURFACE, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                                  relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        self.dir_entry.insert(0, os.getcwd())
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=8, ipady=3)

        browse_btn = tk.Button(d_row, text="📁 Обзор...", font=("Segoe UI", 8), bg=BG_DARK, fg=TEXT_MAIN,
                               relief="flat", cursor="hand2", padx=10, pady=2,
                               highlightthickness=1, highlightbackground=BORDER_COLOR, command=self.browse_dir)
        browse_btn.pack(side="right")

        # Port Row & Start Button
        p_row = tk.Frame(cfg_card, bg=BG_CARD)
        p_row.pack(fill="x")

        tk.Label(p_row, text="Порт сервера:", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, width=14, anchor="w").pack(side="left")
        self.port_entry = tk.Entry(p_row, font=("Consolas", 10), bg=BG_SURFACE, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                                   relief="flat", highlightthickness=1, highlightbackground=BORDER_COLOR, width=10)
        self.port_entry.insert(0, "8000")
        self.port_entry.pack(side="left", padx=(0, 16), ipady=3)

        self.toggle_btn = tk.Button(p_row, text="⚡ Запустить сервер [Enter]", font=("Segoe UI", 9, "bold"),
                                    bg=ACCENT_GREEN, fg="#000000", activebackground="#059669", activeforeground="#ffffff",
                                    relief="flat", cursor="hand2", padx=16, pady=4, command=self.toggle_server)
        self.toggle_btn.pack(side="left")

        # URLs Info Card
        self.urls_card = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=16, pady=10)
        self.urls_card.pack(fill="x", padx=16, pady=(0, 10))

        u1_row = tk.Frame(self.urls_card, bg=BG_CARD)
        u1_row.pack(fill="x", pady=2)
        tk.Label(u1_row, text="Локальный адрес (ПК):", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, width=20, anchor="w").pack(side="left")
        self.loc_url_lbl = tk.Label(u1_row, text="http://localhost:8000", font=("Consolas", 10, "bold"), fg=ACCENT_CYAN, bg=BG_CARD)
        self.loc_url_lbl.pack(side="left")

        open_b = tk.Button(u1_row, text="🌐 Открыть в браузере // by qwstur", font=("Segoe UI", 8), bg=BG_SURFACE, fg=TEXT_MAIN,
                           relief="flat", cursor="hand2", padx=8, pady=1, command=self.open_in_browser)
        open_b.pack(side="right")

        u2_row = tk.Frame(self.urls_card, bg=BG_CARD)
        u2_row.pack(fill="x", pady=2)
        tk.Label(u2_row, text="Сетевой адрес (LAN/Phone):", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, width=20, anchor="w").pack(side="left")
        self.lan_url_lbl = tk.Label(u2_row, text=f"http://{self.lan_ip}:8000", font=("Consolas", 10, "bold"), fg=ACCENT_PURPLE, bg=BG_CARD)
        self.lan_url_lbl.pack(side="left")

        copy_lan_b = tk.Button(u2_row, text="📋 Скопировать LAN // by qwstur", font=("Segoe UI", 8), bg=BG_SURFACE, fg=TEXT_MAIN,
                               relief="flat", cursor="hand2", padx=8, pady=1, command=self.copy_lan)
        copy_lan_b.pack(side="right")

        # Request Logs Card
        log_card = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=10)
        log_card.pack(fill="both", expand=True, padx=16, pady=(0, 10))

        log_top = tk.Frame(log_card, bg=BG_CARD)
        log_top.pack(fill="x", pady=(0, 4))
        tk.Label(log_top, text="Живой лог запросов:", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD).pack(side="left")

        clear_b = tk.Button(log_top, text="🗑️ Очистить // by qwstur", font=("Segoe UI", 8), bg=BG_SURFACE, fg=TEXT_MUTED,
                            relief="flat", cursor="hand2", padx=8, pady=1, command=self.clear_logs)
        clear_b.pack(side="right")

        self.log_text = tk.Text(log_card, bg=BG_DARK, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                                font=("Consolas", 9), wrap="word", relief="flat", padx=10, pady=8)
        self.log_text.pack(fill="both", expand=True)

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        self.status_lbl = tk.Label(footer, text="● Сервер остановлен // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        self.status_lbl.pack(side="left", padx=16, pady=6)

        hint_lbl = tk.Label(footer, text="[Enter] Запуск/Остановка  |  [Esc] Стоп // by qwstur", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        hint_lbl.pack(side="right", padx=16, pady=6)

    def bind_keys(self):
        self.bind("<Return>", lambda e: self.toggle_server())
        self.bind("<Escape>", lambda e: self.stop_server())

    def browse_dir(self):
        d = filedialog.askdirectory(title="Выберите директорию для сервера")
        if d:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, d)

    def toggle_server(self):
        if self.is_running:
            self.stop_server()
        else:
            self.start_server()

    def start_server(self):
        path = self.dir_entry.get().strip()
        if not os.path.isdir(path):
            messagebox.showerror("Ошибка", "Указанная папка не существует!")
            return

        port_str = self.port_entry.get().strip()
        try:
            port = int(port_str)
            if not (1 <= port <= 65535):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный номер порта (1-65535)")
            return

        handler_factory = functools.partial(LogHandler, app_ref=self, directory=path)

        try:
            self.server = http.server.ThreadingHTTPServer(("0.0.0.0", port), handler_factory)
        except Exception as e:
            messagebox.showerror("Ошибка запуска", f"Не удалось открыть порт {port}:\n{e}")
            return

        self.is_running = True
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()

        self.toggle_btn.config(text="🛑 Остановить сервер [Enter]", bg=ACCENT_RED, fg="#ffffff")
        self.loc_url_lbl.config(text=f"http://localhost:{port}")
        self.lan_url_lbl.config(text=f"http://{self.lan_ip}:{port}")
        self.status_lbl.config(text=f"● Сервер активен на порту :{port}", fg=ACCENT_GREEN)
        self.add_log(f"🚀 Веб-сервер запущен: http://localhost:{port} (Каталог: {path})")

    def stop_server(self):
        if not self.is_running:
            return

        self.is_running = False
        if self.server:
            threading.Thread(target=self.server.shutdown, daemon=True).start()

        self.toggle_btn.config(text="⚡ Запустить сервер [Enter]", bg=ACCENT_GREEN, fg="#000000")
        self.status_lbl.config(text="● Сервер остановлен", fg=TEXT_MUTED)
        self.add_log("🛑 Веб-сервер остановлен")

    def add_log(self, text):
        self.after(0, lambda: self._append_log(text))

    def _append_log(self, text):
        self.log_text.insert(tk.END, text + "\n")
        self.log_text.see(tk.END)

    def clear_logs(self):
        self.log_text.delete("1.0", tk.END)

    def open_in_browser(self):
        port = self.port_entry.get().strip()
        webbrowser.open(f"http://localhost:{port}")

    def copy_lan(self):
        port = self.port_entry.get().strip()
        url = f"http://{self.lan_ip}:{port}"
        self.clipboard_clear()
        self.clipboard_append(url)
        self.status_lbl.config(text="✓ LAN ссылка скопирована в буфер!", fg=ACCENT_GREEN)

if __name__ == "__main__":
    app = QuickServerApp()
    app.mainloop()
