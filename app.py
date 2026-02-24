import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from functions import generate_prime, find_pub_key_e, find_priv_key_d, encode, decode


class RSAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RSA Cryptography")
        self.resizable(False, False)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=12)

        keys_frame = ttk.Frame(notebook)
        notebook.add(keys_frame, text="  My Keys  ")
        self._build_keys_tab(keys_frame)

        encrypt_frame = ttk.Frame(notebook)
        notebook.add(encrypt_frame, text="  Encrypt  ")
        self._build_encrypt_tab(encrypt_frame)

        decrypt_frame = ttk.Frame(notebook)
        notebook.add(decrypt_frame, text="  Decrypt  ")
        self._build_decrypt_tab(decrypt_frame)

    # ── My Keys tab ────────────────────────────────────────────────────────────

    def _build_keys_tab(self, parent):
        parent.columnconfigure(0, weight=1)

        ttk.Label(parent, text="Generate your key pair once. Share your public key (e and n) with anyone\n"
                               "who wants to send you a message. Keep your private key (d) secret.",
                  justify="left").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        btn_row = ttk.Frame(parent)
        btn_row.grid(row=1, column=0, pady=(0, 4))
        self.keygen_btn = ttk.Button(btn_row, text="Generate Key Pair", command=self._start_keygen)
        self.keygen_btn.pack(side="left")
        self.keygen_status = ttk.Label(btn_row, text="", foreground="gray")
        self.keygen_status.pack(side="left", padx=(10, 0))

        self._output_block(parent, row=2, label="Public Key  —  e  (share this)", attr="pub_e_output", height=3)
        self._output_block(parent, row=4, label="Public Key  —  n  (share this)", attr="pub_n_output", height=4)
        self._output_block(parent, row=6, label="Private Key  —  d  (keep this secret)", attr="priv_d_output", height=4)

    def _start_keygen(self):
        self.keygen_btn.config(state="disabled")
        self.keygen_status.config(text="Generating keys… (this takes a few seconds)")
        threading.Thread(target=self._run_keygen, daemon=True).start()

    def _run_keygen(self):
        try:
            p, q = generate_prime()
            e, n = find_pub_key_e(p, q)
            d = find_priv_key_d(e, p, q)
            self.after(0, self._finish_keygen, e, n, d)
        except Exception as ex:
            self.after(0, self._keygen_error, str(ex))

    def _finish_keygen(self, e, n, d):
        self.keygen_status.config(text="")
        self.keygen_btn.config(state="normal")
        self._set_text(self.pub_e_output, str(e))
        self._set_text(self.pub_n_output, str(n))
        self._set_text(self.priv_d_output, str(d))

    def _keygen_error(self, msg):
        self.keygen_status.config(text="")
        self.keygen_btn.config(state="normal")
        messagebox.showerror("Key generation error", msg)

    # ── Encrypt tab ────────────────────────────────────────────────────────────

    def _build_encrypt_tab(self, parent):
        parent.columnconfigure(0, weight=1)

        ttk.Label(parent, text="Enter your friend's public key (e and n) and your message.",
                  justify="left").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        fields = [
            ("Friend's Public Key  —  e", "enc_e_input", 2),
            ("Friend's Public Key  —  n", "enc_n_input", 3),
            ("Message", "enc_msg_input", 4),
        ]
        for i, (label, attr, height) in enumerate(fields):
            row = i * 2 + 1
            ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=12, pady=(6, 2))
            box = scrolledtext.ScrolledText(parent, width=70, height=height, wrap="word")
            box.grid(row=row + 1, column=0, padx=12, sticky="ew")
            setattr(self, attr, box)

        self.encrypt_btn = ttk.Button(parent, text="Encrypt", command=self._start_encrypt)
        self.encrypt_btn.grid(row=7, column=0, pady=10)

        self._output_block(parent, row=8, label="Encrypted Message  (send this to your friend)", attr="cipher_output", height=5)

    def _start_encrypt(self):
        try:
            e = int(self.enc_e_input.get("1.0", "end-1c").strip())
            n = int(self.enc_n_input.get("1.0", "end-1c").strip())
            message = self.enc_msg_input.get("1.0", "end-1c").strip()
        except ValueError:
            messagebox.showerror("Input error", "e and n must be valid integers.")
            return
        if not message:
            messagebox.showwarning("Input required", "Please enter a message to encrypt.")
            return

        self.encrypt_btn.config(state="disabled")
        threading.Thread(target=self._run_encrypt, args=(e, n, message), daemon=True).start()

    def _run_encrypt(self, e, n, message):
        try:
            cipher = encode(n, e, message)
            cipher_str = ",".join(map(str, cipher))
            self.after(0, self._finish_encrypt, cipher_str)
        except Exception as ex:
            self.after(0, self._encrypt_error, str(ex))

    def _finish_encrypt(self, cipher_str):
        self.encrypt_btn.config(state="normal")
        self._set_text(self.cipher_output, cipher_str)

    def _encrypt_error(self, msg):
        self.encrypt_btn.config(state="normal")
        messagebox.showerror("Encryption error", msg)

    # ── Decrypt tab ────────────────────────────────────────────────────────────

    def _build_decrypt_tab(self, parent):
        parent.columnconfigure(0, weight=1)

        ttk.Label(parent, text="Enter your private key (d and n) and the encrypted message you received.",
                  justify="left").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 8))

        fields = [
            ("Your Private Key  —  d", "d_input", 3),
            ("Your Public Key  —  n", "n_input", 3),
            ("Encrypted Message  (comma-separated)", "cipher_input", 5),
        ]
        for i, (label, attr, height) in enumerate(fields):
            row = i * 2 + 1
            ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=12, pady=(6, 2))
            box = scrolledtext.ScrolledText(parent, width=70, height=height, wrap="word")
            box.grid(row=row + 1, column=0, padx=12, sticky="ew")
            setattr(self, attr, box)

        self.decrypt_btn = ttk.Button(parent, text="Decrypt", command=self._start_decrypt)
        self.decrypt_btn.grid(row=7, column=0, pady=10)

        self._output_block(parent, row=8, label="Decrypted Message", attr="decrypt_output", height=4)

    def _start_decrypt(self):
        try:
            d = int(self.d_input.get("1.0", "end-1c").strip())
            n = int(self.n_input.get("1.0", "end-1c").strip())
            raw = self.cipher_input.get("1.0", "end-1c").strip()
            cipher_lst = [int(x) for x in raw.split(",")]
        except ValueError:
            messagebox.showerror("Input error", "d, n, and the cipher text must all be valid integers.")
            return

        self.decrypt_btn.config(state="disabled")
        threading.Thread(target=self._run_decrypt, args=(d, n, cipher_lst), daemon=True).start()

    def _run_decrypt(self, d, n, cipher_lst):
        try:
            message = decode(n, d, cipher_lst)
            self.after(0, self._finish_decrypt, message)
        except Exception as ex:
            self.after(0, self._decrypt_error, str(ex))

    def _finish_decrypt(self, message):
        self.decrypt_btn.config(state="normal")
        self._set_text(self.decrypt_output, message)

    def _decrypt_error(self, msg):
        self.decrypt_btn.config(state="normal")
        messagebox.showerror("Decryption error", msg)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _output_block(self, parent, *, row, label, attr, height):
        hdr = ttk.Frame(parent)
        hdr.grid(row=row, column=0, sticky="ew", padx=12, pady=(8, 2))
        ttk.Label(hdr, text=label).pack(side="left")
        ttk.Button(hdr, text="Copy", width=6,
                   command=lambda a=attr: self._copy(a)).pack(side="right")
        box = scrolledtext.ScrolledText(parent, width=70, height=height,
                                        state="disabled", wrap="word")
        box.grid(row=row + 1, column=0, padx=12, sticky="ew")
        setattr(self, attr, box)

    def _set_text(self, widget, text):
        widget.config(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.config(state="disabled")

    def _copy(self, attr):
        text = getattr(self, attr).get("1.0", "end-1c").strip()
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)


if __name__ == "__main__":
    app = RSAApp()
    app.mainloop()
