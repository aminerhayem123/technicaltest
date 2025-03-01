import json
import os
from openai import OpenAI
from config import Config

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", Config.OPENAI_API_KEY))

class CVChatbot:
    def __init__(self):
        self.cv_data = self.load_cv_data()
        self.context = []

    def load_cv_data(self):
        cv_data = {}
        output_dir = Config.OUTPUT_DIR
        if not os.path.exists(output_dir) or not os.listdir(output_dir):
            print(f"Warning: No CV data found in {output_dir}. Process some CVs first.")
            return cv_data
        
        for filename in os.listdir(output_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(output_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        cv_data[filename] = json.load(f)
                except json.JSONDecodeError as e:
                    print(f"Error loading {filename}: {e}")
        return cv_data

    def process_query(self, query):
        if not query or not query.strip():
            return {"query": query, "response": "Please provide a valid query.", "status": "error", "details": "Empty or invalid input"}

        if not self.cv_data:
            return {"query": query, "response": "No CV data available.", "status": "error", "details": "Process CVs first."}

        context_str = "\n".join(self.context[-3:])
        prompt = f"""
        You are an expert CV analysis assistant. Analyze:
        {json.dumps(self.cv_data, indent=2)}
        
        Context: {context_str}
        
        Query: "{query}"
        
        Respond in JSON: {{ "query": "<query>", "response": "<answer>", "status": "success/error", "details": "<info>" }}
        """
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            parsed_response = json.loads(response.choices[0].message.content)
            self.context.extend([f"Query: {query}", f"Response: {json.dumps(parsed_response, indent=2)}"])
            return parsed_response
        except Exception as e:
            return {"query": query, "response": "Error processing query", "status": "error", "details": str(e)}

    def run(self):
        print("CV Chatbot Ready! Type 'exit' to quit.")
        if not self.cv_data:
            print("Note: No CV data loaded. Process CVs first.")
        while True:
            query = input("Query: ").strip()
            if query.lower() == 'exit':
                print("Goodbye!")
                break
            response = self.process_query(query)
            print(f"\nStatus: {response['status']}")
            print(f"Response: {response['response']}")
            if response.get('details'):
                print(f"Details: {response['details']}")
            print()