load data infile '../data/csv/songs.csv'
insert into table song
fields terminated by "," optionally enclosed by '"'
(song_id,title,danceability,energy,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo)