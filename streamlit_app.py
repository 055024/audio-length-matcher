import streamlit as st
import soundfile as sf
import numpy as np
import tempfile
import os
from datetime import datetime
from src.audio_length_matcher import proportionally_adjust_pauses

# Define your output location
output_dir = '/src/'  # Change this to the path where you want to save the file

# Ensure the directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

st.title("Audio Length Matcher")

uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav", "ogg", "flac"])
target_length = st.number_input("Required Output Length (seconds)", min_value=1, step=1)

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
            
            # Create the output file path with the original file name
            output_file_path = os.path.join(output_dir, f"{file_name}_processed.{file_extension}")
            
            # Write the new audio to the output path
            with open(output_file_path, "wb") as temp_out:
                sf.write(output_file_path, new_audio_data, samplerate)
                st.success("Audio processed!")

                # Display download button with the processed file
                with open(output_file_path, "rb") as f:
                    st.download_button(
                        label="Download Output Audio",
                        data=f.read(),
                        file_name=f"{file_name}_processed.{file_extension}",
                        mime=f"audio/{file_extension}"
                    )
