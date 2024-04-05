load data infile '../data/songs.csv'
insert into table song
fields terminated by "," optionally enclosed by '"'
(song_id,title,artist,album,genre,release_yr,lyrics,url)