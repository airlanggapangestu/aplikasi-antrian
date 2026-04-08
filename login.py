import tkinter as tk
from tkinter import messagebox
from db import cursor
from dashboard import buka_dashboard

def buka_login_admin():
    window = tk.Toplevel()
    window.title("Login Admin")
    window.geometry("300x250")

    tk.Label(window, text="LOGIN ADMIN", font=("Arial", 14, "bold")).pack(pady=20)

    tk.Label(window, text="Username").pack()
    entry_user = tk.Entry(window)
    entry_user.pack()

    tk.Label(window, text="Password").pack()
    entry_pass = tk.Entry(window, show="*")
    entry_pass.pack()

    def login():
        username = entry_user.get()
        password = entry_pass.get()

        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Sukses", "Login berhasil")
            window.destroy()
            buka_dashboard()
        else:
            messagebox.showerror("Error", "Login gagal")

    tk.Button(window, text="Login", command=login).pack(pady=15)