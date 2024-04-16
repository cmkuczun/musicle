load data infile '../data/csv/songs.csv'
insert into table song
fields terminated by "," optionally enclosed by '"'
(song_id,song_name,danceability,energy,loudness,song_mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo)
