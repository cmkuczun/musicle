-- disable fk constraints
SET FOREIGN_KEY_CHECKS = 0;

create table song_artist(
    song_id int,
    artist_id int,
    constraint s_id_fk foreign key (song_id) references song(song_id),
    constraint a_id_fk foreign key (artist_id) references artist(artist_id)
);

-- enable fk constraints
SET FOREIGN_KEY_CHECKS = 1;
exit;