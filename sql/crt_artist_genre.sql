create table artist_genre(
    genre_id int,
    artist_id int,
    constraint a_id_fk foreign key (artist_id) references artist(artist_id),
    constraint g_id_fk foreign key (genre_id) references genre(genre_id)
);
exit;