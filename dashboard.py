import tkinter as tk
from tkinter import ttk
from db import cursor, db

def buka_dashboard():
    window = tk.Toplevel()
    window.title("Dashboard Admin")
    window.geometry("700x400")

    tk.Label(window, text="DASHBOARD ANTRIAN", font=("Arial", 16, "bold")).pack(pady=10)

    # TABLE
    columns = ("id", "kode", "status")
    tree = ttk.Treeview(window, columns=columns, show="headings")

    tree.heading("id", text="ID")
    tree.heading("kode", text="Kode")
    tree.heading("status", text="Status")

    tree.pack(fill="both", expand=True)

    # LOAD DATA
    def load_data():
      for row in tree.get_children():
          tree.delete(row)

      cursor.execute("SELECT id, kode_antrian, status FROM antrian")
      for row in cursor.fetchall():
          tree.insert("", "end", values=row)

      # AUTO REFRESH tiap 3 detik (3000 ms)
      window.after(3000, load_data)

    load_data()

    # UPDATE STATUS
    def panggil():
        selected = tree.focus()
        if not selected:
            return

        data = tree.item(selected)["values"]
        cursor.execute("UPDATE antrian SET status='dipanggil' WHERE id=%s", (data[0],))
        db.commit()
        load_data()

    def selesai():
        selected = tree.focus()
        if not selected:
            return

        data = tree.item(selected)["values"]
        cursor.execute("UPDATE antrian SET status='selesai' WHERE id=%s", (data[0],))
        db.commit()
        load_data()

    # DELETE
    def hapus():
        selected = tree.focus()
        if not selected:
            return

        data = tree.item(selected)["values"]
        cursor.execute("DELETE FROM antrian WHERE id=%s", (data[0],))
        db.commit()
        load_data()

    # BUTTONS
    frame = tk.Frame(window)
    frame.pack(pady=10)

    tk.Button(frame, text="Panggil", command=panggil).grid(row=0, column=0, padx=5)
    tk.Button(frame, text="Selesai", command=selesai).grid(row=0, column=1, padx=5)
    tk.Button(frame, text="Hapus", command=hapus).grid(row=0, column=2, padx=5)