load data infile '../data/csv/artists.csv'
insert into table artist
fields terminated by "," optionally enclosed by '"'
(artist_id,artist_name)