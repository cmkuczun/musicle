# CREATE TABLES=======================================================
# main tables
sqlplus guest/guest @crt_song
sqlplus guest/guest @crt_album
sqlplus guest/guest @crt_artist
sqlplus guest/guest @crt_genre
sqlplus guest/guest @crt_user
sqlplus guest/guest @crt_puzzle
sqlplus guest/guest @crt_guess

# one to many tables
sqlplus guest/guest @crt_song_artist
sqlplus guest/guest @crt_song_album
sqlplus guest/guest @crt_artist_genre


# LOAD DATA==========================================================
# song
sqlldr guest/guest control=song.ctl
# artist
sqlldr guest/guest control=artist.ctl
# genre
sqlldr guest/guest control=genre.ctl
# album
sqlldr guest/guest control=album.ctl
# song_artist
sqlldr guest/guest control=song_artist.ctl direct=true
# song_album
sqlldr guest/guest control=song_album.ctl direct=true
# artist_genre
sqlldr guest/guest control=artist_genre.ctl direct=true
