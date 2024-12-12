import tkinter as tk
import tkinter.ttk as ttk
import Loop_Constants.constants as constants


class GuiTrack(ttk.Frame):
    '''
    this class is part of View
    '''
    def __init__(self,
                 gui_loop,
                 trackNumber,
                 controller):
        '''
        GuiTrack constructor
        '''
        super().__init__(gui_loop)

        gridPlacementRow = 0

        self.trackNumber = trackNumber
        self.isTrackDeleted = False
        self.isTrackPlaying = False
        self.controller = controller
        self.gui_loop = gui_loop

        # if this is first track, put these labels - used for radio buttons
        if self.trackNumber == 1:
            self.FLabel = ttk.Label(self, text="F")
            self.RLabel = ttk.Label(self, text="R")
            self.LLabel = ttk.Label(self, text="L")
            self.NLabel = ttk.Label(self, text="N")
            self.HLabel = ttk.Label(self, text="H")

        self.spaceLabel = ttk.Label(self, text="   ")

        self.trackName = ttk.Label(self, text="Track" + str(trackNumber),
                                   width=7)

        self.trackStatus = ttk.Label(self, text=constants.trackStatus[2][0],
                                     foreground=constants.trackStatus[2][1],
                                     width=17)

        # playback direction radio buttons
        self.playbackDirection = tk.IntVar()
        self.playbackDirection.set(0)
        self.playFwdBtn = ttk.Radiobutton(self,
                                          variable=self.playbackDirection,
                                          value=0)
        self.playRevBtn = ttk.Radiobutton(self,
                                          variable=self.playbackDirection,
                                          value=1)

        def changePlaybackDirection(var, index, mode):
            '''
            this function is called whenever a user selects
            a different radio button
            :param var:
            :param index:
            :param mode:
            :return:
            '''
            self.controller.changePlaybackDirectionAndPitch(self, gui_loop)

        self.playbackDirection.trace_add("write",
                                         callback=changePlaybackDirection)

        # pitch radio buttons
        self.pitch = tk.IntVar()
        self.pitch.set(0)

        self.pitchNormalBtn = ttk.Radiobutton(self,
                                              variable=self.pitch,
                                              value=0)
        self.pitchLowBtn = ttk.Radiobutton(self,
                                           variable=self.pitch,
                                           value=1)
        self.pitchHighBtn = ttk.Radiobutton(self,
                                            variable=self.pitch,
                                            value=2)

        def changePitch(var, index, mode):
            '''
            this function is called whenever a user selects
            a different radio button
            :param var:
            :param index:
            :param mode:
            :return:
            '''
            self.controller.changePlaybackDirectionAndPitch(self, gui_loop)

        self.pitch.trace_add("write", callback=changePitch)

        self.trackPlayBtn = ttk.Button(self, text="Play",
                                       command=lambda: self.controller.
                                       playTrack(self, self.gui_loop))

        self.trackStopBtn = ttk.Button(self, text="Stop",
                                       command=lambda: self.controller.
                                       stopTrack(self, self.gui_loop),
                                       state=tk.DISABLED)

        self.trackDeleteBtn = ttk.Button(self, text="Delete",
                                         command=lambda: self.controller.
                                         deleteTrack(self, self.gui_loop))

        ############
        # GUI LAYOUT
        ############

        if self.trackNumber == 1:
            self.FLabel.grid(column=2, row=gridPlacementRow, sticky="ew")
            self.RLabel.grid(column=3, row=gridPlacementRow, sticky="ew")
            self.LLabel.grid(column=5, row=gridPlacementRow, sticky="ew")
            self.NLabel.grid(column=6, row=gridPlacementRow, sticky="ew")
            self.HLabel.grid(column=7, row=gridPlacementRow, sticky="ew")
            gridPlacementRow += 1

        self.trackName.grid(
            column=0,
            row=gridPlacementRow,
            sticky="ew",
            padx=5
            )
        self.trackStatus.grid(column=1, row=gridPlacementRow, sticky="ew")

        self.playFwdBtn.grid(column=2, row=gridPlacementRow, sticky="ew")
        self.playRevBtn.grid(column=3, row=gridPlacementRow, sticky="ew")

        self.spaceLabel.grid(column=4, row=gridPlacementRow, sticky="ew")

        self.pitchLowBtn.grid(column=5, row=gridPlacementRow, sticky="ew")
        self.pitchNormalBtn.grid(column=6, row=gridPlacementRow, sticky="ew")
        self.pitchHighBtn.grid(column=7, row=gridPlacementRow, sticky="ew")

        self.trackPlayBtn.grid(column=8, row=gridPlacementRow, sticky="ew")
        self.trackStopBtn.grid(column=9, row=gridPlacementRow, sticky="ew")
        self.trackDeleteBtn.grid(column=10, row=gridPlacementRow, sticky="ew")

    def playTrack(self):
        '''
        this function
        1) updates gui to show that the track is playing
        2) updates gui state
        :return:
        '''
        # if no other track is playing, start progressBar and progressDial
        if not self.gui_loop.isAnyTrackPlaying():
            self.gui_loop.startProgressBar()
            self.gui_loop.startProgressDial()

        self.isTrackPlaying = True

        statusStr = str(constants.trackStatus[3][0] + " | " +
                        constants.playbackDirectionChar[self.playbackDirection.
                        get()] + " | " + constants.pitchChar[self.pitch.get()])

        self.trackStatus.configure(text=statusStr,
                                   foreground=constants.trackStatus[3][1])
        self.trackPlayBtn.configure(state=tk.DISABLED)
        self.trackStopBtn.configure(state=tk.NORMAL)

    def stopTrack(self):
        '''
        this function
        1) updates gui to show that the track is stopped
        2) updates gui state
        :return:
        '''
        self.isTrackPlaying = False

        # if no track is playing, stop progressBar and progressDial
        if not self.gui_loop.isAnyTrackPlaying():
            self.gui_loop.stopProgressBar()
            self.gui_loop.stopProgressDial()
            self.gui_loop.resetVisualization()

        self.trackStatus.configure(text=constants.trackStatus[2][0],
                                   foreground=constants.trackStatus[2][1])
        self.trackPlayBtn.configure(state=tk.NORMAL)
        self.trackStopBtn.configure(state=tk.DISABLED)
        if not self.gui_loop.isAnyTrackPlaying:
            self.gui_loop.stop()

    def deleteTrack(self):
        '''
        this function
        1) stops the track
        2) removes a track from gui_loop.trackCollection list, and
        3) disables the track row
        :return:
        '''
        self.isTrackPlaying = False
        self.trackStatus.configure(text=constants.trackStatus[4][0],
                                   foreground=constants.trackStatus[4][1])
        self.playFwdBtn.configure(state=tk.DISABLED)
        self.playRevBtn.configure(state=tk.DISABLED)
        self.pitchLowBtn.configure(state=tk.DISABLED)
        self.pitchNormalBtn.configure(state=tk.DISABLED)
        self.pitchHighBtn.configure(state=tk.DISABLED)
        self.trackPlayBtn.configure(state=tk.DISABLED)
        self.trackStopBtn.configure(state=tk.DISABLED)
        self.trackDeleteBtn.configure(state=tk.DISABLED)
        self.isTrackDeleted = True

        # prints to console what tracks are deleted and what are playing
        # self.gui_loop.trackCollectionStatus()
