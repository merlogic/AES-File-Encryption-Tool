from Crypto.Cipher import AES
import tkinter as tk
from tkinter import filedialog, messagebox
import os

key = b'MySecretKey12345'  # 16 bytes key (AES-128)
file_path = ""

# ================= selecting a file =================
def select_file():
    global file_path
    file_path = filedialog.askopenfilename()

    if file_path:
        file_label.config(text=os.path.basename(file_path))
    else:
        file_label.config(text="No file selected")

# ================= ENCRYPT =================
def encrypt_file():
    if not file_path:
        messagebox.showerror("Error", "Please select a file first")
        return

    try:
        with open(file_path, 'rb') as f:
            data = f.read()

        # padding
        while len(data) % 16 != 0:
            data += b' '

        cipher = AES.new(key, AES.MODE_ECB)
        encrypted = cipher.encrypt(data)

        output_path = file_path + ".enc"

        with open(output_path, "wb") as f:
            f.write(encrypted)

        messagebox.showinfo("Success", f"Encrypted:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= DECRYPT =================
def decrypt_file():
    if not file_path:
        messagebox.showerror("Error", "Please select a file first")
        return

    try:
        with open(file_path, 'rb') as f:
            encrypted = f.read()

        cipher = AES.new(key, AES.MODE_ECB)
        decrypted = cipher.decrypt(encrypted).rstrip(b' ')

        output_path = file_path.replace(".enc", "_decrypted")

        with open(output_path, "wb") as f:
            f.write(decrypted)

        messagebox.showinfo("Success", f"Decrypted:\n{output_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= GUI =================
app = tk.Tk()
app.title("SecureVault - AES Encryption Tool")
app.geometry("500x320")
app.configure(bg="#121212")
app.resizable(False, False)

title = tk.Label(
    app,
    text="🔐 SecureVault Encryption",
    font=("Segoe UI", 16, "bold"),
    bg="#121212",
    fg="white"
)
title.pack(pady=15)

# FRAME
frame = tk.Frame(app, bg="#1e1e1e")
frame.pack(pady=10, padx=20, fill="both", expand=True)

file_label = tk.Label(
    frame,
    text="No file selected",
    font=("Segoe UI", 10),
    bg="#1e1e1e",
    fg="#bbbbbb"
)
file_label.pack(pady=15)

btn_select = tk.Button(
    frame,
    text="📂 Select File",
    command=select_file,
    bg="#3b82f6",
    fg="white",
    font=("Segoe UI", 11),
    relief="flat",
    padx=10,
    pady=5
)
btn_select.pack(pady=5)

btn_encrypt = tk.Button(
    frame,
    text="🔒 Encrypt File",
    command=encrypt_file,
    bg="#22c55e",
    fg="white",
    font=("Segoe UI", 11),
    relief="flat",
    padx=10,
    pady=5
)
btn_encrypt.pack(pady=5)

btn_decrypt = tk.Button(
    frame,
    text="🔓 Decrypt File",
    command=decrypt_file,
    bg="#ef4444",
    fg="white",
    font=("Segoe UI", 11),
    relief="flat",
    padx=10,
    pady=5
)
btn_decrypt.pack(pady=5)

footer = tk.Label(
    app,
    text="AES Encryption Tool | Portfolio Project",
    bg="#121212",
    fg="#666",
    font=("Segoe UI", 9)
)
footer.pack(pady=8)

app.mainloop()