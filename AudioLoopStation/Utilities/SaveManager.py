import os
import json
import pathlib
import re


class SaveManager:
    def __init__(self):
        self._app_root = pathlib.Path(__file__).parent.parent.parent
        self._save_dir = self._app_root / '.save'
        self._track_dir = self._save_dir / 'tracks'
        self._loop_dir = self._save_dir / 'loops'
        self._saved_loops = set()
        self._saved_tracks = set()
        self._makedirs()
        self._update_saved_files()

    def get_loop_options(self):
        self._update_saved_files()
        regex = re.compile('[a-zA-Z0-9_ ]+.json')
        options_list = []
        for loop in self._saved_loops:
            loop_name = regex.search(loop).group()
            options_list.append(loop_name[:-5])  # Removes .json from loop
        return options_list

    def get_track_options(self):
        self._update_saved_files()
        regex = re.compile('[a-zA-Z0-9_ ]+.json')
        options_list = []
        for track in self._saved_tracks:
            track_name = regex.search(track).group()
            options_list.append(track_name[:-5])  # Removes .json from track
        return options_list

    def save(self, obj_type: str, save_obj):
        """Saves loop and track objects into json files.
           Loops are saved in .save/loops
           Tracks are saved in .save/tracks

        Args:
            obj_type (str): Two acceptable values: "loop" or "track"
            save_obj (LoopChannel or Track): A LoopChannel or Track object
        """
        save_name = ""
        # save_obj = {}
        if obj_type.lower() == "loop":
            save_name = os.fspath(
                self._loop_dir / f"{save_obj['loop_name']}.json"
                )
        elif obj_type.lower() == "track":
            # TODO: Update to tracks real getObj function
            save_obj = {
                "track_name": "def_track",
                "audio_path": "fake/path/to/nothing.json"
                }
            save_name = os.fspath(
                self._track_dir / f"{save_obj['track_name']}.json"
                )

        if save_name == "":
            print("SAVE ERROR: Invalid ObjType")
            return

        with open(
                save_name, "w"
                ) as file:
            json.dump(save_obj, file)

        self._update_saved_files()

    def load(self, obj_type: str, name: str):
        """Loads a Track of LoopChannel object and returns it.

        Args:
            obj_type (str): Two acceptable values: "loop" or "track"
            name (str): Name of LoopChannel or Track. Ex. "default_loop"

        Returns:
            LoopChannel or Track object
        """
        load_path = ""
        if obj_type == "loop":
            load_path = self._loop_dir / f"{name}.json"
        elif obj_type == "track":
            load_path = self._track_dir / f"{name}.json"
        if load_path == "" or not load_path.exists():
            print(f"LOAD ERROR: Could not find {name} of type {obj_type}")
            return

        loaded_obj = {}
        with open(os.fspath(load_path), "r") as file:
            loaded_obj = json.load(file)

        return loaded_obj

    def _makedirs(self):
        save_dir_str = os.fspath(self._save_dir)
        loop_dir_str = os.fspath(self._loop_dir)
        track_dir_str = os.fspath(self._track_dir)
        if not os.path.exists(save_dir_str):
            os.makedirs(save_dir_str)
            os.makedirs(loop_dir_str)
            os.makedirs(track_dir_str)
        elif not os.path.exists(track_dir_str):
            os.makedirs(track_dir_str)
        elif not os.path.exists(loop_dir_str):
            os.makedirs(loop_dir_str)

    def _update_saved_files(self):
        save_dir = self._app_root / '.save'

        self._saved_loops = set()
        self._saved_tracks = set()
        # update saved loops
        loop_dir = save_dir / 'loops'
        for save_file in loop_dir.iterdir():
            self._saved_loops.add(os.fspath(save_file))

        # # update saved tracks
        track_dir = save_dir / 'tracks'
        for save_file in track_dir.iterdir():
            self._saved_tracks.add(os.fspath(save_file))
