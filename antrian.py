from db import cursor, db
import datetime

def ambil_antrian():
    today = datetime.date.today()

    cursor.execute("""
    SELECT MAX(nomor_urutan) FROM antrian WHERE tanggal = %s
    """, (today,))
    
    result = cursor.fetchone()
    nomor = result[0] + 1 if result[0] else 1

    kode = f"A{nomor:03d}"

    cursor.execute("""
    INSERT INTO antrian (kode_antrian, nomor_urutan, tanggal, waktu_ambil, status)
    VALUES (%s, %s, %s, NOW(), 'menunggu')
    """, (kode, nomor, today))

    db.commit()

    return kode