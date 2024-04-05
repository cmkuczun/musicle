# CREATE TABLES=======================================================
# main tables
@crt_album
@crt_artist
@crt_genre
@crt_daily_guess
@crt_custom_guess
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
sqlplus ckuczun/claud <<EOF 
ALTER TABLE song_artist DISABLE CONSTRAINT s_id_fk; ALTER TABLE song_artist DISABLE CONSTRAINT a_id_fk; exit; 
EOF
sqlldr ckuczun/claud control=sql/song_artist.ctl
sqlplus ckuczun/claud <<EOF 
ALTER TABLE song_artist ENABLE CONSTRAINT s_id_fk; ALTER TABLE song_artist ENABLE CONSTRAINT a_id_fk; exit; 
EOF

# song_album
sqlplus ckuczun/claud <<EOF 
ALTER TABLE song_album DISABLE CONSTRAINT s_id_fk; ALTER TABLE song_album DISABLE CONSTRAINT a_id_fk; exit; 
EOF
sqlldr ckuczun/claud control=sql/song_album.ctl
sqlplus ckuczun/claud <<EOF 
ALTER TABLE song_album ENABLE CONSTRAINT s_id_fk; ALTER TABLE song_album ENABLE CONSTRAINT a_id_fk; exit; 
EOF

# artist_genre
sqlplus ckuczun/claud <<EOF 
ALTER TABLE artist_genre DISABLE CONSTRAINT a_id_fk; ALTER TABLE artist_genre DISABLE CONSTRAINT g_id_fk; exit; 
EOF
sqlldr ckuczun/claud control=sql/artist_genre.ctl
sqlplus ckuczun/claud <<EOF 
ALTER TABLE artist_genre ENABLE CONSTRAINT a_id_fk; ALTER TABLE artist_genre ENABLE CONSTRAINT g_id_fk; exit; 
EOF