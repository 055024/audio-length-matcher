import sys
from pydub import AudioSegment, silence
import numpy as np

# Usage: python audio_length_matcher.py <input_audio> <target_length_seconds> <output_audio>

def proportionally_adjust_pauses(audio, target_length):
    # Detect silent chunks
    silent_ranges = silence.detect_silence(audio, min_silence_len=300, silence_thresh=audio.dBFS-16)
    silent_ranges = [(start, end) for start, end in silent_ranges]
    
    original_length = len(audio)
    pause_durations = [end - start for start, end in silent_ranges]
    total_pause = sum(pause_durations)
    
    # Calculate required change
    length_diff = target_length*1000 - original_length
    if total_pause == 0 or length_diff == 0:
        return audio
    
    # Proportionally adjust each pause
    new_pause_durations = [max(0, int(p + (p/total_pause)*length_diff)) for p in pause_durations]
    
    # Build new audio
    output = AudioSegment.empty()
    last_end = 0
    for idx, (start, end) in enumerate(silent_ranges):
        output += audio[last_end:start]
        silence_chunk = AudioSegment.silent(duration=new_pause_durations[idx])
        output += silence_chunk
        last_end = end
    output += audio[last_end:]
    return output

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python audio_length_matcher.py <input_audio> <target_length_seconds> <output_audio>")
        sys.exit(1)
    input_audio = sys.argv[1]
    target_length = float(sys.argv[2])
    output_audio = sys.argv[3]
    audio = AudioSegment.from_file(input_audio)
    new_audio = proportionally_adjust_pauses(audio, target_length)
    new_audio.export(output_audio, format="wav")
    print(f"Exported: {output_audio}")
