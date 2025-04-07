import io
import os

import fitz
from PIL import Image

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def convert_image_to_pdf(image_path, output_pdf):
    image = Image.open(image_path)
    pdf_bytes = io.BytesIO()
    c = canvas.Canvas(pdf_bytes, pagesize=letter)
    width, height = letter
    image = image.convert('RGB')
    image = image.convert('RGB')
    image.thumbnail((width, height), Image.Resampling.LANCZOS)
    img_width, img_height = image.size
    x = (width - img_width) / 2
    y = (height - img_height) / 2
    c.drawInlineImage(image, x, y, img_width, img_height)
    c.showPage()
    c.save()
    with open(output_pdf, 'wb') as f:
        f.write(pdf_bytes.getvalue())
    return output_pdf


def replace_text_in_pdf(input_pdf, output_pdf, search_text, replace_text):
    doc = fitz.open(input_pdf)
    for page in doc:
        text_instances = page.search_for(search_text)
        for inst in text_instances:
            page.draw_rect(inst, color=(1, 1, 1), fill=(1, 1, 1))

            page.insert_text(
                inst.tl, replace_text, fontname='helv', fontsize=12, color=(0, 0, 0)
            )
    doc.save(output_pdf)
    doc.close()


def process_file(file_path, search_text, replace_text):
    filename, ext = os.path.splitext(file_path)
    ext = ext.lower()
    temp_pdf = filename + '_converted.pdf'
    output_pdf = filename + '_modified.pdf'

    if ext in ['.jpg', '.jpeg', '.png']:
        print('Converting image to PDF...')
        convert_image_to_pdf(file_path, temp_pdf)
        input_pdf = temp_pdf
    elif ext == '.pdf':
        input_pdf = file_path
    else:
        raise ValueError('Unsupported file type. Only PDF or image files allowed.')

    print('Replacing text...')
    replace_text_in_pdf(input_pdf, output_pdf, search_text, replace_text)
    print(f'Output saved to: {output_pdf}')


process_file('base/c1_modified.pdf', 'Subhrajit', 'Bhag')
