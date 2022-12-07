Lab | My first queries
Please, download the file applestore.csv. Install MySQL/Postgresql on your computer. Create a database Upload the file as a new table of your database.

Use the data table to query the data about Apple Store Apps and answer the following questions:

1. What are the different genres?
select prime_genre from applestore group by prime_genre;

2. Which is the genre with the most apps rated?
select prime_genre, rating_count_tot from applestore
group by prime_genre order by rating_count_tot desc limit 1;

3. Which is the genre with most apps?
select prime_genre, sum(vpp_lic) from applestore
group by prime_genre order by sum(vpp_lic) desc limit 1;

4. Which is the one with least?
select prime_genre, sum(vpp_lic) from applestore
group by prime_genre order by sum(vpp_lic) asc limit 1;

5. Find the top 10 apps most rated.
select track_name, rating_count_tot from applestore
order by rating_count_tot desc limit 10;

6. Find the top 10 apps best rated by users.
select track_name, user_rating from applestore
order by user_rating desc limit 10;