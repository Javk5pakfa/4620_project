# CPSC 4620 Project Planner

## 1. Identify Major Entities

---

### Customers

- ID
- Name
- Phone number
- Region

---

### Employees

- ID
- Last name
- Middle initial
- First name
- Region
- Date of hire

---

### Skill

- Skill ID
- Description
- Rate of pay

---

### Region

- NW, SW, MN, MS, NE, SE

---

### Projects

- Project ID
- Customer assigned
- Description
- Project date (date signed)
- Estimated start date
- Estimated end date
- Estimated budget
- Actual start date
- Actual end date
- Actual cost
  - Calculated by: `Cost_week + Cost_actual`
  - `Cost_week = (hours_worked * rate_of_pay) * num_emp`
- One Employee_manager assigned

---

### Project schedules

- **Employee type Manager responsible**
- Task ID
- Task Description
- Starting and Ending dates
- Skills needed
- Number of employees

#### Project tasks

- Initial interview
- Database and System Design
- Implementation
- Coding
- Testing
- Final evaluation
- Sign-off

---

### Assignments

- Manager of a **Project** assigns tasks to **Employees**
- **Employees** sorted by **Region**
- Based on specific **Skills**

---

### Invoice
