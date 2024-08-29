from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import os
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import sys

# Add the AI directory to the Python path
sys.path.append('/home/chahine/Desktop/workspace/NeoLedge 4/AI')

# Import the OCR module
import OCR  # type: ignore

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

# Function to correct typos using LLaMA 3
def correct_text_with_llama(text):
    ollama_llm = Ollama(model="llama3.1")
    prompt_template = PromptTemplate(
        input_variables=["text"],
        template="Correct typos and remove unnecessary whitespaces: {text}",
    )
    chain = LLMChain(llm=ollama_llm, prompt=prompt_template)
    corrected_text = chain.run(text=text)
    return corrected_text

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Preprocess the image and perform OCR
            processed_image = OCR.preprocess_image(file_path)
            extracted_text = OCR.ocr_with_confidence(processed_image)
            
            # Correct the extracted text using LLaMA 3
            corrected_text = correct_text_with_llama(extracted_text)
            
            return render_template(
                'index.html',
                filename=filename,
                text=extracted_text,
                corrected_text=corrected_text
            )
    return render_template('index.html')

@app.route('/display/<filename>')
def display_image(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run()
