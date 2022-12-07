use olist;
select * from order_items;
select product_id, price from order_items
order by price desc limit 1;
select product_id, price from order_items
order by price asc limit 1;
select shipping_limit_date from order_items
order by shipping_limit_date asc limit 1;
select shipping_limit_date from order_items
order by shipping_limit_date desc limit 1;
select * from customers;
select customer_state, count(*) from customers
group by customer_state order by count(*) desc limit 1;
select customer_city, count(*) from customers where customer_state = 'SP'
group by customer_city order by count(*) desc limit 5;
select * from closed_deals;
select business_segment, count(business_segment) from closed_deals
group by business_segment;
select business_segment, sum(declared_monthly_revenue) from closed_deals
group by business_segment order by sum(declared_monthly_revenue) desc limit 3;
select * from order_reviews;
select review_score from order_reviews
group by review_score;
alter table order_reviews add category varchar(20);
update order_reviews set category = 'poor' where review_score = 1;
update order_reviews set category = 'bad' where review_score = 2;
update order_reviews set category = 'OK' where review_score = 3;
update order_reviews set category = 'nice' where review_score = 4;
update order_reviews set category = 'perfect' where review_score = 5;
select review_score, category, count(*) from order_reviews
group by review_score order by count(*) desc limit 1;