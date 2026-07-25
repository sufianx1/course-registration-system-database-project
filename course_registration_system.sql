GO

drop table if EXISTS Fees;
drop table if EXISTS Registration;
drop table if EXISTS CourseInstructor;
drop table if EXISTS courses;
drop table if EXISTS instructors;
drop table if EXISTS students;
drop table if EXISTS departments;
GO

create table departments (
    DepartmentID int primary key identity(1,1),
    DepartmentName varchar(100) NOT NULL unique,
    CreatedAt datetime default getdate()
);

INSERT INTO departments (DepartmentName) VALUES
('Computer Science'),
('Electrical Engineering'),
('Mechanical Engineering'),
('Software Engineering'),
('Information Technology');

create table students (
    studentId int primary key identity(1,1),
    studentName varchar(100) NOT NULL,
    Email varchar(255) NOT NULL unique,
    Phone varchar(15),
    admissionYear int NOT NULL,
    DepartmentID int NOT NULL,
    CreatedAt datetime default getdate(),
    FOREIGN KEY (DepartmentID) REFERENCES departments(DepartmentID),
    CHECK (admissionYear >= 2020 AND admissionYear <= YEAR(GETDATE()))
);

INSERT INTO students (studentName, Email, Phone, admissionYear, DepartmentID) VALUES
('Ahmed Khan','ahmed1@gmail.com','03001234567',2022,1),
('Sara Ali','sara2@gmail.com','03001234568',2021,2),
('Ali Raza','ali3@gmail.com','03001234569',2022,3),
('Ayesha Noor','ayesha4@gmail.com','03001234570',2020,1),
('Omar Farooq','omar5@gmail.com','03001234571',2023,1),
('Zainab Hussain','zainab6@gmail.com','03001234572',2021,2),
('Hassan Tariq','hassan7@gmail.com','03001234573',2024,5),
('Usman Malik','usman8@gmail.com','03001234574',2022,1),
('Fatima Zahra','fatima9@gmail.com','03001234575',2023,4),
('Bilal Ahmed','bilal10@gmail.com','03001234576',2024,5),
('Hira Shah','hira11@gmail.com','03001234577',2022,1),
('Noman Ali','noman12@gmail.com','03001234578',2020,2),
('Maham Khan','maham13@gmail.com','03001234579',2021,3),
('Daniyal Raza','daniyal14@gmail.com','03001234580',2023,1),
('Laiba Noor','laiba15@gmail.com','03001234581',2024,5),
('Saad Ahmed','saad16@gmail.com','03001234582',2022,1),
('Aiman Tariq','aiman17@gmail.com','03001234583',2023,4),
('Arsalan Khan','arsalan18@gmail.com','03001234584',2021,2),
('Sana Malik','sana19@gmail.com','03001234585',2020,1),
('Hamza Ali','hamza20@gmail.com','03001234586',2024,5),
('Iqra Ahmed','iqra21@gmail.com','03001234587',2022,1),
('Zoya Hassan','zoya22@gmail.com','03001234588',2023,4),
('Fahad Raza','fahad23@gmail.com','03001234589',2021,3),
('Maryam Ali','maryam24@gmail.com','03001234590',2020,1),
('Talha Khan','talha25@gmail.com','03001234591',2024,5),
('Esha Noor','esha26@gmail.com','03001234592',2021,2),
('Huzaifa Ahmed','huzaifa27@gmail.com','03001234593',2022,1),
('Sufyan Malik','sufyan28@gmail.com','03001234594',2023,4),
('Anaya Raza','anaya29@gmail.com','03001234595',2024,5),
('Abdullah Khan','abdullah30@gmail.com','03001234596',2022,1);
GO

create table courses (
    CourseID int primary key identity(1,1),
    CourseName varchar(100) NOT NULL,
    CourseCode varchar(100) NOT NULL unique,
    Credits int NOT NULL,
    DepartmentID int NOT NULL,
    MaxCapacity INT DEFAULT 40,
    CreatedAt datetime default getdate(),
    FOREIGN KEY (DepartmentID) REFERENCES departments(DepartmentID),
    CHECK (Credits > 0 AND Credits <= 4),
    CHECK (MaxCapacity > 0)
);

INSERT INTO courses (CourseName, CourseCode, Credits, DepartmentID, MaxCapacity) VALUES
('Database Systems','CS101',3,1,40),
('Data Structures','CS102',3,1,35),
('Computer Networks','CS103',3,1,40),
('Digital Logic Design','EE104',3,2,30),
('Calculus','SE105',3,4,45),
('Linear Algebra','CS106',3,1,40),
('Operating Systems','IT107',3,5,35),
('Software Engineering','SE108',3,4,40),
('Object-Oriented Programming','CS109',3,1,40),
('Microprocessors','EE110',3,2,30);
GO

create table instructors (
    InstructorID int primary key identity(1,1),
    InstructorName varchar(100) NOT NULL,
    Email varchar(255) NOT NULL unique,
    Phone varchar(15),
    DepartmentID int NOT NULL,
    Qualification varchar(50),
    CreatedAt datetime default getdate(),
    FOREIGN KEY (DepartmentID) REFERENCES departments(DepartmentID)
);

INSERT INTO instructors (InstructorName, Email, Phone, DepartmentID, Qualification) VALUES
('Dr. Khan','khan@uni.edu','03101111111',1,'PhD'),
('Dr. Ali','ali@uni.edu','03101111112',2,'PhD'),
('Dr. Sara','sara@uni.edu','03101111113',4,'Masters'),
('Dr. Usman','usman@uni.edu','03101111114',5,'PhD'),
('Dr. Ahmed','ahmed@uni.edu','03101111115',1,'Masters');
GO

create table CourseInstructor (
    AssignID int primary key identity(1,1),
    CourseID int NOT NULL,
    InstructorID int NOT NULL,
    Semester varchar(20) NOT NULL,
    AssignedDate datetime default getdate(),
    unique (CourseID, InstructorID, Semester),
    FOREIGN KEY (CourseID) REFERENCES courses(CourseID),
    FOREIGN KEY (InstructorID) REFERENCES instructors(InstructorID)
);

INSERT INTO CourseInstructor (CourseID, InstructorID, Semester) VALUES
(1,1,'Fall 2024'),
(2,1,'Fall 2024'),
(3,1,'Spring 2025'),
(4,2,'Fall 2024'),
(5,3,'Spring 2025'),
(6,1,'Fall 2024'),
(7,4,'Spring 2025'),
(8,3,'Fall 2024'),
(9,5,'Spring 2025'),
(10,2,'Fall 2024');
GO

create table Registration (
    RegistrationID int primary key identity(1,1),
    StudentID int NOT NULL,
    CourseID int NOT NULL,
    Semester varchar(20) NOT NULL,
    Grade varchar(2),
    RegistrationDate datetime default getdate(),
    unique (StudentID, CourseID, Semester),
    FOREIGN KEY (StudentID) REFERENCES students(studentId),
    FOREIGN KEY (CourseID) REFERENCES courses(CourseID),
    CHECK (Grade IN ('A+','A','B+','B','C+','C','D','F',NULL))
);

INSERT INTO Registration (StudentID, CourseID, Semester, Grade) VALUES
(1,1,'Fall 2024','A'),
(2,4,'Spring 2025',NULL),
(3,5,'Fall 2024','B+'),
(4,1,'Spring 2025',NULL),
(5,3,'Fall 2024','A+'),
(6,4,'Spring 2025','B'),
(7,7,'Fall 2024','C+'),
(8,1,'Fall 2024','A'),
(9,8,'Spring 2025',NULL),
(10,7,'Fall 2024','B+'),
(11,2,'Fall 2024','A'),
(12,4,'Spring 2025','C'),
(13,5,'Fall 2024','B'),
(14,6,'Spring 2025','A'),
(15,7,'Fall 2024','B+'),
(16,1,'Fall 2024','A+'),
(17,8,'Spring 2025',NULL),
(18,4,'Spring 2025','B'),
(19,2,'Fall 2024','B+'),
(20,7,'Fall 2024','C+'),
(21,1,'Fall 2024','A'),
(22,8,'Spring 2025','A'),
(23,5,'Fall 2024','B'),
(24,1,'Spring 2025',NULL),
(25,7,'Fall 2024','A'),
(26,4,'Spring 2025','B+'),
(27,2,'Fall 2024','C'),
(28,8,'Spring 2025','A'),
(29,7,'Fall 2024','B'),
(30,1,'Fall 2024','A+');
GO

create table Fees (
    FeeID int primary key identity(1,1),
    StudentID int NOT NULL unique,
    TotalFee int NOT NULL,
    PaidAmount int NOT NULL default 0,
    DueDate datetime,
    LastPaymentDate datetime,
    CreatedAt datetime default getdate(),
    FOREIGN KEY (StudentID) REFERENCES students(studentId),
    check (TotalFee > 0),
    check (PaidAmount >= 0),
    check (PaidAmount <= TotalFee)
);

INSERT INTO Fees (StudentID, TotalFee, PaidAmount, DueDate, LastPaymentDate) VALUES
(1,50000,50000,'2024-06-30','2024-06-15'),
(2,45000,30000,'2024-06-30',NULL),
(3,40000,40000,'2024-06-30','2024-06-10'),
(4,50000,20000,'2024-06-30',NULL),
(5,55000,55000,'2024-06-30','2024-06-20'),
(6,45000,45000,'2024-06-30','2024-06-18'),
(7,60000,30000,'2024-06-30',NULL),
(8,50000,50000,'2024-06-30','2024-06-12'),
(9,55000,55000,'2024-06-30','2024-06-25'),
(10,60000,60000,'2024-06-30','2024-06-08'),
(11,50000,50000,'2024-06-30','2024-06-22'),
(12,45000,15000,'2024-06-30',NULL),
(13,40000,40000,'2024-06-30','2024-06-14'),
(14,50000,50000,'2024-06-30','2024-06-19'),
(15,60000,30000,'2024-06-30',NULL),
(16,50000,50000,'2024-06-30','2024-06-16'),
(17,55000,55000,'2024-06-30','2024-06-21'),
(18,45000,45000,'2024-06-30','2024-06-11'),
(19,50000,0,'2024-06-30',NULL),
(20,60000,60000,'2024-06-30','2024-06-09'),
(21,50000,50000,'2024-06-30','2024-06-23'),
(22,55000,40000,'2024-06-30',NULL),
(23,40000,40000,'2024-06-30','2024-06-17'),
(24,50000,25000,'2024-06-30',NULL),
(25,60000,60000,'2024-06-30','2024-06-24'),
(26,45000,45000,'2024-06-30','2024-06-13'),
(27,50000,50000,'2024-06-30','2024-06-26'),
(28,55000,55000,'2024-06-30','2024-06-27'),
(29,60000,30000,'2024-06-30',NULL),
(30,50000,50000,'2024-06-30','2024-06-28');
GO

CREATE INDEX idx_students_dept ON students(DepartmentID);
CREATE INDEX idx_courses_dept ON courses(DepartmentID);
CREATE INDEX idx_registration_student ON Registration(StudentID);
CREATE INDEX idx_registration_course ON Registration(CourseID);
CREATE INDEX idx_fees_student ON Fees(StudentID);
CREATE INDEX idx_courseInstructor_course ON CourseInstructor(CourseID);
GO

DROP VIEW IF EXISTS StudentDashboard;
DROP VIEW IF EXISTS CourseStatistics;
DROP VIEW IF EXISTS FeeStatusView;
GO

create view StudentDashboard as
select
    s.studentId,
    s.studentName,
    s.Email,
    d.DepartmentName,
    s.admissionYear,
    count(distinct r.CourseID) as TotalCoursesRegistered,
    case when f.PaidAmount >= f.TotalFee then 'Paid' else 'Pending' end as FeeStatus,
    f.TotalFee,
    f.PaidAmount
from students s
JOIN departments d ON s.DepartmentID = d.DepartmentID
LEFT JOIN Registration r ON s.studentId = r.StudentID
LEFT JOIN Fees f ON s.studentId = f.StudentID
GROUP BY s.studentId, s.studentName, s.Email, d.DepartmentName, s.admissionYear, f.PaidAmount, f.TotalFee;
GO

CREATE VIEW CourseStatistics AS
SELECT 
    c.CourseID,
    c.CourseName,
    c.CourseCode,
    c.Credits,
    d.DepartmentName,
    COUNT(r.StudentID) AS EnrolledStudents,
    c.MaxCapacity,
    (c.MaxCapacity - COUNT(r.StudentID)) AS AvailableSeats,
    i.InstructorName
FROM courses c
LEFT JOIN Registration r ON c.CourseID = r.CourseID
JOIN departments d ON c.DepartmentID = d.DepartmentID
LEFT JOIN CourseInstructor ci ON c.CourseID = ci.CourseID
LEFT JOIN instructors i ON ci.InstructorID = i.InstructorID
GROUP BY c.CourseID, c.CourseName, c.CourseCode, c.Credits, d.DepartmentName, c.MaxCapacity, i.InstructorName;
GO

CREATE VIEW FeeStatusView AS
SELECT 
    s.studentId,
    s.studentName,
    s.Email,
    f.TotalFee,
    f.PaidAmount,
    (f.TotalFee - f.PaidAmount) AS DueAmount,
    CASE WHEN f.PaidAmount >= f.TotalFee THEN 'Paid' ELSE 'Pending' END AS FeeStatus
FROM students s
JOIN Fees f ON s.studentId = f.StudentID;
GO

-- Get all students with their courses and instructors
SELECT s.studentName, c.CourseName, i.InstructorName, r.Semester, r.Grade
FROM Registration r
JOIN students s ON r.StudentID = s.studentId
JOIN courses c ON r.CourseID = c.CourseID
LEFT JOIN CourseInstructor ci ON c.CourseID = ci.CourseID
LEFT JOIN instructors i ON ci.InstructorID = i.InstructorID
ORDER BY s.studentName;

-- Get fee status for all students
SELECT s.studentName, f.TotalFee, f.PaidAmount, 
       CASE WHEN f.PaidAmount >= f.TotalFee THEN 'Paid' ELSE 'Pending' END AS FeeStatus,
       (f.TotalFee - f.PaidAmount) AS DueAmount
FROM students s
JOIN Fees f ON s.studentId = f.StudentID
ORDER BY CASE WHEN f.PaidAmount >= f.TotalFee THEN 0 ELSE 1 END DESC, (f.TotalFee - f.PaidAmount) DESC;

-- Students with pending fees
SELECT s.studentName, s.Email, f.TotalFee, f.PaidAmount, 
       (f.TotalFee - f.PaidAmount) AS DueAmount
FROM students s
JOIN Fees f ON s.studentId = f.StudentID
WHERE f.PaidAmount < f.TotalFee
ORDER BY (f.TotalFee - f.PaidAmount) DESC;
--course stats
SELECT 
    c.CourseID,
    c.CourseName,
    c.CourseCode,
    c.MaxCapacity,
    COUNT(r.StudentID) AS EnrolledStudents,
    (c.MaxCapacity - COUNT(r.StudentID)) AS AvailableSeats,
    CAST(COUNT(r.StudentID) * 100.0 / c.MaxCapacity AS FLOAT) AS FillPercent
FROM courses c
LEFT JOIN Registration r ON c.CourseID = r.CourseID
GROUP BY c.CourseID, c.CourseName, c.CourseCode, c.MaxCapacity
ORDER BY c.CourseName;
