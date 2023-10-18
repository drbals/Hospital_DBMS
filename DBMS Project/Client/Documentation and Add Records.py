import connectiontodb

# Adding Patients to Database
print(connectiontodb.transact("signup", "Patient1", '1999-09-05', "Male",
                              r"D.no: 6-23/3, Street1, Landmark1, Visakhapatnam - 531019",
                              7680005343, "patient1@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(connectiontodb.transact("signup", "Patient2", '1989-07-02', "Female",
                              r"D.no: 6-23/3, Street2, Landmark2, Visakhapatnam - 531019",
                              7680005343, "patient2@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(connectiontodb.transact("signup", "Patient3", '1993-01-05', "Male",
                              r"D.no: 6-23/3, Street3, Landmark3, Visakhapatnam - 531019",
                              7680005343, "patient3@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(connectiontodb.transact("signup", "Patient4", '1970-10-05', "Male",
                              r"D.no: 6-23/3, Street1, Landmark1, Visakhapatnam - 531019",
                              7680005343, "patient4@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(connectiontodb.transact("signup", "Patient5", '1999-09-05', "Female",
                              r"D.no: 6-23/3, Street5, Landmark5, Visakhapatnam - 531019",
                              7680005343, "patient5@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(connectiontodb.transact("signup", "Patient6", '1982-12-05', "Female",
                              r"D.no: 6-23/3, Street6, Landmark6, Visakhapatnam - 531019",
                              7680005343, "patient6@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(connectiontodb.transact("signup", "Patient7", '1979-06-28', "Female",
                              r"D.no: 6-23/3, Street7, Landmark7, Visakhapatnam - 531019",
                              7680005343, "patient7@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(connectiontodb.transact("signup", "Patient8", '1990-03-14', "Male",
                              r"D.no: 6-23/3, Street1, Landmark1, Visakhapatnam - 531019",
                              7680005343, "patient8@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(connectiontodb.transact("signup", "Patient9", '1987-05-27', "Male",
                              r"D.no: 6-23/3, Street1, Landmark1, Visakhapatnam - 531019",
                              7680005343, "patient9@gmail.com", 0, 0, 0, 0, "qwerty123"))
print(connectiontodb.transact("signup", "Patient10", '1990-05-09', "Female",
                              r"D.no: 6-23/3, Street10, Landmark10, Visakhapatnam - 531019",
                              7680005343, "patient10@gmail.com", 0, 0, 0, 0, "qwerty123"))

# Adding Doctors
print(connectiontodb.transact("docsignup", "maaappalammabangaram", "Doctor1", 1, '1980-09-05', "Male",
                              r"D.no: 6-23/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                              7680005343, 200000, "doctor1@gmail.com", "qwerty123"));
print(connectiontodb.transact("docsignup", "maaappalammabangaram", "Doctor2", 1, '1981-09-05', "Male",
                              r"D.no: 6-24/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                              7680005343, 200000, "doctor2@gmail.com", "qwerty123"))
print(connectiontodb.transact("docsignup", "maaappalammabangaram", "Doctor3", 2, '1982-09-05', "Female",
                              r"D.no: 6-25/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                              7680005343, 200000, "doctor3@gmail.com", "qwerty123"))
print(connectiontodb.transact("docsignup", "maaappalammabangaram", "Doctor4", 3, '1983-09-05', "Male",
                              r"D.no: 6-26/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                              7680005343, 200000, "doctor4@gmail.com", "qwerty123"))
print(connectiontodb.transact("docsignup", "maaappalammabangaram", "Doctor5", 3, '1984-09-05', "Female",
                              r"D.no: 6-27/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                              7680005343, 200000, "doctor5@gmail.com", "qwerty123"))
print(connectiontodb.transact("docsignup", "maaappalammabangaram", "Doctor6", 2, '1985-09-05', "Female",
                              r"D.no: 6-28/3, Doctors Colony, Lankelapalem, Visakhapatnam - 531019",
                              7680005343, 200000, "doctor6@gmail.com", "qwerty123"))

# check if the email is already taken
print(connectiontodb.transact("check", "ashishdasari148@gmail.com"))
# add patient
print(connectiontodb.transact("signup", "Ashish Dasari", '1999-09-05', "Male",
                              r"D.no: 6-23/3, Sri Ranganagar Colony, Lankelapalem, Visakhapatnam - 531019",
                              7680005343, "ashishdasari148@gmail.com", 0, 0, 0, 0, "qwerty123"))
# patient login
print(connectiontodb.transact("login", "ashishdasari148@gmail.com", "qwerty123"))
# check if the doc email is already taken
print(connectiontodb.transact("doccheck", "ashishdasari148@gmail.com"))
# add doc
print(connectiontodb.transact("docsignup", "maaappalammabangaram", "Ashish Dasari", 1, '1999-09-05', "Male",
                              r"D.no: 6-23/3, Sri Ranganagar Colony, Lankelapalem, Visakhapatnam - 531019",
                              7680005343, 200000, "ashishdasari148@gmail.com", "qwerty123"))
# Doctor login
print(connectiontodb.transact("doclogin", "ashishdasari148@gmail.com", "qwerty123"))

# get list of all departments
print(connectiontodb.transact("appointmentdept"))

# get list of all doctors
print(connectiontodb.transact("appointmentdoc"))

# get list of doctors in a given dept
print(connectiontodb.transact("appointmentdoc", 1))

# get next available slot of given doctor as datetime.datetime object
print(connectiontodb.transact("nextslot", 1))
nextslot = connectiontodb.transact("nextslot", 1)
# book slot parameters : "bookslot", PatientID, DocID, previously received nextslot
# returns appointmentid on success, else False
print(connectiontodb.transact("bookslot", 1, 1, nextslot))
# showmedslist
print(connectiontodb.transact("showmedslist"))
# prescribe meds parameters : "prescribemeds", appointmentid, list of [medid,quantity]
print(connectiontodb.transact("prescribemeds", 1, [[1, 1], [4, 2], [6, 3], [20, 5]]))
# prescribe tests parameters : "prescribetests", appointmentid, list of tests
print(connectiontodb.transact("prescribetests", 1, [1, 4, 6, 20]))
# check if room already alloted for an appointment ID
print(connectiontodb.transact("checkroomallotted", 1))
# show room availability
print(connectiontodb.transact("showroomavl"))
# book an available room parameters : "bookroom", appointmentid, roomno
print(connectiontodb.transact("bookroom", 1, 1))
# checkout parameters : "checkoutroom", appointmentid
print(connectiontodb.transact("checkoutroom", 1))
# show PrescribedMeds by appointment id
print(connectiontodb.transact("showPrescribedMeds", 1))
# medical shop give meds
print(connectiontodb.transact("givemeds", 1, [[1, 1], [4, 1], [6, 2], [20, 3]]))
# lab perform test
print(connectiontodb.transact("performtests", 1, [1, 6]))
# upload test result
f = open("C:/Users/ashis/Downloads/file-example_PDF_1MB.pdf", "rb")
bstr = f.read()
print(connectiontodb.transact("uploadtestresult", 1, 4, bstr))
# pay bills
print(connectiontodb.transact("pay", 1, 300, 400, 500, 500))
# get report
bstr = connectiontodb.transact("getreport", 1, 4)
f = open("temp.pdf", 'wb')
f.write(bstr)
f.close()

# get patient details
print(connectiontodb.transact("patientdetails", 1))
# get doc details
print(connectiontodb.transact("docdetails", 1))

# Get list of patient records
print(connectiontodb.transact("patientrecords", 1))
# get list of doctor records
print(connectiontodb.transact("docrecords", 1))
# get record details
print(connectiontodb.transact("record retrieve", 1))


# client disconnect
print(connectiontodb.transact(connectiontodb.DISCONNECT_MESSAGE))
