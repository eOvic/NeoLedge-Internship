import cv2
import numpy as np
from PIL import Image
import pytesseract

def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    if image is None:
        raise ValueError(f"Error loading image from path: {image_path}")

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Remove noise
    denoised = cv2.medianBlur(thresh, 3)
    
    # Convert back to PIL Image for pytesseract
    processed_image = Image.fromarray(denoised)
    
    return processed_image

def ocr_with_confidence(image):
    # Perform OCR with detailed data output
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    words = data['text']
    confidences = data['conf']
    processed_text = []
    
    for word, confidence in zip(words, confidences):
        processed_text.append(word)
    
    return ' '.join(processed_text)