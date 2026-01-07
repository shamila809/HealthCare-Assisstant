# Healthcare Assistant

A modular, agent-based intelligence system designed for healthcare environments. This assistant handles audio recording, cleaning, transcription, and summarization to streamline healthcare workflows.

## Features

- **Audio Agent**: Manages high-quality audio recording and hardware interaction.
- **Audio Cleaning Agent**: Processes raw audio to remove noise and improve clarity for transcription.
- **Transcription Agent**: Converts cleaned audio into accurate text using advanced speech-to-text models.
- **Summary Agent**: Generates structured summaries from transcriptions, focusing on key healthcare-relevant information.
- **Accuracy Pipeline**: A specialized pipeline to evaluate and improve the accuracy of transcriptions post-processing.

## Project Structure

```text
Healthcare Assistant2/
├── agents/             # Core agent logic
│   ├── audio_agent.py
│   ├── audio_cleaning_agent.py
│   ├── transcription_agent.py
│   ├── summary_agent.py
│   └── post_whisper_accuracy_pipeline.py
├── audio/              # Storage for raw and cleaned audio files
├── config/             # Configuration files and environment settings
├── .gitignore          # Git exclusion rules
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ayshusaheera-bit/HealthCare-Assisstant.git
   cd "Healthcare Assistant2"
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory and add your API keys (e.g., for Gemini or Whisper).

## Usage

Each agent can be run independently or integrated into a larger workflow. Refer to the documentation in the `agents/` directory for specific module usage.

## License

[MIT License](LICENSE)
