import os
import csv

from PIL import Image, ImageDraw, ImageFont

os.makedirs("generated", exist_ok=True)

with open("names.csv", "r") as file:
    names = csv.reader(file)

    for row in names:
        name = row[0]

        print(f"Generating Certificate For ~ {name}")

        img = Image.open("certificates/C5.png")
        draw = ImageDraw.Draw(img)

        font_path = "fonts/RougeScript-Regular.ttf"
        font = ImageFont.truetype(font_path, 100)

        img_width, img_height = img.size
        bbox = draw.textbbox((0, 0), name, font=font)
        x = (img_width - (bbox[2] - bbox[0])) / 2
        y = 650

        draw.text((x, y), name, font=font, fill=(0, 0, 0))

        filename = f"generated/Certificate {name}.png"
        img.save(filename)

print("Certificates enerated Successfully.")
