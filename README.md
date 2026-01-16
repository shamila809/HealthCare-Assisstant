# Healthcare Assistant

An AI-powered application designed to assist healthcare professionals by recording, transcribing, and generating clinical summaries of medical consultations. This tool leverages OpenAI's Whisper for transcription and Google's Gemini for post-processing accuracy and summarization.

## 🚀 Features

- **Audio Recording**: Captures consultation audio with long-duration support (up to 30 mins).
- **Noise Reduction**: Cleans audio using `noisereduce` and `librosa` for clearer transcription.
- **Accurate Transcription**: Uses OpenAI's Whisper model to transcribe speech to text.
- **Intelligent Correction**: A Post-Whisper Accuracy Pipeline (powered by Gemini) corrects medical terms, protects known entities (names, hospitals), and fixes grammar.
- **Medical Info Extraction**: Extracts structured data (Diseases, Symptoms, Medicines) using `spacy`.
- **Care Suggestions**: Generates rule-based general care advice based on identified conditions.
- **Interactive Editor**: CLI-based tool to review and edit extracted prescriptions before finalizing.
- **Clinical Summarization**: Generates structured clinical notes using Gemini.

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

4.  **Download Spacy Language Model:**
    Required for medical entity extraction.
    ```bash
    python -m spacy download en_core_web_sm
    ```

5.  **Configuration:**
    Create a `.env` file in the root directory and add your Gemini API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## 📋 Usage

The workflow consists of recording, processing, and then interacting with the data.

### Step 1: Record Audio
Run the audio agent to start recording. Press `Ctrl+C` to stop manually.
```bash
python agents/audio_agent.py
```

### Step 2: Transcribe & Summarize
Run the transcription agent to clean audio, transcribe, and generate a summary.
```bash
python agents/transcription_agent.py
```

### Step 3: Extract Medical Data
Extracts structured information (medicines, diseases) from the transcript.
```bash
python agents/medical_extractor.py
```

### Step 4: Generate Care Suggestions
Provides general wellness advice based on the extracted conditions.
```bash
python agents/care_suggestions.py
```

### Step 5: Edit Prescriptions (Optional)
Interactively add, edit, or delete medicines from the extracted list.
```bash
python agents/medicine_cli_editor.py
```

## 📁 Project Structure

```
HealthCare-Assisstant/
├── agents/
│   ├── audio_agent.py                  # Audio recording
│   ├── audio_cleaning_agent.py         # Noise reduction
│   ├── transcription_agent.py          # Transcription pipeline
│   ├── post_whisper_accuracy_pipeline.py # Text correction
│   ├── medical_extractor.py            # Spacy-based entity extraction
│   ├── care_suggestions.py             # Rule-based advice generator
│   ├── medicine_cli_editor.py          # TUI for editing medicines
│   └── summary_agent.py                # Gemini summarization
├── config/
│   └── settings.py                     # Configuration loader
├── audio/                              # Audio files (ignored by git)
├── transcriptions/                     # Generated data (ignored by git)
├── requirements.txt                    # Python dependencies
└── list_models.py                      # Utility to list Gemini models
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
