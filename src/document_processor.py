import pytesseract
from PIL import Image
import pdfplumber
from docx import Document
from config import Config

class DocumentProcessor:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_PATH
        
    def process_pdf(self, file_path):
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text += extracted_text + "\n"
                    else:
                        img = page.to_image().original
                        text += pytesseract.image_to_string(img) + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error processing PDF {file_path}: {e}")
            return None

    def process_docx(self, file_path):
        try:
            doc = Document(file_path)
            text = "\n".join(para.text for para in doc.paragraphs if para.text.strip())
            return text.strip()
        except Exception as e:
            print(f"Error processing DOCX {file_path}: {e}")
            return None

    def process_file(self, file_path):
        if file_path.lower().endswith('.pdf'):
            return self.process_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return self.process_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")