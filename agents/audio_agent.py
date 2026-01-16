import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import os

def record_audio(filename="audio/raw.wav", fs=16000):
    print("🎤 Recording... Press Ctrl+C to stop (Max 30 mins)")
    
    recorded_chunks = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        recorded_chunks.append(indata.copy())

    try:
        # Record for up to 30 minutes (1800 seconds)
        with sd.InputStream(samplerate=fs, channels=1, callback=callback):
            for _ in range(30 * 60 * 10): # Check every 0.1s
                sd.sleep(100)
    except KeyboardInterrupt:
        print("\n✅ Recording stopped manually.")
    
    if not recorded_chunks:
        return

    # Concatenate all chunks
    audio = np.concatenate(recorded_chunks, axis=0)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Save file
    write(filename, fs, audio)
    print(f"✅ Saved to {filename}")

if __name__ == "__main__":
    record_audio()

