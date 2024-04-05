create table custom_puzzle(
   cp_id int primary key,
   user_id int,
   song_id int,
   constraint u_id_fk foreign key (user_id) references user(user_id),
   constraint s_id_fk foreign key (song_id) references song(song_id)
);
exit;