load data infile '../data/song_genres.csv'
insert into table song_genre
fields terminated by "," optionally enclosed by '"'
(song_id,genre)