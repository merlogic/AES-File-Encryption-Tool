from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# ================= KEY =================
key = os.getenv("AES_KEY")

if not key:
    key_missing = True
else:
    key_missing = False
    key = key.encode()

file_paths = []

# ================= HELPERS =================
def set_status(text, color):
    status_label.config(text=text.upper(), fg="#f8fafc")
    status_dot.config(fg=color)

def format_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    else:
        return f"{size / (1024 * 1024):.2f} MB"

# ================= SELECT FILE =================
def select_file():
    global file_paths

    file_paths = filedialog.askopenfilenames()

    if file_paths:
        file_details = []

        for path in file_paths[:5]:
            name = os.path.basename(path)
            ext = os.path.splitext(path)[1] or "No extension"
            size = format_size(os.path.getsize(path))

            file_details.append(f"{name} | {ext} | {size}")

        display_text = "\n".join(file_details)

        if len(file_paths) > 5:
            display_text += f"\n... +{len(file_paths) - 5} more files"

        file_label.config(text=display_text, fg="#38bdf8")
        set_status(f"{len(file_paths)} files loaded", "#38bdf8")

    else:
        file_label.config(text="No file selected", fg="#475569")
        set_status("No file selected", "#ef4444")

# ================= ENCRYPT =================
def encrypt_files():
    if key_missing:
        messagebox.showerror("Error", "AES_KEY is not set")
        return

    if not file_paths:
        messagebox.showerror("Error", "No files selected")
        return

    success, skipped = 0, 0

    for path in file_paths:
        try:
            if path.endswith(".enc"):
                skipped += 1
                continue

            with open(path, 'rb') as f:
                data = f.read()

            nonce = get_random_bytes(12)
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            ciphertext, tag = cipher.encrypt_and_digest(data)

            with open(path + ".enc", "wb") as f:
                f.write(nonce + tag + ciphertext)

            success += 1

        except:
            skipped += 1

    set_status("Encryption complete", "#22c55e")

    messagebox.showinfo(
        "Done",
        f"Encrypted: {success}\nSkipped: {skipped}"
    )

# ================= DECRYPT =================
def decrypt_files():
    if key_missing:
        messagebox.showerror("Error", "AES_KEY is not set")
        return

    if not file_paths:
        messagebox.showerror("Error", "No files selected")
        return

    success, skipped = 0, 0

    for path in file_paths:
        try:
            if not path.endswith(".enc"):
                skipped += 1
                continue

            with open(path, 'rb') as f:
                raw = f.read()

            nonce = raw[:12]
            tag = raw[12:28]
            ciphertext = raw[28:]

            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)

            # ✅ FIXED: restore original file name correctly
            output_path = path[:-4]   # removes ".enc"

            with open(output_path, "wb") as f:
                f.write(data)

            success += 1

        except:
            skipped += 1

    set_status("Decryption complete", "#22c55e")

    messagebox.showinfo(
        "Done",
        f"Decrypted: {success}\nSkipped: {skipped}"
    )

# ================= UI =================
app = tk.Tk()
app.title("SecureVault Pro")
app.geometry("700x450")
app.configure(bg="#0f172a")
app.resizable(False, False)

# ===== SIDEBAR =====
sidebar = tk.Frame(app, bg="#111827", width=220)
sidebar.pack(side="left", fill="y")

tk.Label(
    sidebar,
    text="🔐 SecureVault",
    font=("Segoe UI", 16, "bold"),
    bg="#111827",
    fg="#e2e8f0"
).pack(pady=(30, 5))

tk.Label(
    sidebar,
    text="version 2.0",
    font=("Segoe UI", 9),
    bg="#111827",
    fg="#475569"
).pack(pady=(0, 30))

def make_button(text, command):
    btn = tk.Button(
        sidebar,
        text=text,
        command=command,
        font=("Segoe UI", 10, "bold"),
        bg="#1f2937",
        fg="#cbd5e1",
        relief="flat",
        padx=15,
        pady=10,
        width=18,
        cursor="hand2"
    )
    btn.bind("<Enter>", lambda e: btn.config(bg="#374151"))
    btn.bind("<Leave>", lambda e: btn.config(bg="#1f2937"))
    return btn

make_button("📂 Select Files", select_file).pack(pady=10)
make_button("🔒 Encrypt", encrypt_files).pack(pady=10)
make_button("🔓 Decrypt", decrypt_files).pack(pady=10)

# ===== MAIN =====
main = tk.Frame(app, bg="#0f172a")
main.pack(side="right", expand=True, fill="both")

content = tk.Frame(main, bg="#0f172a")
content.place(relx=0.5, rely=0.5, anchor="center")

card = tk.Frame(content, bg="#0f172a", padx=30, pady=30)
card.pack()

tk.Label(
    card,
    text="SELECTED FILES",
    font=("Segoe UI", 8, "bold"),
    bg="#0f172a",
    fg="#38bdf8"
).pack(anchor="w")

file_label = tk.Label(
    card,
    text="No file selected",
    font=("Consolas", 11),
    bg="#0f172a",
    fg="#475569",
    wraplength=400,
    justify="left",
    anchor="w"
)
file_label.pack(anchor="w", pady=(5, 20))

# ===== STATUS =====
status_frame = tk.Frame(card, bg="#0f172a")
status_frame.pack(anchor="w")

status_dot = tk.Label(
    status_frame,
    text="●",
    font=("Segoe UI", 12),
    bg="#0f172a",
    fg="#334155"
)
status_dot.pack(side="left", padx=(0, 8))

status_label = tk.Label(
    status_frame,
    text="READY",
    font=("Segoe UI", 9, "bold"),
    bg="#0f172a",
    fg="#334155"
)
status_label.pack(side="left")

app.mainloop()