create table song_artist(
    song_id int,
    artist varchar(100),
    constraint s_id_fk foreign key (song_id) references song(song_id)
);
exit;