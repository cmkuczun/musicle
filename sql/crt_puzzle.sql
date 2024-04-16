create table puzzle(
  puzzle_id int primary key,
  song_id varchar(50),
  user_id int,
  puzzle_date date,
  constraint p_s_id_fk foreign key (song_id) references song(song_id),
  constraint p_u_id_fk foreign key (user_id) references usr(user_id)
);
exit;

