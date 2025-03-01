import openai
import time
from config import Config

class LLMProcessor:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.rate_limit_delay = 1  # Seconds to avoid rate limits

    def process(self, prompt):
        """Process a prompt using OpenAI's API."""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Use "gpt-4" or newer if available
                messages=[
                    {"role": "system", "content": "You are an expert CV analysis assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Low temperature for structured output
                max_tokens=2000
            )
            time.sleep(self.rate_limit_delay)
            return response.choices[0].message.content
        except openai.OpenAIError as e:
            return f"OpenAI API error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"