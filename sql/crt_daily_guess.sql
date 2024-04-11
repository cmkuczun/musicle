-- disable fk constraints
SET FOREIGN_KEY_CHECKS = 0;

create table daily_guess(
   guess_id int primary key auto_increment,
   puzzle_id int,
   user_id int,
   song_id int,
   is_correct boolean,
   constraint u_id_fk foreign key (user_id) references user(user_id),
   constraint s_id_fk foreign key (song_id) references song(song_id),
   constraint p_id foreign key (puzzle_id) references daily_puzzle(dp_id)
);

-- enable fk constraints
SET FOREIGN_KEY_CHECKS = 1;
exit;
