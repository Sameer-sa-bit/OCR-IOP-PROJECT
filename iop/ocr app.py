from flask import Flask, render_template, request
import os
from PIL import Image
import pytesseract
from werkzeug.utils import secure_filename

# Set Tesseract path (only need to set once)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')  # Using os.path.join for better path handling
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file selected'
        
        file = request.files['file']
        if file.filename == '':
            return 'No file selected'
        
        if file and allowed_file(file.filename):
            # Secure the filename and save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Perform OCR
            try:
                image = Image.open(filepath)
                text = pytesseract.image_to_string(image)
                return render_template('result.html', 
                                    text=text, 
                                    image_path=os.path.join('uploads', filename))
            except Exception as e:
                return f'Error processing image: {str(e)}'
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)