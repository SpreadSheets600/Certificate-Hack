import fitz  # PyMuPDF
import os

pdf_path = 'base/cirtificate_udemy_1.pdf'
output_folder = 'output_images'
os.makedirs(output_folder, exist_ok=True)

doc = fitz.open(pdf_path)

for page_number in range(len(doc)):
    page = doc.load_page(page_number)
    pix = page.get_pixmap(dpi=300)
    output_path = os.path.join(output_folder, f"page_{page_number+1}.png")
    pix.save(output_path)
    print(f"Saved: {output_path}")
