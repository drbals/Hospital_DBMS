import datetime
import pickle
import socket
import threading
import mysql.connector
import hashlib

HEADER = 64
PORT = 5050
MASTER_PASSWORD = "maaappalammabangaram"
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"


def dbconnect(*args):
    mycursor = mydb.cursor()
    args = list(args)
    if args[0] == "record retrieve":
        sql = f'SELECT AppointmentID, AppointmentTimestamp, Records.PatientID, Patient.PatientName, Records.DoctorID, Doctor.DocName FROM Records LEFT JOIN patient ON records.PatientID = patient.PatientID LEFT JOIN doctor ON records.DoctorID = doctor.DocID WHERE AppointmentID = {args[1]}'
        mycursor.execute(sql)
        result1 = mycursor.fetchone()
        sql = f'SELECT TestName, TestCost, StatusofTest FROM testsprescribed LEFT JOIN Tests ON testsprescribed.testno = tests.testno WHERE AppointmentID = {args[1]}'
        mycursor.execute(sql)
        result2 = mycursor.fetchall()
        sql = f'SELECT MedName, MedCost, Quantity FROM medsprescribed LEFT JOIN Medicines ON medsprescribed.medid = medicines.medid WHERE AppointmentID = {args[1]}'
        mycursor.execute(sql)
        result3 = mycursor.fetchall()
        mycursor.close()
        return result1, result2, result3
    elif args[0] == 'check':
        sql = f'SELECT COUNT(*) FROM PatientCredentials where PatientEmail =\'{args[1]}\''
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result[0]:
            print(f'user: {args[1]} already taken')
            mycursor.close()
            return True
        else:
            print(f'user: {args[1]} is not taken')
            mycursor.close()
            return False
    elif args[0] == 'signup':
        args[-1] = hashlib.md5(args[-1].encode()).hexdigest()
        args = tuple(args)
        sql = f'INSERT INTO Patient(PatientName,PatientDOB,PatientGender,PatientAddress,PatientPhNo,PatientEmail,TreatmentCostUnpaid,MedsCostUnpaid,TestCostUnpaid,AccomodationCostUnpaid) VALUES {args[1:-1]}'
        mycursor.execute(sql)
        sql = f'INSERT INTO PatientCredentials(PatientEmail,PatientID,MD5HashedPassword) VALUES (\'{args[6]}\', last_insert_id(), \'{args[-1]}\');'
        mycursor.execute(sql)
        mycursor.close()
        return True
    elif args[0] == 'login':
        args[-1] = hashlib.md5(args[-1].encode()).hexdigest()
        args = tuple(args)
        sql = f'SELECT COUNT(*), PatientID FROM PatientCredentials where PatientEmail =\'{args[1]}\' and MD5HashedPassword=\'{args[-1]}\''
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result[0]:
            print(f'user: {args[1]} logged in')
            mycursor.close()
            return result[1]
        else:
            mycursor.close()
            return False
    elif args[0] == 'doccheck':
        sql = f'SELECT COUNT(*) FROM DocCredentials where DocEmail =\'{args[1]}\''
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result[0]:
            print(f'user: {args[1]} already taken')
            mycursor.close()
            return True
        else:
            print(f'user: {args[1]} is not taken')
            mycursor.close()
            return False
    elif args[0] == 'docsignup':
        if args[1] == MASTER_PASSWORD:
            args[-1] = hashlib.md5(args[-1].encode()).hexdigest()
            args = tuple(args)
            sql = f'INSERT INTO Doctor(DocName,DeptNo,DocDOB,DocGender,DocAddress,DocPhNo,DocSalary,DocEmail) VALUES {args[2:-1]}'
            mycursor.execute(sql)
            sql = f'INSERT INTO DocCredentials(DocEmail,DocID,MD5HashedPassword) VALUES (\'{args[9]}\', last_insert_id(), \'{args[-1]}\');'
            mycursor.execute(sql)
            temp = datetime.datetime.now()
            sql = f'UPDATE Doctor SET BookedTillTimeStamp = \'{datetime.datetime(year=temp.year, month=temp.month, day=temp.day) + datetime.timedelta(days=1, hours=9)}\' WHERE DocID = last_insert_id()'
            mycursor.execute(sql)
            mycursor.close()
            return True
        else:
            mycursor.close()
            return False
    elif args[0] == 'doclogin':
        args[-1] = hashlib.md5(args[-1].encode()).hexdigest()
        args = tuple(args)
        sql = f'SELECT COUNT(*), DocID FROM DocCredentials where DocEmail =\'{args[1]}\' and MD5HashedPassword=\'{args[-1]}\''
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result[0]:
            print(f'user: {args[1]} logged in')
            mycursor.close()
            return result[1]
        else:
            mycursor.close()
            return False
    elif args[0] == "patientdetails":
        sql = f'SELECT * FROM Patient WHERE PatientID = {args[1]}'
        mycursor.execute(sql)
        result = mycursor.fetchone()
        mycursor.close()
        return result
    elif args[0] == "docdetails":
        sql = f'SELECT Doctor.* , Dept.Deptname FROM Doctor LEFT JOIN Dept ON Doctor.DeptNo = Dept.DeptNo WHERE Doctor.DocID = {args[1]}'
        mycursor.execute(sql)
        result = mycursor.fetchone()
        mycursor.close()
        return result
    elif args[0] == "patientrecords":
        sql = f'SELECT AppointmentTimestamp, AppointmentID, DocName FROM Records LEFT JOIN Doctor ON Records.DoctorID = Doctor.DocID WHERE PatientID = {args[1]}'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        mycursor.close()
        return result
    elif args[0] == "docrecords":
        sql = f'SELECT AppointmentTimestamp, AppointmentID, PatientName FROM Records LEFT JOIN Patient ON Records.PatientID = Patient.PatientID WHERE DoctorID = {args[1]}'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        mycursor.close()
        return result
    elif args[0] == 'appointmentdept':
        sql = f'SELECT DeptNo, Deptname FROM Dept'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        mycursor.close()
        return result
    elif args[0] == 'appointmentdoc':
        if len(args) == 1:
            sql = f'SELECT DocID, DocName FROM Doctor WHERE DeptNo IS NOT NULL'
        else:
            sql = f'SELECT DocID, DocName FROM Doctor WHERE DeptNo={args[1]}'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        mycursor.close()
        return result
    elif args[0] == "nextslot":
        sql = f'SELECT BookedTillTimeStamp FROM Doctor WHERE DocID={args[1]}'
        mycursor.execute(sql)
        result = mycursor.fetchone()
        mycursor.close()
        return result[0]
    elif args[0] == 'bookslot':
        sql = f'SELECT BookedTillTimeStamp FROM Doctor WHERE DocID={args[2]}'
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result[0] == args[3]:
            temp = args[3] + datetime.timedelta(minutes=15)
            # lunch break for an hour from 1 p.m.
            if temp.hour == 13:
                temp = temp + datetime.timedelta(hours=1)
            # shift ends at 6 p.m.
            elif temp.hour == 18:
                temp = temp + datetime.timedelta(hours=15)
            sql = f'INSERT INTO Records(PatientID, DoctorID, AppointmentTimestamp) values ({args[1]},{args[2]}, \'{args[3]}\')'
            mycursor.execute(sql)
            sql = 'SELECT LAST_INSERT_ID()'
            mycursor.execute(sql)
            result = mycursor.fetchone()
            sql = f'UPDATE Doctor SET BookedTillTimeStamp=\'{temp}\' where DocID={args[2]}'
            mycursor.execute(sql)
            mycursor.close()
            return result[0]
        else:
            return False
    elif args[0] == "showmedslist":
        sql = f'SELECT MedID, MedName FROM Medicines'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        mycursor.close()
        return result
    elif args[0] == "prescribemeds":
        for i, j in args[2]:
            sql = f'INSERT INTO MedsPrescribed VALUES ({args[1]}, {i}, {j}, 0)'
            mycursor.execute(sql)
        mycursor.close()
        return True
    elif args[0] == "prescribetests":
        for i in args[2]:
            sql = f'INSERT INTO TestsPrescribed(AppointmentID, TestNo, StatusofTest) VALUES ({args[1]}, {i}, \'Not Done\')'
            mycursor.execute(sql)
        mycursor.close()
        return True
    elif args[0] == "uploadtestresult":
        sql = """UPDATE TestsPrescribed SET Report = %s WHERE AppointmentID = %s AND TestNo = %s"""
        mycursor.execute(sql, (args[3], args[1], args[2]))
        sql = f'UPDATE TestsPrescribed SET StatusofTest = \'ReportCame\' WHERE AppointmentID = {args[1]} AND TestNo = {args[2]}'
        mycursor.execute(sql)
        mycursor.close()
        return True
    elif args[0] == "checkroomallotted":
        sql = f'SELECT COUNT(*) FROM Accomodation where AppointmentID ={args[1]}'
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result[0]:  # room already allotted
            mycursor.close()
            return True
        else:  # room not allotted
            mycursor.close()
            return False
    elif args[0] == "showroomavl":
        sql = f'SELECT RoomNo, Availability FROM RoomAvl ORDER BY Availability DESC'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        mycursor.close()
        return result
    elif args[0] == "bookroom":
        sql = f'SELECT Availability FROM RoomAvl WHERE RoomNo = {args[2]}'
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result[0] == 'True':
            sql = f'UPDATE RoomAvl SET Availability = \'False\' WHERE RoomNo = {args[2]}'
            mycursor.execute(sql)
            sql = f'INSERT INTO Accomodation(AppointmentID,RoomNo,CheckIN) VALUES ({args[1]}, {args[2]}, NOW())'
            mycursor.execute(sql)
            mycursor.close()
            return True
        else:
            return False
    elif args[0] == "checkoutroom":
        sql = f'SELECT CheckOUT, RoomNo FROM Accomodation WHERE AppointmentID = {args[1]}'
        mycursor.execute(sql)
        result = mycursor.fetchone()
        if result[0] is None and result[1] is not None:
            sql = f'UPDATE Accomodation SET CheckOUT = NOW() WHERE RoomNo = AppointmentID = {args[1]}'
            mycursor.execute(sql)
            sql = f'UPDATE RoomAvl SET Availability = \'True\' WHERE RoomNo = {result[1]}'
            mycursor.execute(sql)
            mycursor.close()
            return True
        else:
            return False
    elif args[0] == "showPrescribedMeds":
        pass
        sql = f'SELECT medsprescribed.MedID, MedName, Quantity, MedCost as UnitCost ' \
              f'FROM medsprescribed Left join medicines on medsprescribed.MedID = medicines.MedID ' \
              f'where AppointmentID = {args[1]}'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        mycursor.close()
        return result
    elif args[0] == "givemeds":
        for i, j in args[2]:
            sql = f'UPDATE medsprescribed set Given = {j} where appointmentid = {args[1]} and medid = {i}'
            mycursor.execute(sql)
        mycursor.close()
        return True
    elif args[0] == "performtests":
        for i in args[2]:
            sql = f'update testsprescribed set StatusofTest = \'Taken\' where AppointmentID = {args[1]} and TestNo = {i}'
            mycursor.execute(sql)
        mycursor.close()
        return True
    elif args[0] == "getreport":
        mydbtemp = mysql.connector.connect(
            host="localhost",
            user="Hospital",
            password="appalamma",
            database="hospital",
            use_pure=True
        )
        mycursortemp = mydbtemp.cursor()
        sql = f'SELECT Report FROM TestsPrescribed WHERE AppointmentID = {args[1]} AND TestNo = {args[2]}'
        mycursortemp.execute(sql)
        result = mycursortemp.fetchone()
        mycursortemp.close()
        mydbtemp.close()
        mycursor.close()
        return result[0]
    elif args[0] == "pay":
        sql = f'UPDATE Patient ' \
              f'SET TreatmentCostUnpaid = TreatmentCostUnpaid - {args[2]} , MedsCostUnpaid = MedsCostUnpaid - {args[3]}, ' \
              f'TestCostUnpaid = TestCostUnpaid - {args[4]}, AccomodationCostUnpaid = AccomodationCostUnpaid - {args[5]} ' \
              f'WHERE PatientID = {args[1]}'
        mycursor.execute(sql)
        mycursor.close()
        return True


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = pickle.loads(conn.recv(msg_length))
            if msg[0] == DISCONNECT_MESSAGE:
                connected = False
                print(f"[{addr}] Requested to close connection")
                result = True
            else:
                print(f"[{addr}] {msg[0]}")
                result = dbconnect(*msg)
                mydb.commit()
            message = pickle.dumps(result)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            conn.send(send_length)
            conn.send(message)
    conn.close()
    return


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER_IP}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


if __name__ == '__main__':
    SERVER_IP = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER_IP, PORT)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    print("[STARTING] server is starting...")
    mydb = mysql.connector.connect(
        host="localhost",
        user="Hospital",
        password="appalamma",
        database="hospital"
    )
    start()
