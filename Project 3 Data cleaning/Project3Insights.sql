CREATE DATABASE project3;
USE project3;

SELECT avg(Sales) FROM superstore;
SELECT Region, avg(Sales) FROM superstore
GROUP BY Region;

SELECT sum(Profit) FROM superstore;
SELECT Region, sum(Profit) FROM superstore
GROUP BY Region;

SELECT Quantity, avg(Sales) FROM superstore
GROUP BY Quantity ORDER BY Quantity ASC;

SELECT Ship_Mode, avg(Sales) FROM superstore
GROUP BY Ship_Mode;

