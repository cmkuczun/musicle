#from api.service.queries import *
from queries import *

# TESTING=========================================================================================================
def check_res(res):
    if res is not None:
        print("OUTPUT")
        for elem in res: print(f'> {elem}')

print("===============================================================================")
print("\nTESTING: Commencing test driver functions.\n")


'''TESTS 1-10: run 10 queries to test inserting into all tables'''
# INPUTS
song_id='TEST111'
song_name='TEST SONG NAME111'
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
genre_name='TEST FAKE GENRE'
guess_id=-1111
puzzle_id=-1112
user_id=0
guess_num=1
is_correct=1
puzzle_date='1000-10-11'
username='TESTUSERNAME111'
password='TESTPASSWORD111'

# TESTING
test_inserts = False

if test_inserts:
    print("* TEST 1: song insertion ------------------------------------------------------")
    insert_song(song_id,song_name,danceability,energy,loudness,song_mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo)
    print("* TEST 1 complete.\n")

    print("* TEST 2: album insertion -----------------------------------------------------")
    insert_album(album_id,album_name,release_date)
    print("* TEST 2 complete.\n")

    print("* TEST 3: artist insertion ----------------------------------------------------")
    insert_artist(artist_id,artist_name)
    print("* TEST 3 complete.\n")

    print("* TEST 4: genre insertion -----------------------------------------------------")
    insert_genre(genre_name)
    print("* TEST 4 complete.\n")

    print("* TEST 5: artist_genre insertion ----------------------------------------------")
    insert_artist_genre(artist_id,genre_id)
    print("* TEST 5 complete.\n")

    print("* TEST 6: song_album insertion ------------------------------------------------")
    insert_song_album(song_id,album_id)
    print("* TEST 6 complete.\n")

    print("* TEST 7: song_artist insertion -----------------------------------------------")
    insert_song_artist(song_id,artist_id)
    print("* TEST 7 complete.\n")

    print("* TEST 8: usr insertion -------------------------------------------------------")
    res = create_user(username, password)
    check_res(res)
    print("* TEST 8 complete.\n")

    print("* TEST 9: puzzle insertion ----------------------------------------------------")
    res = insert_puzzle(song_id,user_id,puzzle_date)
    check_res(res)
    print("* TEST 9 complete.\n")

    print("* TEST 10: guess insertion ----------------------------------------------------")
    insert_guess(puzzle_id,user_id,song_id)
    print("* TEST 10 complete.\n")

'''TEST 11: run a query to get all song info associated with exact song name'''
print("* TEST 11: Song info query ----------------------------------------------------")
song_name = 'A Dried Seahorse'
song_id = get_id_from_song(song_name) # returns a list of matching song ids
song_id = song_id[0]
song_stats = get_song_stats(song_id) # returns a dict
pprint.pprint(song_stats)
print("* TEST 11 complete.\n")

'''TEST 12: login as an existing user'''
print("* TEST 12: Login existing user ------------------------------------------------")
test_user_id = login('MidnightMystic23', 'MysticMidnight$7')
print(f'Test user id = {test_user_id}')
print("* TEST 12 complete.\n")

if test_inserts:
    '''TEST 13: create a new user, assign them a new user id'''
    print("* TEST 13: Create new user ----------------------------------------------------")
    test_user = 'ClaudFake2'
    test_pass = 'ClaudFake2'
    uid = create_user(test_user,test_pass)
    print(f'- User ID returned = {uid}')
    print("* TEST 13 complete.\n")

'''TEST 14: get a user's streak'''
print("* TEST 14: Get user streak ----------------------------------------------------")
streak = get_user_streak(60)
print(streak)
print("* TEST 14 complete.\n")

'''TEST 15: get top 10 players by streak'''
print("* TEST 15: Top 10 by streak ----------------------------------------------------")
streaks = get_top_10_by_streak(60)
print(streaks)
print("* TEST 15 complete.\n")

'''TEST 16: get top 10 players by solves'''
print("* TEST 16: Top 10 players by solves --------------------------------------------")
solvers = get_top_10_by_solves(60)
print(solvers)
print("* TEST 16 complete.\n")

'''TEST 17: get top 10 players by avg number of rounds'''
print("* TEST 17: Top 10 players by avg num rounds ------------------------------------")
rounds = get_top_10_by_avg_rounds(60)
print(rounds)
print("* TEST 17 complete.\n")

'''TEST 18: get count of all unique games solved'''
print("* TEST 18: Count all games solved ----------------------------------------------")
cnt = get_overall_total_solved()
print(f' - Total games solved = {cnt}')
print("* TEST 18 complete.\n")

'''TEST 19: get most popular guess'''
print("* TEST 19: Most frequently guessed song ----------------------------------------")
output = most_freq_guessed_song()
print(f'- {output[0]} was guessed {output[1]} times')
print("* TEST 19 complete.\n")

'''TEST 20: get all games played'''
print("* TEST 20: Get all guessed games -----------------------------------------------")
print(f'- Total games played = {get_all_games_played()}')
print("* TEST 20 complete.\n")
