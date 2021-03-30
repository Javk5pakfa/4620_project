create schema 4620Project;

use 4620Project;

CREATE TABLE region (
    Region_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Region_Name CHAR(2) UNIQUE NOT NULL
);

CREATE TABLE skill (
    Skill_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Skill_Descrpt VARCHAR(255) UNIQUE NOT NULL,
    Skill_Rate FLOAT NOT NULL
);

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

CREATE TABLE empskill (
    Emp_ID INT NOT NULL,
    Skill_ID INT NOT NULL,
    PRIMARY KEY (Emp_ID , Skill_ID),
    FOREIGN KEY (Emp_ID)
        REFERENCES employee (Emp_ID),
    FOREIGN KEY (Skill_ID)
        REFERENCES skill (Skill_ID)
);

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