from Utilities.SaveManager import SaveManager
from view import View
from dispatcher import Dispatcher
import Loop_Constants.constants as constants
from recorder import Recorder


class Controller:
    '''
    this class is the Controller in the Model-Control-View architecture
    '''
    def __init__(self):
        # bpm is initially set to 100; the user can later modify it through gui
        self.bpm = 100
        self.recorder = Recorder()  # Initialize the Recorder instance
        self.saveManager = SaveManager()
        self.view = View(self)
        self._dispatcher = Dispatcher(self)
        self._dispatcher.create_loop(constants.LOOP1)
        self._dispatcher.create_loop(constants.LOOP2)

    def main(self):
        '''
        this function starts the mainloop of View
        '''
        self.view.main()

    def load_loop(self, gui_memory, gui_loop, loopName):
        '''
        this function is called when user selects a loop name and clicks a
        load button
        :param gui_loop:
        :param loopName:
        :return:
        '''

        # safety check. prevent further execution if name of the loop doesn't
        # match any of the existing loop names
        if loopName not in self.saveManager.get_loop_options():
            gui_memory.informFailedLoad()
            return

        # tracksToAdd is how many tracks we need to add to GUI
        tracksToAdd = self._dispatcher.load_loop(loopName)

        gui_memory.load()
        # clean up GUI in case there are existing tracks
        gui_loop.removeAllTracksfromGui()

        # update gui_loop original length
        if tracksToAdd > 0:
            gui_loop.setOriginalLength(
                self._dispatcher.get_loop_length(loopName)
                )

        gui_loop.updateLoopName(loopName)

        # controller is telling gui to adding track
        for _ in range(tracksToAdd):
            gui_loop.addTrackToGui()

    def create_loop(self, gui_memory, gui_loop, loopName):
        '''
        this function creates a new loop
        '''
        # safety check. prevent further execution if name matches
        # any of the existing loop names
        if loopName in self.saveManager.get_loop_options():
            gui_memory.informFailedSave()
            return

        # call to dispatcher to create the new loop
        self._dispatcher.create_loop(loopName)

        # update loopName of GuiLoop object
        gui_loop.updateLoopName(loopName)

        # update state of gui_memory
        gui_memory.create()

    def discard_loop(self, gui_memory, gui_loop, loopName):
        '''
        this function discards loop
        '''
        gui_memory.discard()
        gui_loop.removeAllTracksfromGui()

    def save_loop(self, gui_memory, loopName):
        '''
        this function saves loop
        '''
        gui_memory.save()
        self._dispatcher.save_loop(loopName)

    def record(self, gui_loop, loopName: str):
        '''
        Handles recording functionality, including starting/stopping recording,
        managing multiple recordings, and updating GUI state.

        On the first call, it starts the recording process. On the second call,
        it stops the recording, processes the audio, adds it as a track,
        and updates the loop's original length and bpm if it's the first track.
        For subsequent tracks, if the recording length exceeds the original
        loop length, it trims the recording to keep only the portion that
        goes past the original length.

        :param gui_loop: The GUI loop object representing the current loop in
        the interface.
        :param loopName: The name identifying the loop being recorded.
        :return: None
        '''

        if gui_loop.recordBtn['text'] == "Record":
            # First click: start recording
            # Initiate recording of a loop
            self.recorder.start_recording()

            # Update GUI to indicate ongoing recording
            gui_loop.updateRecordBtnState(new_text="Recording")

        elif gui_loop.recordBtn['text'] == "Recording":
            # Second click: stop recording
            # Stop the recording and save the audio file
            recorded_file = self.recorder.stop_recording(
                file_name_prefix="recording"
            )
            if not recorded_file:
                return

            # Add the processed track to the loop
            self._dispatcher.add_track(loopName, recorded_file)

            # Process the recording
            if gui_loop.originalLoopLength == -1:  # First track
                gui_loop.setOriginalLength(
                    self._dispatcher.get_loop_length(loopName)
                    )
            else:  # Not the first track
                # Trim the recording to match the original length criteria
                original_length = gui_loop.originalLoopLength * 1000
                # Convert to ms
                recorded_file = self._trim_to_remainder(
                    recorded_file, original_length
                )

            # Update GUI loop's bpm
            gui_loop.setOriginalBeatsPerMinute(self.bpm)

            # Update the GUI to reset the button state and show the new track
            gui_loop.updateRecordBtnState(new_text="Record")
            gui_loop.addTrackToGui()

    def _trim_to_remainder(self, file_path, original_length):
        '''
        Trims the recorded audio file to keep only the remainder segment
        that extends past the "original length".

        :param file_path: Path to the recorded audio file.
        :param original_length: Original loop length in milliseconds.
        :return: Path to the trimmed audio file.
        '''
        from pydub import AudioSegment

        # Load the audio file
        audio = AudioSegment.from_file(file_path)

        # Calculate the segment to keep
        audio_length = len(audio)  # Length in ms
        if audio_length <= original_length:
            print(
                "Recording is within the original length, no trimming needed.")
            return file_path

        # Calculate the start of the segment to keep
        start_trim = audio_length % original_length

        # Trim the audio
        trimmed_audio = audio[start_trim:]

        # Save the trimmed audio to a new file
        trimmed_file_path = file_path.replace(".wav", "_trimmed.wav")
        trimmed_audio.export(trimmed_file_path, format="wav")
        print(f"Trimmed audio saved to {trimmed_file_path}")

        return trimmed_file_path

    def playTrack(self, gui_track, gui_loop):
        '''
        this function plays a track - engages gui and dispatcher
        '''
        gui_track.playTrack()

        self._dispatcher.play_track(loop_name=gui_loop.loopName,
                                    track_index=gui_track.trackNumber)

    def playLoop(self, gui_loop, loopName: str):
        '''
        this function plays a loop - engages gui and dispatcher
        '''

        if gui_loop.modifiedBeatsPerMinute != self.bpm:
            gui_loop.updateBeatsPerMinute(self.bpm)

        # call to GUI to start progress bar, dial and all non deleted tracks
        gui_loop.startAllTracks()

        # call to dispatcher to start playing the loop
        self._dispatcher.play_loop(loopName)

    def changePlaybackDirectionAndPitch(self, gui_track, gui_loop):
        '''
        this function changes the playback direction and pitch for a track
        within a loop. it gets the file ready to be played
        '''

        playbackDirectionIndex = gui_track.playbackDirection.get()
        pitchIndex = gui_track.pitch.get()

        self._dispatcher.change_effects(
            gui_loop.loopName,
            gui_track.trackNumber,
            playbackDirectionIndex,
            pitchIndex
        )

    def stopTrack(self, gui_track, gui_loop):
        '''
        this function stops a track - engages gui and dispatcher
        '''
        gui_track.stopTrack()
        self._dispatcher.stop_track(gui_loop.loopName, gui_track.trackNumber)

    def deleteTrack(self, gui_track, gui_loop):
        '''
        this function deletes a track - engages gui and dispatcher
        '''
        gui_track.deleteTrack()
        self._dispatcher.delete_track(gui_loop.loopName, gui_track.trackNumber)

    def stopLoop(self, gui_loop, loopName: str):
        '''
        this function stops a loop - engages gui and dispatcher
        '''
        gui_loop.stopAllTracks()
        self._dispatcher.stop_loop(loopName)

    def update_bpm(self, currGuiBeatsPerMinute):
        '''
        as of 3Dec24 this function is not functional
        '''

        self.bpm = currGuiBeatsPerMinute


if __name__ == '__main__':
    app = Controller()
    app.main()
