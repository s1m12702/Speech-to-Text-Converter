import streamlit as st
import speech_recognition as sr
import tempfile
import os
import time


# Function to recognize speech from an audio file
def recognize_from_file(file, progress):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file) as source:
            # Update progress for processing stage
            st.info("Processing audio file...")
            for i in range(10):  # Simulate progress
                time.sleep(0.1)
                progress.progress(50 + (i + 1) * 5)  # Update from 50% to 100%

            audio = recognizer.record(source)  # Read the entire audio file
            text = recognizer.recognize(audio)
            progress.progress(100)  # Complete progress bar
            return f"File Transcription:\n{text}"
    except sr.UnknownValueError:
        return "Could not understand the audio in the file."
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Function to handle live speech recognition
def recognize_speech_live():
    recognizer = sr.Recognizer()
    st.info("Listening... (say 'stop' to end)")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        while True:
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize(audio).lower()
                if text == "stop":
                    return "Listening stopped."
                else:
                    st.write(f"You said: {text}")
            except sr.UnknownValueError:
                st.warning("Could not understand the audio. Please try again.")
            except Exception as e:
                return f"An error occurred: {str(e)}"


# Streamlit UI
st.title("Speech-to-Text Converter")

# File upload with combined progress bar
st.subheader("Transcribe Audio File")
uploaded_file = st.file_uploader("Choose an audio file", type=["wav"])
if uploaded_file is not None:
    progress = st.progress(0)  # Single progress bar for both stages

    # Save the uploaded file temporarily with progress update
    file_size = len(uploaded_file.getbuffer())
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
        buffer_size = 1024 * 1024  # Read in chunks of 1MB
        uploaded_file.seek(0)
        bytes_written = 0

        while chunk := uploaded_file.read(buffer_size):
            temp_file.write(chunk)
            bytes_written += len(chunk)
            progress.progress(min(int(bytes_written / file_size * 50), 50))  # Update from 0% to 50%

        temp_file_path = temp_file.name

    # Recognize speech from the file with continued progress bar
    transcription = recognize_from_file(temp_file_path, progress)
    st.text_area("Transcription Result", transcription, height=200)

    # Clean up temporary file
    os.remove(temp_file_path)

# Live speech recognition
st.subheader("Live Speech Recognition")
if st.button("Start Live Listening"):
    transcription_live = recognize_speech_live()
    st.text(transcription_live)
