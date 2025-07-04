import os
import tempfile
import json
from io import BytesIO
import soundfile as sf
import numpy as np
from groq import Groq
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Charger la clé API Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialiser le client Groq avec la syntaxe correcte
client = Groq(api_key=GROQ_API_KEY)

def preprocess_audio(audio_file):
    """
    Convert uploaded audio to proper format for processing
    Handles both uploaded files and recorded audio bytes
    (Version sans pydub/audioop, compatible Python 3.13+)
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
        if isinstance(audio_file, BytesIO):
            temp_audio.write(audio_file.getvalue())
        else:
            temp_audio.write(audio_file.getvalue())
        temp_audio_path = temp_audio.name

    # Lire l'audio avec soundfile
    data, samplerate = sf.read(temp_audio_path)
    # Normalisation simple (peak normalization)
    peak = np.abs(data).max()
    if peak > 0:
        data = data / peak
    # Sauvegarder l'audio normalisé
    normalized_path = f"{temp_audio_path}_normalized.wav"
    sf.write(normalized_path, data, samplerate)
    return normalized_path

def transcribe_audio(audio_path):
    """
    Transcribe audio using Groq's Whisper API
    """
    try:
        # Open the audio file
        with open(audio_path, "rb") as audio_file:
            # Create a request to the Groq API avec format simplifié
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3-turbo",
                response_format="text",  # Format simplifié
                temperature=0.0,
                language="fr"
            )
            
            # Clean up temporary files
            try:
                os.remove(audio_path)
            except:
                pass
                
            # Retourner directement le texte
            return transcription
            
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return f"Error: {str(e)}"
