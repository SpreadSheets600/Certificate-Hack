import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont


def generate_certificates(
    template_img, name_height, names, font_path, font_size, output_dir
):
    font = ImageFont.truetype(font_path, font_size)
    os.makedirs(output_dir, exist_ok=True)

    img_width, img_height = template_img.size

    for name in names:
        img = template_img.copy()
        draw = ImageDraw.Draw(img)

        text_bbox = font.getbbox(name)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        new_x = (img_width - text_width) // 2
        new_y = name_height - (text_height // 2)

        draw.text((new_x, new_y), name, fill='black', font=font)

        img.save(os.path.join(output_dir, f'{name}_certificate.jpg'))

    print('Certificates Generated Successfully!')


if __name__ == '__main__':
    template_path = 'output.jpg'
    csv_file_path = 'names.csv'
    output_dir = 'output'

    template_img = Image.open(template_path).convert('RGB')

    name_height = 323

    df = pd.read_csv(csv_file_path)
    names = df['Name'].tolist()

    font_path = 'fonts/DejaVuSerifCondensed-Italic.ttf'
    font_size = 30

    generate_certificates(
        template_img, name_height, names, font_path, font_size, output_dir
    )
