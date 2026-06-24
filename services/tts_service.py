from gtts import gTTS
import io
import streamlit as st

def speak_text(raw_text):
    """
    Compiles raw markdown strings into clean audio file memory bytes for immediate playback.
    """
    try:
        # Strip structural markdown noise away before audio streaming synthesis
        clean_text = raw_text.replace("**", "").replace(">", "").replace("- ", "").replace("###", "")
        
        tts = gTTS(text=clean_text, lang='en', slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        
        # Render the audio widget instantly with autoplay
        st.audio(fp, format="audio/mp3", autoplay=True)
        return True
    except Exception as e:
        st.error(f"Text-to-Speech generation timed out: {str(e)}")
        return False