create table song_genre(
    song_id int,
    genre varchar(100),
    constraint s_id_fk foreign key (song_id) references song(song_id)
);
exit;