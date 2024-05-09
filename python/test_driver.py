from queries import *

# TESTING=========================================================================================================
def check_res(res):
    if res is not None:
        print("OUTPUT")
        for elem in res: print(f'> {elem}')

print("===============================================================================")
print("\nTESTING: Commencing test driver functions.\n")

'''TEST 0: run a basic query to test cursor/connection functionality'''
print("* TEST 0: Basic query ---------------------------------------------------------")
q = "select * from song where song_name like '%lemon%'"
res = execute(q)
print("* TEST 0 complete.\n")


'''TESTS 1-10: run 10 queries to test inserting into all tables'''
# INPUTS
song_id='TEST1'
song_name='TEST SONG NAME11'
danceability=0.0
energy=0.0
loudness=0.0
song_mode=0
speechiness=0.0
acousticness=0.0
instrumentalness=0.0
liveness=0.0
valence=0.0
tempo=0.0
album_id='TESTALBUMID11'
album_name='TEST ALBUM NAME11'
release_date='1000-10-11'
artist_id='TESTARTISTID6'
artist_name='TEST ARTIST NAME11'
genre_id=-11000
genre_name='TEST GENRE NAME11'
guess_id=-110000
puzzle_id=-110000
user_id=-110000
guess_num=11
is_correct=0
puzzle_date='1000-10-11'
username='TESTUSERNAME11'
password='TESTPASSWORD11'

print("* TEST 1: song insertion ------------------------------------------------------")
q = insert_song(song_id,song_name,danceability,energy,loudness,song_mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo)
res = execute(q)
print("* TEST 1 complete.\n")

print("* TEST 2: album insertion -----------------------------------------------------")
q = insert_album(album_id,album_name,release_date)
res = execute(q)
check_res(res)
print("* TEST 2 complete.\n")

print("* TEST 3: artist insertion ----------------------------------------------------")
q = insert_artist(artist_id,artist_name)
res = execute(q)
check_res(res)
print("* TEST 3 complete.\n")

print("* TEST 4: genre insertion -----------------------------------------------------")
q = insert_genre(genre_id,genre_name)
res = execute(q)
check_res(res)

print("* TEST 4 complete.\n")

print("* TEST 5: artist_genre insertion ----------------------------------------------")
q = insert_artist_genre(artist_id,genre_id)
res = execute(q)
check_res(res)
print("* TEST 5 complete.\n")

print("* TEST 6: song_album insertion ------------------------------------------------")
q = insert_song_album(song_id,album_id)
res = execute(q)
check_res(res)
print("* TEST 6 complete.\n")

print("* TEST 7: song_artist insertion -----------------------------------------------")
q = insert_song_artist(song_id,artist_id)
res = execute(q)
check_res(res)
print("* TEST 7 complete.\n")

print("* TEST 8: usr insertion -------------------------------------------------------")
q = insert_user(user_id,username,password)
res = execute(q)
check_res(res)
print("* TEST 8 complete.\n")

print("* TEST 9: puzzle insertion ----------------------------------------------------")
q = insert_puzzle(puzzle_id,song_id,user_id,puzzle_date)
res = execute(q)
check_res(res)
print("* TEST 9 complete.\n")

print("* TEST 10: guess insertion ----------------------------------------------------")
q = insert_guess(guess_id,puzzle_id,user_id,song_id,guess_num,is_correct)
res = execute(q)
check_res(res)
print("* TEST 10 complete.\n")

'''TEST 11: run a query to get all song info associated with song_id/song_title'''
print("* TEST 11: Song info query ----------------------------------------------------")
# get song id from song name
song_name = 'Intoxica'
song_stats = get_song_stats(song_name) # returns a dict
print("* TEST 11 complete.\n")

'''TEST 12: login as an existing user'''
print("* TEST 12: Login existing user ------------------------------------------------")
test_user = 'TESTUSERNAME2'
test_pass = 'TESTPASSWORD2'
test_user_id = login(test_user, test_pass)
print(f'> OUTPUT: Test user id = {test_user_id}.')
print("* TEST 12 complete.\n")

'''TEST 13: create a new user, assign them a new user id'''
print("* TEST 13: Create new user ----------------------------------------------------")
test_user = 'TESTCRTUSER2'
test_pass = 'TESTCRTPASS2'
stats = create_user(test_user,test_pass)
print("* TEST 13 complete.\n")

'''TEST 14: create a new user, assign them a new user id'''
print("* TEST 14: Get user streak ----------------------------------------------------")
insert_song('test1111','test1111name',0.0,0.0,0.0,-1,0.0,0.0,0.0,0.0,0.0,0.0)
insert_puzzle(-111,'test1111',0,'1000-10-11')
insert_puzzle(-222,'test1111',0,'1000-10-12')
insert_puzzle(-333,'test1111',0,'1000-10-13')
insert_guess(-111,-111,0,'test1111',1,1)
insert_guess(-222,-222,0,'test1111',1,1)
insert_guess(-333,-333,0,'test1111',1,1)
streak = get_user_streak(0)
print(streak)
print("* TEST 14 complete.\n")

'''TEST 15: get top 10 players by streak'''
print("* TEST 15: top 10 by streak ----------------------------------------------------")
streaks = get_top_10_by_streak(0)
print(streaks)
print("* TEST 15 complete.\n")

'''TEST 16: get top 10 players by solves'''
print("* TEST 16: Top 10 players by solves ----------------------------------------------------")
solvers = get_top_10_by_solves(0)
print(solvers)
print("* TEST 16 complete.\n")

'''TEST 17: get top 10 players by avg number of rounds until solving'''
print("* TEST 17: Top 10 players by avg num rounds ----------------------------------------------------")
rounds = get_top_10_by_avg_rounds(0)
print(rounds)
print("* TEST 17 complete.\n")

'''TEST 18: get count of all unique games solved'''
print("* TEST 18: Count all games solved ----------------------------------------------------")
cnt = get_overall_total_solved()
print(cnt)
print("* TEST 18 complete.\n")

'''TEST 19: get most popular guess (song)'''
print("* TEST 19: Most frequently guessed song ----------------------------------------------------")
output = most_freq_guessed_song()
print(f'{output[0]} was guessed {output[1]} times.')
print("* TEST 19 complete.\n")
