create schema 4620Project;

use 4620Project;

create table region (
	Region_ID int not null auto_increment primary key,
    Region_Name char(2) not null
);

create table skill (
	Skill_ID int not null auto_increment primary key,
    Skill_Descrpt varchar(255) not null,
    Skill_Rate float not null
);

create table customer (
	Cus_ID int not null auto_increment primary key,
    Region_ID int not null,
    Cus_Name varchar(255) not null,
    Cus_Phone varchar(255),
    foreign key (Region_ID)
		references region(Region_ID)
);

create table employee (
	Emp_ID int not null auto_increment primary key,
    Region_ID int not null,
    Emp_Lname varchar(255) not null,
    Emp_Mi char(1),
    Emp_Fname varchar(255) not null,
    Emp_Hiredate Date not null,
    foreign key (Region_ID) references region(Region_ID)
);

create table empskill (
	Emp_ID int not null,
    Skill_ID int not null,
    primary key (Emp_ID, Skill_ID),
    foreign key (Emp_ID) references employee(Emp_ID),
    foreign key (Skill_ID) references skill(Skill_ID)
);

create table project (
	Proj_ID int not null auto_increment primary key,
    Cus_ID int not null,
    Emp_ID int not null,
    Proj_Date Date not null,
    Proj_Descrpt varchar(255) not null,
    Proj_EstDateSt Date not null,
    Proj_EstDateEnd Date not null,
    Proj_EstBudget float not null,
    Proj_ActDateSt date,
    Proj_ActDateEnd date,
    Proj_ActCost float,
    foreign key (Cus_ID) references customer(Cus_ID),
    foreign key (Emp_ID) references employee(Emp_ID)
);

create table task (
	Task_ID int not null auto_increment primary key,
    Proj_ID int not null,
    Task_Info varchar(255) not null,
    Task_DateSt date,
    Task_dateEnd date,
    foreign key (Proj_ID) references project(Proj_ID)
);

create table task_skills (
	TS_ID int not null auto_increment primary key,
    Task_ID int not null,
    Skill_ID int not null,
    TS_Qty int not null,
    foreign key (Task_ID) references task(Task_ID),
    foreign key (Skill_ID) references skill(Skill_ID)
);

create table assign (
	Asn_ID int not null auto_increment primary key,
    Emp_ID int not null,
    Asn_DateSt date,
    Asn_DateEnd date,
    TS_ID int not null,
    foreign key (Emp_ID) references employee(Emp_ID),
    foreign key (TS_ID) references task_skills(TS_ID)
);

create table bill (
	Bill_ID int not null auto_increment primary key,
    Bill_Date date not null,
    Proj_ID int not null,
    foreign key (Proj_ID) references project(Proj_ID)
);

create table worklog (
	WL_ID int not null auto_increment primary key,
    Asn_ID int not null,
    WL_date date not null,
    WL_Hours float,
    Bill_ID int,
    foreign key (Asn_ID) references assign(Asn_ID),
    foreign key (Bill_ID) references bill(Bill_ID)
);

commit;