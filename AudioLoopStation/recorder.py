import sounddevice as sd
from scipy.io.wavfile import write
import wave
import os


class Recorder:
    def __init__(self, output_directory="../Audio", sample_rate=44100):
        self.output_directory = output_directory
        self.sample_rate = sample_rate
        self.is_recording = False
        self.recorded_data = []

    def start_recording(self):
        """Starts audio recording."""
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
        self.is_recording = True
        self.recorded_data = []
        print("Recording started...")
        sd.default.samplerate = self.sample_rate
        sd.default.channels = 1
        self.stream = sd.InputStream(callback=self._callback)
        self.stream.start()

    def _callback(self, indata, frames, time, status):
        """Callback function for streaming audio input."""
        if self.is_recording:
            self.recorded_data.append(indata.copy())

    def stop_recording(self, file_name_prefix="recording"):
        """Stops audio recording and saves the file with a unique name."""
        import numpy as np
        import time

        if not self.is_recording:
            print("No recording in progress.")
            return None
        print("Recording stopped. Saving audio file...")
        self.is_recording = False
        self.stream.stop()
        self.stream.close()

        # Combine recorded data into a single array
        audio_data = np.concatenate(self.recorded_data, axis=0)

        # Convert audio data to 16-bit PCM format
        if audio_data.dtype != np.int16:
            max_value = np.iinfo(np.int16).max
            audio_data = (audio_data * max_value).astype(np.int16)

        # Ensure the output directory exists
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        # Generate a unique filename based on timestamp
        timestamp = int(time.time() * 1000)
        file_name = f"{file_name_prefix}_{timestamp}.wav"
        output_path = os.path.join(self.output_directory, file_name)

        # Save the audio file
        write(output_path, self.sample_rate, audio_data)
        print(f"Audio saved as {output_path}")
        return output_path

    def get_audio_length(self, file_path):
        """Returns the length of the audio file in milliseconds."""
        with wave.open(file_path, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            duration = (frames / float(rate)) * 1000  # Convert seconds to ms
            return duration
