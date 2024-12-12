import re
from loop import LoopChannel as Loop
from Utilities.SaveManager import SaveManager


class Dispatcher:
    '''
    The role of the dispatcher class is manage Audio LoopChannels loaded into
    the application
    '''
    def __init__(self, controller=None):
        self.controller = controller
        self._loops = {}
        self._PLAYING_STRING = "playing"
        self._LOOP_STRING = "loop"
        self._save_manager = SaveManager()

    def load_loop(self, name: str) -> int:
        '''
        Loads audio loop into dispatcher
        :param gui_loop:
        :param name: name of loop
        :return: returns number of added tracks; -1 when couldn't load loop
        '''

        if name in self._loops and self._loops[name][self._PLAYING_STRING]:
            print("Unable to load loop. Need to stop audio first")
            return -1

        loaded_save_obj = self._save_manager.load("loop", name)
        self._loops[name] = {}
        self._loops[name][self._PLAYING_STRING] = False
        self._loops[name][self._LOOP_STRING] = Loop(
            name
            )

        # load tracks into loaded loop
        trackCount = 0
        for path in loaded_save_obj["tracks"]:
            self.add_track(name, path)
            print("Dispatcher: after self.add_track(name, path)")
            trackCount += 1

        return trackCount

    def create_loop(self, name: str) -> None:
        """Saves audio loop using SaveManager

        Args:
            name (str): name of the loop
        """
        new_loop = Loop(name)
        self._save_manager.save("loop", new_loop.get_data())
        self.load_loop(name)    # might need gui_loop

    def save_loop(self, name: str) -> None:
        """_summary_

        Args:
            name (str): _description_
        """
        if name not in self._loops:
            print(f"Unable to save loop. {name} isn't loaded into dispatcher.")

        self._save_manager.save(
            "loop", self._loops[name][self._LOOP_STRING].get_data()
            )

    def play_loop(self, name: str) -> None:
        """Plays audio loop.

        Args:
            name (str): 2 options defined in
                AudioLoopStation/Loop_Constants/constants.py
        """
        if name not in self._loops:
            print(f"ERROR: Unable to play {name}. Load loop before playing...")
            return
        if self._loops[name][self._PLAYING_STRING]:
            print("Loop already playing....")
            return

        self._loops[name][self._LOOP_STRING].play()
        self._loops[name][self._PLAYING_STRING] = True

    def play_track(self, loop_name: str, track_index: int):
        """Plays individual track within an audio loop

        Args:
            loop_name (str): name of audio loop
            track_index (int): index of track within audio loop
        """
        if loop_name not in self._loops:
            print(
                f"ERROR: Unable to play {loop_name}. Load loop first..."
                )
            return
        if (
            track_index <= 0 or
            track_index > len(self.list_tracks(loop_name))
        ):
            print("Track index is out of valid range")
            print(self.list_tracks(loop_name))
            return

        self._loops[loop_name][self._LOOP_STRING].play_track(track_index)

    def stop_track(self, loop_name: str, track_index: int):
        """Stops individual track within an audio loop

        Args:
            loop_name (str): name of audio loop
            track_index (int): index of track within audio loop
        """
        if loop_name not in self._loops:
            print(
                f"ERROR: Unable to stop {loop_name}. Load loop first..."
                )
            return
        if (
            track_index <= 0 or
            track_index > len(self.list_tracks(loop_name))
        ):
            print("Track index is out of valid range")
            return
        self._loops[loop_name][self._LOOP_STRING].stop_track(track_index)

    def add_track(self, name: str, path: str):
        if name not in self._loops:
            print(
                f"ERROR: Unable to add track into {name}. \
                    Loop does not exists..."
                )
            return
        self._loops[name][self._LOOP_STRING].add_track(path)

    def delete_track(self, name: str, track_num: int):
        if name not in self._loops:
            print(
                f"ERROR: Unable to delete track from {name}. \
                    Loop does not exists..."
                )
            return
        self._loops[name][self._LOOP_STRING].delete_track(track_num)

    def toggle_track(self, name: str, track_num: int):
        if name not in self._loops:
            print(
                f"ERROR: Unable to toggle track from {name}. \
                    Loop does not exists..."
                )
            return
        self._loops[name][self._LOOP_STRING].toggle_track(track_num)

    def stop_loop(self, name: str) -> None:
        """Stops audio loop.

        Args:
            name (str): 2 options defined in
                AudioLoopStation/Loop_Constants/constants.py
        """
        if name not in self._loops:
            print("ERROR: Unable to find {name}...")
            return
        if self._loops[name][self._PLAYING_STRING] is None:
            print(f"ERROR: Loop {name} is not playing...")
            return

        self._loops[name][self._LOOP_STRING].stop()
        self._loops[name][self._PLAYING_STRING] = False

    def stop_all(self) -> None:
        for loop in self._loops.keys():
            if self._loops[loop][self._PLAYING_STRING]:
                self._loops[loop][self._LOOP_STRING].stop()
                self._loops[loop][self._PLAYING_STRING] = False

    def start_all(self) -> None:
        for loop in self._loops.keys():
            if not self._loops[loop][self._PLAYING_STRING]:
                self._loops[loop][self._LOOP_STRING].play()
                self._loops[loop][self._PLAYING_STRING] = True

    def list_tracks(self, loop_name: str) -> list[str]:
        """Returns list of all tracks associated with loop matching loop_name
           parameter

        Args:
            loop_name (str): Name of loop loaded into dispatcher

        Returns:
            [str]: List of track names
        """
        if loop_name not in self._loops:
            print(
                f"ERROR: Unable to add track into {loop_name}. \
                    Loop does not exists..."
                )
            return
        regex = re.compile('[a-zA-Z0-9_ ]+.wav')
        track_name_list = []
        for track_obj in self._loops[loop_name][self._LOOP_STRING].tracks:
            if track_obj is not None:
                track_name = regex.search(track_obj.path).group()
                track_name_list.append(track_name[:-4])  # Removes .wav
            else:
                track_name_list.append("")
        return track_name_list

    def list_loaded_loops(self) -> list[str]:
        """returns list of loops loaded into dispatcher

        Returns:
            [str]: list of strings
        """
        loop_list = []
        for key in self._loops.keys():
            loop_list.append(key)
        return loop_list

    def get_loop_length(self, loop_name: str) -> int:
        """Returns loop length

        Args:
            loop_name (str): Name of loaded audio loop

        Returns:
            int: value of loop length. -1 if no loop found
        """
        if loop_name not in self._loops:
            print("ERROR: Unable to find {name}...")
            return -1
        return self._loops[loop_name][self._LOOP_STRING].length

    def change_effects(
            self,
            loop_name: str,
            track_index: int,
            reverse: int,
            pitch: int
            ):
        """Changes the effects of an audio track.

        Args:
            loop_name (str): Name of loaded audio lop
            track_index (int): Index of track within an audio loop [1...n]
            reverse (int): 0 -> not reversed, 1 -> reversed
            pitch (int): 0 -> no shift, 1 -> upshift, 2 -> downshift
        """
        if loop_name not in self._loops:
            print("ERROR: Unable to find {name}...")
            return
        if (
            track_index <= 0 or
            track_index > len(self.list_tracks(loop_name))
        ):
            print("Track index is out of valid range")
            return
        if (
            reverse < 0 or
            reverse > 1 or
            pitch < 0 or
            pitch > 2
        ):
            print("Invalid effect options. Reverse [0,1] Pitch [0,2]")
            return

        self._loops[loop_name][self._LOOP_STRING].change_effects(
            reverse,
            pitch,
            track_index
            )


if __name__ == "__main__":
    import Loop_Constants.constants as constants
    import time
    d = Dispatcher()
    d.create_loop(constants.LOOP1)

    print("Switching to stage 2")
    # Create three more loops and load 1 track into each
    name1, name2, name3 = "drums", "hihats", "synth"
    d.create_loop(name1)
    d.create_loop(name2)
    d.create_loop(name3)
    d.add_track(name1, "../Audio/drums.wav")
    d.add_track(name2, "../Audio/hihats.wav")
    d.add_track(name3, "../Audio/synth.wav")

    print("Start stage 2")
    d.play_loop(name1)
    time.sleep(3)
    d.stop_loop(name1)
    time.sleep(2)
    print("start hihats")
    d.play_loop(name2)
    time.sleep(3)
    d.stop_loop(name2)
    time.sleep(2)
    print("Start synth")
    d.play_loop(name3)
    time.sleep(2)
    d.stop_loop(name3)
    time.sleep(2)
    d.play_loop(name1)
    d.play_loop(name2)
    d.play_loop(name3)
    time.sleep(5)
    d.stop_all()
    print("All stopped")
    time.sleep(2)

    d.add_track(name1, "../Audio/bass.wav")
    d.add_track(name1, "../Audio/chords.wav")
    d.save_loop(name1)
    print(d.list_tracks(name1))
    print(d.list_loaded_loops())

    d.play_track(name1, 3)
    time.sleep(5)
    d.stop_all()
