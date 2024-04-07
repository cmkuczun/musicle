load data infile '../data/csv/genres.csv'
insert into table genre
fields terminated by "," optionally enclosed by '"'
(genre_id,genre)