from google import genai
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import GEMINI_API_KEY

if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found.")
    sys.exit(1)

client = genai.Client(api_key=GEMINI_API_KEY)

# Print models to console
print("--- AVAILABLE MODELS ---")
try:
    for m in client.models.list():
        print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {str(e)}")
print("------------------------")
