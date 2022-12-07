create database bank;
use bank;
create table organizations (
id VARCHAR(128) NULL,
name VARCHAR(255));
DELIMITER $$
CREATE TRIGGER before_insert_organizations
BEFORE INSERT ON organizations
FOR EACH ROW
BEGIN
  IF new.id IS NULL THEN
    SET new.id = uuid();
  END IF;
END $$
DELIMITER ;
INSERT INTO organizations (id, name)
VALUES (NULL, 'Company1'), (NULL, 'Company2'),
(NULL, 'Company3'), (NULL, 'Company4'), (NULL, 'Company5');
ALTER TABLE organizations
ADD PRIMARY KEY (id);
create table transfers (
id VARCHAR(128) NULL,
amount_euro_cents INTEGER
 ) ;
DELIMITER $$
CREATE TRIGGER before_insert_transfers
BEFORE INSERT ON transfers
FOR EACH ROW
BEGIN
  IF new.id IS NULL THEN
    SET new.id = uuid();
  END IF;
END $$
DELIMITER ;
INSERT INTO transfers (id, amount_euro_cents)
VALUES (NULL, 2000), (NULL, 1200), (NULL, 70000), (NULL, 30000), (NULL, 83400),
(NULL, 30000), (NULL, 50000), (NULL, 23400), (NULL, 32000), (NULL, 510000), (NULL, 2300);
ALTER TABLE transfers
ADD PRIMARY KEY (id);
create table bank_accounts (
id VARCHAR(128) NULL,
organization_id VARCHAR(128),
FOREIGN KEY (organization_id) REFERENCES organizations(id)
 );
 DELIMITER $$
CREATE TRIGGER before_insert_bank_accounts
BEFORE INSERT ON bank_accounts
FOR EACH ROW
BEGIN
  IF new.id IS NULL THEN
    SET new.id = uuid();
  END IF;
END $$
DELIMITER ;
INSERT INTO bank_accounts (id, organization_id)
VALUES (NULL, 'ded4fd17-6920-11ed-a6a8-087190799f59'), (NULL, 'ded4fd17-6920-11ed-a6a8-087190799f59'),
(NULL, 'ded50865-6920-11ed-a6a8-087190799f59'), (NULL, 'ded50865-6920-11ed-a6a8-087190799f59'), (NULL, 'ded50865-6920-11ed-a6a8-087190799f59'),
(NULL, 'ded50a3c-6920-11ed-a6a8-087190799f59'), (NULL, 'ded50a3c-6920-11ed-a6a8-087190799f59'),
(NULL, 'ded50b36-6920-11ed-a6a8-087190799f59'), (NULL, 'ded50b36-6920-11ed-a6a8-087190799f59'), (NULL, 'ded50b36-6920-11ed-a6a8-087190799f59'),
(NULL, 'ded50c16-6920-11ed-a6a8-087190799f59');
ALTER TABLE bank_accounts
ADD PRIMARY KEY (id);
create table transactions (
id VARCHAR(128) NULL,
bank_account_id   VARCHAR(128),
subject_id VARCHAR(128),
subject_type VARCHAR(32),
settled_at  TIMESTAMP,
FOREIGN KEY (bank_account_id) REFERENCES bank_accounts(id),
FOREIGN KEY (subject_id) REFERENCES transfers(id)
 );
DELIMITER $$
CREATE TRIGGER before_insert_transactions
BEFORE INSERT ON transactions
FOR EACH ROW
BEGIN
  IF new.id IS NULL THEN
    SET new.id = uuid();
  END IF;
END $$
DELIMITER ;
INSERT INTO transactions (id, bank_account_id, subject_id, subject_type, settled_at)
VALUES
(NULL, 'b97c8a30-6921-11ed-a6a8-087190799f59','e8ebe73c-6920-11ed-a6a8-087190799f59',"CardTransaction",'2021-01-19 03:14:07'),
(NULL, 'b97c8a30-6921-11ed-a6a8-087190799f59','e8ec01f7-6920-11ed-a6a8-087190799f59', "Transfer",'2022-01-19 03:14:07'),
(NULL, 'b97ca046-6921-11ed-a6a8-087190799f59','e8ec01f7-6920-11ed-a6a8-087190799f59',"Transfer",'2022-01-21 01:14:07'),
(NULL, 'b97ca23b-6921-11ed-a6a8-087190799f59','e8ec04a2-6920-11ed-a6a8-087190799f59',"Transfer",'2022-01-19 02:14:07'),
(NULL, 'b97ca8a0-6921-11ed-a6a8-087190799f59','e8ec066e-6920-11ed-a6a8-087190799f59',"Transfer",'2022-04-01 05:14:07'),
(NULL, 'b97cab04-6921-11ed-a6a8-087190799f59','e8ec092c-6920-11ed-a6a8-087190799f59',"Transfer",'2022-04-03 08:14:07'),
(NULL, 'b97cabd4-6921-11ed-a6a8-087190799f59','e8ec0add-6920-11ed-a6a8-087190799f59',"Transfer",'2022-05-04 09:14:07');
ALTER TABLE transactions
ADD PRIMARY KEY (id);
create table card_transactions (
id VARCHAR(128) NULL,
transaction_id  VARCHAR(128),
amount_euro_cents INTEGER,
 FOREIGN KEY (transaction_id) REFERENCES transactions(id)
 );
 DELIMITER $$
CREATE TRIGGER before_insert_card_transactions
BEFORE INSERT ON card_transactions
FOR EACH ROW
BEGIN
  IF new.id IS NULL THEN
    SET new.id = uuid();
  END IF;
END $$
DELIMITER ;
INSERT INTO card_transactions (id, transaction_id, amount_euro_cents)
VALUES (NULL, '3d4ede6d-6924-11ed-a6a8-087190799f59',23000),
(NULL, '3d4f02f8-6924-11ed-a6a8-087190799f59', 3400),
(NULL, '3d4f0cdd-6924-11ed-a6a8-087190799f59',40000),
(NULL, '3d4f0f39-6924-11ed-a6a8-087190799f59',12000),
(NULL, '3d4f0f39-6924-11ed-a6a8-087190799f59',34000),
(NULL, '3d4f095f-6924-11ed-a6a8-087190799f59',2300);
ALTER TABLE card_transactions
ADD PRIMARY KEY (id);
select o.name, month(tns.settled_at) as month,
sum(c_tns.amount_euro_cents)/(sum(tr.amount_euro_cents)+sum(c_tns.amount_euro_cents)) as proportion
from organizations o
join bank_accounts b on
b.organization_id=o.id
left join transactions tns
on  tns.bank_account_id=b.id
left join card_transactions c_tns
on tns.id=c_tns.transaction_id
left join transfers tr
on tns.subject_id=tr.id
where tns.settled_at IS NOT NULL
group by o.name, month ;

SELECT o.name, MONTH(t.settled_at) as month,
sum(c.amount_euro_cents)/(sum(c.amount_euro_cents) + sum(tr.amount_euro_cents)) as ratio
FROM organizations o
LEFT JOIN bank_accounts b ON o.id = b.organization_id
LEFT JOIN transactions t ON b.id = t.bank_account_id
LEFT JOIN card_transactions c ON c.transaction_id = t.id
LEFT JOIN transfert tr ON tr.id = t.id
GROUP BY o.name, month;