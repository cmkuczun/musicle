create table artist_genre(
    artist_id varchar(50),
    genre_id int,
    constraint ag_a_id_fk foreign key (artist_id) references artist(artist_id),
    constraint ag_g_id_fk foreign key (genre_id) references genre(genre_id),
    constraint pk_artist_genre primary key (artist_id, genre_id)
);
exit;
