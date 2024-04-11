-- disable fk constraints
SET FOREIGN_KEY_CHECKS = 0;

create table custom_puzzle(
   cp_id int primary key auto_increment,
   user_id int,
   song_id int,
   constraint u_id_fk foreign key (user_id) references user(user_id),
   constraint s_id_fk foreign key (song_id) references song(song_id)
);

-- enable fk constraints
SET FOREIGN_KEY_CHECKS = 1;
exit;
