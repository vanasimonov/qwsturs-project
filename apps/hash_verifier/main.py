"""
==============================================================================
            ⚡ QWSTUR HASH & CHECKSUM VERIFIER // v1.0
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
ACCENT_CYAN = "#06b6d4"

class HashVerifierApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ QWSTUR HASH & CHECKSUM VERIFIER // v1.0 // by qwstur")
        self.geometry("780x590")
        self.minsize(700, 520)
        self.configure(bg=BG_DARK)

        try:
            DWMWA_USE_IMMERSIVE_DARK_MODE = 20
            set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            value = ctypes.c_int(1)
            set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, ctypes.byref(value), ctypes.sizeof(value))
        except Exception:
            pass

        self.hashes = {"MD5": "", "SHA-1": "", "SHA-256": "", "SHA-512": ""}
        self.is_calculating = False

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

        t_lbl = tk.Label(h_left, text="🛡️ HASH & CHECKSUM VERIFIER // by qwstur", font=("Segoe UI", 12, "bold"), fg=TEXT_MAIN, bg=BG_SURFACE)
        t_lbl.pack(anchor="w")
        s_lbl = tk.Label(h_left, text="Расчет MD5, SHA-1, SHA-256, SHA-512 и автоматическая проверка контрольных сумм // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        s_lbl.pack(anchor="w")

        # Mode Selection & Source
        top_bar = tk.Frame(self, bg=BG_DARK, padx=16, pady=12)
        top_bar.pack(fill="x")

        self.mode_var = tk.StringVar(value="file")
        rb_file = tk.Radiobutton(top_bar, text="Файл", variable=self.mode_var, value="file",
                                 font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_DARK, selectcolor=BG_SURFACE,
                                 activebackground=BG_DARK, activeforeground=TEXT_MAIN, command=self.on_mode_change)
        rb_file.pack(side="left", padx=(0, 12))

        rb_text = tk.Radiobutton(top_bar, text="Текст", variable=self.mode_var, value="text",
                                 font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_DARK, selectcolor=BG_SURFACE,
                                 activebackground=BG_DARK, activeforeground=TEXT_MAIN, command=self.on_mode_change)
        rb_text.pack(side="left", padx=(0, 20))

        # File Select bar
        self.file_frame = tk.Frame(self, bg=BG_DARK, padx=16)
        self.file_frame.pack(fill="x", pady=(0, 8))

        self.file_path_entry = tk.Entry(self.file_frame, font=("Segoe UI", 9), bg=BG_CARD, fg=TEXT_MAIN,
                                        insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1,
                                        highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        self.file_path_entry.pack(side="left", fill="x", expand=True, ipady=3)

        browse_btn = tk.Button(self.file_frame, text="📁 Выбрать файл... [Ctrl+O]", font=("Segoe UI", 8, "bold"),
                               bg=ACCENT_PURPLE, fg="#ffffff", activebackground="#7c3aed",
                               relief="flat", cursor="hand2", padx=12, pady=3, command=self.browse_file)
        browse_btn.pack(side="right", padx=(8, 0))

        # Text input frame (Hidden initially)
        self.text_frame = tk.Frame(self, bg=BG_DARK, padx=16)
        self.input_text = tk.Text(self.text_frame, height=4, font=("Consolas", 9), bg=BG_CARD, fg=TEXT_MAIN,
                                  insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1,
                                  highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        self.input_text.pack(fill="x")
        self.input_text.bind("<KeyRelease>", lambda e: self.calculate_text_hash())

        # Progress bar
        self.prog_frame = tk.Frame(self, bg=BG_DARK, padx=16, pady=4)
        self.prog_frame.pack(fill="x")
        self.progress = ttk.Progressbar(self.prog_frame, mode="determinate")
        self.progress.pack(fill="x")

        # Computed Hashes Container
        hashes_frame = tk.Frame(self, bg=BG_DARK, padx=16, pady=6)
        hashes_frame.pack(fill="x")

        self.hash_entries = {}
        for algo in ("MD5", "SHA-1", "SHA-256", "SHA-512"):
            row = tk.Frame(hashes_frame, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=10, pady=5)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=algo, font=("Consolas", 9, "bold"), width=8, anchor="w", fg=ACCENT_CYAN, bg=BG_CARD).pack(side="left")

            entry = tk.Entry(row, font=("Consolas", 9), bg=BG_SURFACE, fg=TEXT_MAIN, insertbackground=TEXT_MAIN,
                             relief="flat", readonlybackground=BG_SURFACE, state="readonly")
            entry.pack(side="left", fill="x", expand=True, padx=8, ipady=2)
            self.hash_entries[algo] = entry

            copy_btn = tk.Button(row, text="📋 Копия", font=("Segoe UI", 8), bg=BG_DARK, fg=TEXT_MAIN,
                                 activebackground=ACCENT_PURPLE, activeforeground="#ffffff", relief="flat", cursor="hand2",
                                 padx=8, pady=2, command=lambda a=algo: self.copy_hash(a))
            copy_btn.pack(side="right")

        # Verification Box
        verify_frame = tk.Frame(self, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER_COLOR, padx=14, pady=10)
        verify_frame.pack(fill="x", padx=16, pady=10)

        tk.Label(verify_frame, text="🔍 Вставьте хэш для сверки (Compare Hash):", font=("Segoe UI", 9, "bold"), fg=TEXT_MAIN, bg=BG_CARD).pack(anchor="w")

        v_sub = tk.Frame(verify_frame, bg=BG_CARD)
        v_sub.pack(fill="x", pady=(6, 0))

        self.verify_entry = tk.Entry(v_sub, font=("Consolas", 9), bg=BG_SURFACE, fg=TEXT_MAIN,
                                     insertbackground=TEXT_MAIN, relief="flat", highlightthickness=1,
                                     highlightbackground=BORDER_COLOR, highlightcolor=ACCENT_PURPLE)
        self.verify_entry.pack(side="left", fill="x", expand=True, ipady=3)
        self.verify_entry.bind("<KeyRelease>", lambda e: self.check_verification())

        self.verify_badge = tk.Label(v_sub, text="● Ожидание ввода", font=("Segoe UI", 8, "bold"),
                                     bg=BG_SURFACE, fg=TEXT_MUTED, padx=10, pady=3)
        self.verify_badge.pack(side="right", padx=(8, 0))

        # Footer
        footer = tk.Frame(self, bg=BG_SURFACE, height=32, highlightthickness=1, highlightbackground=BORDER_COLOR)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        foot_link = tk.Label(footer, text="⚡ qwsturs store © 2026 // by qwstur | Написать владельцу: @AimBoGAttack",
                             font=("Segoe UI", 8, "underline"), fg=ACCENT_PURPLE, bg=BG_SURFACE, cursor="hand2")
        foot_link.pack(side="right", padx=16, pady=4)
        foot_link.bind("<Button-1>", lambda e: webbrowser.open("https://t.me/AimBoGAttack"))


        self.status_lbl = tk.Label(footer, text="● Выберите файл или введите текст // by qwstur", font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        self.status_lbl.pack(side="left", padx=16, pady=6)

        hint_lbl = tk.Label(footer, text="[Ctrl+O] Открыть файл  |  [Esc] Сброс // by qwstur", font=("Consolas", 8), fg=TEXT_MUTED, bg=BG_SURFACE)
        hint_lbl.pack(side="right", padx=16, pady=6)

    def bind_keys(self):
        self.bind("<Control-o>", lambda e: self.browse_file())
        self.bind("<Escape>", lambda e: self.reset_all())

    def on_mode_change(self):
        mode = self.mode_var.get()
        if mode == "file":
            self.text_frame.pack_forget()
            self.file_frame.pack(fill="x", pady=(0, 8), before=self.prog_frame)
            self.status_lbl.config(text="● Выберите файл для расчета хэша", fg=TEXT_MUTED)
        else:
            self.file_frame.pack_forget()
            self.text_frame.pack(fill="x", pady=(0, 8), before=self.prog_frame)
            self.calculate_text_hash()

    def browse_file(self):
        if self.is_calculating:
            return
        f_path = filedialog.askopenfilename(title="Выберите файл для расчета хэша")
        if f_path:
            self.file_path_entry.delete(0, tk.END)
            self.file_path_entry.insert(0, f_path)
            self.calculate_file_hash_async(f_path)

    def calculate_file_hash_async(self, f_path):
        if not os.path.isfile(f_path):
            self.show_toast("✗ Файл не найден", ACCENT_RED)
            return

        self.is_calculating = True
        self.status_lbl.config(text="⏳ Вычисление хэшей (MD5, SHA-1, SHA-256, SHA-512)...", fg=ACCENT_PURPLE)
        self.progress["value"] = 0

        def worker():
            try:
                total_size = os.path.getsize(f_path)
                read_bytes = 0

                md5 = hashlib.md5()
                sha1 = hashlib.sha1()
                sha256 = hashlib.sha256()
                sha512 = hashlib.sha512()

                with open(f_path, "rb") as f:
                    while chunk := f.read(65536):
                        md5.update(chunk)
                        sha1.update(chunk)
                        sha256.update(chunk)
                        sha512.update(chunk)
                        read_bytes += len(chunk)
                        if total_size > 0:
                            pct = (read_bytes / total_size) * 100
                            self.after(0, lambda p=pct: self.update_progress(p))

                res = {
                    "MD5": md5.hexdigest(),
                    "SHA-1": sha1.hexdigest(),
                    "SHA-256": sha256.hexdigest(),
                    "SHA-512": sha512.hexdigest()
                }
                self.after(0, lambda: self.finish_hashes(res))
            except Exception as e:
                self.after(0, lambda: self.show_toast(f"✗ Ошибка чтения: {str(e)}", ACCENT_RED))
            finally:
                self.is_calculating = False

        threading.Thread(target=worker, daemon=True).start()

    def update_progress(self, val):
        self.progress["value"] = val

    def finish_hashes(self, res):
        self.hashes = res
        for algo, val in res.items():
            ent = self.hash_entries[algo]
            ent.config(state="normal")
            ent.delete(0, tk.END)
            ent.insert(0, val)
            ent.config(state="readonly")

        self.progress["value"] = 100
        self.status_lbl.config(text="✓ Хэши успешно вычислены", fg=ACCENT_GREEN)
        self.check_verification()

    def calculate_text_hash(self):
        raw_text = self.input_text.get("1.0", tk.END).encode("utf-8")
        res = {
            "MD5": hashlib.md5(raw_text).hexdigest(),
            "SHA-1": hashlib.sha1(raw_text).hexdigest(),
            "SHA-256": hashlib.sha256(raw_text).hexdigest(),
            "SHA-512": hashlib.sha512(raw_text).hexdigest()
        }
        self.finish_hashes(res)

    def check_verification(self):
        target = self.verify_entry.get().strip().lower()
        if not target:
            self.verify_badge.config(text="● Ожидание ввода // by qwstur", fg=TEXT_MUTED, bg=BG_SURFACE)
            return

        matched_algo = None
        for algo, val in self.hashes.items():
            if val and val.lower() == target:
                matched_algo = algo
                break

        if matched_algo:
            self.verify_badge.config(text=f"✓ СОВПАДЕНИЕ ({matched_algo})", fg="#ffffff", bg=ACCENT_GREEN)
        else:
            self.verify_badge.config(text="✗ ХЭШИ НЕ СОВПАДАЮТ", fg="#ffffff", bg=ACCENT_RED)

    def copy_hash(self, algo):
        val = self.hashes.get(algo, "")
        if val:
            self.clipboard_clear()
            self.clipboard_append(val)
            self.show_toast(f"✓ {algo} скопирован в буфер", ACCENT_GREEN)

    def show_toast(self, text, color=ACCENT_GREEN):
        self.status_lbl.config(text=text, fg=color)

    def reset_all(self):
        self.file_path_entry.delete(0, tk.END)
        self.input_text.delete("1.0", tk.END)
        self.verify_entry.delete(0, tk.END)
        self.progress["value"] = 0
        self.hashes = {"MD5": "", "SHA-1": "", "SHA-256": "", "SHA-512": ""}
        for ent in self.hash_entries.values():
            ent.config(state="normal")
            ent.delete(0, tk.END)
            ent.config(state="readonly")
        self.verify_badge.config(text="● Ожидание ввода // by qwstur", fg=TEXT_MUTED, bg=BG_SURFACE)
        self.status_lbl.config(text="● Сброшено", fg=TEXT_MUTED)

if __name__ == "__main__":
    app = HashVerifierApp()
    app.mainloop()
