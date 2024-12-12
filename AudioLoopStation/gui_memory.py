import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox


class GuiLoopManagement(ttk.Frame):
    '''
    this class is part of View
    '''
    def __init__(self, parent, gui_loop, controller, labelText):
        '''
        GuiLoopManagement constructor
        '''
        super().__init__(parent)
        self.gui_loop = gui_loop
        self.controller = controller
        self.LabelName = tk.Label(self, text=labelText, font=("Arial", 15))

        buttonWidth = 18

        self.loopNameLabel = tk.Label(self, text="Loop name:",
                                      justify=tk.RIGHT)

        self.loopNameFromComboBox = tk.StringVar()
        self.comboBox = ttk.Combobox(self,
                                     textvariable=self.loopNameFromComboBox,
                                     postcommand=self.updateLoopList)

        self.loadLoopBtn = ttk.Button(self, text="Load",
                                      command=lambda: self.controller.
                                      load_loop(self, self.gui_loop, self.
                                                loopNameFromComboBox.get()),
                                      width=buttonWidth)

        self.createBtn = ttk.Button(self, text="New",
                                    command=lambda: self.controller.
                                    create_loop(self, self.gui_loop, self.
                                                loopNameFromComboBox.get()),
                                    width=buttonWidth)

        self.saveBtn = ttk.Button(self, text="Save",
                                  command=lambda:
                                  self.controller.
                                  save_loop(self,
                                            self.loopNameFromComboBox.get()),
                                  width=buttonWidth,
                                  state=tk.DISABLED)

        self.restartBtn = ttk.Button(self, text="Discard",
                                     command=lambda: self.controller.
                                     discard_loop(self, self.gui_loop, self.
                                                  loopNameFromComboBox.get()),
                                     width=buttonWidth,
                                     state=tk.DISABLED)

        ############
        # GUI LAYOUT
        ############

        # row 0
        self.LabelName.grid(column=0, row=0, columnspan=4, sticky="ew",
                            padx=5, pady=15)

        # row 1
        self.loopNameLabel.grid(column=0, row=1, sticky="e")
        self.comboBox.grid(column=1, row=1, columnspan=3, sticky="ew", padx=5)

        # row 2
        self.loadLoopBtn.grid(column=0, row=2, padx=5, pady=5, sticky="ew")
        self.createBtn.grid(column=1, row=2, padx=5, pady=5, sticky="ew")
        self.saveBtn.grid(column=2, row=2, padx=5, pady=5, sticky="ew")
        self.restartBtn.grid(column=3, row=2, padx=5, pady=5, sticky="ew")

    def updateLoopList(self):
        '''
        This function updates the comboBox dropdown options with current loop
        names
        :return:
        '''
        self.comboBox.configure(values=sorted(self.controller.saveManager.
                                              get_loop_options()))

    def create(self):
        '''
        this function reconfigures gui to guide the user upon loop creation
        '''
        self.loadLoopBtn.configure(state=tk.DISABLED)
        self.createBtn.configure(state=tk.DISABLED)
        self.saveBtn.configure(state=tk.NORMAL)
        self.restartBtn.configure(state=tk.NORMAL)
        self.comboBox.configure(state=tk.DISABLED)

    def discard(self):
        '''
        this function reconfigures gui to guide the user upon discarding loop
        '''
        self.restartBtn.configure(text="Discard")
        self.loadLoopBtn.configure(state=tk.NORMAL)
        self.createBtn.configure(state=tk.NORMAL)
        self.saveBtn.configure(state=tk.DISABLED)
        self.restartBtn.configure(state=tk.DISABLED)
        self.comboBox.configure(state=tk.NORMAL)
        self.loopNameFromComboBox.set("")

    def save(self):
        '''
        this function reconfigures gui to guide the user when save button is
        pressed
        '''
        self.restartBtn.configure(text="Restart")

    def load(self):
        '''
        this function reconfigures gui to guide the user upon loading loop
        '''
        self.create()

    def informFailedLoad(self):
        '''
        this function creates a pop-up window showing error message to the user
        '''
        tk.messagebox.showinfo("Load Failed",
                               "You can load existing loops ONLY. \n"
                               "Please select from the dropdown menu or input "
                               "one that matches an existing loop name and"
                               " try again.")

    def informFailedSave(self):
        '''
        this function creates a pop-up window showing error message to the user
        '''
        tk.messagebox.showinfo("Save Failed",
                               "Please input a unique loop name that "
                               "does not exist in the dropdown and try again.")
