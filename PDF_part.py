import image
import pytesseract

print(pytesseract.image_to_string(open('test1.png')))