import cx_Oracle
import requests
import pprint
from datetime import datetime, timedelta

'''
TODO
- top 10 by solves
- top 10 by avg num rounds
'''

# ORACLE DB SETUP========================================================================================================
# create connection
try: 
    dsn_tns=cx_Oracle.makedsn('localhost','1521','xe')
    connection = cx_Oracle.connect("guest", "guest", dsn_tns)
    print("\nSTATUS: Connected to Oracle database.")
except Exception as e:
    print(print("\nSTATUS: Failed to connect to Oracle database."))
    print("ERROR: ", e)

# create cursor
try: 
    cursor = connection.cursor()
    print("\nSTATUS: Cursor created.\n")
except Exception as e:
    print("\nSTATUS: Failed to create cursor.")
    print("ERROR: ", e)


# EXECUTE QUERIES=========================================================================================================
def execute(q):
    # check for insert statement
    if q.startswith("INSERT"):
        print("NOTE: Insert query; ignore 'NOT A QUERY' error.")

    # try to run the query
    res = []
    try:
        cursor.execute(q)
        connection.commit()
    
        # fetch results
        for row in cursor:
            res.append(row)
        # print(f"SUCCESS: Query executed successfully ({q}).\n")
        return res
    
    except Exception as e:
        print("ERROR: ", e)
        connection.rollback()
        return None


# INSERT QUERIES=========================================================================================================
def insert_song(*args):
    '''
    song_id str primary key,
    song_name str,
    danceability float,
    energy float,
    loudness float,
    mode int,
    speechiness float,
    acousticness float,
    instrumentalness float,
    liveness float,
    valence float,
    tempo float
    '''
    song_id,song_name,danceability,energy,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo = args
    danceability=str(danceability)
    energy=str(energy)
    loudness=str(loudness)
    mode=str(mode)
    speechiness=str(speechiness)
    acousticness=str(acousticness)
    instrumentalness=str(instrumentalness)
    liveness=str(liveness)
    valence=str(valence)
    tempo=str(tempo)
    q = "INSERT INTO song VALUES ('" + song_id + "', '" + song_name + "', " + danceability + ", " + energy + ", " + loudness + ", " + mode + ", " + speechiness + ", " + acousticness + ", " + instrumentalness + ", " + liveness + ", " + valence + ", " + tempo + ")"
    return q

def insert_puzzle(*args):
    '''
    puzzle_id int primary key,
    song_id str,
    user_id int,
    puzzle_date date
    '''  
    puzzle_id,song_id,user_id,puzzle_date = args
    puzzle_id=str(puzzle_id)
    user_id=str(user_id)
    puzzle_date = "TO_DATE('" + puzzle_date + "', 'YYYY-MM-DD')"

    q = "INSERT INTO puzzle VALUES (" + puzzle_id + ", '" + song_id + "', " + user_id + ", " + puzzle_date + ")"
    return q

def insert_guess(*args):
    '''
    guess_id int primary key,
    puzzle_id int,
    user_id int,
    song_id int,
    guess_num int,
    is_correct int,
    '''
    guess_id,puzzle_id,user_id,song_id,guess_num,is_correct = args
    guess_id=str(guess_id)
    puzzle_id=str(puzzle_id)
    user_id=str(user_id)
    guess_num=str(guess_num)
    is_correct=str(is_correct)
    q = "INSERT INTO guess VALUES (" + guess_id + ", " + puzzle_id + ", " + user_id + ", '" + song_id + "', " + guess_num + ", " + is_correct + ")"
    res = execute(q)

def insert_song_artist(*args):
    '''
    song_id str,
    artist_id str    
    '''
    song_id,artist_id = args
    q = "INSERT INTO song_artist VALUES ('" + song_id + "', '" + artist_id + "')"
    return q

def insert_song_album(*args):
    '''
    song_id str,
    album_id str
    '''
    song_id,album_id = args
    q = "INSERT INTO song_album VALUES ('" + song_id + "', '" + album_id + "')"
    return q

def insert_artist_genre(*args):
    '''
    artist_id str,
    genre_id int
    '''
    artist_id,genre_id = args
    genre_id=str(genre_id)
    q = "INSERT INTO artist_genre VALUES ('" + artist_id + "', " + genre_id + ")"
    return q

def insert_genre(*args):
    '''
    genre_id int primary key,
    genre_name str
    '''
    genre_id,genre_name = args
    genre_id=str(genre_id)

    q = "INSERT INTO genre VALUES (" + genre_id + ", '" + genre_name + "')"
    return q

def insert_user(*args):
    '''
    user_id int primary key,
    username str,
    password str
    '''
    user_id,username,password = args
    user_id=str(user_id)

    q = "INSERT INTO usr VALUES (" + user_id + ", '" + username + "', '" + password + "')"
    return q

def insert_album(*args):
    '''
    album_id str primary key,
    album_name str,
    release_date str
    '''
    album_id,album_name,release_date = args
    release_date = "TO_DATE('" + release_date + "', 'YYYY-MM-DD')"

    q = "INSERT INTO album VALUES ('" + album_id + "', '" + album_name + "', " + release_date + ")"
    return q

def insert_artist(*args):
    '''
    artist_id str primary key,
    artist_name str
    '''
    artist_id,artist_name = args
    q = "INSERT INTO artist VALUES ('" + artist_id + "', '" + artist_name + "')"
    return q


# BASIC QUERIES=========================================================================================================
def get_id_from_song(song_name):
    ''' search for song id using EXACT song name
        returns: song id
    '''
    q = "select song_id from song where song_name like '%{}%'".format(song_name) 
    res = execute(q)
    # handle multiple songs
    if len(res) > 1:
        res_arr = []
        for song in res:
            res_arr.append(song[0])
        return res_arr
    return res[0][0]

def get_song_info_from_id(song_id):
    ''' get song characteristics using song id
        returns: array of song characteristics
    '''
    q = "select danceability,energy,loudness,song_mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo from song where song_id like '{}'".format(song_id) 
    res = execute(q)
    return list(res[0])

def get_album_from_song(song_id):
    ''' get album id from song id
        returns: album id
    '''
    q = "select album_id from song_album where song_id='{}'".format(song_id)
    res = execute(q)
    return res[0][0]

def get_album_from_id(album_id):
    ''' get album info from album_id
        returns: array of [album name, release date]
    '''
    q = "select album_name,release_date from album where album_id='{}'".format(album_id)
    res = execute(q)
    return list(res[0])

def get_artist_from_song(song_id):
    ''' get artist id from song id
        returns: artist_id
    '''
    q = "select artist_id from song_artist where song_id='{}'".format(song_id)
    res = execute(q)
    # handle multiple artists
    if len(res) > 1:
        res_arr = []
        for artist in res:
            res_arr.append(artist[0])
        return res_arr
    return list(res[0])

def get_artist_from_id(artist_id):
    ''' get artist name from artist id
        returns: artist name
    '''
    q = "select artist_name from artist where artist_id='{}'".format(artist_id)
    res = execute(q)
    return res[0][0]

def get_genre_from_artist(artist_id):
    ''' get genre id from artist id
        returns: genre_id
    '''
    q = "select genre_id from artist_genre where artist_id='{}'".format(artist_id)
    res = execute(q)
    # handle multiple genres
    if len(res) == 0:
        print('ERROR: No genre found.')
        return []
    if len(res) > 1:
        res_arr = []
        for genre in res:
            res_arr.append(genre[0])
        return res_arr
    return res[0][0]

def get_genre_from_id(genre_id):
    ''' get genre name from genre id
        returns: genre name
    '''
    if genre_id is not None:
        q = "select genre_name from genre where genre_id='{}'".format(str(genre_id))
        res = execute(q)
        return res[0][0]
    return None

def get_user_id(username,password):
    ''' supporting method to return just user id
        returns: user id
    '''
    q = "select user_id from usr where username='{}' and password='{}'".format(username,password)
    res = execute(q)
    user_id = res[0][0]
    return user_id

def get_album_id_from_album(album_str):
    '''returns: album ids for albums matching the input string'''
    output = []
    q = "select album_id from album where album_name like '%{}%'".format(album_str)
    res = execute(q)
    for entry in res:
        output.append(entry[0])
    return output

def get_artist_id_from_artist(artist_str):
    '''returns: artist ids for artists matching the input string'''
    output = []
    q = "select artist_id from artist where artist_name like '%{}%'".format(artist_str)
    res = execute(q)
    for entry in res:
        output.append(entry[0])
    return output

def get_song_from_artist(artist_id):
    '''returns: song id associated with artist id'''
    song_id = None
    q = ""
    # TODO query & parse result
    return song_id

def get_song_from_album(album_id):
    '''returns: song id associated with album id'''
    song_id = None
    q = ""
    # TODO query & parse result
    return song_id


# ADVANCED FUNCTIONS====================================================================================================
def build_dict(target_song_name, target_song_id, target_song_info,
                target_album_id, target_album_info,
                target_artist_ids, target_artist_names,
                target_genre_ids, target_genres):
    ''' given song statistics, form a dictionary (JSON object)
        returns: dictionary of a song and all associated information
    '''
    song_stats = dict()
    song_stats['song id'] = target_song_id # add to output dict
    song_stats['song name'] = target_song_name
    song_stats['danceability'] = target_song_info[0]
    song_stats['energy'] = target_song_info[1]
    song_stats['loudness'] = target_song_info[2]
    song_stats['song_mode'] = target_song_info[3]
    song_stats['speechiness'] = target_song_info[4]
    song_stats['acousticness'] = target_song_info[5]
    song_stats['instrumentalness'] = target_song_info[6]
    song_stats['liveness'] = target_song_info[7]
    song_stats['valence'] = target_song_info[8]
    song_stats['tempo'] = target_song_info[9]
    # make a dictionary for all artists
    song_stats['artists'] = []
    for a_id, a_name in zip(target_artist_ids,target_artist_names):
        curr_artist = dict()
        curr_artist['artist_id'] = a_id
        curr_artist['artist_name'] = a_name   
        # for each genre id of the current artist id
        curr_genres = {}
        for g_id in target_genre_ids[a_id]:
            # get the genre name
            g_name = target_genres[g_id]
            curr_genres[g_id] = g_name
        curr_artist['genres'] = curr_genres
        song_stats['artists'].append(curr_artist)
    # make a dictionary for album
    album_stats = dict()
    album_stats['album_id'] = target_album_id
    album_stats['album_name'] = target_album_info[0]
    album_stats['release_date'] = target_album_info[1]
    song_stats['album'] = album_stats
    # print output and make dict
    pprint.pprint(song_stats)
    return song_stats

def get_song_stats(target_song_name):
    '''get all information regarding a song, starting with song name
       build the dict as you execute the queries
       returns: the song's information
    '''
    # get song id from song name
    target_song_id = get_id_from_song(target_song_name)
    # get song information
    target_song_info = get_song_info_from_id(target_song_id)
    # get album id
    target_album_id = get_album_from_song(target_song_id)
    # get album name
    target_album_info = get_album_from_id(target_album_id)
    # get artist id
    target_artist_ids = get_artist_from_song(target_song_id)
    # get artist(s) from id(s)
    target_artist_names = []
    for a_id in target_artist_ids:
        res = get_artist_from_id(a_id)
        target_artist_names.append(res)
    # get genre id
    target_genre_ids = {}
    for curr_artist in target_artist_ids:
        target_genre_ids[curr_artist] = []
        curr_genres = get_genre_from_artist(curr_artist)
        target_genre_ids[curr_artist].append(curr_genres)
    target_genres = {}
    if len(target_genre_ids) > 0:
        for g_ids in target_genre_ids.values():
            for g_id in g_ids:
                genre = get_genre_from_id(g_id)
                target_genres[g_id] = genre
    # build and return the resulting dictionary
    song_stats = build_dict(target_song_name, target_song_id, target_song_info,
                            target_album_id, target_album_info,
                            target_artist_ids, target_artist_names,
                            target_genre_ids, target_genres)
    return song_stats

def create_user(username, password):
    ''' create a new user given username/password
        returns: user id (if exists) or False (something went wrong)
    '''
    # create a new user
    q = "INSERT INTO usr (user_id, username, password) SELECT COALESCE(MAX(user_id), -1) + 1, '{}', '{}' FROM usr".format(username,password)
    res = execute(q)
    # check that you can login as the user (it exists)
    check_insert = login(username, password)
    # check if inserted properly
    if check_insert:
        # return the user_id of new user
        return check_insert
    else: 
        print("ERROR: Something went wrong when create account for {}.".format(username))
        return False
    
def login(username, password):
    ''' checks for matching username/password row in usr table
        returns: user_id if exists or None if does not exist
    '''
    # try to get the user id
    q = "select user_id from usr where username='{}' and password='{}'".format(username,password)
    res = execute(q)
    if len(res) > 0:
        # return user_id if exists
        user_id = res[0][0]
        return user_id
    # return NULL
    return None

def get_user_streak(user_id):
    ''' get user daily streak: how many days in a row played puzzles
        returns: streak of inputted user id
    '''
    streak = 0
    q = f"""
        SELECT COUNT(*) AS streak
        FROM (
            SELECT puzzle_date,
                ROW_NUMBER() OVER (ORDER BY puzzle_date) - ROW_NUMBER() 
                OVER (PARTITION BY trunc(puzzle_date) ORDER BY puzzle_date) AS grp
            FROM (
                SELECT p.puzzle_date
                FROM puzzle p
                LEFT JOIN guess g ON p.puzzle_id = g.puzzle_id AND p.user_id = g.user_id
                WHERE p.user_id = {user_id}
                AND (g.user_id IS NOT NULL OR p.user_id = {user_id})
            )
        )
        WHERE ROWNUM < 2
        GROUP BY grp
        ORDER BY COUNT(*) DESC
    """
    res = execute(q)
    if len(res) == 0:
        streak = 0
    else:
        streak = res[0][0]
    return streak

def get_top_10_by_streak(user_id):
    ''' get top 10 players by daily streaks
        include the inputted user_id in top 10 or as an additional output
        returns: dictionary of {user_id: current_streak}
    '''
    
    players = {}
    q = f"""
        SELECT user_id, streak
        FROM (
            SELECT user_id, streak,
                RANK() OVER (ORDER BY streak DESC) AS rank
            FROM (
                SELECT user_id,
                    COUNT(*) AS streak
                FROM (
                    SELECT p.user_id,
                        ROW_NUMBER() OVER (PARTITION BY p.user_id ORDER BY p.puzzle_date) -
                        ROW_NUMBER() OVER (PARTITION BY p.user_id, trunc(p.puzzle_date) ORDER BY p.puzzle_date) AS grp
                    FROM puzzle p
                    LEFT JOIN guess g ON p.puzzle_id = g.puzzle_id AND p.user_id = g.user_id
                    WHERE (g.user_id IS NOT NULL OR p.user_id = {user_id})
                )
                GROUP BY user_id, grp
            )
        )
        WHERE rank <= 10 OR user_id = {user_id}
        ORDER BY rank
        """
    res = execute(q)
    for r in res:
        players[r[0]] = r[1]
    return players

def get_top_10_by_solves(user_id):
    ''' get top 10 players by number of rounds needed to solve puzzles (including inputted user)
        returns: dictionary of {user id: number of rounds}
    '''
    players = {}
    q = f"""
        SELECT user_id, total_rounds
        FROM (
            SELECT user_id, total_rounds,
                RANK() OVER (ORDER BY total_rounds ASC) AS rank
            FROM (
                SELECT user_id,
                    SUM(
                        CASE
                            WHEN is_correct = 1 THEN guess_num
                            ELSE 0
                        END
                    ) AS total_rounds
                FROM (
                    SELECT p.user_id, g.is_correct, g.guess_num,
                        SUM(
                            CASE
                                WHEN g.is_correct = 1 THEN 1
                                ELSE 0
                            END
                        ) OVER (PARTITION BY p.user_id, p.puzzle_id ORDER BY g.guess_id) AS correct_guesses
                    FROM puzzle p
                    JOIN guess g ON p.puzzle_id = g.puzzle_id AND p.user_id = g.user_id
                ) sub
                WHERE correct_guesses > 0
                GROUP BY user_id
            )
        )
        WHERE rank <= 10 OR user_id = {user_id}
        ORDER BY total_rounds
        """
    # TODO NOT WORKING
    res = execute(q)
    for r in res:
        p_id = r[0]
        num_rounds = r[1]
        players[p_id] = num_rounds
    return players
   
def get_top_10_by_avg_rounds(user_id):
    ''' get top 10 players by average rounds needed to solve puzzles including inputted user
        returns: dictionary of {player id: average rounds}
    '''
    q = f"""
        WITH AvgRounds AS (
        SELECT
            p.user_id,
            AVG(
                CASE 
                    WHEN g.is_correct = 1 
                        THEN g.guess_num 
                    ELSE NULL END
            ) AS avg_rounds,
            RANK() OVER (ORDER BY AVG(CASE WHEN g.is_correct = 1 THEN g.guess_num ELSE NULL END) ASC) AS rank
        FROM puzzle p
        JOIN guess g ON p.puzzle_id = g.puzzle_id 
            AND p.user_id = g.user_id
        GROUP BY p.user_id
        HAVING MAX(g.is_correct) = 1
    )
    SELECT user_id, AVG(avg_rounds) AS average_rounds
    FROM AvgRounds
    WHERE rank <= 10 OR user_id = {user_id}
    GROUP BY user_id
    ORDER BY average_rounds
    """
    players = {}
    res = execute(q)
    for r in res:
        players[r[0]] = r[1]
    return players

def get_overall_total_solved():
    ''' get total unique games solved by all players
        i.e. count number of unique game id's for which there is a is_correct=1
        returns: number of solved games
    '''
    count = 0
    q = """
        SELECT COUNT(DISTINCT puzzle_id) AS total_solved
        FROM guess
        WHERE is_correct = 1
        """
    res = execute(q)
    try:
        count = res[0][0]
        return count
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def get_avg_solved_game_len():
    ''' get average game solve length by all players
        returns: number 
    '''
    average = 0
    q = """
        WITH AvgRounds AS (
            SELECT
                p.user_id,
                SUM(
                    CASE WHEN g.is_correct = 1 THEN g.guess_num ELSE NULL END
                ) AS total_rounds,
                COUNT(DISTINCT p.puzzle_id) AS solved_puzzles_count
            FROM puzzle p
            JOIN
                guess g ON p.puzzle_id = g.puzzle_id AND p.user_id = g.user_id
            WHERE g.is_correct = 1
            GROUP BY p.user_id
            )
            SELECT
                AVG(total_rounds) AS average_game_solve_length
            FROM
        AvgRounds;
        """
    return average

def most_freq_guessed_song():
    '''get the most frequently guessed song'''
    q = """
        SELECT * FROM (
            SELECT s.song_name, COUNT(*) AS guess_count
            FROM guess g
            JOIN song s ON g.song_id = s.song_id
            GROUP BY s.song_name
            ORDER BY guess_count DESC
        ) WHERE ROWNUM < 2
        """
    res = execute(q)
    # return song_name,count
    return res[0]

def get_all_games_played():
    '''get all unique puzzle ids'''
    q = """
        SELECT COUNT(DISTINCT puzzle_id)
        FROM puzzle
        """
    res = execute(q)
    return res[0][0]

def get_songs_from_input(input_str):
    ''' get albums that match input, then match album ids with songs
        get artists that match input, then match these artists' ids with songs
        also get song names that match input string
        returns: set of song stats dictionaries containing the matching albums
    ''' 
    output = []
    # get albums, artists, songs that match the input
    matching_albums = get_album_id_from_album(input_str)
    matching_artists = get_artist_id_from_artist(input_str)
    matching_songs = get_id_from_song(input_str) # returns song ids
    # get song ids from artists
    for a_id in matching_artists:
        associated_s_id = get_song_from_artist(a_id)
        matching_songs.append(associated_s_id)
    # get song ids from albums
    for a_id in matching_albums:
        associated_s_id = get_song_from_album(a_id)
        matching_songs.append(associated_s_id)
    # get song info for each song id
    for s_id in matching_songs:
        s_info = get_song_stats(s_id)
        output.append(s_info)
    return output


# API KEY FOR LAST.FM====================================================================================================
api_key = 'YOUR_API_KEY'

# API QUERY==============================================================================================================
# query API to get similar artists
def query_similar_artists(artist_name):#
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist={artist_name}&api_key={api_key}&format=json"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if 'similarartists' in data and 'artist' in data['similarartists']:
            similar_artists = [artist['name'] for artist in data['similarartists']['artist']]
            return similar_artists
        else:
            print("WARNING: couldn't find similar artists.")
            return None
    except Exception as e:
        print(f"ERROR: {e}")
        return None

