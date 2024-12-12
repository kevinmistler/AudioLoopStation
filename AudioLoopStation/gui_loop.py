import tkinter as tk
import tkinter.ttk as ttk
from tkdial import Dial
from gui_track import GuiTrack


class GuiLoop(ttk.Frame):
    '''
    this class is part of View
    '''
    def __init__(self, parent, labelLoopName, controller,
                 beatsPerMeasure=4,
                 originalBeatsPerMinute=140,
                 originalLoopLength=-1,
                 numberOfTracks=4):
        '''
        GuiLoop constructor
        '''
        super().__init__(parent)

        #################
        # Variables
        #################
        self.controller = controller
        self.beatsPerMeasure = beatsPerMeasure

        self.originalLoopLength = originalLoopLength
        self.modifiedLoopLength = self.originalLoopLength

        self.originalBeatsPerMinute = originalBeatsPerMinute
        self.modifiedBeatsPerMinute = self.originalBeatsPerMinute

        self.progBarRunning = False
        self.progDialRunning = False

        # in milliseconds between beats
        if self.originalBeatsPerMinute == -1:
            self.pauseBetweenBeats = -1
        else:
            self.pauseBetweenBeats = int(
                60 / self.modifiedBeatsPerMinute * 1000)

        self.loopName = ""

        ###################
        # UI Components
        ###################
        self.LabelName = tk.Label(self, text=labelLoopName, font=("Arial", 15),
                                  justify=tk.CENTER)

        # dictionary that holds GuiTrack objects
        # Ex:
        # self.trackCollection.update({self.nextTrackNumber : self.track})
        # if track is deleted, track's attribute self.isTrackDeleted = True
        self.trackCollection = {}

        self.nextTrackNumber = 1
        self.nextTrackRow = 2

        self.recordBtn = ttk.Button(self, text="Record",
                                    state=tk.NORMAL,
                                    command=lambda:
                                    self.controller.record(self, self.loopName)
                                    )

        self.playBtn = ttk.Button(self, text="Play All Tracks",
                                  command=lambda:
                                  self.controller.playLoop(self, self.loopName)
                                  )

        self.stopBtn = ttk.Button(self, text="Stop All Tracks",
                                  command=lambda:
                                  self.controller.stopLoop(self, self.loopName)
                                  )

        self.volumeScale = ttk.Scale(self, orient=tk.VERTICAL)

        self.progBar = ttk.Progressbar(self, orient=tk.HORIZONTAL,
                                       mode="determinate")

        # end of progDial gets updated to loop length later on the program
        self.progDial = Dial(self, text="Sec: ", start=0, end=10000,
                             state=tk.DISABLED, integer=True)

        ############
        # GUI LAYOUT
        ############
        # this is how many rows we are reserving for tracks
        rowsReservedForTracks = 100

        # row 0
        self.LabelName.grid(column=0, row=0, columnspan=6, sticky="ew", padx=0,
                            pady=10)

        # row 1
        self.volumeScale.grid(column=5, row=1,
                              rowspan=5 + rowsReservedForTracks,
                              sticky="ns")

        # row (1 + rowsReservedForTracks)
        self.progBar.grid(column=3,
                          row=1 + rowsReservedForTracks,
                          columnspan=2,
                          sticky="ew")

        # row (2 + rowsReservedForTracks)
        self.progDial.grid(column=3, row=2 + rowsReservedForTracks, rowspan=4,
                           columnspan=2, sticky="w", padx=30)

        # row (3 + rowsReservedForTracks) TO (5 + rowsReservedForTracks)
        self.recordBtn.grid(column=1, row=3 + rowsReservedForTracks,
                            columnspan=2, sticky="ew")
        self.playBtn.grid(column=1,
                          row=4 + rowsReservedForTracks,
                          columnspan=2,
                          sticky="ew")
        self.stopBtn.grid(column=1,
                          row=5 + rowsReservedForTracks,
                          columnspan=2,
                          sticky="ew")

    def updateLoopName(self, loopName):
        '''
        this function updates the loop name
        '''
        self.loopName = loopName

    def setOriginalLength(self, length):
        '''
        this function sets the original loop length which is used for progDial
        '''
        # length is in milliseconds
        self.originalLoopLength = length
        self.modifiedLoopLength = self.originalLoopLength

        # this sets progDial end - 0 to this number to go full circle
        # end is converted into seconds
        self.progDial.configure(end=self.originalLoopLength / 1000)

    def setOriginalBeatsPerMinute(self, bpm):
        '''
        this function sets the original beats per minute
        '''
        self.originalBeatsPerMinute = bpm
        self.modifiedBeatsPerMinute = self.originalBeatsPerMinute

        # in milliseconds between beats
        self._updatePauseBetweenBeats()

    def updateBeatsPerMinute(self, bpm):
        '''
        this function updates the beats per minute and related
        as of 3Dec24 this functionality is not used
        '''
        self._updateBeatsPerMinute(bpm)
        self._updatePauseBetweenBeats()
        self._updateLoopLength()

    def _updateBeatsPerMinute(self, bpm):
        '''
        this function updates the beats per minute
        '''
        self.modifiedBeatsPerMinute = bpm

    def _updatePauseBetweenBeats(self):
        '''
        this function updates the length of pauses between beats
        '''
        self.pauseBetweenBeats = int(60 / self.modifiedBeatsPerMinute * 1000)

    def _updateLoopLength(self):
        '''
        this function updates the loop length
        as of 3Dec24 this functionality is not used
        '''
        self.modifiedLoopLength = (self.originalLoopLength /
                                   self.modifiedBeatsPerMinute *
                                   self.originalBeatsPerMinute)

        # this sets progDial end - 0 to this number to go full circle
        # end is converted into seconds
        self.progDial.configure(end=self.modifiedLoopLength / 1000)

    def updateRecordBtnState(self, new_text="Recording", event=None):
        '''
        function updates RECORD button text and state when the initial loop
        is recorded
        :param event:
        :return:
        '''
        if self.recordBtn['text'] != new_text:
            self.recordBtn.config(text=new_text)
        else:
            self.recordBtn.config(text="Record")

    def addTrackToGui(self):
        '''
        1) add a track to gui
        2) add it to the collection
        :return:
        '''
        self.track = GuiTrack(gui_loop=self,
                              trackNumber=self.nextTrackNumber,
                              controller=self.controller)

        self.track.grid(row=self.nextTrackRow, columnspan=5, sticky="new")

        # add new GuiTrack object to collection
        self.trackCollection.update({self.nextTrackNumber: self.track})
        self.nextTrackRow += 1
        self.nextTrackNumber += 1

    def removeAllTracksfromGui(self, ):
        '''
        remove all tracks from gui and reset data members
        :return:
        '''
        for track in self.trackCollection.keys():
            # destroy() function destroys GuiTrack widget
            self.trackCollection[track].destroy()

        self.trackCollection = {}
        self.nextTrackRow = 2
        self.nextTrackNumber = 1

    def startProgressBar(self, num=0):
        '''
        this function starts the progress bar
        '''
        self.progBarRunning = True
        self.updateProgBar(num)

    def startProgressDial(self, num=0):
        '''
        this function starts the progress dial
        '''
        self.progDialRunning = True
        # Splits dial to 36 increments
        self.updateProgDial(num, (self.originalLoopLength / 1000) / 36)

    def startAllTracks(self):
        '''
        this function starts all tracks - this affects gui ONLY
        '''
        for track in self.trackCollection.values():
            if not track.isTrackDeleted:
                track.playTrack()

    def updateProgBar(self, curProgressValue):
        '''
        this function updates the progress bar
        '''
        if self.progBarRunning:
            if curProgressValue >= 100:
                curProgressValue = (curProgressValue - 100 +
                                    100 / self.beatsPerMeasure)
            else:
                curProgressValue += 100 / self.beatsPerMeasure
            self.progBar['value'] = curProgressValue

            # waits some time and then increases the bar
            self.after(self.pauseBetweenBeats, self.updateProgBar,
                       int(curProgressValue))

    def updateProgDial(self, curProgressValue, dialIncrement, i=0):
        '''
        this function updates the progress dial
        '''

        if self.progDialRunning:
            # to go a full circle, there are 36 steps
            # see startProgressDial()
            if i == 36:
                for track in self.trackCollection.values():
                    if not track.isTrackDeleted:
                        if track.isTrackPlaying:
                            self.controller.playTrack(track, track.gui_loop)
                curProgressValue = dialIncrement
                i = 1
            else:
                curProgressValue += dialIncrement
                i += 1

            self.progDial.set(curProgressValue)

            # waits some time and then increases the dial
            self.after(int(dialIncrement * 1000), self.updateProgDial,
                       curProgressValue, dialIncrement, i)

    def stopAllTracks(self, event=None):
        '''
        this function stops all tracks - gui ONLY
        '''
        for track in self.trackCollection.values():
            if track.isTrackPlaying:
                track.stopTrack()

    def stopProgressBar(self):
        '''
        this function stops the progress bar
        '''
        self.progBarRunning = False

    def stopProgressDial(self):
        '''
        this function stops the progress dial
        '''
        self.progDialRunning = False

    def setVolume(self, event=None):
        '''
        this function sets the volume
        as of 3Dec24 this functionality is not used
        '''
        pass

    def resetVisualization(self):
        '''
        this function resets the visualization
        '''
        self.progBar['value'] = 0
        self.progDial.set(0)
        self.recordBtn.config(state=tk.NORMAL)
        self.update_idletasks()

    def isAnyTrackPlaying(self) -> bool:
        '''
        checks if any track in trackCollection is playing
        :return: true if any track in trackCollection is playing;
        false otherwise
        '''
        for track in self.trackCollection.values():
            if track.isTrackPlaying:
                return True

        return False

    def trackCollectionStatus(self):
        '''
        prints trackCollectionStatus
        goes track by track and tells whether track is deleted and or playing
        :return:
        '''
        output = str()
        for track in self.trackCollection.keys():
            output += (
                "Track" +
                (
                    str(track) +
                    " - isTrackDeleted: " +
                    str(self.trackCollection[track].isTrackDeleted) +
                    ", isTrackPlaying - " +
                    str(self.trackCollection[track].isTrackPlaying) + "\n"
                )
                )
        print(output)
