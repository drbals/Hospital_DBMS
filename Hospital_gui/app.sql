drop table Accomodation;
drop table RoomAvl;
drop table MedsPrescribed;
drop table Medicines;
drop table TestsPrescribed;
drop table Tests;
drop table Lab;
drop table Records;
drop table DocCredentials;
drop table Doctor;
drop table Dept;
drop table PatientCredentials;
drop table Patient;

create table Patient(
  PatientID int unsigned not null auto_increment,
  primary key(PatientID),
  PatientName varchar(20),
  PatientDOB date,
  PatientGender varchar(7),
  PatientAddress varchar(100),
  PatientPhNo DECIMAL(10,0),
  PatientEmail varchar(25),
  TreatmentCostUnpaid int,
  MedsCostUnpaid int,
  TestCostUnpaid int,
  AccomodationCostUnpaid int
);
create table PatientCredentials(
    PatientEmail varchar(25),
    primary key(PatientEmail),
    PatientID int unsigned,
    MD5HashedPassword varchar(50),
    foreign key(PatientID) references Patient(PatientID) on delete cascade
);
create table Dept(
  DeptNo int unsigned not null auto_increment,
  primary key(DeptNo),
  Deptname varchar(20),
  DeptChief varchar(20)
);
-- Adding Departments
insert into Dept(Deptname,DeptChief)
values ('Department1','Doctor1'),
       ('Department2','Doctor3'),
       ('Department3','Doctor4');
       
create table Doctor(
  DocID int unsigned not null auto_increment,
  primary key(DocID),
  DocName varchar(20),
  DeptNo int unsigned,
  DocDOB date,
  DocGender varchar(7),
  BookedTillTimeStamp timestamp,
  DocAddress varchar(100),
  DocPhNo DECIMAL(10,0),
  DocSalary int,
  DocEmail varchar(25),
  foreign key(DeptNo) references Dept(DeptNo) on delete cascade
);
create table DocCredentials(
    DocEmail varchar(25),
    primary key(DocEmail),
    DocID int unsigned,
    MD5HashedPassword varchar(50),
    foreign key(DocID) references Doctor(DocID) on delete cascade
);
create table Records(
  AppointmentID int unsigned not null auto_increment,
  primary key(AppointmentID),
  PatientID int unsigned,
  DoctorID int unsigned,
  AppointmentTimestamp timestamp,
  foreign key(PatientID) references Patient(PatientID) on delete cascade,
  foreign key(DoctorID) references Doctor(DocID) on delete cascade
);
create trigger fees after insert on records for each row
update patient set TreatmentCostUnpaid = TreatmentCostUnpaid + 300 where PatientID = NEW.PatientID;
create table Lab(
  LabNo int unsigned not null auto_increment,
  primary key(LabNo),
  LabName varchar(15)
);
-- Adding Labs
insert into Lab(LabName)
values ('Lab1'),
	   ('Lab2'),
       ('Lab3'),
       ('Lab4'),
       ('Lab5');
create table Tests(
  TestNo int unsigned not null auto_increment,
  primary key(TestNo),
  LabNo int unsigned,
  TestName varchar(20),
  TestCost  int unsigned,
  foreign key(LabNo) references Lab(LabNo) on delete cascade
);
-- Adding Tests
insert into Tests(LabNo,TestName,TestCost)
values (1,'Test1',500),
       (1,'Test2',200),
       (1,'Test3',200),
       (1,'Test4',250),
       (1,'Test5',600),
       (2,'Test6',1000),
       (2,'Test7',2000),
       (2,'Test8',1500),
       (3,'Test9',300),
       (3,'Test10',400),
       (3,'Test11',200),
       (3,'Test12',200),
       (3,'Test13',900),
       (4,'Test14',1000),
       (4,'Test15',200),
       (4,'Test16',300),
       (5,'Test17',400),
       (5,'Test18',500),
       (5,'Test19',800),
       (5,'Test20',1200);
create table TestsPrescribed(
  AppointmentID int unsigned,
  TestNo int unsigned,
  StatusofTest varchar(10),
  Report longblob,
  primary key(AppointmentID, TestNo),
  foreign key(AppointmentID) references Records(AppointmentID) on delete cascade,
  foreign key(TestNo) references Tests(TestNo) on delete cascade
);

DELIMITER $$
create trigger testperformed after update on TestsPrescribed for each row begin
if (NEW.StatusofTest = 'Taken') then
update Patient SET TestCostUnpaid = TestCostUnpaid + (select TestCost from Tests where TestNo = NEW.TestNo) 
where PatientID = (select patientid from records where appointmentid = NEW.AppointmentID);
end if;
END $$
DELIMITER ;


create table Medicines(
  MedID int unsigned not null auto_increment,
  primary key(MedID),
  MedName varchar(20),
  MedCost int unsigned
);
-- Adding Medicines
insert into Medicines(MedName,MedCost)
values ('Medicine1',100),
       ('Medicine2',100),
       ('Medicine3',100),
       ('Medicine4',200),
       ('Medicine5',200),
       ('Medicine6',200),
       ('Medicine7',200),
       ('Medicine8',200),
       ('Medicine9',200),
       ('Medicine10',300),
       ('Medicine11',300),
       ('Medicine12',300),
       ('Medicine13',300),
       ('Medicine14',300),
       ('Medicine15',300),
       ('Medicine16',300),
       ('Medicine17',300),
       ('Medicine18',300),
       ('Medicine19',40),
       ('Medicine20',400),
       ('Medicine21',400),
       ('Medicine22',400),
       ('Medicine23',400),
       ('Medicine24',400),
       ('Medicine25',500),
       ('Medicine26',500),
       ('Medicine27',500),
       ('Medicine28',500),
       ('Medicine29',500),
       ('Medicine30',500),
       ('Medicine31',500),
       ('Medicine32',500),
       ('Medicine33',500),
       ('Medicine34',100),
       ('Medicine35',100),
       ('Medicine36',100),
       ('Medicine37',100),
       ('Medicine38',100),
       ('Medicine39',70),
       ('Medicine40',700),
       ('Medicine41',700),
       ('Medicine42',50),
       ('Medicine43',50),
       ('Medicine44',50),
       ('Medicine45',50),
       ('Medicine46',50),
       ('Medicine47',60),
       ('Medicine48',20),
       ('Medicine49',20),
       ('Medicine50',20);
create table MedsPrescribed(
  AppointmentID int unsigned,
  MedID int unsigned,
  Quantity int unsigned,
  Given varchar(5),
  primary key(AppointmentID, MedID),
  foreign key(AppointmentID) references Records(AppointmentID) on delete cascade,
  foreign key(MedID) references Medicines(MedID) on delete cascade
);
create trigger medsgiven after update on MedsPrescribed for each row
update Patient SET MedsCostUnpaid = MedsCostUnpaid + ((select MedCost from Medicines where MedID = NEW.MedID)*(NEW.Given - Old.Given)) where PatientID = (select patientid from records where appointmentid = NEW.AppointmentID);
create table RoomAvl(
  RoomNo int unsigned not null auto_increment,
  primary key(RoomNo),
  Availability varchar(5)
);
-- Adding Room Availability
insert into RoomAvl(Availability)
values ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('False'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('False'),
       ('True'),
       ('True'),
       ('True'),
       ('False'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('False'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('False'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True'),
       ('True');
create table Accomodation(
  AppointmentID int unsigned not null auto_increment,
  primary key(AppointmentID),
  RoomNo int unsigned,
  CheckIN timestamp,
  CheckOUT timestamp,
  foreign key(AppointmentID) references Records(AppointmentID) on delete cascade,
  foreign key(RoomNo) references RoomAvl(RoomNo) on delete cascade
);
create trigger roomcheckout after update on Accomodation for each row
Update patient set AccomodationCostUnpaid = 1000 * (TIMESTAMPDIFF(DAY, NEW.CheckOUT, New.CheckIN)+1) where PatientID = (select patientid from records where appointmentid = NEW.AppointmentID);