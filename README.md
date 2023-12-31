# Audio Processing Tool for Audible/ACX

This Python script allows you to process a folder of raw audio files (in the .mp3 format) to meet Audible/ACX requirements. It applies dynamic range compression, normalization, limiting, and adjusts the RMS level to a target value using the PyDub library.

Audiobooks should be recorded in 16 bit / 44.1 kHz wav file format, which is considered CD quality and is best for archiving. When you are ready to upload your files, they must be saved as a 192kbps mp3.

This code formats your final recordings in mono rather than stereo for a uniform listener experience.

## Prerequisites

Before using this tool, make sure you have the following prerequisites installed:

- Python 3.x
- PyDub library (install using `pip install pydub`)

## Usage

1. Place your raw audio files (in .mp3 format) in a folder called `raw`. You can customize the directory name if needed.

2. Open the `audio_processing.py` script in a code editor or IDE.

3. Configure the desired target RMS level (`target_rms_db`) in the script. You can adjust this value as needed to meet Audible/ACX requirements. The recommended target RMS level for ACX is -23 dB.

4. Run the script using the following command:
```bash
   python audio_processing.py
```

The script will process each .mp3 file in the `raw` directory, apply dynamic range compression, normalization, limiting, and adjust the RMS level to the specified target.

5. The processed audio files will be saved in the `processed` directory with the same file names.

## Notes

- You can adjust the compression threshold and ratio in the `compress_dynamic_range` function call in the script to further customize the processing. However, make sure the resulting audio still meets Audible/ACX requirements.

- Make sure to back up your original audio files before running the script, as it will overwrite them with the processed versions.

- Double-check Audible/ACX requirements and guidelines for any additional specifications.

Enjoy using this tool to prepare your audio files for Audible/ACX!

For more information about Audible/ACX requirements, visit [ACX Audio Submission Requirements](https://www.acx.com/help/acx-audio-submission-requirements/201456300).

