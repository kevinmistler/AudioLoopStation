import os
from pydub import AudioSegment, playback
import soundfile
import librosa


class LoopChannel:
    def __init__(self, name="default", *args):
        self.name = name

        #   Tracks array that houses all tracks associated with the loop
        self.tracks = []

        #   Creates track objects from args
        for file in args:
            self.tracks.append(Track(file))

        #   The length of the loop in seconds, None if there are no tracks
        self.length = self.tracks[0].get_length()/1000 if self.tracks else None

    def play(self):
        i = 0
        while i < len(self.tracks):
            if self.tracks[i] is not None and self.tracks[i].is_active:
                self.tracks[i].play()
            i = i + 1

    def stop(self):
        i = 0
        while i < len(self.tracks):
            if self.tracks[i] is not None:
                self.tracks[i].stop()
            i = i + 1

    def add_track(self, file):
        self.tracks.append(Track(file))
        if self.length is None:
            self.length = self.tracks[0].get_length()

    #   Overwrite sound files to each track
    def overwrite_track(self, file, track_num):
        real_index = track_num - 1
        self.tracks[real_index] = Track(file)

    def delete_track(self, track_num):
        real_index = track_num - 1
        self.tracks[real_index] = None

    def toggle_track(self, track_num):
        real_index = track_num - 1
        self.tracks[real_index].toggle_activation()

    def get_data(self):
        #   Returns data needed for saving loops
        file_paths = []
        for track in self.tracks:
            if track is not None:
                file_paths.append(track.get_path())
        save_obj = {
            "loop_name": self.name,
            "tracks": file_paths
        }
        return save_obj

    def play_track(self, track_num):
        real_index = track_num - 1
        self.tracks[real_index].play()

    def stop_track(self, track_num):
        real_index = track_num - 1
        self.tracks[real_index].stop()

    def change_effects(self, reverse: int, pitch: int, track_num: int):
        #   Changes the effects of track_num
        real_index = track_num - 1
        self.tracks[real_index].update_effects(reverse, pitch)


class Track:
    def __init__(self, audio):
        self.path = audio
        '''
            The effects attribute is a 2D array that holds the different
            permutations of effects per the following schema:
            [regular track, regular_upshift, regular_downshift],
            [reversed, reversed_upshift, reversed_downshift]
        '''
        self.effects = []
        #   Initial call  to cut down on time switching between effects
        self.create_effects_files()
        #   Flag for if a track is reversed, 0 for no, 1 for yes
        self.reverse = 0
        #   Flag for if a track is pitched up or down.
        #   0 for none, -1 for down, 1 for up.
        self.pitch = 0
        #   Current version of the track set to play, init to original version
        self.track = self.effects[self.reverse][self.pitch]
        self._play_obj = None
        #   Length of the track in milliseconds
        self.length = len(self.track)
        #   Indicates whether track should be played for loop.play method
        self.active = True

    def play(self):
        if self.active is True:
            self._play_obj = playback._play_with_simpleaudio(self.track)

    def stop(self):
        if self._play_obj is not None:
            self._play_obj.stop()

    def toggle_activation(self):
        self.active = not self.active
        if self.active is False:
            self.stop()

    def create_effects_files(self):
        # Create forward track with and without effects
        regular_track = AudioSegment.from_wav(self.path)
        forward_pitch_up = self.create_pitch_shift_up(self.path)
        forward_pitch_down = self.create_pitch_shift_down(self.path)
        forward_array = [regular_track, forward_pitch_up, forward_pitch_down]
        self.effects.append(forward_array)

        # Create reversed track
        reversed_track, reverse_path = self.create_reverse()
        reverse_pitch_up = self.create_pitch_shift_up(reverse_path)
        reverse_pitch_down = self.create_pitch_shift_down(reverse_path)
        reverse_array = [reversed_track, reverse_pitch_up, reverse_pitch_down]
        self.effects.append(reverse_array)

    def create_pitch_shift_up(self, path):
        cut_front = self.path[9:]
        cut_back = cut_front[:-4]

        if path == self.path:
            new_path = f"../Audio/Mods/{cut_back}_upshift.wav"
        else:
            new_path = f"../Audio/Mods/reversed_{cut_back}_upshift.wav"

        if os.path.exists(new_path):
            return AudioSegment.from_wav(new_path)

        #   y is the data, sr is sample rate
        y, sr = librosa.load(path)
        y_high = librosa.effects.pitch_shift(
            y,
            sr=sr,
            n_steps=12,
            bins_per_octave=12
        )
        soundfile.write(new_path, y_high, sr)
        return AudioSegment.from_wav(new_path)

    def create_pitch_shift_down(self, path):
        cut_front = self.path[9:]
        cut_back = cut_front[:-4]

        if path == self.path:
            new_path = f"../Audio/Mods/{cut_back}_downshift.wav"
        else:
            new_path = f"../Audio/Mods/reversed_{cut_back}_downshift.wav"

        if os.path.exists(new_path):
            return AudioSegment.from_wav(new_path)

        #   y is the data, sr is sample rate
        y, sr = librosa.load(path)
        y_high = librosa.effects.pitch_shift(
            y,
            sr=sr,
            n_steps=-12,
            bins_per_octave=12
        )
        soundfile.write(new_path, y_high, sr)
        return AudioSegment.from_wav(new_path)

    def create_reverse(self):
        cut_front = self.path[9:]
        cut_back = cut_front[:-4]
        new_path = f"../Audio/Mods/reverse_{cut_back}.wav"

        if os.path.exists(new_path):
            reverse_track = AudioSegment.from_wav(self.path).reverse()
            return reverse_track, new_path

        reverse_track = AudioSegment.from_wav(self.path).reverse()
        reverse_track.export(new_path, format="wav")

        return reverse_track, new_path

    def change_effects(self, reverse, pitch):
        self.track = self.effects[reverse][pitch]

    def get_length(self):
        return self.length

    def get_path(self):
        return self.path

    def is_active(self):
        return self.active

    def update_effects(self, reverse: int, pitch: int):
        self.track = self.effects[reverse][pitch]
