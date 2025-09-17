import streamlit as st
import soundfile as sf
import numpy as np
import tempfile
from datetime import datetime
from src.audio_length_matcher import proportionally_adjust_pauses

st.title("Audio Length Matcher")

uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "ogg", "flac"])

# Allow decimal input for target length
target_length = st.number_input(
    "Required Output Length (seconds)",
    min_value=0.1,
    step=0.1,
    format="%.2f"
)

if uploaded_file and target_length:
    if st.button("Process Audio"):
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_in:
            temp_in.write(uploaded_file.read())
            temp_in.flush()
            audio_data, samplerate = sf.read(temp_in.name)

            # Get the original file name without extension
            file_name = uploaded_file.name.split('.')[0]
            file_extension = uploaded_file.name.split('.')[-1]

            # Generate a timestamp of the uploaded file
            upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.write(f"File uploaded at: {upload_time}")

            # Process the audio to adjust pauses
            new_audio_data = proportionally_adjust_pauses(audio_data, samplerate, target_length)

            # Save the processed audio in memory, avoiding saving to disk
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_out:
                output_file_path = temp_out.name
                sf.write(output_file_path, new_audio_data, samplerate)
                
                st.success("Audio processed!")

                # Provide the download button for the processed audio file
                with open(output_file_path, "rb") as f:
                    st.download_button(
                        label="Download Output Audio",
                        data=f.read(),
                        file_name=f"{file_name}.{file_extension}",
                        mime=f"audio/{file_extension}"
                    )
