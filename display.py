import tkinter as tk
from db import connect_db
from gtts import gTTS
from playsound import playsound
import os
import threading

last_called = None


# ================= SUARA NATURAL =================
def speak(text):
    def run():
        try:
            tts = gTTS(text=text, lang='id')
            filename = "voice.mp3"
            tts.save(filename)
            playsound(filename)
            os.remove(filename)
        except:
            print("Gagal play suara")

    threading.Thread(target=run).start()


# ================= DISPLAY =================
def open_display():
    global last_called

    win = tk.Toplevel()
    win.title("Display Antrian")
    win.state("zoomed")
    win.configure(bg="#020617")
    win.attributes("-fullscreen", True)

    frame = tk.Frame(win, bg="#020617")
    frame.pack(fill="both", expand=True)

    # HEADER
    tk.Label(frame,
             text="SISTEM ANTRIAN",
             font=("Segoe UI", 30, "bold"),
             fg="#38bdf8",
             bg="#020617").pack(pady=20)

    # NOMOR
    label_nomor = tk.Label(frame,
                           text="-",
                           font=("Segoe UI", 140, "bold"),
                           fg="#22c55e",
                           bg="#020617")
    label_nomor.pack(pady=10)

    # INFO
    label_info = tk.Label(frame,
                          text="Menunggu panggilan...",
                          font=("Segoe UI", 35, "bold"),
                          fg="white",
                          bg="#020617")
    label_info.pack()

    # INSTRUKSI
    label_instruksi = tk.Label(frame,
                               text="",
                               font=("Segoe UI", 20),
                               fg="#94a3b8",
                               bg="#020617")
    label_instruksi.pack(pady=10)

    # NEXT
    label_next = tk.Label(frame,
                          text="",
                          font=("Segoe UI", 24),
                          fg="#facc15",
                          bg="#020617")
    label_next.pack(pady=30)

    # ================= ANIMASI =================
    current_size = 140
    direction = 1

    def animate():
        nonlocal current_size, direction

        current_size += direction * 2

        if current_size >= 155:
            direction = -1
        elif current_size <= 140:
            direction = 1

        label_nomor.config(font=("Segoe UI", current_size, "bold"))

        win.after(80, animate)

    # ================= UPDATE =================
    def update_display():
        global last_called

        try:
            db = connect_db()
            cursor = db.cursor()

            # nomor dipanggil
            cursor.execute("""
            SELECT nomor FROM antrian 
            WHERE status='dipanggil'
            ORDER BY id_antrian DESC LIMIT 1
            """)
            now = cursor.fetchone()

            # next
            cursor.execute("""
            SELECT nomor FROM antrian 
            WHERE status='menunggu'
            ORDER BY id_antrian ASC LIMIT 3
            """)
            next_data = cursor.fetchall()

        except Exception as e:
            label_info.config(text="Database error!")
            print(e)
            win.after(2000, update_display)
            return

        if now:
            nomor = now[0]

            label_nomor.config(text=nomor)
            label_info.config(text=f"Nomor {nomor} sedang dipanggil")
            label_instruksi.config(text="Silakan menuju loket pelayanan")

            if nomor != last_called:
                speak(f"Nomor {nomor} dipanggil, silakan menuju loket")
                last_called = nomor

        else:
            label_nomor.config(text="-")
            label_info.config(text="Belum ada panggilan")
            label_instruksi.config(text="Silakan menunggu")

        if next_data:
            next_text = "  |  ".join([n[0] for n in next_data])
            label_next.config(text=f"Antrian berikutnya: {next_text}")
        else:
            label_next.config(text="")

        win.after(2000, update_display)

    win.bind("<Escape>", lambda e: win.destroy())

    animate()
    update_display()