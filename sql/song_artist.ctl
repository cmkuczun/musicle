load data infile '../data/csv/song_artists.csv'
insert into table song_artist
fields terminated by "," optionally enclosed by '"'
(song_id,artist_id)
