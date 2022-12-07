use apple_test;
create table if not exists prob_solv_comp (
Emp_ID int,
Name Varchar(30),
Surname Varchar(30),
Department Varchar(30),
Salary Float);
insert into prob_solv_comp (Emp_ID, Name, Surname, Department, Salary)
values (1, "Sam","Smith",  "DA", 3500.4),
(2,"Tim","Black",  "UX/UI", 6432.1 ),
(3, "Tom", "Martin", "Cybsec", 5848.6);
insert into prob_solv_comp (Emp_ID, Name, Surname, Department, Salary)
values (4, "Frank","Alanson",  "DA", 7435.4),
(5,"John","McDagan",  "UX/UI", 4351.1 );
select * from prob_solv_comp;
select Emp_ID from prob_solv_comp group by Emp_ID;
select concat(Name, ' ', Surname) as Full_Name, 0.2 * Salary as Taxes from prob_solv_comp;
select Salary from prob_solv_comp order by Salary desc limit 1;
select Salary from prob_solv_comp order by Salary asc limit 1;
select Department, avg(Salary) from prob_solv_comp group by Department;