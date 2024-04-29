import cx_Oracle
import requests
import pprint
import time

# ORACLE DB SETUP========================================================================================================
# create connection
try: 
    dsn_tns=cx_Oracle.makedsn('localhost','1521','xe')
    connection = cx_Oracle.connect("guest", "guest", dsn_tns)
    time.sleep(1)
    print("\nSTATUS: Connected to Oracle database.")
except Exception as e:
    print(print("\nSTATUS: Failed to connect to Oracle database."))
    print("ERROR: ", e)

# create cursor
try: 
    cursor = connection.cursor()
    print("\nSTATUS: Cursor created.\n")
except cx_Oracle.DatabaseError as e:
        error, = e.args
        print("Oracle-Error-Code:", error.code)
        print("Oracle-Error-Message:", error.message)
        print("Oracle-Error-Context:", error.context)
        print("\nSTATUS: Failed to create cursor.")
except Exception as e:
    print("\nSTATUS: Failed to create cursor.")
    print("ERROR: ", e)


def execute(q):
    '''execute queries'''
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
def insert_song(song_id,song_name,danceability,energy,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo):
    '''
    inputs: all song attributes
    inserts new song entry into database
    '''
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
    execute(q)

def insert_album(album_id,album_name,release_date):
    '''
    inputs: album_id, album_name, release_date (YYYY-MM-DD format)
    inserts a new album entry
    '''
    release_date = "TO_DATE('" + release_date + "', 'YYYY-MM-DD')"

    q = "INSERT INTO album VALUES ('" + album_id + "', '" + album_name + "', " + release_date + ")"
    execute(q)

def insert_artist(artist_id,artist_name):
    '''
    inputs: artist_id, artist_name
    inserts new artist
    '''
    q = "INSERT INTO artist VALUES ('" + artist_id + "', '" + artist_name + "')"
    execute(q)

def insert_puzzle(song_id,user_id,puzzle_date):
    '''
    inputs: song_id, user_id, puzzle_date 
    (NOTE - for daily puzzle, user_id must be None)
    returns: puzzle_id of new puzzle
    '''

    # daily puzzle
    if user_id is None:
        user_id='NULL'
    # custom puzzle
    else:
        user_id=str(user_id)

    puzzle_date=str(puzzle_date)
    song_id=str(song_id)
    puzzle_date = "TO_DATE('" + puzzle_date + "', 'YYYY-MM-DD')"
    
    # create the puzzle
    q1 = '''INSERT INTO puzzle (puzzle_id, song_id, user_id, puzzle_date) 
            SELECT COALESCE(MAX(puzzle_id), -1) + 1, '{}', {}, {} FROM puzzle
        '''.format(song_id, user_id, puzzle_date)
    execute(q1)
    
    # get new puzzle id
    q2 = '''SELECT puzzle_id FROM puzzle WHERE puzzle_id = (SELECT COALESCE(MAX(puzzle_id), -1) FROM puzzle)'''
    puzzle_id = execute(q2)[0][0]

    # return new id
    return puzzle_id

def insert_guess(puzzle_id,user_id,song_id):
    '''
    inputs: puzzle_id, user_id, song_id
    (guess_id, guess_num, and is_correct are automatically generated)
    '''
    puzzle_id=str(puzzle_id)
    user_id=str(user_id)
    song_id=str(song_id)
    q = f'''
        INSERT INTO guess (guess_id, puzzle_id, user_id, song_id, guess_num, is_correct)
        SELECT
            (SELECT COALESCE(MAX(guess_id), 0) + 1 FROM guess),
            {puzzle_id},
            {user_id},
            '{song_id}',
            (SELECT COALESCE(MAX(guess_num), 0) + 1 FROM guess WHERE user_id = {user_id}),
            CASE WHEN EXISTS (SELECT 1 FROM puzzle WHERE puzzle_id = {puzzle_id} AND song_id = '{song_id}') THEN 1 ELSE 0 END
        FROM dual
        '''
    execute(q)

def insert_song_artist(song_id,artist_id):
    '''
    inputs: song_id, artist_id
    adds a song/artist relation  
    '''
    q = "INSERT INTO song_artist VALUES ('" + song_id + "', '" + artist_id + "')"
    execute(q)

def insert_song_album(song_id,album_id):
    '''
    inputs: song_id, album_id
    adds a song/album relation  
    '''
    q = "INSERT INTO song_album VALUES ('" + song_id + "', '" + album_id + "')"
    execute(q)

def insert_artist_genre(artist_id,genre_id):
    '''
    inputs: artist_id, genre_id (genre_id = INT)
    adds a artist/genre relation  
    '''
    genre_id=str(genre_id)
    q = "INSERT INTO artist_genre VALUES ('" + artist_id + "', " + genre_id + ")"
    execute(q)

def insert_genre(genre_name):
    '''
    input: new genre name
    inserts new genre, genre id is automatically generated
    '''
    q = f"INSERT INTO genre (genre_id, genre_name) SELECT COALESCE(MAX(genre_id), -1) + 1, '{genre_name}' FROM genre"
    execute(q)


# BASIC QUERIES=========================================================================================================
def get_id_from_song(song_name):
    ''' search for song id using song name
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
    return [res[0][0]]

def get_song_name_from_id(song_id):
    ''' get song name using existing song id
        returns: song name string
    '''
    q = "select song_name from song where song_id = '{}'".format(song_id) 
    print(q)
    res = execute(q)
    return res[0][0]

def get_song_info_from_id(song_id):
    ''' get song characteristics using song id
        returns: array of song characteristics
    '''
    q = "select song_name,danceability,energy,loudness,song_mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo from song where song_id like '{}'".format(song_id) 
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
    ''' get genre name from genre id (genre id = NUMBER)
        returns: genre name
    '''
    q = "select genre_name from genre where genre_id={}".format(str(genre_id))
    res = execute(q)
    if res is not None:
        return res[0][0]
    return None

def get_user_id(username,password):
    ''' supporting method to return just user id
        returns: user id
    '''
    q = "select puzzle_id from usr where username='{}' and password='{}'".format(username,password)
    res = execute(q)
    puzzle_id = res[0][0]
    return puzzle_id

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
    q = "select song_id from song_artist where artist_id='{}'".format(artist_id)
    res = execute(q)
    if res:
        song_id = res[0][0]
    return song_id

def get_song_from_album(album_id):
    '''returns: song id associated with album id'''
    song_id = None
    q = "select song_id from song_album where album_id='{}'".format(album_id)
    res = execute(q)
    if res:
        song_id = res[0][0]
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
        if isinstance(target_genre_ids[a_id], int):
            g_id = target_genre_ids[a_id]
            g_name = target_genres[g_id]
            curr_genres[g_id] = g_name
            curr_artist['genres'] = curr_genres
            song_stats['artists'].append(curr_artist)
        else:
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
    return song_stats

def get_song_stats(target_song_id):
    '''get all information regarding a song, starting with song id
       build the dict as you execute the queries
       input: target song id for which you want the stats
       returns: the song's information
    '''
    # get song id from song name
    target_song_name = get_song_name_from_id(target_song_id)
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
        # target_genre_ids[curr_artist] = []
        curr_genres = get_genre_from_artist(curr_artist)
        target_genre_ids[curr_artist] = curr_genres
    target_genres = {}
    if len(target_genre_ids) > 0:
        for _,ids in target_genre_ids.items():
            if isinstance(ids, int):
                genre = get_genre_from_id(ids)
                target_genres[ids] = genre
            else:
                for g_id in ids:
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
        returns: new user id (if success) or False (something went wrong)
    '''
    # create a new user
    q = "INSERT INTO usr (user_id, username, password) SELECT COALESCE(MAX(user_id), -1) + 1, '{}', '{}' FROM usr".format(username, password)
    execute(q)
    # check that you can login as the user (it exists/was created successfully)
    check_insert = login(username, password)
    if check_insert:
        # return user_id of new user
        return check_insert
    # return False
    print("ERROR: Something went wrong when creating account for {}.".format(username))
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
                LEFT JOIN guess g ON p.user_id = g.user_id 
                    AND p.puzzle_id = g.puzzle_id
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
        returns: lict of lists formatted as [user_id, streak, rank]
    '''
    players = []
    q = f"""SELECT *
            FROM (
                SELECT user_id,
                    MAX(streak_length) AS streak,
                    RANK() OVER (ORDER BY MAX(streak_length) DESC) AS rank
                FROM (
                    SELECT user_id, SUM(streak) AS streak_length
                    FROM (
                        SELECT user_id,
                            CASE WHEN puzzle_date = LAG(puzzle_date, 1) OVER (PARTITION BY user_id ORDER BY puzzle_date)
                                    THEN 0
                                    ELSE 1
                                END AS streak
                        FROM (
                            SELECT g.user_id, p.puzzle_date
                            FROM guess g
                            JOIN puzzle p ON g.puzzle_id = p.puzzle_id
                            WHERE g.user_id IS NOT NULL
                            AND g.user_id != 0
                            ORDER BY g.user_id, p.puzzle_date DESC
                        )
                    ) GROUP BY user_id
                ) GROUP BY user_id
            )
            WHERE (rank <= 10 OR user_id = {user_id}) AND ROWNUM <= 11
            ORDER BY streak DESC
        """
    res = execute(q)
    for r in res:
        players.append([r[0],r[1],r[2]])
    return players

def get_top_10_by_solves(user_id):
    ''' get top 10 players by minimum number of rounds needed to solve puzzles (including inputted user)
        returns: dictionary of {user id: number of rounds}
    '''
    players = {}
    q = f"""
        SELECT user_id, guess_num
        FROM (
            SELECT user_id, guess_num,
                RANK() OVER (ORDER BY guess_num ASC) AS rank
            FROM guess
            WHERE is_correct = 1
        )
        WHERE (rank <= 10 OR user_id = {user_id}) AND ROWNUM <= 11
        ORDER BY guess_num
        """
    res = execute(q)
    for r in res:
        p_id = r[0]
        num_rounds = r[1]
        players[p_id] = num_rounds
    return players
   
def get_top_10_by_avg_rounds(user_id):
    ''' get top 10 players by lowerst average rounds needed to solve puzzles 
        (including inputted user)
        returns: dictionary of {player id: average rounds}
    '''
    q = f"""
        SELECT user_id, average_rounds
        FROM (
            SELECT user_id, AVG(guess_num) AS average_rounds, RANK() OVER (ORDER BY AVG(guess_num) ASC) AS rank
            FROM (
                SELECT g.user_id, g.guess_num
                FROM puzzle p
                JOIN guess g ON p.puzzle_id = g.puzzle_id
                WHERE g.is_correct = 1
            ) sub
            GROUP BY user_id
            ORDER BY average_rounds
        ) top_players
        WHERE rank <= 10
        UNION ALL
        SELECT {user_id} AS user_id, AVG(guess_num) AS average_rounds
        FROM (
            SELECT g.user_id, g.guess_num
            FROM puzzle p
            JOIN guess g ON p.puzzle_id = g.puzzle_id
            WHERE g.is_correct = 1
        ) sub_inputted_user
        WHERE user_id = {user_id}
    """
    players = {}
    res = execute(q)
    for r in res:
        players[r[0]] = r[1]
    return players

def get_overall_total_solved():
    ''' get total unique games solved by all players
        (count number of unique game id's for which there is a is_correct=1)
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
    except Exception as err:
        print(f"ERROR: {err}")
        return None

def get_avg_solved_game_len():
    ''' get average game solve length by all players
        returns: number 
    '''
    average = 0
    q = """
        SELECT AVG(solved_game_len) AS avg_length
        FROM (
            SELECT AVG(g.guess_num) AS solved_game_len
            FROM guess g
            WHERE g.is_correct = 1
            GROUP BY g.puzzle_id
        ) solved_games
        """
    res = execute(q)
    average = res[0][0]
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
    q = "SELECT COUNT(DISTINCT puzzle_id) FROM puzzle"
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
