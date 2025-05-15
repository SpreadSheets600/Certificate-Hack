import cv2
import pytesseract
import numpy as np


text_to_remove = ['Subhrajit', 'Pal']

image = cv2.imread('output_images/page_1.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
boxes = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DICT)

mask = np.zeros(image.shape[:2], dtype=np.uint8)

for i in range(len(boxes['text'])):
    if (
        int(boxes['conf'][i]) > 60
        and boxes['text'][i].strip()
        and any(
            remove_text.lower() in boxes['text'][i].lower()
            for remove_text in text_to_remove
        )
    ):
        (x, y, w, h) = (
            boxes['left'][i],
            boxes['top'][i],
            boxes['width'][i],
            boxes['height'][i],
        )
        mask[y : y + h, x : x + w] = 255

result = cv2.inpaint(image, mask, inpaintRadius=5, flags=cv2.INPAINT_TELEA)

cv2.imwrite('output.jpg', result, [cv2.IMWRITE_JPEG_QUALITY, 100])

cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()
