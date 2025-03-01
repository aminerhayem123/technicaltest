import os
from src.document_processor import DocumentProcessor
from src.data_extractor import CVExtractor
from src.chatbot import CVChatbot
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