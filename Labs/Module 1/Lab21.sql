create database lab21;
use lab21;
select * from authors;
select * from titles;
select * from titleauthor;
select * from publishers;

select a.au_id, a.au_lname, a.au_fname, t.title, p.pub_name from titleauthor ta
left join authors a on a.au_id = ta.au_id
left join titles t on t.title_id = ta.title_id
left join publishers p on p.pub_id = t.pub_id;

select a.au_id, a.au_lname, a.au_fname, count(t.title) as title_count, p.pub_name from  titleauthor ta
left join authors a on a.au_id = ta.au_id
left join titles t on t.title_id = ta.title_id
left join publishers p on p.pub_id = t.pub_id
group by a.au_id;

select count(*) from titleauthor;

select a.au_id, a.au_lname, a.au_fname, sum(t.ytd_sales) as total from titleauthor ta
left join authors a on a.au_id = ta.au_id
left join titles t on t.title_id = ta.title_id
group by a.au_id order by total desc limit 3;

select a.au_id, a.au_lname, a.au_fname, if(sum(t.ytd_sales) = NULL, 0, sum(t.ytd_sales)) as total from titleauthor ta
left join authors a on a.au_id = ta.au_id
left join titles t on t.title_id = ta.title_id
group by a.au_id order by total desc;

