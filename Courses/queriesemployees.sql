USE employees;
SELECT dept_no FROM departments;
SELECT * FROM departments;
SELECT * FROM employees LIMIT 10;
SELECT * FROM employees WHERE first_name = 'Elvis';
SELECT * FROM employees WHERE first_name = 'Kellie' and gender = 'F';
SELECT * FROM employees WHERE first_name = 'Kellie' or first_name = 'Aruna';
SELECT * FROM employees WHERE first_name IN ('Denis', 'Elvis');