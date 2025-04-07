import pytesseract
from PIL import Image, ImageDraw, ImageFont
import logging
import os

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'

# Input image path
image_path = 'c1.jpg'

# Text replacement pairs: ("Text to Replace", "Replacement Text")
replace_map = [
    ('Subhrajit', 'Bhag'),
    # Add more as needed
]
# Load image
image = Image.open(image_path)
draw = ImageDraw.Draw(image)

# Use a system font that's likely to exist
font_size = 24

# Create fonts directory if it doesn't exist
fonts_dir = 'fonts'
if not os.path.exists(fonts_dir):
    os.makedirs(fonts_dir)

# Try loading the font from different possible locations
try:
    # Try to use font from local fonts directory
    font = ImageFont.truetype(
        os.path.join(fonts_dir, 'DejaVuSerifCondensed-Italic.ttf'), font_size
    )
except OSError:
    try:
        # Fallback to system font
        if os.name == 'nt':  # Windows
            font = ImageFont.truetype('arial.ttf', font_size)
        else:  # Linux/Mac
            font = ImageFont.truetype(
                'fonts/DejaVuSerifCondensed-Italic.ttf', font_size
            )
    except OSError:
        # Final fallback to PIL's default font
        logging.warning('Could not load specified fonts. Using default font.')
        font = ImageFont.load_default()

# Run OCR
data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

# Track how many replacements were made
replacements_done = 0

# Loop through detected OCR words
for i in range(len(data['text'])):
    word = data['text'][i].strip()
    x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

    for old_text, new_text in replace_map:
        if word == old_text:
            logging.info(
                f"Replacing '{old_text}' with '{new_text}' at position ({x}, {y})"
            )

            # Cover old text (white background — adjust to your image's bg color)
            draw.rectangle([x, y, x + w, y + h], fill='white')

            # Draw new text
            draw.text((x, y), new_text, fill='black', font=font)

            replacements_done += 1
            break  # Move to next word

if replacements_done == 0:
    logging.warning('No matches found to replace.')
else:
    logging.info(f'Total replacements made: {replacements_done}')

# Save the modified image
output_path = 'output_image.png'
image.save(output_path)
logging.info(f'Modified image saved as: {output_path}')
