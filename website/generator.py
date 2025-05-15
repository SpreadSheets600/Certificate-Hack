import os
import csv
import uuid
import qrcode
import sqlite3
import datetime

from PIL import Image, ImageDraw, ImageFont

BASE_URL = "http://dono-03.danbot.host:4753/"
QR_BOX_SIZE = 10

os.makedirs("database", exist_ok=True)
os.makedirs("generated", exist_ok=True)

conn = sqlite3.connect("database/certificates.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS certificates (
    name TEXT NOT NULL,
    id TEXT PRIMARY KEY,
    place TEXT DEFAULT 'Kolkata',
    date TEXT DEFAULT '2025-03-10',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# Generator
with open("names.csv", "r") as file:
    names = csv.reader(file)
    date = "2025-03-10"
    place= "Kolkata"

    for row in names:
        name = row[0]
        certificate_id = str(uuid.uuid4())[:8]
        print(f"Generating For ~ {name} (ID: {certificate_id})")

        img = Image.open("certificates/C4.png")
        draw = ImageDraw.Draw(img)

        font_path = "fonts/RougeScript-Regular.ttf"
        font_path_id = "fonts/Luciole-Regular.ttf"
        font = ImageFont.truetype(font_path, 100)
        id_font = ImageFont.truetype(font_path_id, 30)

        img_width, img_height = img.size
        bbox = draw.textbbox((0, 0), name, font=font)
        x = (img_width - (bbox[2] - bbox[0])) / 2
        y = 480

        draw.text((x, y), name, font=font, fill=(0, 0, 0))

        id_text = f"Certificate ID: {certificate_id}"
        id_bbox = draw.textbbox((0, 0), id_text, font=id_font)
        id_x = img_width - (id_bbox[2] - id_bbox[0]) - 75
        id_y = img_height - 200

        draw.text((id_x, id_y), id_text, font=id_font, fill=(100, 100, 100))

        qr_data = f"{BASE_URL}{certificate_id}"
        qr = qrcode.QRCode(box_size=QR_BOX_SIZE, border=1)
        qr.add_data(qr_data)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        qr_width, qr_height = qr_img.size

        qr_x = id_x + (id_bbox[2] - id_bbox[0] - qr_width) // 2
        qr_y = id_y - qr_height - 15

        img.paste(qr_img, (qr_x, qr_y))

        filename = f"generated/Certificate {name} - {certificate_id}.png"
        img.save(filename)

        cursor.execute(
            "INSERT INTO certificates (name, id, place, date, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, certificate_id, place, date, datetime.datetime.now())
        )
        conn.commit()

conn.close()
print("Certificates Generated, QR Codes Added, And Database Updated.")
