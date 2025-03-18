from flask import Flask, render_template, request, send_file, jsonify, url_for
import pytesseract
from PIL import Image
import os
import uuid
from fpdf import FPDF
from docx import Document

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"})

    if file:
        file_ext = file.filename.split(".")[-1]
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], unique_filename)
        file.save(file_path)

        extracted_text = extract_text(file_path)

        return jsonify({
            "text": extracted_text,
            "image_url": url_for("uploaded_file", filename=unique_filename)
        })

def extract_text(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return f"Error processing image: {e}"

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_file(os.path.join(app.config["UPLOAD_FOLDER"], filename))

@app.route("/download/<file_type>", methods=["POST"])
def download_file(file_type):
    text = request.form["text"]
    if not text.strip():
        return "No text available to download", 400

    file_path = os.path.join(UPLOAD_FOLDER, f"extracted_text_{uuid.uuid4().hex[:6]}.{file_type}")

    if file_type == "txt":
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

    elif file_type == "pdf":
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf.output(file_path)

    elif file_type == "docx":
        doc = Document()
        doc.add_paragraph(text)
        doc.save(file_path)

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
