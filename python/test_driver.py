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
check_res(res)
print("* TEST 0 complete.\n")


'''TESTS 1-10: run 10 queries to test inserting into all tables'''
# INPUTS
song_id='TESTSONGID6'
song_name='TEST SONG NAME6'
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
album_id='TESTALBUMID6'
album_name='TEST ALBUM NAME6'
release_date='1000-10-10'
artist_id='TESTARTISTID6'
artist_name='TEST ARTIST NAME6'
genre_id=-6000
genre_name='TEST GENRE NAME6'
guess_id=-60000
puzzle_id=-60000
user_id=-60000
guess_num=6
is_correct=0
puzzle_date='1000-10-10'
username='TESTUSERNAME6'
password='TESTPASSWORD6'

print("* TEST 1: song insertion ------------------------------------------------------")
q = insert_song(song_id,song_name,danceability,energy,loudness,song_mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo)
res = execute(q)
check_res(res)
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

# get song id from song name
test_user = 'TESTCRTUSER2'
test_pass = 'TESTCRTPASS2'
stats = create_user(test_user,test_pass)
print("* TEST 13 complete.\n")
