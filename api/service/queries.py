import cx_Oracle
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

def db_connect():
    try: 
        dsn_tns=cx_Oracle.makedsn('localhost','1521','xe')
        connection = cx_Oracle.connect("guest", "guest", dsn_tns)
        #print("\nSTATUS: Connected to Oracle database.")
    except Exception as e:
        print(print("\nSTATUS: Failed to connect to Oracle database."))
        print("ERROR: ", e)
    try: 
        cursor = connection.cursor()
        #print("\nSTATUS: Cursor created.\n")
        return cursor, connection
    except Exception as e:
        print("\nSTATUS: Failed to create cursor.")
        print("ERROR: ", e)
    return None, None


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


def execute_query(connection, query, parameters=None):
    try:
        cursor = connection.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        connection.commit()
        result = cursor.fetchall()
        return result
    except cx_Oracle.Error as error:
        print("ERROR:", error)
        connection.rollback()
        return None
    finally:
        if cursor:
            cursor.close()


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
    song_id=str(song_id)
    song_name=str(song_name)

    q = "INSERT INTO song VALUES ('" + song_id + "', '" + song_name + "', " + danceability + ", " + energy + ", " + loudness + ", " + mode + ", " + speechiness + ", " + acousticness + ", " + instrumentalness + ", " + liveness + ", " + valence + ", " + tempo + ")"
    execute_query(connection,q)

def insert_album(album_id,album_name,release_date):
    '''
    inputs: album_id, album_name, release_date (YYYY-MM-DD format)
    inserts a new album entry
    '''
    album_id=str(album_id)
    album_name=str(album_name)
    release_date=str(release_date)
    release_date = "TO_DATE('" + release_date + "', 'YYYY-MM-DD')"

    q = "INSERT INTO album VALUES ('" + album_id + "', '" + album_name + "', " + release_date + ")"
    execute_query(connection,q)

def insert_artist(artist_id,artist_name):
    '''
    inputs: artist_id, artist_name
    inserts new artist
    '''
    artist_id=str(artist_id)
    artist_name=str(artist_name)
    q = "INSERT INTO artist VALUES ('" + artist_id + "', '" + artist_name + "')"
    execute_query(connection,q)

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
    execute_query(connection,q1)
    
    # get new puzzle id
    q2 = '''SELECT puzzle_id FROM puzzle WHERE puzzle_id = (SELECT COALESCE(MAX(puzzle_id), -1) FROM puzzle)'''
    puzzle_id = execute_query(connection,q2)[0][0]

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
    execute_query(connection,q)

def insert_song_artist(song_id,artist_id):
    '''
    inputs: song_id, artist_id
    adds a song/artist relation  
    '''
    song_id=str(song_id)
    artist_id=str(artist_id)
    q = "INSERT INTO song_artist VALUES ('" + song_id + "', '" + artist_id + "')"
    execute_query(connection,q)

def insert_song_album(song_id,album_id):
    '''
    inputs: song_id, album_id
    adds a song/album relation  
    '''
    q = "INSERT INTO song_album VALUES ('" + song_id + "', '" + album_id + "')"
    execute_query(connection,q)

def insert_artist_genre(artist_id,genre_id):
    '''
    inputs: artist_id, genre_id (genre_id = INT)
    adds a artist/genre relation  
    '''
    genre_id=str(genre_id)
    q = "INSERT INTO artist_genre VALUES ('" + artist_id + "', " + genre_id + ")"
    execute_query(connection,q)

def insert_genre(genre_name):
    '''
    input: new genre name
    inserts new genre, genre id is automatically generated
    returns: newly created genre id
    '''
    e = genre_name.replace("'", "''")
    q = f"INSERT INTO genre (genre_id, genre_name) SELECT COALESCE(MAX(genre_id), -1) + 1, '{e}' FROM genre"
    execute_query(connection,q)

    q = "select genre_id from genre where genre_id = (select coalesce(max(genre_id), -1) + 1) from genre"
    res = execute_query(connection,q)
    if res is not None and len(res) > 0:
        return res[0][0]

    else:
        return None


# BASIC QUERIES=========================================================================================================
def get_id_from_song(song_name):
    ''' search for song id using song name
        returns: song id
    '''
    q = "select song_id from song where song_name like '%{}%'".format(song_name) 
    res = execute_query(connection,q)
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
    res = execute_query(connection,q)
    if res is None or len(res) == 0:
        return []
    return res[0][0]

def get_song_info_from_id(song_id):
    ''' get song characteristics using song id
        returns: array of song characteristics
    '''
    q = "select song_name,danceability,energy,loudness,song_mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo from song where song_id like '{}'".format(song_id) 
    res = execute_query(connection,q)
    if res is None or len(res) == 0:
        return []
    return list(res[0])

def get_album_from_song(song_id):
    ''' get album id from song id
        returns: album id
    '''
    q = "select album_id from song_album where song_id='{}'".format(song_id)
    res = execute_query(connection,q)
    if res is None or len(res) == 0:
        return []
    return res[0][0]

def get_album_from_id(album_id):
    ''' get album info from album_id
        returns: array of [album name, release date]
    '''
    q = "select album_name,release_date from album where album_id='{}'".format(album_id)
    res = execute_query(connection,q)
    return list(res[0])

def get_artist_from_song(song_id):
    ''' get artist id from song id
        returns: artist_id
    '''
    q = "select artist_id from song_artist where song_id='{}'".format(song_id)
    res = execute_query(connection,q)
    # handle multiple artists
    print(res)
    if res is None or len(res) == 0:
        return []
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
    res = execute_query(connection,q)
    return res[0][0]

def get_genre_from_artist(artist_id):
    ''' get genre id from artist id
        returns: genre_id
    '''
    q = "select genre_id from artist_genre where artist_id='{}'".format(artist_id)
    res = execute_query(connection,q)
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
    res = execute_query(connection,q)
    if res is not None:
        return res[0][0]
    return None

def get_user_id(username,password):
    ''' supporting method to return just user id
        returns: user id
    '''
    q = "select puzzle_id from usr where username='{}' and password='{}'".format(username,password)
    res = execute_query(connection,q)
    puzzle_id = res[0][0]
    return puzzle_id

def get_album_id_from_album(album_str):
    '''returns: album ids for albums matching the input string'''
    output = []
    q = "select album_id from album where album_name like '%{}%'".format(album_str)
    res = execute_query(connection,q)
    for entry in res:
        output.append(entry[0])
    return output

def get_artist_id_from_artist(artist_str):
    '''returns: artist ids for artists matching the input string'''
    output = []
    q = "select artist_id from artist where artist_name like '%{}%'".format(artist_str)
    res = execute_query(connection,q)
    for entry in res:
        output.append(entry[0])
    return output

def get_song_from_artist(artist_id):
    '''returns: song id associated with artist id'''
    song_id = None
    q = "select song_id from song_artist where artist_id='{}'".format(artist_id)
    res = execute_query(connection,q)
    if res:
        song_id = res[0][0]
    return song_id

def get_song_from_album(album_id):
    '''returns: song id associated with album id'''
    song_id = None
    q = "select song_id from song_album where album_id='{}'".format(album_id)
    res = execute_query(connection,q)
    if res:
        song_id = res[0][0]
    return song_id

def get_id_from_genre(genre):
    '''
        input: genre name to search for
        returns: genre id if  genre exists
    '''
    genre=str(genre)
    escaped_g = genre.replace("'", "''")
    q = "select genre_id from genre where genre_name = '{}'".format(escaped_g)

def get_user_from_id(uid):
    uid=str(uid)
    q = f"select username from usr where user_id={uid}"
    res = execute_query(connection,q)
    return None if (res is None or len(res) == 0) else res[0][0]


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
    song_stats['danceability'] = target_song_info[1]
    song_stats['energy'] = target_song_info[2]
    song_stats['loudness'] = target_song_info[3]
    song_stats['song_mode'] = target_song_info[4]
    song_stats['speechiness'] = target_song_info[5]
    song_stats['acousticness'] = target_song_info[6]
    song_stats['instrumentalness'] = target_song_info[7]
    song_stats['liveness'] = target_song_info[8]
    song_stats['valence'] = target_song_info[9]
    song_stats['tempo'] = target_song_info[10]
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
    if not target_album_id:
        target_album_id = []
    # get album name
    target_album_info = get_album_from_id(target_album_id)
    # get artist id
    target_artist_ids = get_artist_from_song(target_song_id)
    if not target_artist_ids:
        target_artist_ids = []
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
    execute_query(connection,q)
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
    res = execute_query(connection, q)
    print(res)
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
    res = execute_query(connection, q)
    if not res or len(res) == 0: 
        return 0
    return res[0][0]

def get_user_best_streak(user_id):
    '''get user's best daily streak'''
    streak = 0
    q = f"""
        SELECT MAX(streak) AS streak
        FROM (
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
            GROUP BY grp
        )
    """
    res = execute_query(connection, q)
    if not res or len(res) == 0:
        return 0
    return res[0][0]

def get_top_10_by_streak():
    ''' get top 10 players by daily streaks
        include the inputted user_id in top 10 or as an additional output
        returns: list of lists formatted as [user_id, streak, rank]
    '''
    q = f"""
        WITH streaks AS (
    SELECT
        guess.user_id,
        usr.username,
        ROW_NUMBER() OVER (PARTITION BY guess.user_id ORDER BY puzzle.puzzle_date) -
        ROW_NUMBER() OVER (PARTITION BY guess.user_id, guess.is_correct ORDER BY puzzle.puzzle_date) AS streak_group
    FROM
        guess
    INNER JOIN
        puzzle ON guess.puzzle_id = puzzle.puzzle_id
    INNER JOIN
        usr ON guess.user_id = usr.user_id
    ORDER BY
        puzzle.puzzle_date
    )
    SELECT
    RANK() OVER (ORDER BY COUNT(DISTINCT streak_group) DESC) AS rank,
    user_id,
    username,
    COUNT(DISTINCT streak_group) AS current_streak
    FROM
    streaks
	where rownum <= 10
    GROUP BY
    user_id, username
    HAVING
    COUNT(DISTINCT streak_group) > 0
        """
    res = execute_query(connection, q)
    if res == None or len(res) == 0:
        return []
    return list(res)

def get_top_10_by_solves(): # TODO
    ''' get top 10 players by minimum number of rounds needed to solve puzzles (including inputted user)
        returns: dictionary of {user id: number of rounds}
    '''
    q = f"""
        WITH puzzle_counts AS (
    SELECT
        usr.user_id,
        usr.username,
        COUNT(DISTINCT puzzle_id) AS num_puzzles_solved
    FROM
        guess
    INNER JOIN
        usr ON guess.user_id = usr.user_id
    WHERE
        is_correct = 1
    GROUP BY
        usr.user_id, usr.username
)
SELECT
    RANK() OVER (ORDER BY num_puzzles_solved DESC) AS rank,
    user_id,
    username,
    num_puzzles_solved
FROM
    puzzle_counts
WHERE
    ROWNUM <= 10
        """
    res = execute_query(connection, q)
    if res == None or len(res) == 0:
        return []
    return list(res)
   
def get_top_10_by_avg_rounds():
    ''' get top 10 players by lowest average rounds needed to solve puzzles 
        (including inputted user)
        returns: dictionary of {player id: average rounds}
    '''
    q = f"""
        WITH avg_guesses AS (
    SELECT
        guess.user_id,
        usr.username,
        AVG(CASE WHEN guess.is_correct = 1 THEN guess.guess_num END) AS avg_rounds
    FROM
        guess
    INNER JOIN
        usr ON guess.user_id = usr.user_id
    GROUP BY
        guess.user_id, usr.username
    ORDER BY
        avg_rounds ASC
    )
    SELECT
    ROWNUM AS rank,
    user_id,
    username,
    avg_rounds
    FROM
    avg_guesses
    WHERE
    ROWNUM <= 10
    """
    players = []
    res = execute_query(connection, q)
    if res == None or len(res) == 0:
        return []
    return list(res)

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
    res = execute_query(connection, q)
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
    res = execute_query(connection, q)
    return (res[0][0] if res is not None and len(res) > 0 else None)

def get_all_games_played():
    '''get all unique puzzle ids'''
    q = "SELECT COUNT(DISTINCT puzzle_id) FROM puzzle"
    res = execute_query(connection, q)
    return (res[0][0] if res is not None else None)

def get_songs_from_input(input_str):
    ''' get albums that match input, then match album ids with songs
        get artists that match input, then match these artists' ids with songs
        also get song names that match input string
        returns: set of song stats dictionaries containing the matching albums
    ''' 
    output = []
    try:
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
    except Exception as e:
        print(f"ERROR: {e}")
        return None

def load_user_recent_games(user_id, page=0):
    '''
    inputs: target user id, which page you want
    NOTE - puzzle_date is datetime() object
    returns: recent game entries [puzzle_id,puzzle_date,guess_number,correctness] 
             from (page*page_size) to (page+1 * page_size) 
             OR empty list [] if no result
    '''
    page_size = 10
    start_idx = page*page_size # including this
    end_idx = (page+1)*page_size # until this (exclusive)
    q = """
       WITH user_puzzles AS (
            SELECT DISTINCT p.*, 
                ROW_NUMBER() OVER (ORDER BY p.puzzle_date DESC) AS row_num, 
                g.guess_num,
                g.is_correct
            FROM puzzle p
            JOIN guess g ON p.puzzle_id = g.puzzle_id
            WHERE g.user_id = {}
        )
        SELECT 
            puzzle_id as pid,
            puzzle_date pdate,
            CASE WHEN MAX(CASE WHEN is_correct = 1 THEN guess_num END) IS NOT NULL 
                THEN MAX(CASE WHEN is_correct = 1 THEN guess_num END) 
                ELSE MAX(guess_num) KEEP (DENSE_RANK LAST ORDER BY CASE WHEN is_correct = 1 THEN 1 ELSE 0 END, row_num) 
            END AS guesses,
            MAX(is_correct) AS correct
        FROM user_puzzles
        WHERE (row_num BETWEEN {} AND {}) 
        GROUP BY puzzle_id, puzzle_date
        """.format(user_id,start_idx,end_idx)
    print(q)
    res = execute_query(connection,q)
    if len(res) == 0: return []
    formatted_res = []
    for r in res:
        temp_r = list(r)
        formatted_date = r[1].strftime('%Y.%m.%d')
        temp_r[1] = formatted_date
        formatted_res.append(temp_r)
    return formatted_res

def get_profile_stats(user_id): # TODO
    stats = {}
    # num games solved
    # current streak
    # best streak
    # avg guesses to solve (all time)
    return stats

def most_freq_guessed_song():
    '''
    get the most frequently guessed song
    returns: song name of most frequently guessed song
    '''
    q = """
        SELECT song_id, guess_count
        FROM (
            SELECT song_id, COUNT(*) AS guess_count
            FROM guess g
            GROUP BY song_id
            ORDER BY guess_count DESC
        )
        WHERE ROWNUM = 1
        """
    res = execute_query(connection, q)
    if not res or len(res) < 0:
        return None
    song_id = res[0][0]
    guess_cnt = res[0][1]
    song = get_song_name_from_id(song_id)
    artist_id = get_artist_from_song(song_id)
    artist_id = artist_id[0]
    artist = get_artist_from_id(artist_id)
    
    return [song, artist, guess_cnt]

def most_freq_guessed_artist():
    '''
    returns: artist name for most frequently guessed artist and how many times they were guessed
    '''
    q = """
        SELECT artist_name, guess_count
        FROM (
            SELECT a.artist_name, COUNT(*) AS guess_count
            FROM guess g, song_artist sa, artist a
            WHERE g.song_id = sa.song_id AND a.artist_id = sa.artist_id
            GROUP BY artist_name
            ORDER BY guess_count DESC
        )
        WHERE ROWNUM = 1
        """
    res = execute_query(connection, q)
    return None if not (res and len(res)) else res[0]

'''
def get_puzzle_config(user_id,puzzle_id):
	inputs: user id and puzzle id
	gets the current status of the puzzle game
	return: the config (the details of the puzzle and the current state of the game in one JSON object
    q=""
    res = execute(q)
    if not (res and len(res)): return None
    output = build_config(res) # TODO this is not built yet tbh
    return output
'''


def custom_setup(min_yr=1928, max_yr=2024, genres=[]):
    '''
	inputs: minimum and maximum years for querying, and genre subset to pull from
	- if no range is given, use all years
	- if no genres selected, use all genres
	returns: a random song (its stats) in the list of possible songs
    '''
    # format min/max years
    min_dt = f"TO_DATE('{min_yr}-01-01', 'YYYY-MM-DD')"
    max_dt = f"TO_DATE('{max_yr}-12-31', 'YYYY-MM-DD')"
    # select random song_id from list!
    # no genres to filter by
    if len(genres) == 0:
        q = f'''
            SELECT *
                FROM (
                    SELECT s.song_id
                    FROM song s
                	JOIN song_album sal ON s.song_id = sal.song_id
                    JOIN album al ON al.album_id = sal.album_id
                    JOIN song_artist sar ON s.song_id = sar.song_id
                    JOIN artist ar ON sar.artist_id = ar.artist_id
                    LEFT JOIN puzzle p ON s.song_id = p.song_id
                WHERE al.release_date >= {min_dt} AND al.release_date <= {max_dt}
                AND p.song_id IS NULL
                ORDER BY DBMS_RANDOM.VALUE
                )
            WHERE ROWNUM = 1
        '''
    # must filter by genres and build genre string
    else:
        str_g = [str(g) for g in genres]
        q = f'''
            SELECT * FROM (
                SELECT s.song_id
                FROM song s
                	JOIN song_album sal ON s.song_id = sal.song_id
                    JOIN album al ON al.album_id = sal.album_id
                    JOIN song_artist sar ON s.song_id = sar.song_id
                    JOIN artist ar ON sar.artist_id = ar.artist_id
                    JOIN artist_genre ag ON ar.artist_id = ag.artist_id
                    JOIN genre g ON ag.genre_id = g.genre_id
                    LEFT JOIN puzzle p ON s.song_id = p.song_id
                WHERE al.release_date >= {min_dt} AND al.release_date <= {max_dt}
          	    AND g.genre_name IN (
            '''
        for g in str_g:
            q += f"'{g}',"
        q_mod = q[:-1]
        q_mod +=") AND p.song_id IS NULL ORDER BY DBMS_RANDOM.VALUE) WHERE ROWNUM = 1"
        q = q_mod

    # get list of valid songs
    valid_songs = []
    sid = execute_query(connection,q)
    if not (sid and len(sid)):
        return None
    sid = sid[0][0]
	# return this song’s stats
    song_stats = get_song_stats(sid)
    return song_stats

def get_random_song_id():
    '''returns: random song id that has not yet been used for a puzzle''' 
    q="""	
		SELECT *
		FROM (
    		SELECT s.song_id
    		FROM song s
    		LEFT JOIN puzzle p ON s.song_id = p.song_id
    		AND p.song_id IS NULL
    		ORDER BY DBMS_RANDOM.VALUE
		) WHERE ROWNUM = 1
	""" 
    res = execute_query(connection, q)
    if not (res and len(res)):
        return None
    return res[0][0]

def top_solvers():
    '''
    input: user id logged in
    gets the top 10 players who have solved the most puzzles, ordered by num of games solved
    returns: array of 10 or 11 usernames, and their guess count, and their place (ROWNUM) -> [place,username,guess_count]
        NOTE - include the inputted user id and their results whether they are in top 10 or not
    '''
    q = f'''
            WITH top_solvers AS (
    SELECT
        usr.user_id,
        usr.username,
        COUNT(DISTINCT puzzle.puzzle_id) AS num_solved_puzzles
    FROM
        guess
    INNER JOIN
        puzzle ON guess.puzzle_id = puzzle.puzzle_id
    INNER JOIN
        usr ON guess.user_id = usr.user_id
    WHERE
        guess.is_correct = 1
    GROUP BY
        usr.user_id, usr.username
    ORDER BY
        num_solved_puzzles DESC
    )
    SELECT
    ROWNUM AS rank,
    user_id,
    username,
    num_solved_puzzles
    FROM
    top_solvers
    WHERE
    ROWNUM <= 10
        '''
    res = execute_query(connection,q)
    if res is None or len(res) == 0:
        return []
    return res

def top_guessers():
    '''
    input: user id logged in
    gets top 10 players who have lowest average num guesses to solve game (add total num of guesses, div by total num guesses in solved games
    returns: array of 10 or 11 usernames, guess counts, and ROWNUMS
    - include inputted user id and their results always
    '''
    q=f'''
        WITH avg_guesses AS (
    SELECT
        guess.user_id,
        usr.username,
        COUNT(guess.guess_id) AS total_guesses,
        COUNT(DISTINCT puzzle.puzzle_id) AS total_solved_games
    FROM
        guess
    INNER JOIN
        puzzle ON guess.puzzle_id = puzzle.puzzle_id
    INNER JOIN
        usr ON guess.user_id = usr.user_id
    WHERE
        guess.is_correct = 1
    GROUP BY
        guess.user_id, usr.username
    )
    SELECT
    ROWNUM AS rank,
    user_id,
    username,
    total_guesses / total_solved_games AS avg_guesses
    FROM
    avg_guesses
    WHERE
    ROWNUM <= 10
    ORDER BY
    avg_guesses ASC
        '''
    res = execute_query(connection,q)
    if res is None or len(res) == 0:
        return []
    return res

def avg_solve_cnt():
    '''
    total games solved / total guesses made on solved games
    returns: average number of games players need to solve puzzles
    '''
    q=f'''
    SELECT
        (SELECT COUNT(*)
        FROM puzzle p
        INNER JOIN guess g ON p.puzzle_id = g.puzzle_id
        WHERE g.is_correct = 1) AS total_solved,
        (SELECT SUM(guess_num)
        FROM guess
        WHERE is_correct = 1) AS total_guesses
    FROM DUAL
    '''
    res = execute_query(connection,q)
    if res is None or len(res) == 0:
        return None
    if res[0][0] is None or res[0][0] == 0:
        return 0
    if res[0][0] is None or res[0][1] == 0:
        return -1
    return res[0][1]/res[0][0]

def user_total_solved(user_id):
    '''returns total number of games solved by user'''
    q = f'''
        select count(*) from puzzle p, guess g 
        where p.puzzle_id = g.puzzle_id and g.user_id={user_id}
        and g.is_correct = 1
        '''
    res = execute_query(connection,q)
    if res is None or res[0][0] is None:
        return 0
    return res[0][0]


def user_avg_guesses(user_id):
    '''returns average number of guesses for user with id to solves games'''
    # get sum of all guesses for correct games
    q = f'''
        select sum(guess_num) 
        from guess g, puzzle p
        where g.puzzle_id = p.puzzle_id and g.is_correct = 1
            and g.user_id = {user_id}
        '''

    res = execute_query(connection,q)
    if res is None:
        return 0
    sum_guesses = res[0][0]
    if sum_guesses is None:
        sum_guesses = 0
    # print(f"Sum guesses: {sum_guesses}")
    all_games = user_total_solved(user_id)
    if all_games == 0:
        return 0
    return sum_guesses/all_games

def get_top_10_by_overall_streak():
    '''returns list of 10 or 11 rows of [rank, user_id, streak]'''
    q = f'''
        WITH streaks AS (
    SELECT
        usr.user_id,
        usr.username,
        ROW_NUMBER() OVER (PARTITION BY guess.user_id ORDER BY puzzle.puzzle_date) -
        ROW_NUMBER() OVER (PARTITION BY guess.user_id, guess.is_correct ORDER BY puzzle.puzzle_date) AS streak_group
    FROM
        guess
    INNER JOIN
        puzzle ON guess.puzzle_id = puzzle.puzzle_id
    INNER JOIN
        usr ON guess.user_id = usr.user_id
)
SELECT
    RANK() OVER (ORDER BY highest_overall_streak DESC) AS rank,
    user_id,
    username,
    highest_overall_streak
FROM (
    SELECT
        user_id,
        username,
        MAX(streak_length) AS highest_overall_streak
    FROM (
        SELECT
            user_id,
            username,
            COUNT(DISTINCT streak_group) AS streak_length
        FROM
            streaks
        GROUP BY
            user_id, username
        HAVING
            COUNT(DISTINCT streak_group) > 0
    )
    GROUP BY
        user_id, username
)
WHERE rownum <= 10
    ''' 
    res = execute_query(connection, q)

    if res is not None and len(res) == 0:
        return []
    return list(res)