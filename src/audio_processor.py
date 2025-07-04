import os
import tempfile
import json
from io import BytesIO
from pydub import AudioSegment
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
    """
    
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
        # Check if it's bytes data (from recorder) or file object (from uploader)
        if isinstance(audio_file, BytesIO):
            # From audio recorder - already in bytes format
            temp_audio.write(audio_file.getvalue())
        else:
            # From file uploader - get the bytes
            temp_audio.write(audio_file.getvalue())
        temp_audio_path = temp_audio.name
    
    # Convert to wav format if needed
    audio = AudioSegment.from_file(temp_audio_path)
    
    # Normalize audio - adjust volume to a standard level
    normalized_audio = audio.normalize()
    
    # Save the normalized audio
    normalized_path = f"{temp_audio_path}_normalized.wav"
    normalized_audio.export(normalized_path, format="wav")
    
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
