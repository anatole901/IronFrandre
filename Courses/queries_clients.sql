use test;

CREATE TABLE clients_crm(
id INT,
FirstName VARCHAR(30),
LastName VARCHAR(30),
PhoneNumber VARCHAR(20),
CreationDate date
);

CREATE TABLE calls(
id INT,
called_number VARCHAR(20),
date date,
duration_in_sec INT,
incoming_number INT
);

INSERT INTO calls(id, called_number, date, duration_in_sec, incoming_number)
VALUES (1, '3379324983', '2019-01-20', 1200, 67711),  (2, '3379324984', '2019-01-20', 900, 67788),
(3, '3379324986', '2019-01-25', 300, 67722), (4, '3379324985', '2019-01-22', 600, 67799);

INSERT INTO clients_crm(id, FirstName, LastName, PhoneNumber, CreationDate)
VALUES (1, 'Paul', 'Machin', '3379324983', '2019-01-20'),  (2, 'Salah', 'Mohamed', '3379324987', '2019-01-18'),
(3, 'Jurgen', 'Klopp', '3379324986', '2019-01-16'), (4, 'Ibrahima', 'Konate', '3379324981', '2019-01-14');

SELECT * from clients_crm;

 SELECT id, FirstName, LastName, PhoneNumber, CreationDate FROM
 (SELECT id, FirstName, LastName, PhoneNumber, CreationDate, row_number() over (partition by id order by CreationDate) as rn
 FROM clients_crm) t
 WHERE rn = 1;
 
 SELECT DAY(ca.date) as day, count(ca.id) as num_calls, count(cl.id) as num_clients, sum(IF(cl.id IS NULL, 0, 1))/count(ca.id) as transformation_rate
FROM calls ca
LEFT JOIN clients_crm cl ON cl.PhoneNumber = CONVERT(ca.incoming_number, CHAR)
GROUP BY day;

SELECT cl.id, cl.FirstName, cl.LastName, IF(min(ca.date) IS NULL, cl.CreationDate, min(ca.date)) as first_call_date, IF(cl.PhoneNumber IS NULL, CONVERT(ca.incoming_number, CHAR), cl.PhoneNumber) as phone_number
FROM calls ca
FULL OUTER JOIN clients_crm cl ON cl.PhoneNumber = CONVERT(ca.incoming_number, CHAR) 
GROUP BY ca.incoming_number;