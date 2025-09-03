from flask import Flask, render_template, request, send_file
import soundfile as sf
import numpy as np
import os
import tempfile

app = Flask(__name__)

# Import the function from your script
from src.audio_length_matcher import proportionally_adjust_pauses

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        audio_file = request.files['audio']
        target_length = float(request.form['length'])
        if not audio_file:
            return 'No file uploaded', 400
        # Save uploaded file to temp
        temp_in = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        audio_file.save(temp_in.name)
        audio_data, samplerate = sf.read(temp_in.name)
        new_audio_data = proportionally_adjust_pauses(audio_data, samplerate, target_length)
        temp_out = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        sf.write(temp_out.name, new_audio_data, samplerate)
        os.unlink(temp_in.name)
        return send_file(temp_out.name, as_attachment=True, download_name='output.wav')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
