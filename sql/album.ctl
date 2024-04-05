load data infile '../data/albums.csv'
insert into table album
fields terminated by "," optionally enclosed by '"'
(album_id,album_name,release_date)