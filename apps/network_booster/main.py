"""
==============================================================================
                 ⚡ QWSTUR PING & NETWORK BOOSTER // v1.0
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
import subprocess
import threading
import time
import webbrowser
import ctypes
import tkinter as tk
from tkinter import ttk

BG_DARK = "#09090b"
BG_SURFACE = "#121216"
BG_CARD = "#18181f"
BORDER_COLOR = "#272733"
TEXT_MAIN = "#f4f4f5"
TEXT_MUTED = "#a1a1aa"
ACCENT_GREEN = "#10b981"
ACCENT_PURPLE = "#a855f7"
ACCENT_BLUE = "#38bdf8"

SERVERS_TO_PING = [
    ("Cloudflare DNS", "1.1.1.1"),
    ("Google DNS", "8.8.8.8"),
    ("Valve / Steam EU", "155.133.248.51"),
    ("Discord Gateway", "router.discord.gg"),
    ("Riot Games EU", "104.160.141.3")
]

class NetworkBoosterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("⚡ QWSTUR PING & NETWORK BOOSTER // by qwstur")
        self.geometry("740x520")
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

        self.ping_labels = {}
        self.create_ui()
        self.start_ping_thread()

    def create_ui(self):
        # Header
        header = tk.Frame(self, bg=BG_SURFACE, height=65, highlightthickness=1, highlightbackground=BORDER_COLOR)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        tb = tk.Frame(header, bg=BG_SURFACE)
        tb.pack(side="left", padx=20, pady=10)

        t_lbl = tk.Label(tb, text="⚡ QWSTUR NETWORK BOOSTER // by qwstur", font=("Segoe UI", 13, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(tb, text="Тюнинг TCP/IP, ускорение пинга и игровой буст сети // by qwstur", font=("Segoe UI", 9), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        tg_btn = tk.Button(header, text="✉️ Написать владельцу", font=("Segoe UI", 9, "bold"),
                           bg=ACCENT_BLUE, fg="#000000", activebackground="#7dd3fc", activeforeground="#000000",
                           relief="flat", cursor="hand2", padx=12, pady=5, command=self.open_tg)
        tg_btn.pack(side="right", padx=20)

        # Body
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=20, pady=15)

        # Left Column - Ping Monitor
        left = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, width=320)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        lh = tk.Frame(left, bg=BG_SURFACE, height=35)
        lh.pack(fill="x")
        lh.pack_propagate(False)
        lh_lbl = tk.Label(lh, text="📊 МОНИТОРИНГ ЗАДЕРЖКИ (PING) // by qwstur", font=("Consolas", 9, "bold"), fg=TEXT_MUTED, bg=BG_SURFACE)
        lh_lbl.pack(side="left", padx=12, pady=8)

        retest_btn = tk.Button(lh, text="🔄 Тест", font=("Segoe UI", 8), bg=BG_CARD, fg=TEXT_MAIN, relief="flat", cursor="hand2", command=self.start_ping_thread)
        retest_btn.pack(side="right", padx=10, pady=5)

        pings_box = tk.Frame(left, bg=BG_CARD, padx=12, pady=10)
        pings_box.pack(fill="both", expand=True)

        for name, host in SERVERS_TO_PING:
            row = tk.Frame(pings_box, bg=BG_CARD)
            row.pack(fill="x", pady=6)

            n_lbl = tk.Label(row, text=name, font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD)
            n_lbl.pack(side="left")

            h_lbl = tk.Label(row, text=f"({host})", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_CARD)
            h_lbl.pack(side="left", padx=(5, 0))

            val_lbl = tk.Label(row, text="Тест...", font=("Consolas", 9, "bold"), fg=TEXT_MUTED, bg=BG_CARD)
            val_lbl.pack(side="right")
            self.ping_labels[name] = val_lbl

        # Right Column - Actions & Tweaks
        right = tk.Frame(body, bg=BG_DARK)
        right.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.create_action_card(
            right,
            title="⚡ TCP Auto-Tuning & Netsh Fix",
            desc="Включает оптимальное динамическое окно TCP для плавной передачи пакетов.",
            btn_text="Применить твик",
            cmd=self.tweak_tcp
        )

        self.create_action_card(
            right,
            title="🔄 Winsock & IP Stack Reset",
            desc="Сброс сетевых каталогов Windows и протоколов до идеального заводского состояния.",
            btn_text="Сбросить стек",
            cmd=self.reset_winsock
        )

        self.create_action_card(
            right,
            title="🛡️ Сброс ARP и DNS Таблиц",
            desc="Очищает локальную таблицу маршрутизации и ARP-кэш для защиты от спама.",
            btn_text="Очистить таблицы",
            cmd=self.clear_arp_dns
        )

        # Log box inside right
        log_box = tk.Frame(right, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR)
        log_box.pack(fill="both", expand=True, pady=(5, 0))

        self.log_text = tk.Text(log_box, bg="#0d0d11", fg="#e4e4e7", font=("Consolas", 8),
                                wrap="word", relief="flat", padx=10, pady=8, height=6)
        self.log_text.pack(fill="both", expand=True)

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=35, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        foot_lbl = tk.Label(footer, text="⚡ qwsturs store © 2026 // Сочно и для своих // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        foot_lbl.pack(side="left", padx=20, pady=8)

        tg_link = tk.Label(footer, text="✈️ t.me/AimBoGAttack // by qwstur", font=("Segoe UI", 8, "underline"), fg=ACCENT_BLUE, bg=BG_SURFACE, cursor="hand2")
        tg_link.pack(side="right", padx=20, pady=8)
        tg_link.bind("<Button-1>", lambda e: self.open_tg())

        self.log("🚀 QWSTUR NETWORK BOOSTER готов к работе.")

    def create_action_card(self, parent, title, desc, btn_text, cmd):
        card = tk.Frame(parent, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=12, pady=8)
        card.pack(fill="x", pady=4)

        top = tk.Frame(card, bg=BG_CARD)
        top.pack(fill="x")

        t_lbl = tk.Label(top, text=title, font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD)
        t_lbl.pack(side="left")

        btn = tk.Button(top, text=btn_text, font=("Segoe UI", 8, "bold"), bg=ACCENT_PURPLE, fg="#ffffff",
                        activebackground="#9333ea", activeforeground="#ffffff", relief="flat", cursor="hand2", padx=10, pady=3, command=cmd)
        btn.pack(side="right")

        d_lbl = tk.Label(card, text=desc, font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD, wraplength=310, justify="left")
        d_lbl.pack(anchor="w", pady=(2, 0))

    def log(self, text):
        t_str = time.strftime("[%H:%M:%S]")
        self.log_text.insert("end", f"{t_str} {text}\n")
        self.log_text.see("end")

    def open_tg(self):
        webbrowser.open("https://t.me/AimBoGAttack")

    def start_ping_thread(self):
        for name, lbl in self.ping_labels.items():
            lbl.config(text="Замер...", fg=TEXT_MUTED)

        def run_pings():
            for name, host in SERVERS_TO_PING:
                try:
                    # Windows ping
                    res = subprocess.run(["ping", "-n", "1", "-w", "1000", host], capture_output=True, text=True)
                    out = res.stdout
                    if "Average =" in out or "Среднее =" in out:
                        if "Average =" in out:
                            ms = out.split("Average =")[-1].strip()
                        else:
                            ms = out.split("Среднее =")[-1].strip()
                        ms_num = int(''.join(filter(str.isdigit, ms)))
                        color = ACCENT_GREEN if ms_num < 45 else ("#facc15" if ms_num < 90 else "#ef4444")
                        self.after(0, self.update_ping_lbl, name, f"{ms_num} ms", color)
                    elif "time=" in out or "время=" in out:
                        line = [l for l in out.splitlines() if "time=" in l or "время=" in l][0]
                        time_part = line.split("time=")[-1].split("ms")[0] if "time=" in line else line.split("время=")[-1].split("мс")[0]
                        ms_num = int(''.join(filter(str.isdigit, time_part)))
                        color = ACCENT_GREEN if ms_num < 45 else ("#facc15" if ms_num < 90 else "#ef4444")
                        self.after(0, self.update_ping_lbl, name, f"{ms_num} ms", color)
                    else:
                        self.after(0, self.update_ping_lbl, name, "Таймаут", "#ef4444")
                except Exception:
                    self.after(0, self.update_ping_lbl, name, "Ошибка", "#ef4444")

        threading.Thread(target=run_pings, daemon=True).start()

    def update_ping_lbl(self, name, text, color):
        if name in self.ping_labels:
            self.ping_labels[name].config(text=text, fg=color)

    def tweak_tcp(self):
        def task():
            self.log("⚡ Применение TCP AutoTuning Level...")
            try:
                subprocess.run("netsh int tcp set global autotuninglevel=normal", shell=True)
                subprocess.run("netsh int tcp set global rss=enabled", shell=True)
                self.log("✅ [OK] TCP AutoTuning и RSS успешно активированы!")
            except Exception as e:
                self.log(f"⚠️ Ошибка: {e}")
        threading.Thread(target=task, daemon=True).start()

    def reset_winsock(self):
        def task():
            self.log("🔄 Сброс сетевого каталога Winsock...")
            try:
                subprocess.run("netsh winsock reset", shell=True)
                self.log("✅ [OK] Winsock очищен! Сетевые протоколы сброшены.")
            except Exception as e:
                self.log(f"⚠️ Ошибка: {e}")
        threading.Thread(target=task, daemon=True).start()

    def clear_arp_dns(self):
        def task():
            self.log("🛡️ Очистка DNS и ARP таблицы...")
            try:
                subprocess.run("ipconfig /flushdns", shell=True)
                subprocess.run("arp -d *", shell=True)
                self.log("✅ [OK] DNS и ARP таблицы полностью очищены!")
            except Exception as e:
                self.log(f"⚠️ Ошибка: {e}")
        threading.Thread(target=task, daemon=True).start()

if __name__ == "__main__":
    app = NetworkBoosterApp()
    app.mainloop()
