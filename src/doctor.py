from tkinter import *
from tkinter import messagebox
import client

root = Tk()
root.title("Doctor Dashboard")
root.iconbitmap("images/house.ico")
root.geometry("1200x600")

# --------------------------------DOCTOR DASHBOARD
DOCTOR_ID = 1


history_lbl = Label(root, text="Medical History", relief=SUNKEN, anchor='center', width=20, bg="green", fg="white")
history_lbl.grid(row=0, column=0, columnspan=3, sticky=N + S + E + W)


record_lbl = Label(root, text="Record Details", relief=SUNKEN, anchor='center', width=60, bg="blue", fg="white")
record_lbl.grid(row=0, column=3, columnspan=4, sticky=N + S + E + W)


prescribe_lbl = Label(root, text="Prescription & Reports", relief=SUNKEN, anchor='center', width=60, bg="brown", fg="white")
prescribe_lbl.grid(row=0, column=7, columnspan=4, sticky=N + S + E + W)

def showRecord(id):
    if id == 0 or id == "Enter":
        messagebox.showinfo("Lifeline Hospitals", "Please select a record!")
    else:
        detailsList, testsList, medsList = cdb.transact("record retrieve", id)
        apptIdLbl = Label(root, text="Appt.ID: " + str(detailsList[0]))
        apptIdLbl.grid(row=1, column=4)
        apptTimeLbl = Label(root, text="Appt.Time: " + str(detailsList[1]))
        apptTimeLbl.grid(row=1, column=6)
        ptIdLbl = Label(root, text="Patient ID: " + str(detailsList[2]))
        ptIdLbl.grid(row=2, column=4)
        ptNameLbl = Label(root, text="Patient Name: " + str(detailsList[3]))
        ptNameLbl.grid(row=2, column=6)
        docIdLbl = Label(root, text="Doctor ID: " + str(detailsList[4]))
        docIdLbl.grid(row=3, column=4)
        docNameLbl = Label(root, text="Doctor Name: " + str(detailsList[5]))
        docNameLbl.grid(row=3, column=6)
        # diseaseNameLbl = Label(root, text="Disease Name: " + str(detailsList[6]))
        # diseaseNameLbl.grid(row=4, column=4, columnspan=4)

        # Medicines prescribed Heading
        meds_lbl = Label(root, text="Medicines Prescribed", relief=SUNKEN, anchor='center', width=50, bg="blue",fg="white")
        meds_lbl.grid(row=4, column=3, columnspan=4, sticky=N + S + E + W)
        r_value = 5

        medLbl = Label(root, text="Medicine Name" + "              " + "Quantity" + "               " + "Cost Per Medicine")
        medLbl.grid(row=r_value, column=3, columnspan=4, sticky=N + S + E + W)
        r_value += 1
        for med, medCost, medQuantity in medsList:
            medLbl = Label(root, text=med + "                           " + str(
                medQuantity) + "                            " + str(medCost) + "/-")
            medLbl.grid(row=r_value, column=3, columnspan=4, sticky=N + S + E + W)
            r_value += 1

        # Tests prescribed Heading
        tests_lbl = Label(root, text="Tests Prescribed", relief=SUNKEN, anchor='center', width=50, bg="blue",
                          fg="white")
        tests_lbl.grid(row=r_value, column=3, columnspan=4, sticky=N + S + E + W)
        r_value += 1

        testLbl = Label(root, text="Test Name" + "               " + "Test Cost" + "              " + "Test Status")
        testLbl.grid(row=r_value, column=3, columnspan=3, sticky=N + S + E + W)
        r_value += 1
        for testName, testCost, testStatus in testsList:
            testLbl = Label(root, text=testName + "                     " + str(
                testCost) + "/-" + "                      " + str(testStatus))
            testLbl.grid(row=r_value, column=4, columnspan=3, sticky=N + S + E + W)
            r_value += 1



def getReffCases(id):
    recordsList = cdb.transact("docrecords", id)
    idValue = IntVar()
    r_value = 3
    c_value = 0
    for timeStamp, ID, ptName in recordsList:
        Radiobutton(root, text="Appt ID " + str(ID) + " treated "+ ptName + " on "+str(timeStamp), variable=idValue, value=ID).grid(row=r_value, column=c_value, columnspan=2)
        r_value += 1
    recordBtn = Button(root, text="Show Record", command=lambda: showRecord(idValue.get()))
    recordBtn.grid(row=r_value, column=0)


apptIdLbl = Label(root, text="Appointment ID:", anchor=W, width=10)
apptIdLbl.grid(row=1, column=0, sticky= W + E)

idEntry = Entry(root, width=20, bg="white", fg="black", borderwidth="5")
idEntry.grid(row=1, column=1, sticky= W + E)
idEntry.insert(0, "Enter")

getRecBtn = Button(root, text="Show Record", command=lambda: showRecord(idEntry.get()))
getRecBtn.grid(row=1, column=2)

refCasesLbl = Label(root, text="Reffered Cases", bg="red", fg="white")
refCasesLbl.grid(row=2, column=1, pady=10, sticky= W + E)

getReffCases(DOCTOR_ID)

giveMedsLbl = Label(root, text="Prescribe Meds")
root.state('zoomed')
root.mainloop()
