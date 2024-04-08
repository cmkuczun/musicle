# CREATE TABLES=======================================================
# main tables
sqlplus @crt_album
sqlplus @crt_artist
sqlplus @crt_genre
sqlplus @crt_daily_guess
sqlplus @crt_custom_guess
sqlplus @crt_song
sqlplus @crt_user
sqlplus @crt_cp
sqlplus @crt_dp

# one to many tables
sqlplus @crt_song_artist
sqlplus @crt_song_genre
sqlplus @crt_artist_genre


# LOAD DATA==========================================================
# song
sqlldr ckuczun/claud control=sql/song.ctl skip=1
# artist
sqlldr ckuczun/claud control=sql/artist.ctl skip=1
# genre
sqlldr ckuczun/claud control=sql/genre.ctl skip=1
# album
sqlldr ckuczun/claud control=sql/album.ctl skip=1

# song_artist
sqlplus ckuczun/claud <<EOF 
ALTER TABLE song_artist DISABLE CONSTRAINT s_id_fk; ALTER TABLE song_artist DISABLE CONSTRAINT a_id_fk; exit; 
EOF
sqlldr ckuczun/claud control=sql/song_artist.ctl skip=1
sqlplus ckuczun/claud <<EOF 
ALTER TABLE song_artist ENABLE CONSTRAINT s_id_fk; ALTER TABLE song_artist ENABLE CONSTRAINT a_id_fk; exit; 
EOF

# song_album
sqlplus ckuczun/claud <<EOF 
ALTER TABLE song_album DISABLE CONSTRAINT s_id_fk; ALTER TABLE song_album DISABLE CONSTRAINT a_id_fk; exit; 
EOF
sqlldr ckuczun/claud control=sql/song_album.ctl skip=1
sqlplus ckuczun/claud <<EOF 
ALTER TABLE song_album ENABLE CONSTRAINT s_id_fk; ALTER TABLE song_album ENABLE CONSTRAINT a_id_fk; exit; 
EOF

# artist_genre
sqlplus ckuczun/claud <<EOF 
ALTER TABLE artist_genre DISABLE CONSTRAINT a_id_fk; ALTER TABLE artist_genre DISABLE CONSTRAINT g_id_fk; exit; 
EOF
sqlldr ckuczun/claud control=sql/artist_genre.ctl skip=1
sqlplus ckuczun/claud <<EOF 
ALTER TABLE artist_genre ENABLE CONSTRAINT a_id_fk; ALTER TABLE artist_genre ENABLE CONSTRAINT g_id_fk; exit; 
EOF
