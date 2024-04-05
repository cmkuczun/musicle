-- disable fk constraints
SET FOREIGN_KEY_CHECKS = 0;

create table song_album(
    song_id int,
    album_id int,
    constraint s_id_fk foreign key (song_id) references song(song_id),
    constraint a_id_fk foreign key (album_id) references album(album_id)
);

-- enable fk constraints
SET FOREIGN_KEY_CHECKS = 1;
exit;