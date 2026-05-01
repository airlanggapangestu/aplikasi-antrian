import tkinter as tk
from tkinter import ttk, simpledialog
from db import connect_db


def open_dashboard(nama_admin="Admin"):
    win = tk.Toplevel()
    win.title("Dashboard Admin")
    win.state("zoomed")
    win.configure(bg="#020617")

    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview",
                    background="#0b1220",
                    foreground="white",
                    rowheight=34,
                    fieldbackground="#0b1220",
                    bordercolor="#0b1220")

    style.map("Treeview",
              background=[("selected", "#3b82f6")])

    style.configure("Treeview.Heading",
                    background="#111827",
                    foreground="white",
                    font=("Segoe UI", 10, "bold"))

    def create_btn(parent, text, color, hover, cmd):
        b = tk.Label(parent,
                     text=text,
                     bg=color,
                     fg="white",
                     font=("Segoe UI", 10, "bold"),
                     padx=12,
                     pady=6,
                     cursor="hand2")

        b.bind("<Enter>", lambda e: b.config(bg=hover))
        b.bind("<Leave>", lambda e: b.config(bg=color))
        b.bind("<Button-1>", lambda e: cmd())
        return b

    navbar_wrapper = tk.Frame(win, bg="#020617")
    navbar_wrapper.pack(fill="x", pady=12)

    navbar = tk.Frame(navbar_wrapper,
                      bg="#0f172a",
                      height=72)
    navbar.pack(fill="x", padx=20)
    navbar.pack_propagate(False)

    left_frame = tk.Frame(navbar, bg="#0f172a")
    left_frame.pack(side="left", padx=20)

    tk.Label(left_frame,
             text=f"Hello, {nama_admin}",
             font=("Segoe UI", 16, "bold"),
             fg="white",
             bg="#0f172a").pack(anchor="w")

    tk.Label(left_frame,
             text="Selamat datang kembali 👋",
             font=("Segoe UI", 10),
             fg="#94a3b8",
             bg="#0f172a").pack(anchor="w")

    right_frame = tk.Frame(navbar, bg="#0f172a")
    right_frame.pack(side="right", padx=20)

    search_box = tk.Frame(right_frame,
                          bg="#020617",
                          bd=1,
                          relief="solid")
    search_box.pack(side="left", padx=6)

    search_entry = tk.Entry(search_box,
                            font=("Segoe UI", 11),
                            bg="#020617",
                            fg="white",
                            insertbackground="white",
                            relief="flat",
                            width=30)
    search_entry.pack(ipady=6, ipadx=6)

    container = tk.Frame(win, bg="#020617")
    container.pack(fill="both", expand=True, padx=20, pady=10)

    stats_frame = tk.Frame(container, bg="#020617")
    stats_frame.pack(fill="x", pady=(6, 12))

    for i in range(4):
        stats_frame.columnconfigure(i, weight=1)

    def stat_box(parent, title, color, col):
        frame = tk.Frame(parent, bg="#0f172a", padx=20, pady=18)
        frame.grid(row=0, column=col, padx=8, sticky="nsew")

        tk.Label(frame,
                 text=title,
                 fg="#94a3b8",
                 bg="#0f172a",
                 font=("Segoe UI", 11)).pack(anchor="w")

        value = tk.Label(frame,
                         text="0",
                         fg=color,
                         bg="#0f172a",
                         font=("Segoe UI", 28, "bold"))
        value.pack(anchor="w", pady=(6, 0))

        return value

    total_label = stat_box(stats_frame, "Total", "#38bdf8", 0)
    menunggu_label = stat_box(stats_frame, "Menunggu", "#facc15", 1)
    dipanggil_label = stat_box(stats_frame, "Dipanggil", "#22c55e", 2)
    selesai_label = stat_box(stats_frame, "Selesai", "#60a5fa", 3)

    action_frame = tk.Frame(container, bg="#020617")
    action_frame.pack(fill="x", pady=(0, 10))

    table_frame = tk.Frame(container, bg="#020617")
    table_frame.pack(fill="both", expand=True)

    columns = ("id", "nama", "hp", "nomor", "status")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col.upper())
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True)

    def update_table(data):
        for i in tree.get_children():
            tree.delete(i)

        for row in data:
            tree.insert("", "end", values=row)

        total = len(data)
        menunggu = sum(1 for d in data if d[4] == "menunggu")
        dipanggil = sum(1 for d in data if d[4] == "dipanggil")
        selesai = sum(1 for d in data if d[4] == "selesai")

        total_label.config(text=total)
        menunggu_label.config(text=menunggu)
        dipanggil_label.config(text=dipanggil)
        selesai_label.config(text=selesai)

    def load_data():
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("""
        SELECT antrian.id_antrian, users.nama, users.no_hp, antrian.nomor, antrian.status
        FROM antrian
        JOIN users ON antrian.id_user = users.id_user
        """)

        update_table(cursor.fetchall())

    def search():
        keyword = search_entry.get()

        db = connect_db()
        cursor = db.cursor()

        cursor.execute("""
        SELECT antrian.id_antrian, users.nama, users.no_hp, antrian.nomor, antrian.status
        FROM antrian
        JOIN users ON antrian.id_user = users.id_user
        WHERE users.nama LIKE %s OR antrian.nomor LIKE %s
        """, (f"%{keyword}%", f"%{keyword}%"))

        update_table(cursor.fetchall())

    def edit_status():
        selected = tree.selection()
        if not selected:
            return

        id_antrian = tree.item(selected[0])["values"][0]

        status = simpledialog.askstring("Edit Status", "Masukkan status (menunggu/dipanggil/selesai):")
        if not status:
            return

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("UPDATE antrian SET status=%s WHERE id_antrian=%s",
                       (status, id_antrian))
        db.commit()
        load_data()

    def delete_data():
        selected = tree.selection()
        if not selected:
            return

        id_antrian = tree.item(selected[0])["values"][0]

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM antrian WHERE id_antrian=%s", (id_antrian,))
        db.commit()
        load_data()

    def reset_all():
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM antrian")
        cursor.execute("DELETE FROM users")
        db.commit()
        load_data()

    create_btn(action_frame, "Edit Status", "#22c55e", "#16a34a", edit_status).pack(side="left", padx=5)
    create_btn(action_frame, "Delete", "#ef4444", "#dc2626", delete_data).pack(side="left", padx=5)
    create_btn(action_frame, "Reset", "#f59e0b", "#d97706", reset_all).pack(side="left", padx=5)
    create_btn(right_frame, "Search", "#3b82f6", "#2563eb", search).pack(side="left", padx=6)

    def auto_refresh():
        load_data()
        win.after(3000, auto_refresh)

    load_data()
    auto_refresh()