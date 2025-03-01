CV Analysis System
A Python-based system to process CVs (PDF/DOCX), extract key information using OpenAI's API or a basic fallback, and provide an interactive chatbot to query the extracted data.

Features
Extracts personal information, education, work experience, skills, projects, and certifications from CVs.
Supports PDF and DOCX file formats.
Uses OpenAI's GPT-3.5-turbo for advanced extraction (optional) with a fallback to rule-based extraction.
Interactive chatbot to query CV data.
Stores extracted data in JSON format.
Prerequisites
Python 3.8+: Ensure Python is installed on your system.
Tesseract-OCR: Required for PDF text extraction when text isn’t directly extractable.
Windows: Download and install from Tesseract at UB Mannheim. Default path: C:\Program Files\Tesseract-OCR\tesseract.exe.
Linux: sudo apt-get install tesseract-ocr
macOS: brew install tesseract
Git: To clone and manage the repository.
OpenAI API Key (optional): For advanced extraction. Get it from OpenAI Platform. Free tier has strict quotas; a paid plan is recommended for consistent use.
Setup
1. Clone the Repository
bash
Envelopper
Copier
git clone https://github.com/aminerhayem123/technicaltest.git
cd technicaltest
2. Create a Virtual Environment
bash
Envelopper
Copier
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
3. Install Dependencies
bash
Envelopper
Copier
pip install -r requirements.txt
If requirements.txt doesn’t exist yet, install these manually:

bash
Envelopper
Copier
pip install openai pdfplumber pytesseract pillow python-docx
4. Set Up Environment Variables
OpenAI API Key (optional):
Set your API key as an environment variable:
bash
Envelopper
Copier
export OPENAI_API_KEY="your-openai-api-key"  # Linux/macOS
set OPENAI_API_KEY=your-openai-api-key      # Windows
If not set, the system falls back to basic rule-based extraction.
5. Directory Structure
Ensure the following structure exists:

text
Envelopper
Copier
technicaltest/
├── data/
│   ├── input_cvs/       # Place your CV files here (PDF/DOCX)
│   └── processed_data/  # Extracted JSON files will be saved here
├── src/
│   ├── CVChatbot.py
│   ├── CVExtractor.py
│   ├── DocumentProcessor.py
│   └── LLMProcessor.py
├── config.py
├── main.py
└── README.md
Create the data directories if they don’t exist:

bash
Envelopper
Copier
mkdir -p data/input_cvs data/processed_data
Usage
1. Process CVs
Place CV files (e.g., cv.pdf, resume.docx) in data/input_cvs.
Run the main script:
bash
Envelopper
Copier
python main.py
Output: Extracted data will be saved as JSON files in data/processed_data (e.g., cv.json).
2. Run the Chatbot
After processing CVs, the chatbot starts automatically.
Interact with it:
text
Envelopper
Copier
CV Chatbot Ready! Type 'exit' to quit.
Query: What are the skills?
Example queries:
"What’s the name?"
"List the skills."
"Show work experience."
Type exit to quit.
Example main.py
If not already present, create main.py:

python
Envelopper
Copier
import os
from src.document_processor import DocumentProcessor
from src.cv_extractor import CVExtractor
from src.cv_chatbot import CVChatbot
from config import Config

def main():
    os.makedirs(Config.INPUT_DIR, exist_ok=True)
    os.makedirs(Config.OUTPUT_DIR, exist_ok=True)

    processor = DocumentProcessor()
    extractor = CVExtractor()

    for filename in os.listdir(Config.INPUT_DIR):
        file_path = os.path.join(Config.INPUT_DIR, filename)
        try:
            text = processor.process_file(file_path)
            data = extractor.extract_information(text)
            extractor.save_extracted_data(data, os.path.splitext(filename)[0])
            print(f"Processed: {filename}")
        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

    chatbot = CVChatbot()
    chatbot.run()

if __name__ == "__main__":
    main()
Configuration
Edit config.py if needed:

INPUT_DIR: Directory for input CVs.
OUTPUT_DIR: Directory for processed JSON files.
TESSERACT_PATH: Path to Tesseract executable.
EXTRACTION_PROMPT: Customize the prompt for CV extraction.
Troubleshooting
OpenAI API Errors
Quota Exceeded (429): Free tier limits are strict. Set OPENAI_API_KEY to a valid key or rely on the fallback extraction.
No API Key: If unset, the system uses basic rule-based extraction. Check with:
bash
Envelopper
Copier
echo %OPENAI_API_KEY%  # Windows
echo $OPENAI_API_KEY   # Linux/macOS
Tesseract Issues
Not Found: Ensure TESSERACT_PATH in config.py matches your installation. Verify with:
bash
Envelopper
Copier
tesseract --version
GitHub Push Blocked
If you see GH013: Repository rule violations:
Install git-filter-repo:
bash
Envelopper
Copier
pip install git-filter-repo
Remove secrets from history:
bash
Envelopper
Copier
git filter-repo --path __pycache__/ --path config.py --invert-paths --force
Update config.py to use environment variables.
Force push:
bash
Envelopper
Copier
git push -u origin main --force
Contributing
Fork the repository.
Create a branch: git checkout -b feature-name.
Commit changes: git commit -m "Add feature".
Push: git push origin feature-name.
Open a pull request.
License
This project is unlicensed (public domain). Use it freely.

Notes for Your Project
Replace "your-openai-api-key" in the README with instructions rather than a hardcoded value to avoid future GitHub issues.
If you want to fully remove OpenAI dependency, let me know, and I can adapt the README and code for a local model like TinyLLaMA.
Save this as README.md in your project root, commit it, and push it to GitHub after resolving the secret issue. Let me know if you need help testing or refining it further!
