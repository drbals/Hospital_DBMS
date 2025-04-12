import client

# Adding Patients to Database
print(client.transact("signup", "Patient1", '1999-09-05', "Male",
                              r"D.no: 6-23/3, Street1, Landmark1, Visakhapatnam - 531019",
                   7680005343, "patient1@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(client.transact("signup", "Patient2", '1989-07-02', "Female",
                              r"D.no: 6-23/3, Street2, Landmark2, Visakhapatnam - 531019",
                   7680005343, "patient2@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(client.transact("signup", "Patient3", '1993-01-05', "Male",
                              r"D.no: 6-23/3, Street3, Landmark3, Visakhapatnam - 531019",
                   7680005343, "patient3@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(client.transact("signup", "Patient4", '1970-10-05', "Male",
                              r"D.no: 6-23/3, Street1, Landmark1, Visakhapatnam - 531019",
                   7680005343, "patient4@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(client.transact("signup", "Patient5", '1999-09-05', "Female",
                              r"D.no: 6-23/3, Street5, Landmark5, Visakhapatnam - 531019",
                   7680005343, "patient5@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(client.transact("signup", "Patient6", '1982-12-05', "Female",
                              r"D.no: 6-23/3, Street6, Landmark6, Visakhapatnam - 531019",
                   7680005343, "patient6@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(client.transact("signup", "Patient7", '1979-06-28', "Female",
                              r"D.no: 6-23/3, Street7, Landmark7, Visakhapatnam - 531019",
                   7680005343, "patient7@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(client.transact("signup", "Patient8", '1990-03-14', "Male",
                              r"D.no: 6-23/3, Street1, Landmark1, Visakhapatnam - 531019",
                   7680005343, "patient8@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(client.transact("signup", "Patient9", '1987-05-27', "Male",
                              r"D.no: 6-23/3, Street1, Landmark1, Visakhapatnam - 531019",
                   7680005343, "patient9@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(client.transact("signup", "Patient10", '1990-05-09', "Female",
                              r"D.no: 6-23/3, Street10, Landmark10, Visakhapatnam - 531019",
                   7680005343, "patient10@gmail.com", 0, 0, 0, 0, "qwerty123"))

# Adding Doctors
print(client.transact("docsignup", "doctorPass", "Doctor1", 1, '1980-09-05', "Male",
                              r"D.no: 6-23/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                   7680005343, 200000, "doctor1@gmail.com", "qwerty123"))
print(client.transact("docsignup", "doctorPass", "Doctor2", 1, '1981-09-05', "Male",
                              r"D.no: 6-24/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                   7680005343, 200000, "doctor2@gmail.com", "qwerty123"))
print(client.transact("docsignup", "doctorPass", "Doctor3", 2, '1982-09-05', "Female",
                              r"D.no: 6-25/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                   7680005343, 200000, "doctor3@gmail.com", "qwerty123"))
print(client.transact("docsignup", "doctorPass", "Doctor4", 3, '1983-09-05', "Male",
                              r"D.no: 6-26/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                   7680005343, 200000, "doctor4@gmail.com", "qwerty123"))
print(client.transact("docsignup", "doctorPass", "Doctor5", 3, '1984-09-05', "Female",
                              r"D.no: 6-27/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                   7680005343, 200000, "doctor5@gmail.com", "qwerty123"))
print(client.transact("docsignup", "doctorPass", "Doctor6", 2, '1985-09-05', "Female",
                              r"D.no: 6-28/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                   7680005343, 200000, "doctor6@gmail.com", "qwerty123"))

# check if the email is already taken
print(client.transact("check", "ashishdasari148@gmail.com"))
# add patient
print(client.transact("signup", "Ashish Dasari", '1999-09-05', "Male",
                              r"D.no: 6-23/3, Sri Ranganagar Colony, Lankelapalem, Visakhapatnam - 531019",
                   7680005343, "ashishdasari148@gmail.com", 0, 0, 0, 0, "qwerty123"))
# patient login
print(client.transact("login", "ashishdasari148@gmail.com", "qwerty123"))
# check if the doc email is already taken
print(client.transact("doccheck", "ashishdasari148@gmail.com"))
# add doc
print(client.transact("docsignup", "doctorPass", "Ashish Dasari", 1, '1999-09-05', "Male",
                              r"D.no: 6-23/3, Sri Ranganagar Colony, Lankelapalem, Visakhapatnam - 531019",
                   7680005343, 200000, "ashishdasari148@gmail.com", "qwerty123"))
# Doctor login
print(client.transact("doclogin", "ashishdasari148@gmail.com", "qwerty123"))

# get list of all departments
print(client.transact("appointmentdept"))

# get list of all doctors
print(client.transact("appointmentdoc"))

# get list of doctors in a given dept
print(client.transact("appointmentdoc", 1))

# get next available slot of given doctor as datetime.datetime object
print(client.transact("nextslot", 1))
nextslot = client.transact("nextslot", 1)
# book slot parameters : "bookslot", PatientID, DocID, previously received nextslot
# returns appointmentid on success, else False
print(client.transact("bookslot", 1, 1, nextslot))
# showmedslist
print(client.transact("showmedslist"))
# prescribe meds parameters : "prescribemeds", appointmentid, list of [medid,quantity]
print(client.transact("prescribemeds", 1, [[1, 1], [4, 2], [6, 3], [20, 5]]))
# prescribe tests parameters : "prescribetests", appointmentid, list of tests
print(client.transact("prescribetests", 1, [1, 4, 6, 20]))
# check if room already alloted for an appointment ID
print(client.transact("checkroomallotted", 1))
# show room availability
print(client.transact("showroomavl"))
# book an available room parameters : "bookroom", appointmentid, roomno
print(client.transact("bookroom", 1, 1))
# checkout parameters : "checkoutroom", appointmentid
print(client.transact("checkoutroom", 1))
# show PrescribedMeds by appointment id
print(client.transact("showPrescribedMeds", 1))
# medical shop give meds
print(client.transact("givemeds", 1, [[1, 1], [4, 1], [6, 2], [20, 3]]))
# lab perform test
print(client.transact("performtests", 1, [1, 6]))
# upload test result
f = open("Invoice.pdf", "rb")
bstr = f.read()
print(client.transact("uploadtestresult", 1, 4, bstr))
# pay bills
print(client.transact("pay", 1, 300, 400, 500, 500))
# get report
bstr = client.transact("getreport", 1, 4)
f = open("temp.pdf", 'wb')
f.write(bstr)
f.close()

# get patient details
print(client.transact("patientdetails", 1))
# get doc details
print(client.transact("docdetails", 1))

# Get list of patient records
print(client.transact("patientrecords", 1))
# get list of doctor records
print(client.transact("docrecords", 1))
# get record details
print(client.transact("record retrieve", 1))


# client disconnect
print(client.transact(client.DISCONNECT_MESSAGE))
