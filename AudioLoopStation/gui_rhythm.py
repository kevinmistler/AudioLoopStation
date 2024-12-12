import tkinter as tk
import tkinter.ttk as ttk
from tkdial import Dial


class GuiRhythm(ttk.Frame):
    '''
    this class is part of View
    as of 3Dec24 this class puts up the gui elements but they are not used
    '''
    def __init__(self, parent, LabelText, controller):
        super().__init__(parent)

        self.LabelName = tk.Label(self, text=LabelText, font=("Arial", 15))
        self.LabelName.grid(column=0, row=0, columnspan=2, sticky="ew", padx=5,
                            pady=5)

        self.onBtn = ttk.Button(self, text="ON", command=self.on,
                                state=tk.ACTIVE)
        self.onBtn.grid(column=0, row=1, sticky="ew")

        self.offBtn = ttk.Button(self, text="OFF", command=self.off)
        self.offBtn.grid(column=0, row=2, sticky="ew")

        # routeSoundChoice - a variable that dictates whether metronome/drum
        # sound goes to the user ONLY or to the user and the loops
        # routeSoundChoice == 0 - user only
        # routeSoundChoice == 1 - loops and user can hear it
        self.routeSoundChoice = tk.IntVar()
        self.routeSoundChoice.set(0)
        self.userOnlyRadioBtn = ttk.Radiobutton(self, text="User Only",
                                                variable=self.routeSoundChoice,
                                                value=1)
        self.userAndLoopsRadioBtn = ttk.Radiobutton(
            self, text="User and Loops",
            variable=self.routeSoundChoice, value=0
            )
        self.userOnlyRadioBtn.grid(column=0, row=3, sticky="ew")
        self.userAndLoopsRadioBtn.grid(column=0, row=4, sticky="ew")

        self.beatTypeChoice = tk.IntVar()
        self.beatTypeChoice.set(1)
        self.beatType1RadioBtn = ttk.Radiobutton(self, text="Metronome",
                                                 variable=self.beatTypeChoice,
                                                 value=1)
        self.beatType3RadioBtn = ttk.Radiobutton(self, text="Fund Drum",
                                                 variable=self.beatTypeChoice,
                                                 value=2)
        self.beatType4RadioBtn = ttk.Radiobutton(self, text="Rock Drum",
                                                 variable=self.beatTypeChoice,
                                                 value=3)
        self.beatType2RadioBtn = ttk.Radiobutton(self, text="Jazz Drum",
                                                 variable=self.beatTypeChoice,
                                                 value=4)
        self.beatType1RadioBtn.grid(column=1, row=1, sticky="ew")
        self.beatType2RadioBtn.grid(column=1, row=2, sticky="ew")
        self.beatType3RadioBtn.grid(column=1, row=3, sticky="ew")
        self.beatType4RadioBtn.grid(column=1, row=4, sticky="ew")

        self.bpmDial = Dial(self, start=40, end=218, text="BPM", integer=True,
                            command=lambda:
                            controller.update_bpm(self.bpmDial.get())
                            )
        self.bpmDial.set(controller.bpm)
        self.bpmDial.grid(column=0, row=5, sticky="ew", padx=5, pady=15)

        self.volumeDial = Dial(self, text="Volume", integer=True)
        self.volumeDial.set(50)
        self.volumeDial.grid(column=1, row=5, sticky="ew", padx=5,
                             pady=15)

    def on(self, event=None):
        pass

    def off(self, event=None):
        pass
