from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
import mysql.connector
from datetime import datetime
import cdb

root = Tk()
root.title("Patient Dashboard")
root.iconbitmap("images/house.ico")
root.geometry("1200x600")

# --------------------------------PATIENT DASHBOARD
PATIENT_ID = 1
slotLbl = Label(root, text="")

history_lbl = Label(root, text="Appointment & Patient History", relief=SUNKEN, anchor='center', width=50, bg="green", fg="white")
history_lbl.grid(row=0, column=0, columnspan=4, sticky=N + S + E + W)

record_lbl = Label(root, text="Record Details", relief=SUNKEN, anchor='center', width=60, bg="blue", fg="white")
record_lbl.grid(row=0, column=4, columnspan=4, sticky=N + S + E + W)

def docDisplay():
    global docList, docListResult, docDrop
    deptNoClicked = giveNum(deptListResult, deptClicked.get())
    docListResult = cdb.transact("appointmentdoc", deptNoClicked)
    docList = [row[1] for row in docListResult]
    docDrop = OptionMenu(root, docClicked, *docList)
    docDrop.grid(row=1, column=1)

def giveNum(deplist, dept):
    for i in range(0, len(deplist)):
        if deplist[i][1] == dept:
            return deplist[i][0]
    return 0

def slotDisplay():
    global docNoClicked, nextSlot, slotLbl, bookBtn
    docNoClicked = giveNum(docListResult, docClicked.get())
    nextSlot = cdb.transact("nextslot", docNoClicked)
    slotLbl = Label(root, text="NextSlot at "+str(nextSlot), bg="yellow")
    slotLbl.grid(row=3, column=0)
    bookBtn = Button(root, text="Book slot", command=lambda: bookSlot(docNoClicked, nextSlot))
    bookBtn.grid(row=3, column=1)


def bookSlot(docNo, slotnext):
    global PATIENT_ID
    status = cdb.transact("bookslot", PATIENT_ID, docNo, slotnext)
    if not status:
        messagebox.showinfo("Lifeline Hospitals", "Slot not booked!")
    else:
        messagebox.showinfo("Lifeline Hospitals", "Slot booked! Your AppointmentID is "+str(status))
    slotLbl.destroy()
    bookBtn.destroy()
    getRecords()

def showRecord(id):
    if id == 0:
        messagebox.showinfo("Lifeline Hospitals", "Please select a record!")
        return
    detailsList, testsList, medsList = cdb.transact("record retrieve", id)
    apptIdLbl = Label(root, text="Appt.ID: "+str(detailsList[0]))
    apptIdLbl.grid(row=1, column=4)
    apptTimeLbl = Label(root, text="Appt.Time: "+ str(detailsList[1]))
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

    meds_lbl = Label(root, text="Medicines Prescribed", relief=SUNKEN, anchor='center', width=60, bg="blue", fg="white")
    meds_lbl.grid(row=4, column=4, columnspan=4, sticky=N + S + E + W)
    r_value = 5
    # Medicines prescribed Heading
    medLbl = Label(root, text="Medicine Name" + "              " + "Quantity" + "               " + "Cost Per Medicine")
    medLbl.grid(row=r_value, column=4, columnspan=4, sticky=N + S + E + W)
    r_value += 1
    for med, medCost, medQuantity in medsList:
        medLbl= Label(root, text=med + "                           " + str(medQuantity) + "                            " + str(medCost)+"/-")
        medLbl.grid(row=r_value, column=4, columnspan=4, sticky=N + S + E + W)
        r_value += 1
    # Tests prescribed Heading
    tests_lbl = Label(root, text="Tests Prescribed", relief=SUNKEN, anchor='center', width=60, bg="blue", fg="white")
    tests_lbl.grid(row=r_value, column=4, columnspan=4, sticky=N + S + E + W)
    r_value += 1
    testLbl = Label(root, text="Test Name" + "               " + "Test Cost" + "              " + "Test Status" )
    testLbl.grid(row=r_value, column=4, columnspan=3, sticky=N + S + E + W)
    r_value += 1

    for testName, testCost, testStatus in testsList:
        testLbl = Label(root, text=testName + "                     " + str(testCost)+ "/-" + "                      " + str(testStatus))
        testLbl.grid(row=r_value, column=4, columnspan=3, sticky=N + S + E + W)
        r_value += 1


def getRecords():
    recordsList = cdb.transact("patientrecords", PATIENT_ID)
    idValue = IntVar()
    r_value = 5
    c_value = 0
    for timeStamp, ID, docName in recordsList:
        Radiobutton(root, text="Appt ID " + str(ID) + " with "+docName + " on "+str(timeStamp), variable=idValue, value=ID).grid(row=r_value, column=c_value)
        r_value += 1
    recordBtn = Button(root, text="Show Record", command=lambda: showRecord(idValue.get()))
    recordBtn.grid(row=r_value, column=0)


# DeptList Dropdown
deptListResult = cdb.transact("appointmentdept")
deptList = [row[1] for row in deptListResult]
deptClicked = StringVar()
deptClicked.set("Select Department")
deptDrop = OptionMenu(root, deptClicked, *deptList)
deptDrop.grid(row=1, column=0)

deptBtn = Button(root, text="See Doctors", command=docDisplay)
deptBtn.grid(row=2, column=0)

# DocList Dropdown
docList = ["Select Doctor"]
docListResult =[]
docClicked = StringVar()
docClicked.set("Select Doctor")
docDrop = OptionMenu(root, docClicked, *docList)
docDrop.grid(row=1, column=1)
nextSlot = datetime.now()
docNoClicked = 0
docBtn = Button(root, text="show next slot", command=slotDisplay)
docBtn.grid(row=2, column=1)

# bookSlot button
bookBtn = Button(root, text="Book slot", command=lambda: bookSlot(docNoClicked, nextSlot))

# Past Records
recordsLbl = Label(root, text="Past Records", bg="red", fg="white")
recordsLbl.grid(row=4, column=0, pady=10, sticky= W + E)
getRecords()


details_lbl = Label(root, text="Patient Details & Reports", relief=SUNKEN, anchor='center', width=60, bg="brown", fg="white")
details_lbl.grid(row=0, column=8, columnspan=4, sticky=N + S + E + W)




root.mainloop()
