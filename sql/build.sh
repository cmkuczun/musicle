# CREATE TABLES=======================================================
# main tables
@crt_album
@crt_artist
@crt_genre
@crt_guess
@crt_song
@crt_user
@crt_cp
@crt_dp

# one to many tables
@crt_song_artist
@crt_song_genre
@crt_artist_genre


# LOAD DATA==========================================================
# song
sqlldr ckuczun/claud control=sql/song.ctl
# artist
sqlldr ckuczun/claud control=sql/artist.ctl
# genre
sqlldr ckuczun/claud control=sql/genre.ctl
# album
sqlldr ckuczun/claud control=sql/album.ctl
# song_artist
sqlldr ckuczun/claud control=sql/song_artist.ctl
# song_album
sqlldr ckuczun/claud control=sql/song_album.ctl
# artist_genre
sqlldr ckuczun/claud control=sql/artist_genre.ctl