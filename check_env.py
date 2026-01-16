import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

if key:
    print(f"✅ GEMINI_API_KEY is set (Length: {len(key)})")
    if key.startswith("AIza"):
        print("✅ Key format looks correct (starts with AIza)")
    else:
        print("⚠️ Key might be invalid (does not start with AIza)")
else:
    print("❌ GEMINI_API_KEY is NOT set.")
