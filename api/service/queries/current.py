from .oracle import execute
import logging


logger = logging.getLogger(__name__)

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
    res = execute(q)
    if res is None or len(res) == 0:
        return []
    return res[0][0]

def get_song_info_from_id(song_id):
    ''' get song characteristics using song id
        returns: array of song characteristics
    '''
    q = "select song_name,danceability,energy,loudness,song_mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo from song where song_id like '{}'".format(song_id) 
    res = execute(q)
    if res is None or len(res) == 0:
        return []
    return list(res[0])

def get_album_from_song(song_id):
    ''' get album id from song id
        returns: album id
    '''
    q = "select album_id from song_album where song_id='{}'".format(song_id)
    res = execute(q)
    if res is None or len(res) == 0:
        return []
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
    logger.debug(q)
    res = execute(q)
    logger.debug(res)
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
    print(q)
    res = execute(q)
    print(res)
    if res:
        song_id = res[0][0]
    return song_id

def get_id_from_genre(genre):
    '''
        input: genre name to search for
        returns: genre id if genre exists
    '''
    genre=str(genre)
    escaped_g = genre.replace("'", "''")
    q = "select genre_id from genre where genre_name = '{}'".format(escaped_g)
    res = execute(q)
    if res is not None and len(res) > 0:
        return res[0][0]
    else:
        return None

def get_user_from_id(uid):
    uid=str(uid)
    q = f"select username from usr where user_id={uid}"
    res = execute(q)
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
    res = execute(q)
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
    res = execute(q)
    if not res or len(res) == 0:
        return 0
    return res[0][0]

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
    res = execute(q)
    if len(res) == 0: return []
    formatted_res = []
    for r in res:
        temp_r = list(r)
        formatted_date = r[1].strftime('%Y.%m.%d')
        temp_r[1] = formatted_date
        formatted_res.append(temp_r)
    return formatted_res

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
    sid = execute(q)
    if not (sid and len(sid)):
        return None
    sid = sid[0][0]
	# return this song’s stats
    song_stats = get_song_stats(sid)
    return song_stats

# def get_random_song_id():
#     '''returns: random song id that has not yet been used for a puzzle''' 
#     q="""	
# 		SELECT *
# 		FROM (
#     		SELECT s.song_id
#     		FROM song s
#     		LEFT JOIN puzzle p ON s.song_id = p.song_id
#     		AND p.song_id IS NULL
#     		ORDER BY DBMS_RANDOM.VALUE
# 		) WHERE ROWNUM = 1
# 	""" 
#     res = execute(q)
#     if not (res and len(res)):
#         return None
#     return res[0][0]

def user_total_solved(user_id):
    '''returns total number of games solved by user'''
    q = f'''
        select count(*) from puzzle p, guess g 
        where p.puzzle_id = g.puzzle_id and g.user_id={user_id}
        and g.is_correct = 1
        '''
    res = execute(q)
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

    res = execute(q)
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
