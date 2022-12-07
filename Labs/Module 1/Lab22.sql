create database publications;
use publications;

SELECT titles.title_id, authors.au_id, titles.advance * titleauthor.royaltyper / 100 as advance,
titles.price * sales.qty * titles.royalty / 100 * titleauthor.royaltyper / 100 as sales_royalty
from