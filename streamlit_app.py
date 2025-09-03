import streamlit as st
from pydub import AudioSegment
import tempfile
from src.audio_length_matcher import proportionally_adjust_pauses

st.title("Audio Length Matcher")

uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "ogg", "flac"])
target_length = st.number_input("Required Output Length (seconds)", min_value=1, step=1)

if uploaded_file and target_length:
    if st.button("Process Audio"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_in:
            temp_in.write(uploaded_file.read())
            temp_in.flush()
            audio = AudioSegment.from_file(temp_in.name)
            new_audio = proportionally_adjust_pauses(audio, target_length)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_out:
                new_audio.export(temp_out.name, format="wav")
                st.success("Audio processed!")
                with open(temp_out.name, "rb") as f:
                    st.download_button(
                        label="Download Output Audio",
                        data=f.read(),
                        file_name="output.wav",
                        mime="audio/wav"
                    )
