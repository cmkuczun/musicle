create table guess(
   guess_id int primary key,
   user_id int,
   song_id int,
   guess_title varchar(200),
   guess_artist varchar(100),
   guess_genre varchar(100),
   guess_release_yr varchar(4),
   is_correct boolean,
   constraint u_id_fk foreign key (user_id) references user(user_id),
   constraint s_id_fk foreign key (song_id) references song(song_id)
);
exit;
