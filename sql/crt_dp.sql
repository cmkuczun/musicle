create table daily_puzzle(
   dp_id int,
   song_id int,
   dp_date date,
   constraint s_id_fk foreign key (song_id) references song(song_id)
);
exit;
