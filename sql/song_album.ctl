load data infile '../data/song_albums.csv'
insert into table song_album
fields terminated by "," optionally enclosed by '"'
(song_id,album_id)