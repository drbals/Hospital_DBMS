import hashlib
import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import client

LARGE_FONT = ("Verdana", 12)
HISTORY_LABEL_WIDTH = 50
RECORD_LABEL_WIDTH = 60
MEDICINE_LABEL_WIDTH = 60
TEST_LABEL_WIDTH = 60
FORM_FIELD_WIDTH = 30

class LoginPage(tk.Frame):
    """Login and Signup page for users."""

    def __init__(self, parent, controller):
        super().__init__(parent)
        label_0 = tk.Label(self, text="Login/Signup", width=20, font=("bold", 20))
        label_0.place(x=90, y=10)

        self.var = tk.IntVar()
        tk.Radiobutton(self, text="Patient", padx=5, variable=self.var, value=1, font=("bold", 10)).place(x=150, y=80)
        tk.Radiobutton(self, text="Doctor", padx=5, variable=self.var, value=2, font=("bold", 10)).place(x=220, y=80)
        tk.Radiobutton(self, text="Staff", padx=5, variable=self.var, value=3, font=("bold", 10)).place(x=290, y=80)

        label_1 = tk.Label(self, text="Email ID", width=20, font=("bold", 10))
        label_1.place(x=80, y=130)

        self.entry_1 = tk.Entry(self)
        self.entry_1.place(x=240, y=130)

        label_2 = tk.Label(self, text="Password", width=20, font=("bold", 10))
        label_2.place(x=68, y=180)

        self.entry_2 = tk.Entry(self, show='*')
        self.entry_2.place(x=240, y=180)

        self.emailID = None
        self.pwd = None
        self.section = None
        # This function is called after Login Button is clicked
        def login():
            self.emailID = self.entry_1.get()
            self.pwd = self.entry_2.get()
            self.section = self.var.get()
            self.var.set(0)
            self.entry_1.delete(0, 'end')
            self.entry_2.delete(0, 'end')

            print(self.emailID, self.pwd, self.section)
            if self.section == 0 or self.emailID == "" or self.pwd == "":
                messagebox.showwarning("Lifeline Hospitals", "Please enter required data!")
            else:
                if self.section == 1:
                    answer = client.transact("login", str(self.emailID), str(self.pwd))
                    # answer = 1
                    print(answer)
                    if answer == "False":
                        messagebox.showwarning("Lifeline Hospitals", "Patient not yet registered!")
                    else:
                        PatientLogin.patientId = answer
                        controller.get_frame(PatientLogin)
                elif self.section == 2:
                    answer = client.transact("doclogin", str(self.emailID), str(self.pwd))
                    if answer == "False":
                        messagebox.showwarning("Lifeline Hospitals", "Doctor not yet registered!")
                    else:
                        DoctorLogin.doctorId = answer
                        controller.get_frame(DoctorLogin)
                elif self.section == 3:
                    controller.get_frame(StaffLogin)

        # This function is called after signup Button is clicked
        def signup():
            self.section = self.var.get()
            self.var.set(0)
            if self.section == 0:
                messagebox.showwarning("Lifeline Hospitals", "Please enter required data!")
            else:
                if self.section == 1:
                    controller.get_frame(PatientSignup)
                elif self.section == 2:
                    controller.get_frame(DoctorSignup)

        tk.Button(self, text='Login', command=login).place(x=250, y=250)
        tk.Button(self, text='Sign Up', command=signup).place(x=170, y=250)

    def load_frame(self):
        pass


class PatientSignup(tk.Frame):
    """Patient signup page."""
    
    def __init__(self, parent, controller=None):
        """
        Initialize the PatientSignup form.
        If a controller is provided, you can use it to switch frames.
        """
        super().__init__(parent)
        self.controller = controller

        self.header = tk.Label(self, text="Patient Signup", font=LARGE_FONT)
        self.header.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        tk.Label(self, text="Patient Name:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(self, width=FORM_FIELD_WIDTH)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Date of Birth (YYYY-MM-DD):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.dob_entry = tk.Entry(self, width=FORM_FIELD_WIDTH)
        self.dob_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Gender:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.gender_var = tk.StringVar(value="Select")
        self.gender_option = tk.OptionMenu(self, self.gender_var, "Male", "Female", "Other")
        self.gender_option.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Address:").grid(row=4, column=0, sticky="ne", padx=5, pady=5)
        self.address_text = tk.Text(self, width=FORM_FIELD_WIDTH, height=3)
        self.address_text.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self, text="Contact Number:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.contact_entry = tk.Entry(self, width=FORM_FIELD_WIDTH)
        self.contact_entry.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self, text="Email:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = tk.Entry(self, width=FORM_FIELD_WIDTH)
        self.email_entry.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self, text="Password:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(self, width=FORM_FIELD_WIDTH, show="*")
        self.password_entry.grid(row=7, column=1, padx=5, pady=5)

        submit_btn = tk.Button(self, text="Submit", command=self.submit_form)
        submit_btn.grid(row=8, column=0, columnspan=2, pady=10)

    def submit_form(self):
        """Extract form data, validate inputs, and make the client call to sign up."""
        patientName = self.name_entry.get().strip()
        dob_str = self.dob_entry.get().strip()
        gender = self.gender_var.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        # Validate required fields
        if not (patientName and dob_str and gender and address and contact and email and password):
            messagebox.showerror("Error", "All fields are required.")
            return
        if gender == "Select":
            messagebox.showerror("Error", "Please select a gender.")
            return

        # Validate DOB format
        try:
            datetime.strptime(dob_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date of Birth must be in YYYY-MM-DD format.")
            return

        # Validate Contact Number (should be all digits)
        if not contact.isdigit():
            messagebox.showerror("Error", "Contact number must contain only digits.")
            return

        # Validate Password Length
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return

        try:
            # Perform the client call.
            result = client.transact("signup", patientName, dob_str, gender,
                                     address, int(contact), email, 0, 0, 0, 0, password)
            messagebox.showinfo("Success", f"Sign up successful! Result: {result}")
            self.controller.get_frame(LoginPage)
        except Exception as e:
            messagebox.showerror("Error", f"Sign up failed: {e}")

    def load_frame(self):
        pass


class DoctorSignup(tk.Frame):
    """Doctor signup page."""

    def __init__(self, parent, controller=None):
        """
        Initialize the Doctor Signup form.
        'controller' can be used to navigate between pages in a multi-page app.
        """
        super().__init__(parent)
        self.controller = controller

        self.header = tk.Label(self, text="Doctor Signup", font=LARGE_FONT)
        self.header.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        tk.Label(self, text="Master Password:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.master_pass_entry = tk.Entry(self, width=FORM_FIELD_WIDTH, show="*")
        self.master_pass_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Doctor Name:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.name_entry = tk.Entry(self, width=FORM_FIELD_WIDTH)
        self.name_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self, text="Department Number:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.dept_entry = tk.Entry(self, width=FORM_FIELD_WIDTH)
        self.dept_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self, text="Date of Birth (YYYY-MM-DD):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.dob_entry = tk.Entry(self, width=FORM_FIELD_WIDTH)
        self.dob_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self, text="Gender:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.gender_var = tk.StringVar(value="Select")
        self.gender_option = tk.OptionMenu(self, self.gender_var, "Male", "Female", "Other")
        self.gender_option.grid(row=5, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self, text="Address:").grid(row=6, column=0, sticky="ne", padx=5, pady=5)
        self.address_text = tk.Text(self, width=FORM_FIELD_WIDTH, height=3)
        self.address_text.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self, text="Contact Number:").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        self.contact_entry = tk.Entry(self, width=FORM_FIELD_WIDTH)
        self.contact_entry.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(self, text="Salary:").grid(row=8, column=0, sticky="e", padx=5, pady=5)
        self.salary_entry = tk.Entry(self, width=FORM_FIELD_WIDTH)
        self.salary_entry.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(self, text="Email:").grid(row=9, column=0, sticky="e", padx=5, pady=5)
        self.email_entry = tk.Entry(self, width=FORM_FIELD_WIDTH)
        self.email_entry.grid(row=9, column=1, padx=5, pady=5)

        tk.Label(self, text="Account Password:").grid(row=10, column=0, sticky="e", padx=5, pady=5)
        self.password_entry = tk.Entry(self, width=FORM_FIELD_WIDTH, show="*")
        self.password_entry.grid(row=10, column=1, padx=5, pady=5)

        submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        submit_button.grid(row=11, column=0, columnspan=2, pady=10)

    def load_frame(self):
        pass

    def submit_form(self):
        """Validates the input and submits the signup form."""
        master_pass = self.master_pass_entry.get().strip()
        doctor_name = self.name_entry.get().strip()
        dept_num = self.dept_entry.get().strip()
        dob_str = self.dob_entry.get().strip()
        gender = self.gender_var.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        contact = self.contact_entry.get().strip()
        salary = self.salary_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not (master_pass and doctor_name and dept_num and dob_str and gender and address and contact and salary and email and password):
            messagebox.showerror("Error", "All fields are required.")
            return

        if gender == "Select":
            messagebox.showerror("Error", "Please select a gender.")
            return

        try:
            dept_num = int(dept_num)
        except ValueError:
            messagebox.showerror("Error", "Department Number must be an integer.")
            return

        try:
            datetime.strptime(dob_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date of Birth must be in YYYY-MM-DD format.")
            return

        if not contact.isdigit():
            messagebox.showerror("Error", "Contact number must contain only digits.")
            return

        try:
            salary = float(salary)
        except ValueError:
            messagebox.showerror("Error", "Salary must be a number.")
            return

        if master_pass != "doctorPass":
            messagebox.showerror("Error", "Invalid Master Password.")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long.")
            return

        try:
            result = client.transact("docsignup", master_pass, doctor_name, dept_num, dob_str, gender,
                                      address, int(contact), salary, email, password)
            if result:
                messagebox.showinfo("Success", "Signup successful!")
                self.controller.get_frame(LoginPage)
            else:
                messagebox.showerror("Error", "Signup failed. Please check your details and try again.")
        except Exception as e:
            messagebox.showerror("Error", f"Signup encountered an exception:\n{e}")

class PatientLogin(tk.Frame):
    patientId = None
    """Patient dashboard page."""
    def __init__(self, parent, controller=None):
        """
        Initializes the patient dashboard.
        When used within a larger application (controller is provided), the frame
        can be switched among other pages. If controller is None, the frame can run standalone.
        """
        super().__init__(parent)
        self.controller = controller

        self.header = tk.Label(self, text="Patient Dashboard", font=LARGE_FONT)
        self.header.grid(row=0, column=0, columnspan=12, pady=10, padx=10)

        self.history_lbl = tk.Label(self, text="Appointment & Patient History",
                                    relief=tk.SUNKEN, anchor='center',
                                    width=HISTORY_LABEL_WIDTH, bg="green", fg="white")
        self.history_lbl.grid(row=1, column=0, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

        self.record_lbl = tk.Label(self, text="Record Details",
                                   relief=tk.SUNKEN, anchor='center',
                                   width=RECORD_LABEL_WIDTH, bg="blue", fg="white")
        self.record_lbl.grid(row=1, column=4, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

        self.details_lbl = tk.Label(self, text="Patient Details & Reports",
                                    relief=tk.SUNKEN, anchor='center',
                                    width=RECORD_LABEL_WIDTH, bg="brown", fg="white")
        self.details_lbl.grid(row=1, column=8, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

        self.deptListResult = client.transact("appointmentdept")
        self.deptList = [row[1] for row in self.deptListResult]
        self.deptClicked = tk.StringVar()
        self.deptClicked.set("Select Department")
        self.deptDrop = tk.OptionMenu(self, self.deptClicked, *self.deptList)
        self.deptDrop.grid(row=2, column=0)

        self.deptBtn = tk.Button(self, text="See Doctors", command=self.doc_display)
        self.deptBtn.grid(row=3, column=0)

        self.logOutBtn = tk.Button(self, text="Logout", command=lambda: controller.get_frame(LoginPage))
        self.logOutBtn.grid(row=4, column=18)

        self.docClicked = tk.StringVar()
        self.docClicked.set("Select Doctor")
        self.docList = ["Select Doctor"]
        self.docListResult = []
        self.docDrop = tk.OptionMenu(self, self.docClicked, *self.docList)
        self.docDrop.grid(row=2, column=1)

        self.docBtn = tk.Button(self, text="Show Next Slot", command=self.slot_display)
        self.docBtn.grid(row=3, column=1)

        self.slotLbl = None
        self.bookBtn = None

        self.recordsLbl = tk.Label(self, text="Past Records", bg="red", fg="white")
        self.recordsLbl.grid(row=5, column=0, pady=10, sticky=tk.W + tk.E)

    def load_frame(self):
        if PatientLogin.patientId is not None:
            self.get_records()

    def doc_display(self):
        """Updates the doctor dropdown based on the selected department."""
        deptNoClicked = self.give_num(self.deptListResult, self.deptClicked.get())
        self.docListResult = client.transact("appointmentdoc", deptNoClicked)
        self.docList = [row[1] for row in self.docListResult]
        # Update the OptionMenu with the new doctor list:
        self.docDrop["menu"].delete(0, "end")
        for doc in self.docList:
            self.docDrop["menu"].add_command(label=doc,
                                             command=lambda value=doc: self.docClicked.set(value))

    def give_num(self, deplist, dept):
        """Return the numeric id for the selected department."""
        for item in deplist:
            if item[1] == dept:
                return item[0]
        return 0

    def slot_display(self):
        """Displays the next available appointment slot for the selected doctor."""
        self.docNoClicked = self.give_num(self.docListResult, self.docClicked.get())
        self.nextSlot = client.transact("nextslot", self.docNoClicked)
        if self.slotLbl:
            self.slotLbl.destroy()
        self.slotLbl = tk.Label(self, text="NextSlot at " + str(self.nextSlot), bg="yellow")
        self.slotLbl.grid(row=4, column=0)
        if self.bookBtn:
            self.bookBtn.destroy()
        self.bookBtn = tk.Button(self, text="Book slot",
                                 command=lambda: self.book_slot(self.docNoClicked, self.nextSlot))
        self.bookBtn.grid(row=4, column=1)

    def book_slot(self, docNo, slotNext):
        """Attempts to book a slot and refreshes the records."""
        status = client.transact("bookslot", PatientLogin.patientId, docNo, slotNext)
        if not status:
            messagebox.showinfo("Lifeline Hospitals", "Slot not booked!")
        else:
            messagebox.showinfo("Lifeline Hospitals", "Slot booked! Your AppointmentID is " + str(status))
        if self.slotLbl:
            self.slotLbl.destroy()
            self.slotLbl = None
        if self.bookBtn:
            self.bookBtn.destroy()
            self.bookBtn = None
        self.get_records()

    def show_record(self, id):
        """Displays detailed information for a selected appointment record."""
        if id == 0:
            messagebox.showinfo("Lifeline Hospitals", "Please select a record!")
            return

        record_columns = [4, 5, 6, 7]
        for widget in self.winfo_children():
            grid_info = widget.grid_info()
            if grid_info.get('column') in record_columns and grid_info.get('row') != 1:
                widget.destroy()

        detailsList, testsList, medsList = client.transact("record retrieve", id)
        r_value = 2
        apptIdLbl = tk.Label(self, text="Appt.ID: " + str(detailsList[0]))
        apptIdLbl.grid(row=r_value, column=4)
        apptTimeLbl = tk.Label(self, text="Appt.Time: " + str(detailsList[1]))
        apptTimeLbl.grid(row=r_value, column=6)
        r_value += 1
        ptIdLbl = tk.Label(self, text="Patient ID: " + str(detailsList[2]))
        ptIdLbl.grid(row=r_value, column=4)
        ptNameLbl = tk.Label(self, text="Patient Name: " + str(detailsList[3]))
        ptNameLbl.grid(row=r_value, column=6)
        r_value += 1
        docIdLbl = tk.Label(self, text="Doctor ID: " + str(detailsList[4]))
        docIdLbl.grid(row=r_value, column=4)
        docNameLbl = tk.Label(self, text="Doctor Name: " + str(detailsList[5]))
        docNameLbl.grid(row=r_value, column=6)

        # Display Prescribed Medicines
        r_value += 1
        meds_lbl = tk.Label(self, text="Medicines Prescribed", relief=tk.SUNKEN, anchor='center',
                            width=MEDICINE_LABEL_WIDTH, bg="blue", fg="white")
        meds_lbl.grid(row=r_value, column=4, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
        r_value += 1
        medLbl = tk.Label(self, text="Medicine Name              Quantity               Cost Per Medicine")
        medLbl.grid(row=r_value, column=4, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
        r_value += 1
        for med, medCost, medQuantity in medsList:
            medLbl = tk.Label(self, text=med + "                           " + str(
                medQuantity) + "                            " + str(medCost) + "/-")
            medLbl.grid(row=r_value, column=4, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
            r_value += 1

        # Display Prescribed Tests
        tests_lbl = tk.Label(self, text="Tests Prescribed", relief=tk.SUNKEN, anchor='center',
                             width=TEST_LABEL_WIDTH, bg="blue", fg="white")
        tests_lbl.grid(row=r_value, column=4, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
        r_value += 1
        testLbl = tk.Label(self, text="Test Name               Test Cost              Test Status")
        testLbl.grid(row=r_value, column=4, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W)
        r_value += 1
        for testName, testCost, testStatus in testsList:
            testLbl = tk.Label(self, text=testName + "                     " + str(
                testCost) + "/-" + "                      " + str(testStatus))
            testLbl.grid(row=r_value, column=4, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W)
            r_value += 1

    def get_records(self):
        """Retrieves and displays past appointment records."""
        recordsList = client.transact("patientrecords", PatientLogin.patientId)
        idValue = tk.IntVar()
        r_value = 7
        c_value = 0
        for timeStamp, ID, docName in recordsList:
            tk.Radiobutton(self, text="Appt ID " + str(ID) + " with " + docName + " on " + str(timeStamp),
                           variable=idValue, value=ID).grid(row=r_value, column=c_value)
            r_value += 1
        recordBtn = tk.Button(self, text="Show Record", command=lambda: self.show_record(idValue.get()))
        recordBtn.grid(row=r_value, column=0)


class DoctorLogin(tk.Frame):
    """Doctor dashboard page."""
    doctorId = None
    def __init__(self, parent, controller=None):
        """
        Initializes the doctor dashboard.
        If a controller is provided, this frame can be used as part of a larger application.
        Otherwise, it runs standalone.
        """
        super().__init__(parent)
        self.controller = controller

        self.header = tk.Label(self, text="Doctor Dashboard", font=LARGE_FONT)
        self.header.grid(row=0, column=0, columnspan=12, pady=10, padx=10)

        self.history_lbl = tk.Label(self, text="Medical History",
                                    relief=tk.SUNKEN, anchor='center',
                                    width=HISTORY_LABEL_WIDTH, bg="green", fg="white")
        self.history_lbl.grid(row=1, column=0, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W)

        self.record_lbl = tk.Label(self, text="Record Details",
                                   relief=tk.SUNKEN, anchor='center',
                                   width=RECORD_LABEL_WIDTH, bg="blue", fg="white")
        self.record_lbl.grid(row=1, column=3, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

        self.prescribe_lbl = tk.Label(self, text="Prescription & Reports",
                                      relief=tk.SUNKEN, anchor='center',
                                      width=RECORD_LABEL_WIDTH, bg="brown", fg="white")
        self.prescribe_lbl.grid(row=1, column=7, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

        self.apptIdLbl = tk.Label(self, text="Appointment ID:", anchor=tk.W, width=10)
        self.apptIdLbl.grid(row=2, column=0, sticky=tk.W + tk.E)

        self.idEntry = tk.Entry(self, width=20, bg="white", fg="black", borderwidth=5)
        self.idEntry.grid(row=2, column=1, sticky=tk.W + tk.E)
        self.idEntry.insert(0, "Enter")

        self.getRecBtn = tk.Button(self, text="Show Record",
                                   command=lambda: self.show_record(self.idEntry.get()))
        self.getRecBtn.grid(row=2, column=2)

        self.refCasesLbl = tk.Label(self, text="Reffered Cases", bg="red", fg="white")
        self.refCasesLbl.grid(row=3, column=1, pady=10, sticky=tk.W + tk.E)

        self.giveMedsLbl = tk.Label(self, text="Prescribe Meds")
        self.giveMedsLbl.grid(row=4, column=0)

        self.logOutBtn = tk.Button(self, text="Logout", command=lambda: controller.get_frame(LoginPage))
        self.logOutBtn.grid(row=4, column=18)

    def load_frame(self):
        if DoctorLogin.doctorId is not None:
            self.get_reff_cases(DoctorLogin.doctorId)

    def show_record(self, rec_id):
        """Display detailed record information for a given record id."""
        if rec_id == 0 or rec_id == "Enter":
            messagebox.showinfo("Lifeline Hospitals", "Please select a record!")
            return

        record_columns = [3, 4, 5, 6]
        for widget in self.winfo_children():
            grid_info = widget.grid_info()
            if grid_info.get('column') in record_columns and grid_info.get('row') != 1:
                widget.destroy()

        detailsList, testsList, medsList = client.transact("record retrieve", rec_id)
        r_value = 2

        apptIdLbl = tk.Label(self, text="Appt.ID: " + str(detailsList[0]))
        apptIdLbl.grid(row=r_value, column=4)
        apptTimeLbl = tk.Label(self, text="Appt.Time: " + str(detailsList[1]))
        apptTimeLbl.grid(row=r_value, column=6)
        r_value += 1

        ptIdLbl = tk.Label(self, text="Patient ID: " + str(detailsList[2]))
        ptIdLbl.grid(row=r_value, column=4)
        ptNameLbl = tk.Label(self, text="Patient Name: " + str(detailsList[3]))
        ptNameLbl.grid(row=r_value, column=6)
        r_value += 1

        docIdLbl = tk.Label(self, text="Doctor ID: " + str(detailsList[4]))
        docIdLbl.grid(row=r_value, column=4)
        docNameLbl = tk.Label(self, text="Doctor Name: " + str(detailsList[5]))
        docNameLbl.grid(row=r_value, column=6)

        # Display Prescribed Medicines
        meds_lbl = tk.Label(self, text="Medicines Prescribed", relief=tk.SUNKEN,
                            anchor='center', width=MEDICINE_LABEL_WIDTH, bg="blue", fg="white")
        meds_lbl.grid(row=4, column=3, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
        r_value = 6
        medLbl = tk.Label(self, text="Medicine Name              Quantity               Cost Per Medicine")
        medLbl.grid(row=r_value, column=3, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
        r_value += 1
        for med, medCost, medQuantity in medsList:
            medLbl = tk.Label(self, text=med + "                           " + str(
                medQuantity) + "                            " + str(medCost) + "/-")
            medLbl.grid(row=r_value, column=3, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
            r_value += 1

        # Display Prescribed Tests
        tests_lbl = tk.Label(self, text="Tests Prescribed", relief=tk.SUNKEN,
                             anchor='center', width=TEST_LABEL_WIDTH, bg="blue", fg="white")
        tests_lbl.grid(row=r_value, column=3, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
        r_value += 1
        testLbl = tk.Label(self, text="Test Name               Test Cost              Test Status")
        testLbl.grid(row=r_value, column=3, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)
        r_value += 1
        for testName, testCost, testStatus in testsList:
            testLbl = tk.Label(self, text=testName + "                     " + str(
                testCost) + "/-" + "                      " + str(testStatus))
            testLbl.grid(row=r_value, column=4, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W)
            r_value += 1

    def get_reff_cases(self, doc_id):
        """Fetch and display referred cases for the given doctor id."""
        recordsList = client.transact("docrecords", doc_id)
        idValue = tk.IntVar()
        r_value = 4
        c_value = 0
        for timeStamp, ID, ptName in recordsList:
            rb = tk.Radiobutton(self, text="Appt ID " + str(ID) + " treated " + ptName + " on " + str(timeStamp),
                                variable=idValue, value=ID)
            rb.grid(row=r_value, column=c_value, columnspan=2)
            r_value += 1
        recordBtn = tk.Button(self, text="Show Record", command=lambda: self.show_record(idValue.get()))
        recordBtn.grid(row=r_value, column=0)


class StaffLogin(tk.Frame):
    """Staff dashboard page."""

    def __init__(self, parent, controller):
        super().__init__(parent)

        label = tk.Label(self, text="Staff Dashboard", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Logout", command=lambda: controller.get_frame(LoginPage))
        button1.pack()

    def load_frame(self):
        pass