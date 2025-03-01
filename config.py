# config.py
import os

class Config:
    INPUT_DIR = "data/input_cvs"
    OUTPUT_DIR = "data/processed_data"
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # No default value to avoid hardcoding
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    EXTRACTION_PROMPT = """
    Extract the following information from this CV text in JSON format:
    - Personal Information (name, email, phone)
    - Education History (degree, institution, year)
    - Work Experience (company, role, duration, responsibilities)
    - Skills
    - Projects
    - Certifications
    
    Text: {cv_text}
    """