# 🔑 How to Get a Gemini API Key

To use the **Gemini 1.5 Flash** model (which is stable and fast), you need an API key from Google AI Studio.

## Steps

1.  **Go to Google AI Studio:**
    Open [https://aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) in your browser.

2.  **Sign In:**
    Log in with your Google Account.

3.  **Create API Key:**
    *   Click the blue **"Create API key"** button.
    *   If asked, choose "Create API key in new project".
    *   Copy the generated key (it starts with `AIza...`).

4.  **Update Your Project:**
    *   Open the `.env` file in your project folder (`HealthCare-Assisstant`).
    *   Replace the old key with your new one:
        ```env
        GEMINI_API_KEY=AIzaSyNewKeyHere...
        ```

5.  **Verify:**
    *   Save the `.env` file.
    *   Run `python list_models.py` to confirm `models/gemini-1.5-flash` appears in the list.
