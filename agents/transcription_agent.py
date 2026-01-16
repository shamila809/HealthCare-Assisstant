import whisper
import os
import sys

# Add project root to sys.path to ensure we can import agents module if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.post_whisper_accuracy_pipeline import PostWhisperAccuracyPipeline
from agents.summary_agent import SummaryAgent


def transcribe_audio(input_file="audio/cleaned.wav", model_size="large"):
    """
    Transcribe audio file to English text using OpenAI Whisper.
    
    Args:
        input_file (str): Path to the input audio file.
        model_size (str): Size of the Whisper model to use (tiny, base, small, medium, large).
        
    Returns:
        str: Transcribed English text.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Audio file not found: {input_file}")

    print(f"🔄 Loading Whisper model ('{model_size}')...")
    model = whisper.load_model(model_size)
    
    print(f"🎧 Transcribing '{input_file}' to English...")
    # task="translate" ensures the output is in English regardless of input language
    result = model.transcribe(input_file, task="translate")
    
    transcribed_text = result["text"].strip()
    
    print("✅ Transcription complete:")
    print(f"📝 Raw Whisper: \"{transcribed_text}\"")

    # -------------------------------------------------------
    # Post-Processing Integration
    # -------------------------------------------------------
    print("\nStarting Post-Whisper Accuracy Pipeline...")
    
    # Initialize pipeline (Entities can be passed dynamically in a real app)
    # For now, using default known entities or empty
    pipeline = PostWhisperAccuracyPipeline(known_entities={
        "name": "Aysha Saheera", 
        "college": "KMCT Institute of Emerging Technology and Management"
    })
    
    # Use 'en' as default or detect from whisper result if available (result['language'])
    # Whisper result object has language info: result['language']
    detected_lang = result.get('language', 'en')
    
    final_cleaned_text = pipeline.process(transcribed_text, detected_language=detected_lang)
    
    print("\n✨ Cleaned & Corrected Text:")
    print(f"👉 \"{final_cleaned_text}\"")
    
    # -------------------------------------------------------
    # Summary Generation Integration
    # -------------------------------------------------------
    print("\nGenerating Clinical Summary (Gemini)...")
    try:
        summary_agent = SummaryAgent()
        summary = summary_agent.generate_summary(final_cleaned_text)
        print("\n📝 Final Clinical Summary:")
        print(f"{summary}")
    except Exception as e:
        print(f"Warning: Could not generate summary: {e}")
        summary = None
    
    # Save final cleaned text to file for the medical extractor
    # Ensure transcriptions directory exists
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "transcriptions")
    os.makedirs(output_dir, exist_ok=True)
    
    output_filename = os.path.join(output_dir, "transcription_output.txt")
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(final_cleaned_text)
    print(f"\n💾 Transcription saved to '{output_filename}'")
    
    return final_cleaned_text, summary

if __name__ == "__main__":
    transcribe_audio()
