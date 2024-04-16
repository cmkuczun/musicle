create table song_album(
    song_id varchar(50),
    album_id varchar(50),
    constraint sa_s_id_fk foreign key (song_id) references song(song_id),
    constraint sa_a_id_fk foreign key (album_id) references album(album_id),
    constraint pk_song_album primary key (song_id, album_id)
);
exit;
