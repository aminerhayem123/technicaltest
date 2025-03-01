import json
import os
from config import Config
from openai import OpenAI
import time

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", Config.OPENAI_API_KEY))

class CVExtractor:
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or Config.OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
        self.rate_limit_delay = 1

    def extract_information(self, text):
        if not text:
            return None

        prompt = Config.EXTRACTION_PROMPT.format(cv_text=text)
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert CV analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=2000
            )
            time.sleep(self.rate_limit_delay)
            response_text = response.choices[0].message.content
            return json.loads(response_text)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return None
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return None

    def save_extracted_data(self, data, base_filename):
        if not data:
            print(f"No data to save for {base_filename}")
            return

        output_filename = f"{base_filename}.json"
        output_path = os.path.join(self.output_dir, output_filename)

        if os.path.exists(output_path):
            print(f"Skipping {output_filename} - already exists")
            return

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            print(f"Saved data to {output_filename}")
        except Exception as e:
            print(f"Error saving {output_filename}: {e}")