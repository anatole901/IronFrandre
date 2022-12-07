USE employees_mod;

DELIMITER $$
CREATE PROCEDURE av_salary()
BEGIN
SELECT avg(salary) FROM t_salaries;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE emp_info(in first varchar(14), in last varchar(16))
BEGIN
SELECT emp_no FROM t_employees
WHERE first_name = first AND last_name = last;
END $$
DELIMITER ;

SELECT * FROM t_employees LIMIT 5;

CALL emp_info('Mary', 'Sluis');

se