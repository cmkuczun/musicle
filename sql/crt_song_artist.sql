create table song_artist(
    song_id varchar(50),
    artist_id varchar(50),
    constraint sar_s_id_fk foreign key (song_id) references song(song_id),
    constraint sar_a_id_fk foreign key (artist_id) references artist(artist_id),
    constraint pk_song_artist primary key (song_id, artist_id)
);
exit;
