create database lab20;
use lab20;
create table cars (
ID int,
VIN varchar(30),
Manufacturer varchar(30),
Model varchar(30),
Year int,
Color varchar(30));

create table customers(
ID int,
Customer_ID varchar(30),
Name varchar(30),
Phone varchar(30),
Email varchar(30),
Address varchar(100),
City varchar(20),
State_Province varchar(20),
Country	varchar(20),
Postal int);

create table salespersons(
ID int,
Staff_ID varchar(20),
Name varchar(40),
Store varchar(20));

create table invoices(
ID int,
Invoice_Number int,
Date varchar(20),
Car int,
Customer int,
Sales_Person int);

insert into cars
values (0,'3K096I98581DHSNUP', 'Volkswagen', 'Tiguan', 2019, 'Blue'),
(1, 'ZM8G7BEUQZ97IH46V', 'Peugeot', 'Rifter', 2019, 'Red'),
(2, 'RKXVNNIHLVVZOUB4M', 'Ford', 'Fusion', 2018, 'White'),
(3, 'HKNDGS7CU31E9Z7JW', 'Toyota', 'RAV4', 2018, 'Silver'),
(4, 'DAM41UDN3CHU2WVF6', 'Volvo', 'V60', 2019, 'Gray'),
(5,	'DAM41UDN3CHU2WVF6', 'Volvo', 'V60 Cross Country', 2019, 'Gray');

insert into customers
values (0, '10001', 'Pablo Picasso', '+34 636 17 63 82', '-', 'Paseo de la Chopera, 14', 'Madrid', 'Madrid', 'Spain', 28045),
(1, '20001', 'Abraham Lincoln', '+1 305 907 7086', '-', '120 SW 8th St', 'Miami', 'Florida', 'United States', 33130),
(2, '30001', 'Napoléon Bonaparte', '+33 1 79 75 40 00', '-', '40 Rue du Colisée', 'Paris', 'Île-de-France', 'France', 75008);

insert into salespersons
values (0, '00001', 'Petey Cruiser', 'Madrid'),
(1, '00002', 'Anna Sthesia', 'Barcelona'),
(2,	'00003', 'Paul Molive', 'Berlin'),
(3,	'00004', 'Gail Forcewind', 'Paris'),
(4, '00005', 'Paige Turner', 'Mimia'),
(5, '00006', 'Bob Frapples', 'Mexico City'),
(6, '00007', 'Walter Melon', 'Amsterdam'),
(7, '00008', 'Shonda Leer', 'São Paulo');

insert into invoices
values (0, 852399038, '2018-08-22', 0, 1, 3),
(1, 731166526, '2018-12-31', 3, 0, 5),
(2, 271135104, '2019-01-22', 2, 2, 7);

update salespersons
set Store = 'Miami' where Store = 'Mimia';

delete from cars
where ID = 4;

update customers
set Email = 'ppicasso@gmail.com' where Name = 'Pablo Picasso';
update customers
set Email = 'lincoln@us.gov' where Name = 'Abraham Lincoln';
update customers
set Email = 'hello@napoleon.me' where Name = 'Napoléon Bonaparte';