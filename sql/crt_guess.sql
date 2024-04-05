create table guess(
   guess_id int primary key auto_increment,
   user_id int,
   song_id int,
   is_correct boolean,
   constraint u_id_fk foreign key (user_id) references user(user_id),
   constraint s_id_fk foreign key (song_id) references song(song_id)
);
exit;
