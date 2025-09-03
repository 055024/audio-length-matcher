import streamlit as st
import soundfile as sf
import numpy as np
import tempfile
from src.audio_length_matcher import proportionally_adjust_pauses

st.title("Audio Length Matcher")

uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "ogg", "flac"])
target_length = st.number_input("Required Output Length (seconds)", min_value=1, step=1)

if uploaded_file and target_length:
    if st.button("Process Audio"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_in:
            temp_in.write(uploaded_file.read())
            temp_in.flush()
            audio_data, samplerate = sf.read(temp_in.name)
            new_audio_data = proportionally_adjust_pauses(audio_data, samplerate, target_length)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_out:
                sf.write(temp_out.name, new_audio_data, samplerate)
                st.success("Audio processed!")
                with open(temp_out.name, "rb") as f:
                    st.download_button(
                        label="Download Output Audio",
                        data=f.read(),
                        file_name="output.wav",
                        mime="audio/wav"
                    )
