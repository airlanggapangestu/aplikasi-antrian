import tkinter as tk
from db import connect_db
from admin_dashboard import open_dashboard

def open_login_window():
    win = tk.Toplevel()
    win.title("Login Admin")
    win.geometry("400x350")
    win.configure(bg="#0f172a")

    frame = tk.Frame(win, bg="#1e293b")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=250)

    tk.Label(frame, text="Admin Login",
             font=("Segoe UI", 18, "bold"),
             fg="white", bg="#1e293b").pack(pady=20)

    username = tk.Entry(frame, font=("Segoe UI", 12))
    username.pack(pady=10)

    password = tk.Entry(frame, show="*", font=("Segoe UI", 12))
    password.pack(pady=10)

    def login():
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username.get(), password.get())
        )

        if cursor.fetchone():
            win.destroy()
            open_dashboard()
        else:
            print("Login gagal")

    tk.Button(frame, text="Login", command=login,
              bg="#22c55e", fg="white").pack(pady=20)