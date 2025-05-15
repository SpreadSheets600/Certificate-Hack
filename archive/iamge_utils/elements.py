import cv2
import pytesseract

image_path = 'base/c2.jpg'
image = cv2.imread(image_path)

if image is None:
    raise FileNotFoundError('File Not Found')

image = cv2.resize(image, (1000, int(image.shape[0] * 1000 / image.shape[1])))

rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'
data = pytesseract.image_to_data(rgb, output_type=pytesseract.Output.DICT)

for i in range(len(data['text'])):
    if int(data['conf'][i]) > 60:
        x, y, w, h = (
            data['left'][i],
            data['top'][i],
            data['width'][i],
            data['height'][i],
        )
        text = data['text'][i]
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            image,
            f'{text} ({x},{y})',
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 0, 0),
            1,
        )

height, width = image.shape[:2]
center_y = height // 2
center_x = width // 2

cv2.line(image, (0, center_y), (width, center_y), (0, 0, 255), 2)
cv2.line(image, (center_x, 0), (center_x, height), (0, 0, 255), 2)

cv2.putText(
    image,
    f'({center_x}, {center_y})',
    (center_x + 10, center_y + 20),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.7,
    (0, 0, 255),
    2,
)

cv2.imshow('Detected Text With Positions', image)

cv2.waitKey(0)
cv2.destroyAllWindows()
