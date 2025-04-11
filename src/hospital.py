import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import client

LARGE_FONT = ("Verdana", 12)
PATIENT_ID = 0
DOCTOR_ID = 0
WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0


class hospitalApp(tk.Tk):
    """Main application class for Lifeline Hospitals."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iconbitmap("images/house.ico")
        self.title("Lifeline Hospitals")

        # Container setup
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        # Frame loading
        for F in (loginPage, patientSignup, doctorSignup, patientLogin, doctorLogin, staffLogin):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(loginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class loginPage(tk.Frame):
    """Login and Signup page for users."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        label_0 = tk.Label(self, text="Login/Signup", width=20, font=("bold", 20))
        label_0.place(x=90, y=10)

        var = tk.IntVar()
        tk.Radiobutton(self, text="Patient", padx=5, variable=var, value=1, font=("bold", 10)).place(x=150, y=80)
        tk.Radiobutton(self, text="Doctor", padx=5, variable=var, value=2, font=("bold", 10)).place(x=220, y=80)
        tk.Radiobutton(self, text="Staff", padx=5, variable=var, value=3, font=("bold", 10)).place(x=290, y=80)

        label_1 = tk.Label(self, text="Email ID", width=20, font=("bold", 10))
        label_1.place(x=80, y=130)

        entry_1 = tk.Entry(self)
        entry_1.place(x=240, y=130)

        label_2 = tk.Label(self, text="Password", width=20, font=("bold", 10))
        label_2.place(x=68, y=180)

        entry_2 = tk.Entry(self, show='*')
        entry_2.place(x=240, y=180)

        # This function is called after Login Button is clicked
        def login():
            global PATIENT_ID, DOCTOR_ID
            emailid = entry_1.get()
            pwd = entry_2.get()
            section = var.get()
            var.set(0)
            entry_1.delete(0, 'end')
            entry_2.delete(0, 'end')

            if section == 0 or emailid == "" or pwd == "":
                messagebox.showwarning("Lifeline Hospitals", "Please enter required data!")
            else:
                if section == 1:
                    answer = client.transact("login", str(emailid), str(pwd))
                    if answer == "False":
                        messagebox.showwarning("Lifeline Hospitals", "Patient not yet registered!")
                    else:
                        PATIENT_ID = answer
                        controller.show_frame(patientLogin)
                elif section == 2:
                    answer = client.transact("doclogin", str(emailid), str(pwd))
                    if answer == "False":
                        messagebox.showwarning("Lifeline Hospitals", "Doctor not yet registered!")
                    else:
                        DOCTOR_ID = answer
                        controller.show_frame(doctorLogin)
                elif section == 3:
                    controller.show_frame(staffLogin)

        # This function is called after signup Button is clicked
        def signup():
            section = var.get()
            var.set(0)
            if section == 0:
                messagebox.showwarning("Lifeline Hospitals", "Please enter required data!")
            else:
                if section == 1:
                    controller.show_frame(patientSignup)
                elif section == 2:
                    controller.show_frame(doctorSignup)

        tk.Button(self, text='Login', command=login).place(x=250, y=250)
        tk.Button(self, text='Sign Up', command=signup).place(x=170, y=250)


class patientSignup(tk.Frame):
    """Patient signup page."""

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Patient Signup", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        button1.pack()


class doctorSignup(tk.Frame):
    """Doctor signup page."""

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Doctor Signup", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        button1.pack()


class patientLogin(tk.Frame):
    """Patient dashboard page."""

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Patient Dashboard", font=LARGE_FONT)
        label.pack(pady=10, padx=10)


class doctorLogin(tk.Frame):
    """Doctor dashboard page."""

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Doctor Dashboard", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        button1.pack()


class staffLogin(tk.Frame):
    """Staff dashboard page."""

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Staff Dashboard", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Logout", command=lambda: controller.show_frame(loginPage))
        button1.pack()


app = hospitalApp()
app.state('zoomed')
WINDOW_WIDTH = app.winfo_screenwidth()
WINDOW_HEIGHT = app.winfo_screenheight()
app.geometry("%dx%d+0+0" % (WINDOW_WIDTH, WINDOW_HEIGHT))
app.mainloop()
