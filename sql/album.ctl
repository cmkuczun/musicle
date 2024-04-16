load data infile '../data/csv/albums.csv'
insert into table album
fields terminated by "," optionally enclosed by '"'
(album_id,album_name,release_date date "YYYY-MM-DD")
