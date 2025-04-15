from app import *
import os
import tkinter as tk

class HospitalApp(tk.Tk):
    """Main application class for Lifeline Hospitals."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iconbitmap("images/house.ico")
        self.title("Lifeline Hospitals")

        # Container setup
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        # Frame loading
        for F in (LoginPage, PatientSignup, DoctorSignup, PatientLogin, DoctorLogin):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.get_frame(LoginPage)

    def get_frame(self, page):
        frame = self.frames[page]
        frame.load_frame()
        frame.tkraise()


app = HospitalApp()
app.state('zoomed')
WINDOW_WIDTH = app.winfo_screenwidth()
WINDOW_HEIGHT = app.winfo_screenheight()
app.geometry("%dx%d+0+0" % (WINDOW_WIDTH, WINDOW_HEIGHT))
app.mainloop()
