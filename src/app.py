import tkinter as tk
from datetime import datetime
from tkinter import messagebox
import client
from config import *
from base_page import BasePage
import re
from validator import Validator
 
class LoginPage(BasePage):
    """Login and Signup page for users."""

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        # Using grid for layout (replacing place)
        self.create_label("Login/Signup", row=0, column=1, colspan=2, font=LARGE_FONT, sticky="nsew")

        self.var = tk.IntVar()
        # Radio buttons can remain using place if you wish, but here we'll convert them to grid as well:
        self.create_radiobutton("Patient", self.var, 1, row=1, column=1)
        self.create_radiobutton("Doctor", self.var, 2, row=1, column=2)
        self.create_radiobutton("Staff", self.var, 3, row=1, column=3)

        self.create_label("Email ID", row=2, column=1, sticky="e")
        self.entry_email = self.create_entry(row=2, column=2, colspan=2)

        self.create_label("Password", row=3, column=1, sticky="e")
        self.entry_pwd = self.create_entry(row=3, column=2, colspan=2, show='*')

        self.emailID = None
        self.pwd = None
        self.section = None

        self.create_button("Login", self.login, row=4, column=1, sticky="w")
        self.create_button("Sign Up", self.signup, row=4, column=3, sticky="w")

        # Add a column of whitespace to the right
        self.create_label("", row=0, column=4)
        self.make_grid_responsive()

    def login(self):
        self.emailID = self.entry_email.get()
        self.pwd = self.entry_pwd.get()
        self.section = self.var.get()
        self.var.set(0)

        if self.section == 0 or not self.emailID or not self.pwd:
            messagebox.showwarning("Lifeline Hospitals", "Please enter required data!")
        else:
            if self.section == 1:
                answer = client.transact("login", str(self.emailID), str(self.pwd))
                if not answer:
                    messagebox.showwarning("Lifeline Hospitals", "Authentication failed!")
                else:
                    PatientLogin.patientId = answer
                    print("Patient ID: ", PatientLogin.patientId)
                    self.controller.get_frame(PatientLogin)
            elif self.section == 2:
                answer = client.transact("doclogin", str(self.emailID), str(self.pwd))
                if not answer:
                    messagebox.showwarning("Lifeline Hospitals", "Authentication failed!")
                else:
                    DoctorLogin.doctorId = answer
                    self.controller.get_frame(DoctorLogin)
            elif self.section == 3:
                self.controller.get_frame(StaffLogin)

    def signup(self):
        self.section = self.var.get()
        self.var.set(0)
        if self.section == 0:
            messagebox.showwarning("Lifeline Hospitals", "Please enter required data!")
        else:
            if self.section == 1:
                self.controller.get_frame(PatientSignup)
            elif self.section == 2:
                self.controller.get_frame(DoctorSignup)

    def load_frame(self):
        pass

class PatientSignup(BasePage):
    """Patient signup page."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)
        self.header = self.create_label("Patient Signup", row=0, column=0, colspan=2, font=LARGE_FONT)

        self.create_label("Patient Name:", row=1, column=0, sticky="e")
        self.name_entry = self.create_entry(row=1, column=1)

        self.create_label("Date of Birth (YYYY-MM-DD):", row=2, column=0, sticky="e")
        self.dob_entry = self.create_entry(row=2, column=1)

        self.create_label("Gender:", row=3, column=0, sticky="e")
        self.gender_var = tk.StringVar(value="Select")
        self.create_optionmenu(self.gender_var, ["Male", "Female", "Others"], row=3, column=1, sticky="w")

        self.create_label("Address:", row=4, column=0, sticky="e")
        self.address_text = tk.Text(self, width=TEXT_FIELD_WIDTH, height=TEXT_FIELD_HEIGHT)
        self.address_text.grid(row=4, column=1, sticky="w")

        self.create_label("Contact Number:", row=5, column=0, sticky="e")
        self.contact_entry = self.create_entry(row=5, column=1)

        self.create_label("Email:", row=6, column=0, sticky="e")
        self.email_entry = self.create_entry(row=6, column=1)

        self.create_label("Password:", row=7, column=0, sticky="e")
        self.password_entry = self.create_entry(row=7, column=1, show="*")

        self.create_button("Submit", self.submit_form, row=8, column=0, colspan=2)
        self.make_grid_responsive()

    def submit_form(self):
        print("name": self.name_entry.get())
        patientName = self.name_entry.get().strip()
        dob_str = self.dob_entry.get().strip()
        gender = self.gender_var.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not (patientName and dob_str and gender and address and contact and email and password):
            messagebox.showerror("Error", "All fields are required.")
            return

        valid, msg = Validator.validate_gender(gender)
        if not valid:   
            messagebox.showerror("Error", msg)
            return
        
        valid, msg = Validator.validate_dob(dob_str)
        if not valid:
            messagebox.showerror("Error", msg)
            return

        valid, msg = Validator.validate_contact(contact)
        if not valid:
            messagebox.showerror("Error", msg)
            return

        valid, msg = Validator.validate_email(email)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        valid, msg = Validator.validate_password(password)
        if not valid:
            messagebox.showerror("Error", msg)
            return

        try:
            result = client.transact("signup", patientName, dob_str, gender,
                                       address, int(contact), email, 0, 0, 0, 0, password)
            messagebox.showinfo("Success", f"Sign up successful! Result: {result}")
            self.controller.get_frame(LoginPage)
        except Exception as e:
            messagebox.showerror("Error", f"Sign up failed: {e}")

    def load_frame(self):
        pass

class DoctorSignup(BasePage):
    """Doctor signup page."""

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)
        self.header = self.create_label("Doctor Signup", row=0, column=0, colspan=2, font=LARGE_FONT)

        self.create_label("Master Password:", row=1, column=0, sticky="e")
        self.master_pass_entry = self.create_entry(row=1, column=1, show="*")

        self.create_label("Doctor Name:", row=2, column=0, sticky="e")
        self.name_entry = self.create_entry(row=2, column=1)

        self.create_label("Department Number:", row=3, column=0, sticky="e")
        self.dept_entry = self.create_entry(row=3, column=1)

        self.create_label("Date of Birth (YYYY-MM-DD):", row=4, column=0, sticky="e")
        self.dob_entry = self.create_entry(row=4, column=1)

        self.create_label("Gender:", row=5, column=0, sticky="e")
        self.gender_var = tk.StringVar(value="Select")
        self.create_optionmenu(self.gender_var, ["Male", "Female", "Others"], row=5, column=1, sticky="w")

        self.create_label("Address:", row=6, column=0, sticky="e")
        self.address_text = tk.Text(self, width=TEXT_FIELD_WIDTH, height=TEXT_FIELD_HEIGHT)
        self.address_text.grid(row=6, column=1, sticky="w")

        self.create_label("Contact Number:", row=7, column=0, sticky="e")
        self.contact_entry = self.create_entry(row=7, column=1)

        self.create_label("Salary:", row=8, column=0, sticky="e")
        self.salary_entry = self.create_entry(row=8, column=1)

        self.create_label("Email:", row=9, column=0, sticky="e")
        self.email_entry = self.create_entry(row=9, column=1)

        self.create_label("Account Password:", row=10, column=0, sticky="e")
        self.password_entry = self.create_entry(row=10, column=1, show="*")

        self.create_button("Submit", self.submit_form, row=11, column=0, colspan=2)
        self.make_grid_responsive()

    def load_frame(self):
            pass
    
    def submit_form(self):
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


        valid, msg = Validator.validate_dept_number(dept_num)
        if not valid:
            messagebox.showerror("Error", msg)
            return
    
        valid, msg = Validator.validate_dob(dob_str)
        if not valid:
            messagebox.showerror("Error", msg)
            return
    
        valid, msg = Validator.validate_gender(gender)
        if not valid:   
            messagebox.showerror("Error", msg)
            return
        
        valid, msg = Validator.validate_contact(contact)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        valid, msg = Validator.validate_doc_salary(salary)
        if not valid:
            messagebox.showerror("Error", msg)
            return

        valid, msg = Validator.validate_email(email)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        valid, msg = Validator.validate_password(password)
        if not valid:
            messagebox.showerror("Error", msg)
            return
        
        valid, msg = Validator.validate_doctor_masterpwd(master_pass)
        if not valid:
            messagebox.showerror("Error", msg)
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
    
class PatientLogin(BasePage):
    patientId = None
    """Patient dashboard page."""
    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)
        # Header
        self.header = self.create_label("Patient Dashboard", row=0, column=0, colspan=12, pady=10, padx=10, font=LARGE_FONT,
                                        sticky="nsew", relief=tk.SUNKEN, bg="light blue", fg="black")
        self.logOutBtn = self.create_button("Logout", lambda: self.controller.get_frame(LoginPage), row=0, column=10,
                                            sticky="w", relief=tk.SUNKEN, bg="white", fg="black")

        self.history_lbl = self.create_label("Appointment & Patient History", row=1, column=0, colspan=4, sticky="nsew", 
                                             font=MEDIUM_FONT, relief=tk.SUNKEN, width=HISTORY_LABEL_WIDTH, bg="green", fg="white")
        self.record_lbl = self.create_label("Record Details", row=1, column=4, colspan=4, sticky="nsew", 
                                            font=MEDIUM_FONT, relief=tk.SUNKEN, width=RECORD_LABEL_WIDTH, bg="blue", fg="white")
        self.details_lbl = self.create_label("Patient Details & Reports", row=1, column=8, colspan=4, sticky="nsew", 
                                             font=MEDIUM_FONT, relief=tk.SUNKEN, width=RECORD_LABEL_WIDTH, bg="brown", fg="white")

        self.deptListResult = client.transact("appointmentdept")
        self.deptList = [row[1] for row in self.deptListResult]
        self.deptClicked = tk.StringVar()
        self.deptClicked.set("Select Department")
        self.deptDrop = tk.OptionMenu(self, self.deptClicked, *self.deptList)
        self.deptDrop.grid(row=2, column=0)

        self.docClicked = tk.StringVar()
        self.docClicked.set("Select Doctor")
        self.docList = ["Select Doctor"]
        self.docListResult = []
        self.docDrop = tk.OptionMenu(self, self.docClicked, *self.docList)
        self.docDrop.grid(row=2, column=1, sticky="w")

        self.deptBtn = tk.Button(self, text="See Doctors", command=self.doc_display)
        self.deptBtn.grid(row=3, column=0)

        self.docBtn = tk.Button(self, text="Show Next Slot", command=self.slot_display)
        self.docBtn.grid(row=3, column=1, sticky="w")

        self.slotLbl = None
        self.bookBtn = None

        self.recordsLbl = self.create_label("Past Records", row=5, column=0, colspan=4, sticky="nsew", 
                                            font=MEDIUM_FONT, width=HISTORY_LABEL_WIDTH, relief=tk.SUNKEN, bg="green", fg="white")
        self.make_grid_responsive()

    def load_frame(self):
        if PatientLogin.patientId is not None:
            self.get_records()

    def doc_display(self):
        deptNoClicked = self.give_num(self.deptListResult, self.deptClicked.get())
        self.docListResult = client.transact("appointmentdoc", deptNoClicked)
        self.docList = [row[1] for row in self.docListResult]
        self.docDrop["menu"].delete(0, "end")
        for doc in self.docList:
            self.docDrop["menu"].add_command(label=doc, command=lambda value=doc: self.docClicked.set(value))

    def give_num(self, deplist, dept):
        for item in deplist:
            if item[1] == dept:
                return item[0]
        return 0

    def slot_display(self):
        self.docNoClicked = self.give_num(self.docListResult, self.docClicked.get())
        self.nextSlot = client.transact("nextslot", self.docNoClicked)
        if self.slotLbl:
            self.slotLbl.destroy()
        self.slotLbl = tk.Label(self, text="Next Slot at " + str(self.nextSlot), bg="yellow")
        self.slotLbl.grid(row=4, column=0)
        if self.bookBtn:
            self.bookBtn.destroy()
        self.bookBtn = tk.Button(self, text="Book slot", command=lambda: self.book_slot(self.docNoClicked, self.nextSlot))
        self.bookBtn.grid(row=4, column=1)

    def book_slot(self, docNo, slotnext):
        status = client.transact("bookslot", PatientLogin.patientId, docNo, slotnext)
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
        if id == 0:
            messagebox.showinfo("Lifeline Hospitals", "Please select a record!")
            return
        # Clear previous record widgets
        record_columns = [3,4,5,6]
        for widget in self.winfo_children():
            grid_info = widget.grid_info()
            if grid_info.get('column') in record_columns and grid_info.get('row') != 1:
                widget.destroy()

        detailsList, testsList, medsList = client.transact("record retrieve", id)
        r_value = 2
        self.create_label("Appt.ID: " + str(detailsList[0]), row=r_value, column=4)
        self.create_label("Appt.Time: " + str(detailsList[1]), row=r_value, column=6)

        r_value += 1
        self.create_label("Patient ID: " + str(detailsList[2]), row=r_value, column=4)
        self.create_label("Patient Name: " + str(detailsList[3]), row=r_value, column=6)

        r_value += 1
        self.create_label("Doctor ID: " + str(detailsList[4]), row=r_value, column=4)
        self.create_label("Doctor Name: " + str(detailsList[5]), row=r_value, column=6)

        r_value += 1
        self.create_label("Medicines Prescribed", row=r_value, column=4, colspan=4, sticky="nsew",
                          relief=tk.SUNKEN, width=MEDICINE_LABEL_WIDTH, bg="blue", fg="white")

        r_value += 1
        self.create_label("Medicine Name              Quantity               Cost Per Medicine", row=r_value, column=4, colspan=4, sticky="nsew")
        
        r_value += 1
        for med, medCost, medQuantity in medsList:
            self.create_label(med + "                           " + str(medQuantity) + "                            " + str(medCost) + "/-",
                              row=r_value, column=4, colspan=4, font=SMALL_FONT,sticky="nsew")
            r_value += 1

        self.create_label("Tests Prescribed", row=r_value, column=4, colspan=4, sticky="nsew", 
                          relief=tk.SUNKEN, width=TEST_LABEL_WIDTH, bg="blue", fg="white")
        
        r_value += 1
        self.create_label("Test Name               Test Cost              Test Status", row=r_value, column=4, colspan=3, sticky="nsew")
        
        r_value += 1
        for testName, testCost, testStatus in testsList:
            self.create_label(f"{testName}                     {testCost}/-                      {testStatus}", 
                              row=r_value, column=4, colspan=3, font=SMALL_FONT, sticky="nsew")
            r_value += 1

    def get_records(self):
        recordsList = client.transact("patientrecords", PatientLogin.patientId)
        idValue = tk.IntVar()
        r_value = 7
        c_value = 0
        for timeStamp, ID, docName in recordsList:
            self.create_radiobutton("Appt ID " + str(ID) + " with "+docName + " on "+str(timeStamp),
                                   variable=idValue, value=ID, row=r_value, column=c_value, font=SMALL_FONT)
            r_value += 1

        self.create_button("Show Record", lambda: self.show_record(idValue.get()), row=r_value, column=0)

class DoctorLogin(BasePage):
    """Doctor dashboard page."""
    doctorId = None

    def __init__(self, parent, controller=None):
        super().__init__(parent, controller)

        self.create_label("Doctor Dashboard", row=0, column=0, colspan=12, font=LARGE_FONT, pady=10)

        # Section Labels
        self.create_label("Medical History", row=1, column=0, colspan=3, sticky='nsew',
                          bg="green", fg="white", relief=tk.SUNKEN, width=HISTORY_LABEL_WIDTH)
        self.create_label("Record Details", row=1, column=3, colspan=4, sticky='nsew',
                          bg="blue", fg="white", relief=tk.SUNKEN, width=RECORD_LABEL_WIDTH)
        self.create_label("Prescription & Reports", row=1, column=7, colspan=4, sticky='nsew',
                          bg="brown", fg="white", relief=tk.SUNKEN, width=RECORD_LABEL_WIDTH)

        # Appointment ID input
        self.create_label("Appointment ID:", row=2, column=0, sticky='e')
        self.id_entry = self.create_entry(row=2, column=1)
        self.id_entry.insert(0, "Enter")

        self.create_button("Show Record", lambda: self.show_record(self.id_entry.get()), row=2, column=2)

        # Referred Cases Label
        self.create_label("Referred Cases", row=3, column=1, bg="red", fg="white", sticky='we', pady=10)

        # Prescribe Medicines Label
        self.create_label("Prescribe Meds", row=4, column=0)

        # Logout Button
        self.create_button("Logout", lambda: controller.get_frame(LoginPage), row=4, column=10)
        self.make_grid_responsive()

    def load_frame(self):
        if DoctorLogin.doctorId:
            self.get_referred_cases()

    def show_record(self, rec_id):
        """Displays detailed record information."""
        if rec_id == "Enter" or not rec_id.isdigit():
            messagebox.showinfo("Lifeline Hospitals", "Please enter a valid record ID!")
            return

        record_columns = [3, 4, 5, 6]
        for widget in self.winfo_children():
            grid_info = widget.grid_info()
            if grid_info.get('column') in record_columns and grid_info.get('row') > 1:
                widget.destroy()

        detailsList, testsList, medsList = client.transact("record retrieve", int(rec_id))
        r_value = 2

        self.create_label(f"Appt.ID: {detailsList[0]}", row=r_value, column=4)
        self.create_label(f"Appt.Time: {detailsList[1]}", row=r_value, column=6)
        r_value += 1
        self.create_label(f"Patient ID: {detailsList[2]}", row=r_value, column=4)
        self.create_label(f"Patient Name: {detailsList[3]}", row=r_value, column=6)
        r_value += 1
        self.create_label(f"Doctor ID: {detailsList[4]}", row=r_value, column=4)
        self.create_label(f"Doctor Name: {detailsList[5]}", row=r_value, column=6)
        r_value += 1

        # Medicines Section
        self.create_label("Medicines Prescribed", row=r_value, column=3, colspan=4, bg="blue", fg="white",
                          relief=tk.SUNKEN, width=MEDICINE_LABEL_WIDTH)
        r_value += 1
        self.create_label("Medicine Name              Quantity               Cost Per Medicine",
                          row=r_value, column=3, colspan=4)
        r_value += 1
        for med, medCost, medQuantity in medsList:
            med_text = f"{med}             {medQuantity}              {medCost}/-"
            self.create_label(med_text, row=r_value, column=3, colspan=4)
            r_value += 1

        # Tests Section
        self.create_label("Tests Prescribed", row=r_value, column=3, colspan=4, bg="blue", fg="white",
                          relief=tk.SUNKEN, width=TEST_LABEL_WIDTH)
        r_value += 1
        self.create_label("Test Name              Test Cost              Test Status",
                          row=r_value, column=3, colspan=4)
        r_value += 1
        for testName, testCost, testStatus in testsList:
            test_text = f"{testName}             {testCost}/-             {testStatus}"
            self.create_label(test_text, row=r_value, column=3, colspan=4)
            r_value += 1

    def get_referred_cases(self):
        """Fetches and displays referred cases for the doctor."""
        records_list = client.transact("docrecords", DoctorLogin.doctorId)
        id_value = tk.IntVar()
        r_value = 4

        for timeStamp, ID, ptName in records_list:
            text = f"Appt ID {ID} treated {ptName} on {timeStamp}"
            tk.Radiobutton(self, text=text, variable=id_value, value=ID).grid(row=r_value, column=0, columnspan=2)
            r_value += 1

        self.create_button("Show Record", lambda: self.show_record(str(id_value.get())),
                           row=r_value, column=0)

class StaffLogin(BasePage):
    """Staff dashboard page."""

    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.create_label("Staff Dashboard", row=0, column=0, colspan=2, font=LARGE_FONT, pady=10, padx=10)
        self.create_button("Logout", lambda: controller.get_frame(LoginPage), row=1, column=0, colspan=2)
