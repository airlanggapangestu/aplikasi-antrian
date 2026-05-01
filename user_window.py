import tkinter as tk
from db import connect_db
from display import open_display


# ================== GENERATE NOMOR ==================
def generate_nomor():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("SELECT nomor FROM antrian ORDER BY id_antrian DESC LIMIT 1")
    last = cursor.fetchone()

    if last:
        angka = int(last[0][1:]) + 1
    else:
        angka = 1

    return f"A{angka:03}"


# ================== AMBIL ANTRIAN ==================
def ambil_antrian(nama_entry, hp_entry, label_nomor):
    nama = nama_entry.get().strip()
    hp = hp_entry.get().strip()

    if nama == "" or hp == "":
        label_nomor.config(text="⚠ Isi semua data!", fg="#ef4444")
        return

    db = connect_db()
    cursor = db.cursor()

    # CEK NO HP SUDAH ADA BELUM (YANG MASIH AKTIF)
    cursor.execute("""
    SELECT * FROM users 
    JOIN antrian ON users.id_user = antrian.id_user
    WHERE users.no_hp=%s AND antrian.status != 'selesai'
    """, (hp,))

    if cursor.fetchone():
        label_nomor.config(text="⚠ Nomor sudah ambil antrian!", fg="red")
        return

    # BARU INSERT
    cursor.execute("INSERT INTO users (nama, no_hp) VALUES (%s,%s)", (nama, hp))
    id_user = cursor.lastrowid

    nomor = generate_nomor()

    cursor.execute(
        "INSERT INTO antrian (nomor, status, id_user) VALUES (%s,'menunggu',%s)",
        (nomor, id_user)
    )

    db.commit()

    label_nomor.config(text=nomor, fg="#22c55e")

    nama_entry.delete(0, tk.END)
    hp_entry.delete(0, tk.END)


# ================== BUTTON MODERN ==================
def create_button(parent, text, color, hover, command):
    btn = tk.Label(parent, text=text, bg=color, fg="white",
                   font=("Segoe UI", 12, "bold"),
                   cursor="hand2", padx=20, pady=10)

    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=color))
    btn.bind("<Button-1>", lambda e: command())

    return btn


# ================== UI USER ==================
def open_user_window():
    win = tk.Toplevel()
    win.title("Ambil Antrian")
    win.state("zoomed")
    win.configure(bg="#0f172a")

    # ================= CONTAINER =================
    container = tk.Frame(win, bg="#0f172a")
    container.pack(expand=True)

    # ================= CARD =================
    card = tk.Frame(container, bg="#1e293b", padx=40, pady=30)
    card.pack()

    # ================= TITLE =================
    tk.Label(card,
             text="Ambil Nomor Antrian",
             font=("Segoe UI", 22, "bold"),
             fg="#e2e8f0",
             bg="#1e293b").pack(pady=(0, 10))

    tk.Label(card,
             text="Silakan isi data Anda",
             font=("Segoe UI", 10),
             fg="#94a3b8",
             bg="#1e293b").pack(pady=(0, 20))

    # ================= INPUT =================
    def input_field(label_text):
        tk.Label(card, text=label_text,
                 fg="#cbd5e1", bg="#1e293b").pack(anchor="w")

        entry = tk.Entry(card,
                         font=("Segoe UI", 12),
                         bg="#334155",
                         fg="white",
                         insertbackground="white",
                         relief="flat",
                         width=30)
        entry.pack(pady=(5, 15), ipady=6)
        return entry

    nama_entry = input_field("Nama")
    hp_entry = input_field("No HP")

    # ================= NOMOR =================
    label_nomor = tk.Label(card,
                           text="",
                           font=("Segoe UI", 42, "bold"),
                           fg="#22c55e",
                           bg="#1e293b")
    label_nomor.pack(pady=20)

    # ================= BUTTON WRAPPER =================
    btn_frame = tk.Frame(card, bg="#1e293b")
    btn_frame.pack(pady=10, fill="x")

    # GRID RESPONSIVE
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)

    # ================= BUTTON =================
    btn_ambil = create_button(
        btn_frame,
        "Ambil Antrian",
        "#22c55e",
        "#16a34a",
        lambda: ambil_antrian(nama_entry, hp_entry, label_nomor)
    )
    btn_ambil.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

    btn_display = create_button(
        btn_frame,
        "Lihat Antrian",
        "#3b82f6",
        "#2563eb",
        open_display
    )
    btn_display.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    btn_back = create_button(
        btn_frame,
        "Kembali",
        "#ef4444",
        "#dc2626",
        win.destroy
    )
    btn_back.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="ew")