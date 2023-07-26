-- CREATING EMPLOYEES TABLE AND IMPORT DATA FROM EMPLOYEES.CSV

CREATE TABLE employees(
    emp_no int UNIQUE PRIMARY KEY,
	emp_title VARCHAR (5) NOT NULL,
	birth_date DATE NOT NULL,
	first_name VARCHAR (50) NOT NULL,
	last_name VARCHAR (50) NOT NULL,
	sex CHAR (1) NOT NULL,
	hire_date DATE NOT NULL
)

COPY employees(emp_no, emp_title, birth_date, first_name, last_name, sex, hire_date)
FROM 'G:\Anthony\AstraDigital\Data Management\Task 1\solution\EmployeeSQL\data\employees.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM employees


-- CREATING SALARIES TABLE AND IMPORT DATA FROM SALARIES.CSV

CREATE TABLE salaries(
	emp_no INT UNIQUE PRIMARY KEY,
	salary INT
)

COPY salaries(emp_no, salary)
FROM 'G:\Anthony\AstraDigital\Data Management\Task 1\solution\EmployeeSQL\data\salaries.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM salaries

-- CREATING TITLES TABLE AND IMPORT DATA FROM TITLES.CSV

CREATE TABLE titles(
	title_id CHAR (5) PRIMARY KEY,
	title VARCHAR (50)
)

COPY titles(title_id, title)
FROM 'G:\Anthony\AstraDigital\Data Management\Task 1\solution\EmployeeSQL\data\titles.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM titles

-- CREATING DEPT_MANAGER TABLE AND IMPORT DATA FROM DEPT_MANAGER.CSV

CREATE TABLE dept_manager(
	dept_no CHAR (4),
	emp_no INT UNIQUE PRIMARY KEY
)

COPY dept_manager(dept_no, emp_no)
FROM 'G:\Anthony\AstraDigital\Data Management\Task 1\solution\EmployeeSQL\data\dept_manager.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM dept_manager

-- CREATING DEPT_EMP TABLE AND IMPORT DATA FROM DEPT_EMP.CSV

CREATE TABLE dept_emp(
	emp_no INT,
	dept_no CHAR (4),
	PRIMARY KEY (emp_no, dept_no)
)

COPY dept_emp(emp_no, dept_no)
FROM 'G:\Anthony\AstraDigital\Data Management\Task 1\solution\EmployeeSQL\data\dept_emp.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM dept_emp

-- CREATING DEPT_MANAGER TABLE AND IMPORT DATA FROM DEPT_MANAGER.CSV

CREATE TABLE departments(
	dept_no CHAR (4) UNIQUE PRIMARY KEY,
	dept_name VARCHAR(50)
)

COPY departments(dept_no, dept_name)
FROM 'G:\Anthony\AstraDigital\Data Management\Task 1\solution\EmployeeSQL\data\departments.csv'
DELIMITER ','
CSV HEADER;

SELECT * FROM departments

-- ADD FOREIGN KEY TO EACH TABLE

-- ADD FOREIGN KEY TO SALARIES TABLE
ALTER TABLE salaries
	ADD CONSTRAINT fk_emp_no FOREIGN KEY (emp_no) REFERENCES employees (emp_no)

-- ADD FOREIGN KEY TO DEPT MANAGER TABLE
ALTER TABLE dept_manager
	ADD CONSTRAINT fk_dept_no FOREIGN KEY (dept_no) REFERENCES departments (dept_no)
	
ALTER TABLE dept_manager
	ADD CONSTRAINT fk_emp_no FOREIGN KEY (emp_no) REFERENCES employees (emp_no)
	
-- ADD FOREIGN KEY TO DEPT EMP TABLE
ALTER TABLE dept_emp
	ADD CONSTRAINT fk_dept_no FOREIGN KEY (dept_no) REFERENCES departments (dept_no)
	
ALTER TABLE dept_emp
	ADD CONSTRAINT fk_emp_no FOREIGN KEY (emp_no) REFERENCES employees (emp_no)

-- ADD FOREIGN KEY TO EMPLOYEES TABLE
ALTER TABLE employees
	ADD CONSTRAINT fk_title_id FOREIGN KEY (emp_title) REFERENCES titles (title_id)