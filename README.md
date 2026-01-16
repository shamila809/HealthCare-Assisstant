# Healthcare Assistant

An AI-powered application designed to assist healthcare professionals by recording, transcribing, and generating clinical summaries of medical consultations. This tool leverages OpenAI's Whisper for transcription and Google's Gemini for post-processing accuracy and summarization.

## 🚀 Features

- **Audio Recording**: Captures consultation audio with long-duration support (up to 30 mins).
- **Noise Reduction**: Cleans audio using `noisereduce` and `librosa` for clearer transcription.
- **Accurate Transcription**: Uses OpenAI's Whisper model to transcribe speech to text.
- **Intelligent Correction**: A Post-Whisper Accuracy Pipeline (powered by Gemini) corrects medical terms, protects known entities (names, hospitals), and fixes grammar.
- **Clinical Summarization**: Generates structured clinical notes (Symptoms, Duration, Severity, Advice) using Gemini.

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd HealthCare-Assisstant
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration:**
    Create a `.env` file in the root directory and add your Gemini API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## 📋 Usage

The workflow consists of two main stages: Recording and Processing.

### Step 1: Record Audio
Run the audio agent to start recording. Press `Ctrl+C` to stop recording manually.
```bash
python agents/audio_agent.py
```
*Output: Saves the raw audio to `audio/raw.wav`.*

### Step 2: Transcribe & Summarize
Run the transcription agent to clean the audio, transcribe it, and generate a summary.
```bash
python agents/transcription_agent.py
```
*Output:*
- *Cleans audio to `audio/cleaned.wav`*
- *Prints raw Whisper transcription*
- *Prints corrected text (Post-Processing)*
- *Prints final Clinical Summary*

## 📁 Project Structure

```
HealthCare-Assisstant/
├── agents/
│   ├── audio_agent.py                  # Audio recording logic
│   ├── audio_cleaning_agent.py         # Noise reduction
│   ├── transcription_agent.py          # Main processing pipeline
│   ├── post_whisper_accuracy_pipeline.py # Text correction (Gemini)
│   └── summary_agent.py                # Summary generation (Gemini)
├── config/
│   └── settings.py                     # Configuration loader
├── audio/                              # Directory for audio files (generated)
├── requirements.txt                    # Python dependencies
└── list_models.py                      # Utility to list available Gemini models
```

## ⚙️ Dependencies

- `openai-whisper`
- `google-generativeai`
- `sounddevice`
- `scipy`, `numpy`
- `librosa`, `noisereduce`
- `torch`

## 🛡️ License

[Your License Here]
