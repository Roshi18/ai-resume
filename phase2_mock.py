import streamlit as st
import speech_recognition as sr
import sounddevice as sd
import wavio
import tempfile
import os
import numpy as np

st.title("🎤 AI Interview Simulator (Phase 2)")
st.write("This is Phase 2: Mock Interview Recording. Questions will be integrated after Phase 1.")

roles = ["Data Analyst", "Web Developer", "AI Engineer", "Cybersecurity Analyst"]
role = st.selectbox("Select Role", roles)

if role:
    st.success(f"You selected: {role}")

# Function to record audio
def record_audio(duration=10, samplerate=44100):
    st.info("🎙️ Recording... Speak now!")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    st.success("✅ Recording complete!")
    return recording, samplerate

# Speech-to-text using SpeechRecognition
def recognize_speech(file_path):
    r = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = r.record(source)
    try:
        text = r.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, could not understand your speech."
    except sr.RequestError:
        return "Speech recognition service unavailable."

# --- UI Buttons ---
if "recording" not in st.session_state:
    st.session_state.recording = None

if st.button("🎙️ Start Recording"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        recording, samplerate = record_audio(duration=7)  # record for 7 seconds
        wavio.write(tmp_file.name, recording, samplerate, sampwidth=2)
        st.session_state.recording = tmp_file.name

if st.button("⏹️ Stop Recording"):
    if st.session_state.recording:
        text = recognize_speech(st.session_state.recording)
        st.subheader("🗣️ Recognized Speech:")
        st.write(text)
        os.remove(st.session_state.recording)
        st.session_state.recording = None
    else:
        st.warning("No active recording found.")
