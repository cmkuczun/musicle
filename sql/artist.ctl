load data infile '../data/artists.csv'
insert into table artist
fields terminated by "," optionally enclosed by '"'
(artist_id,artist_name)