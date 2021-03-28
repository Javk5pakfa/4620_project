create schema 4620Project;

use 4620Project;

CREATE TABLE region (
    Region_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Region_Name CHAR(2) UNIQUE NOT NULL
);

insert into region(Region_Name) values ('NW');
insert into region(Region_Name) values ('SW');
insert into region(Region_Name) values ('MN');
insert into region(Region_Name) values ('MS');
insert into region(Region_Name) values ('NE');
insert into region(Region_Name) values ('SE');

CREATE TABLE skill (
    Skill_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Skill_Descrpt VARCHAR(255) UNIQUE NOT NULL,
    Skill_Rate FLOAT NOT NULL
);

insert into skill(Skill_Descrpt) 
	values 
		('data entry I'),
        ('data entry II'), 
        ('systems analyst I'), 
        ('systems analyst II'), 
        ('database designer I'), 
        ('database designer II'), 
        ('Cobol I'), 
        ('Cobol II'), 
        ('C++ I'), 
        ('C++ II'), 
        ('VB I'), 
        ('VB II'), 
        ('ColdFusion I'), 
        ('ColdFusion II'), 
        ('ASP I'), 
        ('ASP II'), 
        ('Oracle DBA'), 
        ('MS SQL Server DBA'), 
        ('network engineer I'), 
        ('network engineer II'), 
        ('web administrator'), 
        ('technical writer'), 
        ('project manager');

CREATE TABLE customer (
    Cus_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Region_ID INT NOT NULL,
    Cus_Name VARCHAR(255) NOT NULL,
    Cus_Phone VARCHAR(255),
    FOREIGN KEY (Region_ID)
        REFERENCES region (Region_ID)
);

CREATE TABLE employee (
    Emp_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Region_ID INT NOT NULL,
    Emp_Lname VARCHAR(255) NOT NULL,
    Emp_Mi CHAR(1),
    Emp_Fname VARCHAR(255) NOT NULL,
    Emp_Hiredate DATE NOT NULL,
    FOREIGN KEY (Region_ID)
        REFERENCES region (Region_ID)
);

insert into employee(Emp_ID, Region_ID, Emp_Lname, Emp_Fname)
	values (501, 1, 'Connor', 'Sean');

insert into employee(Region_ID, Emp_Lname, Emp_Fname)
	values
		(2, 'Seaton', 'Amy'),
		(2, 'Chandler', 'Joseph'),
		(3, 'Williams', 'Josh'),
		(3, 'Yarbrough', 'Peter'),
		(4, 'Underwood', 'Trish'),
		(4, 'Robbins', 'Erin'),
		(1, 'Zebras', 'Steve'),
		(1, 'Burklow', 'Shane'),
		(1, 'Smith', 'Mary'),
		(1, 'Smith', 'Jose'),
		(1, 'Summers', 'Anna'),
		(1, 'Ellis', 'Maria'),
		(1, 'Epahnor', 'Victor'),
		(1, 'Kilby', 'Surgena'),
		(1, 'Bush', 'Emily'),
		(2, 'Bender', 'Larry'),
		(2, 'Batts', 'Melissa'),
		(4, 'Newton', 'Christopher'),
		(4, 'Duarte', 'Miriam'),
		(6, 'Rogers', 'Adam'),
		(6, 'Bible', 'Hanah'),
		(6, 'Cope', 'Leslie'),
		(3, 'Pascoe', 'Jonathan'),
		(5, 'Paine', 'Brad'),
		(5, 'Craig', 'Brett');

CREATE TABLE empskill (
    Emp_ID INT NOT NULL,
    Skill_ID INT NOT NULL,
    PRIMARY KEY (Emp_ID, Skill_ID),
    FOREIGN KEY (Emp_ID)
        REFERENCES employee (Emp_ID),
    FOREIGN KEY (Skill_ID)
        REFERENCES skill (Skill_ID)
);

insert into empskill(Emp_ID, Skill_ID)
	values
		(501, 23),
		(502, 1),
		(502, 2),
		(503, 4),
		(504, 1),
		(504, 2),
		(505, 5),
		(505, 6),
		(505, 18),
		(506, 1),
		(507, 3),
		(507, 4),
		(508, 3),
		(508, 11),
		(508, 12),
		(509, 4),
		(510, 5),
		(510, 19),
		(510, 20),
		(510, 21),
		(511, 9),
		(511, 17),
		(511, 18),
		(512, 7),
		(513, 7),
		(513, 11),
		(514, 7),
		(514, 8),
		(515, 22),
		(516, 3),
		(516, 13),
		(516, 14),
		(516, 15),
		(516, 19),
		(516, 20),
		(516, 21),
		(517, 22),
		(518, 8),
		(519, 12),
		(519, 14),
		(519, 16),
		(519, 21),
		(520, 13),
		(520, 15),
		(520, 16),
		(521, 9),
		(521, 10),
		(522, 10),
		(523, 9),
		(524, 6),
		(524, 17),
		(525, 23),
		(526, 3);

CREATE TABLE project (
    Proj_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Cus_ID INT NOT NULL,
    Emp_ID INT NOT NULL,
    Proj_Date DATE NOT NULL,
    Proj_Descrpt VARCHAR(255) NOT NULL,
    Proj_EstDateSt DATE NOT NULL,
    Proj_EstDateEnd DATE NOT NULL,
    Proj_EstBudget FLOAT NOT NULL,
    Proj_ActDateSt DATE,
    Proj_ActDateEnd DATE,
    Proj_ActCost FLOAT,
    FOREIGN KEY (Cus_ID)
        REFERENCES customer (Cus_ID),
    FOREIGN KEY (Emp_ID)
        REFERENCES employee (Emp_ID)
);

CREATE TABLE task (
    Task_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Proj_ID INT NOT NULL,
    Task_Info VARCHAR(255) NOT NULL,
    Task_DateSt DATE,
    Task_dateEnd DATE,
    FOREIGN KEY (Proj_ID)
        REFERENCES project (Proj_ID)
);

CREATE TABLE task_skills (
    TS_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Task_ID INT NOT NULL,
    Skill_ID INT NOT NULL,
    TS_Qty INT NOT NULL,
    FOREIGN KEY (Task_ID)
        REFERENCES task (Task_ID),
    FOREIGN KEY (Skill_ID)
        REFERENCES skill (Skill_ID)
);

CREATE TABLE assign (
    Asn_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Emp_ID INT NOT NULL,
    Asn_DateSt DATE,
    Asn_DateEnd DATE,
    TS_ID INT NOT NULL,
    FOREIGN KEY (Emp_ID)
        REFERENCES employee (Emp_ID),
    FOREIGN KEY (TS_ID)
        REFERENCES task_skills (TS_ID)
);

CREATE TABLE bill (
    Bill_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Bill_Date DATE NOT NULL,
    Proj_ID INT NOT NULL,
    FOREIGN KEY (Proj_ID)
        REFERENCES project (Proj_ID)
);

CREATE TABLE worklog (
    WL_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Asn_ID INT NOT NULL,
    WL_date DATE NOT NULL,
    WL_Hours FLOAT,
    Bill_ID INT,
    FOREIGN KEY (Asn_ID)
        REFERENCES assign (Asn_ID),
    FOREIGN KEY (Bill_ID)
        REFERENCES bill (Bill_ID)
);

commit;