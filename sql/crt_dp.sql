-- disable fk constraints
SET FOREIGN_KEY_CHECKS = 0;

create table daily_puzzle(
   dp_id int primary key auto_increment,
   song_id int,
   dp_date date,
   constraint s_id_fk foreign key (song_id) references song(song_id)
);

-- enable fk constraints
SET FOREIGN_KEY_CHECKS = 1;
exit;