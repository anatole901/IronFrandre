create database if not exists apple_test;
use apple_test;
select * from applestore;
select track_name, price from applestore;
select track_name, price from applestore
where price > 2 and rating_count_tot < 4
order by track_name desc;
select track_name, avg(price) from applestore
group by track_name;
select currency, avg(price) from applestore
group by currency;
select prime_genre from applestore group by prime_genre;
select prime_genre, rating_count_tot from applestore
group by prime_genre order by rating_count_tot desc;
select prime_genre, sum(vpp_lic) from applestore
group by prime_genre order by sum(vpp_lic) asc limit 1;
select track_name, rating_count_tot from applestore
order by rating_count_tot desc limit 10;
select track_name, user_rating from applestore
order by user_rating desc limit 10;

update applestore
set track_name = 'Other' where price = 0;
select * from applestore;