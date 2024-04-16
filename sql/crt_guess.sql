create table guess(
  guess_id int primary key,
  puzzle_id int,
  user_id int,
  song_id varchar(50),
  guess_num int,
  is_correct int,
  constraint g_u_id_fk foreign key (user_id) references usr(user_id),
  constraint g_s_id_fk foreign key (song_id) references song(song_id),
  constraint g_p_id foreign key (puzzle_id) references puzzle(puzzle_id)
);
exit;

