"""
Summary Agent
Uses Google's Gemini API to generate concise medical summaries from transcribed text.
"""

from google import genai
import sys
import os
import time

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import GEMINI_API_KEY

class SummaryAgent:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing. Please set it in .env or environment variables.")
        
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        # Using gemini-flash-latest alias (Likely maps to 1.5 Flash or stable version)
        self.model_id = 'gemini-flash-latest'



    def generate_summary(self, text):
        """
        Generates a concise clinical summary from the provided text.
        """
        if not text:
            return "No text provided for summary."

        prompt = f"""
        You are a healthcare assistant.
        
        Create a clear and structured medical summary from the transcription below.
        
        Include:
        - Symptoms
        - Duration
        - Severity
        - Advice / Medicines (if mentioned)
        - further conseltation details (if mentioned)
        
        Use simple English.
        Do not add new information.
        
        Text: "{text}"
        
        Clinical Note:
        """
        
        # Increased retries to handle long rate limit pauses (up to 60s)
        max_retries = 2
        base_delay = 10

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                # Check for 429 Resource Exhausted
                # The error message from SDK usually contains the code or status
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = base_delay * (2 ** attempt)
                        print(f"⚠️ Quota exceeded. Retrying summary generation in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                
                return f"Error generating summary: {e}"

if __name__ == "__main__":
    # Test block
    agent = SummaryAgent()
    sample_text = "My name is Aysha Sahira and I have had a severe headache since yesterday. I also feel a bit feverish."
    print("Generating summary...")
    print(agent.generate_summary(sample_text))
