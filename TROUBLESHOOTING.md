# 🛠️ Troubleshooting Guide

This document tracks known issues and solutions for the Healthcare Assistant project.

## 🔴 Critical Issues

### 1. Whisper Model Download Error (SHA256 Mismatch)
**Error Message:**
> `RuntimeError: Model has been downloaded but the SHA256 checksum does not match.`

**Cause:**
The "large" Whisper model is approximately **3GB**. If the internet connection is unstable or interrupted during download, the file becomes corrupted. When the script tries to load it, it checks the file integrity (checksum), finds it invalid, and throws this error.

**Solutions:**
*   **Option A (Retry):** Delete the corrupted file manually from `C:\Users\<User>\.cache\whisper\` and run the script again.
*   **Option B (Switch Model):** Use a smaller model like `base` (~150MB) or `medium` (~1.5GB) which are faster to download and less prone to interruption.
    *   *To switch:* Edit `agents/transcription_agent.py` and change `model_size="large"` to `model_size="base"`.

### 2. Google GenAI SDK Deprecation
**Error Message:**
> `All support for the google.generativeai package has ended.`

**Solution:**
The project has been migrated to the new `google-genai` SDK. Ensure you have installed the latest dependencies:
```bash
pip install google-genai
```

### 3. Missing API Key
**Error Message:**
> `GEMINI_API_KEY is not set in environment or .env file`

**Solution:**
Create a `.env` file in the project root with:
```env
GEMINI_API_KEY=AIzaSy...
```

## ⚠️ Performance Notes
*   **"large" model:** Very accurate but slow; requires ~3GB download and ~10GB RAM.
*   **"base" model:** Very fast, less accurate; requires ~150MB download and <1GB RAM.
