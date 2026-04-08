import tkinter as tk
from db import cursor

def buka_display():
    window = tk.Toplevel()
    window.title("Display Antrian")
    window.geometry("600x400")

    tk.Label(window, text="PANGGILAN ANTRIAN", font=("Arial", 16, "bold")).pack(pady=10)

    label_sekarang = tk.Label(window, text="-", font=("Arial", 30, "bold"), fg="red")
    label_sekarang.pack(pady=10)

    tk.Label(window, text="Antrian Berikutnya", font=("Arial", 12)).pack()

    frame_list = tk.Frame(window)
    frame_list.pack(pady=10)

    label_list = []

    for i in range(5):
        lbl = tk.Label(frame_list, text="-", font=("Arial", 14))
        lbl.pack()
        label_list.append(lbl)

    # =========================
    # LOAD DATA
    # =========================
    def load_display():
        # Sedang dipanggil
        cursor.execute("""
        SELECT kode_antrian FROM antrian
        WHERE status='dipanggil'
        ORDER BY nomor_urutan ASC LIMIT 1
        """)
        result = cursor.fetchone()

        if result:
            label_sekarang.config(text=result[0])
        else:
            label_sekarang.config(text="-")

        # Antrian berikutnya
        cursor.execute("""
        SELECT kode_antrian FROM antrian
        WHERE status='menunggu'
        ORDER BY nomor_urutan ASC LIMIT 5
        """)
        results = cursor.fetchall()

        for i in range(5):
            if i < len(results):
                label_list[i].config(text=results[i][0])
            else:
                label_list[i].config(text="-")

        # AUTO REFRESH
        window.after(2000, load_display)

    load_display()