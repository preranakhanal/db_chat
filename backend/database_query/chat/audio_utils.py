import whisper
from TTS.api import TTS
import tempfile
import os
import soundfile as sf

# Speech-to-Text using Whisper
def transcribe_audio(audio_file_path, model_name="base"):
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_file_path)
    return result["text"]

# Text-to-Speech using Coqui TTS
def text_to_speech(text, output_path=None, tts_model="tts_models/en/ljspeech/tacotron2-DDC"):
    tts = TTS(tts_model)
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd)
    tts.tts_to_file(text=text, file_path=output_path)
    return output_path
