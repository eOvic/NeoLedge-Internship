# NeoLedge-Internship
<h3> app.py</h3>
File Upload:

Allows users to upload image files (png, jpg, jpeg, gif) through a web interface.
Saves the uploaded files in a specified folder.


Image Processing and OCR:

Uses a custom OCR (Optical Character Recognition) module to extract text from the uploaded images.


Text Correction:

Utilizes the Ollama LLM (Language Model) with the "llama3.1" model to correct typos and remove unnecessary whitespace from the extracted text.


Web Interface:

Provides a home page for file upload.
Displays the uploaded image, the raw extracted text, and the corrected text.


Security Features:

Implements file type restrictions and secure filename handling.
Sets a maximum file size limit.


Error Handling:

Provides flash messages for various error conditions (e.g., no file selected).



The application uses Flask for web server functionality, Werkzeug for file handling, Langchain for integrating with the Ollama LLM, and a custom OCR module for text extraction from images.
When a file is uploaded, the app processes it through OCR, corrects the extracted text using the LLM, and then displays both the original and corrected versions to the user.

<h3>Models.py</h3>
Database Model Definition:

Creates a class called Image that inherits from db.Model.
This class represents a table in the database for storing image information.


Table Columns:

id: An integer column that serves as the primary key for each image record.
filename: A string column (maximum 100 characters) to store the filename of the image. It cannot be null.


Serialization Method:

The to_dict() method is defined to convert an Image object into a dictionary.
This method is useful for easily serializing the object data, which can be helpful when sending data as JSON in API responses.



This model allows the application to:

Store information about uploaded images in a database.
Retrieve image information easily.
Serialize image data for use in API responses or other parts of the application that require a dictionary or JSON format.

To use this model in the main application:

You would typically import it in your main app file or route handlers.
Use it to create new records when images are uploaded.
Query the database to retrieve image information as needed.

This model complements the file upload functionality in the main app.py file by providing a way to persistently store metadata about the uploaded images in a database.

<h3>Templates</h3>

This folder contains the base.html and index.html for the frontend. 

