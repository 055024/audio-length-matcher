import sys
import numpy as np
import soundfile as sf

# Usage: python audio_length_matcher.py <input_audio> <target_length_seconds> <output_audio>

def proportionally_adjust_pauses(audio_data, samplerate, target_length):
    # Detect silence (simple threshold-based)
    abs_audio = np.abs(audio_data)
    silence_thresh = 0.01  # Adjust as needed
    min_silence_len = int(0.3 * samplerate)  # 300 ms
    silent_ranges = []
    start = None
    for i, sample in enumerate(abs_audio):
        if sample < silence_thresh:
            if start is None:
                start = i
        else:
            if start is not None and i - start >= min_silence_len:
                silent_ranges.append((start, i))
            start = None
    original_length = len(audio_data)
    pause_durations = [end - start for start, end in silent_ranges]
    total_pause = sum(pause_durations)
    length_diff = int(target_length * samplerate) - original_length
    if total_pause == 0 or length_diff == 0:
        return audio_data
    new_pause_durations = [max(0, int(p + (p/total_pause)*length_diff)) for p in pause_durations]
    output = []
    last_end = 0
    for idx, (start, end) in enumerate(silent_ranges):
        output.extend(audio_data[last_end:start])
        output.extend(np.zeros(new_pause_durations[idx], dtype=audio_data.dtype))
        last_end = end
    output.extend(audio_data[last_end:])
    return np.array(output, dtype=audio_data.dtype)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python audio_length_matcher.py <input_audio> <target_length_seconds> <output_audio>")
        sys.exit(1)
    input_audio = sys.argv[1]
    target_length = float(sys.argv[2])
    output_audio = sys.argv[3]
    audio_data, samplerate = sf.read(input_audio)
    new_audio_data = proportionally_adjust_pauses(audio_data, samplerate, target_length)
    sf.write(output_audio, new_audio_data, samplerate)
    print(f"Exported: {output_audio}")
