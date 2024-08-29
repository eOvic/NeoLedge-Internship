
import cv2
import numpy as np
from PIL import Image
import pytesseract
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

# Preprocess the image for better OCR results
def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    # Check if the image was successfully loaded
    if image is None:
        raise FileNotFoundError(f"Image file '{image_path}' not found or could not be read.")
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Remove noise
    denoised = cv2.medianBlur(thresh, 3)
    
    # Convert back to PIL Image for pytesseract
    processed_image = Image.fromarray(denoised)
    
    return processed_image

# Perform OCR with confidence levels
def ocr_with_confidence(image):
    # Perform OCR with detailed data output
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    words = data['text']
    confidences = data['conf']
    processed_text = []
    
    for word, confidence in zip(words, confidences):
        # Replace words with low confidence with '####'
        if int(confidence) < 50:  # Adjust confidence threshold as needed
            processed_text.append('####')
        else:
            processed_text.append(word)
    
    return ' '.join(processed_text)

# Load the GPT-2 model and tokenizer
def load_gpt2_model():
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    return tokenizer, model

# Generate text with GPT-2
def generate_text_with_gpt2(context, tokenizer, model):
    # Encode the context into input IDs
    input_ids = tokenizer.encode(context, return_tensors="pt")
    
    # Ensure the input length is within the model's capacity
    max_input_length = 1024  # Maximum length of input tokens for GPT-2
    if input_ids.size(1) > max_input_length:
        input_ids = input_ids[:, -max_input_length:]  # Truncate to max_input_length
    
    # Generate text
    with torch.no_grad():
        output_ids = model.generate(
            input_ids,
            max_new_tokens=50,  # Number of new tokens to generate
            num_return_sequences=1,
            pad_token_id=tokenizer.eos_token_id,
            no_repeat_ngram_size=2,
            temperature=0.7
        )
    
    # Decode the generated text
    generated_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return generated_text

# Fill in missing words using GPT-2
def fill_missing_words(text, tokenizer, model):
    words = text.split()
    
    for i, word in enumerate(words):
        if word == '####':
            # Get context around the missing word
            context_before = ' '.join(words[max(0, i-5):i])  # 5 words before
            context_after = ' '.join(words[i+1:i+6])  # 5 words after
            
            # Generate the missing word using GPT-2
            context = f"{context_before} [MASK] {context_after}"
            filled_word = generate_text_with_gpt2(context, tokenizer, model)
            
            # Replace '####' with the generated word
            words[i] = filled_word
    
    return ' '.join(words)

# Main function
def main(image_path):
    # Load the GPT-2 model and tokenizer once
    tokenizer, model = load_gpt2_model()
    
    # Preprocess the image
    processed_image = preprocess_image(image_path)
    
    # Use pytesseract to do OCR on the preprocessed image
    text_with_confidence = ocr_with_confidence(processed_image)
    
    # Fill in the missing words using GPT-2
    fixed_text = fill_missing_words(text_with_confidence, tokenizer, model)
    
    print("Fixed Text:\n", fixed_text)

# Path to your image
image_path = '/content/figure-65.png'

# Run the main function
if __name__ == "__main__":
    main(image_path)
