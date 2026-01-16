"""
PostWhisperAccuracyPipeline (Gemini Edition)
Cleans, translates, and normalizes Whisper transcriptions using Gemini 2.0 Flash.
"""

from google import genai
import sys
import os
import time

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import GEMINI_API_KEY

class PostWhisperAccuracyPipeline:
    def __init__(self, known_entities=None):
        """
        known_entities example:
        {
            "name": "Aysha Saheera",
            "college": "KMCT Institute of Emerging Technology and Management"
        }
        """
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is missing from configuration.")
        
        # Initialize the new GenAI Client
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        
        # Using gemini-flash-latest alias
        self.model_id = "gemini-flash-latest" 
        self.known_entities = known_entities or {}

    def process(self, whisper_text, detected_language):
        """
        Processes raw transcription text through Gemini for:
        - Translation to English (if not already)
        - Grammar and spelling correction
        - Medical term normalization
        - Proper noun protection (using known_entities)
        """
        if not whisper_text:
            return ""

        entities_context = "\n".join([f"- {k}: {v}" for k, v in self.known_entities.items()])
        
        prompt = f"""
        You are an expert medical transcriptionist and language expert.
        
        TASK:
        Clean and normalize the following medical transcription.
        
        RULES:
        1. Translate to English if the input is in another language.
        2. Fix all spelling and grammar errors.
        3. Normalize medical shorthand (e.g., "bp high" -> "blood pressure is high").
        4. PROTECT the following known entities:
        {entities_context}
         Ensure these specific names and details are spelled exactly as provided above.
        5. Return ONLY the cleaned English text. No explanations.

        INPUT TEXT:
        "{whisper_text}"

        CLEANED TEXT:
        """

        max_retries = 2
        base_delay = 10

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt
                )
                # Basic cleaning of response in case models adds quotes
                cleaned_text = response.text.strip().replace('"', '')
                return cleaned_text
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    if attempt < max_retries - 1:
                        wait_time = base_delay * (2 ** attempt)
                        print(f"⚠️ Quota exceeded. Retrying accuracy correction in {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                
                print(f"Warning: Gemini-based accuracy pipeline failed: {e}")
                # Fallback to raw text if API fails
                return whisper_text
        
        return whisper_text

if __name__ == "__main__":
    # Test
    pipeline = PostWhisperAccuracyPipeline(known_entities={"name": "Aysha Saheera"})
    test_text = "My name is aisha sahara and i have chest pain undu"
    print(f"Original: {test_text}")
    print(f"Processed: {pipeline.process(test_text, 'en')}")
