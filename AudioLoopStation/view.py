from gui_loop import GuiLoop
from gui_rhythm import GuiRhythm
from gui_memory import GuiLoopManagement
import tkinter as tk


class View(tk.Tk):
    '''
    this class is the View in the Model-Control-View architecture
    View assembles all of the GUI elements
    gui_loop.py, gui_memory.py, gui_rhythm.py, and gui_track.py are part of View
    '''

    def __init__(self, controller):
        '''
        View constructor
        '''
        super().__init__()
        self.controller = controller
        self.title("Audio Loop")
        self._make_loop()
        self._make_memory()
        self._make_rhythm()

    def main(self):
        '''
        this function calls tkinter mainloop, an infinite loop that listens
        for gui events, processes them and updates gui
        '''
        self.mainloop()

    def _make_loop(self):
        '''
        this function creates two GuiLoop objects and places them on the screen
        '''
        self.loop1 = GuiLoop(parent=self,
                             labelLoopName="Loop1",
                             controller=self.controller,
                             numberOfTracks=6)

        self.loop2 = GuiLoop(parent=self,
                             labelLoopName="Loop2",
                             controller=self.controller)

        self.loop1.grid(row=1, column=0, columnspan=2, sticky="new")
        self.loop2.grid(row=1, column=2, columnspan=2, sticky="new")

    def _make_memory(self):
        '''
        this function creates two GuiLoopManagement objects and places them
        on the screen
        '''
        self.memory1 = GuiLoopManagement(parent=self,
                                         gui_loop=self.loop1,
                                         controller=self.controller,
                                         labelText="Loop1 Management")

        self.memory2 = GuiLoopManagement(parent=self,
                                         gui_loop=self.loop2,
                                         controller=self.controller,
                                         labelText="Loop2 Management")

        self.memory1.grid(row=0, column=0, columnspan=2, sticky="new")
        self.memory2.grid(row=0, column=2, columnspan=2, sticky="new")

    def _make_rhythm(self):
        '''
        this function creates GuiRhythm object and places it on the screen.
        as of 3Dec24 we've not integrated events from this area of gui into the
        app.
        '''
        self.rhythm = GuiRhythm(self, "Rhythm", self.controller)
        self.rhythm.grid(row=1, column=4, columnspan=2, sticky="new")
