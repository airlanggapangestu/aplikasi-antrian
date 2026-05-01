import tkinter as tk
from user_window import open_user_window
from admin_login import open_login_window

root = tk.Tk()
root.title("Aplikasi Antrian")
root.state("zoomed")
root.configure(bg="#0f172a")

frame = tk.Frame(root, bg="#0f172a")
frame.pack(fill="both", expand=True)

tk.Label(frame, text="APLIKASI ANTRIAN",
         font=("Segoe UI", 30, "bold"),
         fg="white", bg="#0f172a").pack(pady=50)


def btn(text, color, cmd):
    b = tk.Label(frame, text=text, bg=color, fg="white",
                 font=("Segoe UI", 14, "bold"),
                 width=20, height=2, cursor="hand2")

    b.bind("<Enter>", lambda e: b.config(bg="#334155"))
    b.bind("<Leave>", lambda e: b.config(bg=color))
    b.bind("<Button-1>", lambda e: cmd())

    b.pack(pady=15)


btn("Ambil Antrian", "#22c55e", open_user_window)
btn("Login Admin", "#f59e0b", open_login_window)

root.mainloop()
