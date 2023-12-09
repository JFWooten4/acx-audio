from pydub import AudioSegment
from pydub.effects import normalize
import numpy as np
import os

def limiter(audio_segment, threshold=-3.0):
  normalized_audio = normalize(audio_segment)
  limited_audio = normalized_audio.apply_gain(gain_reduction)

  threshold_amplitude = 10 ** (threshold / 20.0) * limited_audio.max_possible_amplitude
  audio_data = np.array(limited_audio.get_array_of_samples())
  audio_data = np.where(audio_data > threshold_amplitude, threshold_amplitude, audio_data)
  audio_data = np.where(audio_data < -threshold_amplitude, -threshold_amplitude, audio_data)

  if limited_audio.sample_width == 2:
    audio_data = audio_data.astype(np.int16)
  elif limited_audio.sample_width == 4:
    audio_data = audio_data.astype(np.int32)

  return limited_audio._spawn(audio_data.tobytes())

def calculate_rms(audio_segment):
  samples = np.array(audio_segment.get_array_of_samples(), dtype=np.float64)
  rms = np.sqrt(np.mean(np.square(samples)))
  rms_db = 20 * np.log10(rms / audio_segment.max_possible_amplitude)
  return rms_db

def adjust_rms_level(audio_segment, target_rms_db):
  current_rms_db = calculate_rms(audio_segment)
  required_gain_db = target_rms_db - current_rms_db
  return audio_segment.apply_gain(required_gain_db)

from pydub.effects import compress_dynamic_range

# Modify here
directory = "raw"
target_rms_db = -18

for filename in os.listdir(directory):
  if filename.endswith(".mp3"):
    file_path = os.path.join(directory, filename)
    
    audio = AudioSegment.from_mp3(file_path)
    audio_mono = audio.set_channels(1)
    audio_mono_44100 = audio_mono.set_frame_rate(44100)

    compressed_audio = compress_dynamic_range(audio_mono_44100, threshold=-20.0, ratio=2.0)
    normalized_audio = normalize(compressed_audio)
    limited_audio = limiter(normalized_audio, -3)
    adjusted_audio = adjust_rms_level(limited_audio, target_rms_db)

    formatted_filename = f"__{filename}"
    adjusted_audio.export(os.path.join(directory, formatted_filename), format="mp3", bitrate="192k")
