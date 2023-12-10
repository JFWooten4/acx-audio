from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
from pydub.utils import make_chunks
import numpy as np
import os

# Modify config here
INPUT_DIR = "raw"
TARGET_RMS_Db = -18

PROCESSED_DIR = "processed"
CHUNK_LEN_MS = 560000

def limitAudio(audioSeg, threshold=-3.0):
  threshold_amplitude = 10 ** (threshold / 20.0) * audioSeg.max_possible_amplitude
  data = np.array(audioSeg.get_array_of_samples())
  data = np.where(data > threshold_amplitude, threshold_amplitude, data)
  data = np.where(data < -threshold_amplitude, -threshold_amplitude, data)
  match audioSeg.sample_width:
    case 2:
      data = data.astype(np.int16)
    case 4:
      data = data.astype(np.int32)
  return audioSeg._spawn(data.tobytes())

def calcRMS(audioSeg):
  samples = np.array(audioSeg.get_array_of_samples(), dtype=np.float64)
  rms = np.sqrt(np.mean(np.square(samples)))
  if rms == 0:
    return -np.inf
  RMS_Db = 20 * np.log10(rms / audioSeg.max_possible_amplitude)
  return RMS_Db

def fixRMS(audioSeg, TARGET_RMS_Db):
  current_RMS_Db = calcRMS(audioSeg)
  required_gain_db = TARGET_RMS_Db - current_RMS_Db
  return audioSeg.apply_gain(required_gain_db)

def fixChunk(audioSeg):
  mono = audioSeg.set_channels(1)
  mono44k = mono.set_frame_rate(44100)
  compressed = compress_dynamic_range(mono44k, threshold=-20.0, ratio=2.0)
  normalized = normalize(compressed)
  limited = limitAudio(normalized, -3)
  adjusted = fixRMS(limited, TARGET_RMS_Db)
  # Any extra processing here
  return adjusted

if not os.path.exists(PROCESSED_DIR):
  os.makedirs(PROCESSED_DIR)

for filename in os.listdir(INPUT_DIR):
  if filename.endswith(".mp3"):
    path = os.path.join(INPUT_DIR, filename)
    audio = AudioSegment.from_mp3(path)
    chunks = make_chunks(audio, CHUNK_LEN_MS)
    processedChunks = [fixChunk(chunk) for chunk in chunks]
    combinedChunks = sum(processedChunks, AudioSegment.silent(duration=0))
    combinedChunks.export(os.path.join(PROCESSED_DIR, filename), format="mp3", bitrate="192k")
# add .wav case here or just sub in above
