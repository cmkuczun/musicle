load data infile '../data/artist_genres.csv'
insert into table artist_genre
fields terminated by "," optionally enclosed by '"'
(genre_id,artist_id)