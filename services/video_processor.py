import os
import tempfile
import speech_recognition as sr
from moviepy.editor import VideoFileClip

def extract_video_text(uploaded_video_file):
    """
    Saves video bytes locally, extracts the audio stream as a .wav file,
    and runs a speech-to-text transcription pass.
    """
    # 1. Create a secure temporary directory on your disk
    temp_dir = tempfile.gettempdir()
    video_path = os.path.join(temp_dir, "temp_input_video.mp4")
    audio_path = os.path.join(temp_dir, "extracted_audio.wav")
    
    try:
        # Write the Streamlit upload bytes to disk safely
        with open(video_path, "wb") as f:
            f.write(uploaded_video_file.read())
            
        # 2. Extract the audio track via MoviePy
        video_clip = VideoFileClip(video_path)
        if video_clip.audio is None:
            return "Error: The uploaded video file does not contain an active audio stream track."
            
        video_clip.audio.write_audiofile(audio_path, logger=None)
        video_clip.close()
        
        # 3. Transcribe spoken words to text using SpeechRecognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            # Record the full audio clip length
            audio_data = recognizer.record(source)
            
        # Convert audio waveforms into raw string text lines
        transcribed_text = recognizer.recognize_google(audio_data)
        return transcribed_text
        
    except sr.UnknownValueError:
        return "Error: Speech recognition engine could not understand the audio track dialogue."
    except sr.RequestError as e:
        return f"Error: Transcription service unreachable; {str(e)}"
    except Exception as e:
        return f"Error processing video file elements: {str(e)}"
    finally:
        # 4. Clean up disk files to prevent memory leaks on your Mac
        for path in [video_path, audio_path]:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass