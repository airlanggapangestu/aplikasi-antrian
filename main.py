import tkinter as tk
from antrian import ambil_antrian
from login import buka_login_admin
from display import buka_display

def buka_antrian():
    kode = ambil_antrian()

    window = tk.Toplevel()
    window.title("Nomor Antrian")
    window.geometry("400x300")

    tk.Label(window, text="Nomor Antrian Anda", font=("Arial", 14)).pack(pady=20)
    tk.Label(window, text=kode, font=("Arial", 30, "bold")).pack(pady=10)
    tk.Label(window, text="Silahkan Menunggu").pack(pady=10)

    tk.Button(window, text="OK", command=window.destroy).pack(pady=20)

root = tk.Tk()
root.title("Aplikasi Antrian")
root.geometry("400x300")

tk.Label(root, text="SELAMAT DATANG", font=("Arial", 16, "bold")).pack(pady=30)

tk.Button(root, text="Ambil Nomor Antrian", width=25, height=2, command=buka_antrian).pack(pady=10)

tk.Button(root, text="Admin Login", width=25, height=2, command=buka_login_admin).pack(pady=10)

tk.Button(root, text="Display Antrian", width=25, height=2, command=buka_display).pack(pady=10)

root.mainloop()