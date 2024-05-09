from .oracle import execute
from .current import get_id_from_genre
# import requests
# import time

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
    execute(q)

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
    execute(q)

def insert_artist(artist_id,artist_name):
    '''
    inputs: artist_id, artist_name
    inserts new artist
    '''
    artist_id=str(artist_id)
    artist_name=str(artist_name)
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

    puzzle_id = execute('''SELECT puzzle_id FROM puzzle WHERE puzzle_id = (SELECT COALESCE(MAX(puzzle_id), -1) FROM puzzle)''')[0][0] + 1
    print("query's song_id", song_id)
    
    # create the puzzle
    q = '''INSERT INTO puzzle (puzzle_id, song_id, user_id, puzzle_date) 
            SELECT COALESCE(MAX(puzzle_id), -1) + 1, '{}', {}, {} FROM puzzle
        '''.format(song_id, user_id, puzzle_date)
    execute(q)
    
    # get new puzzle id
    q = '''SELECT puzzle_id FROM puzzle WHERE puzzle_id = (SELECT COALESCE(MAX(puzzle_id), -1) FROM puzzle)'''
    puzzle_id = execute(q)[0][0]

    # return new id
    return puzzle_id

def insert_guess(puzzle_id,user_id,song_id):
    '''
    inputs: puzzle_id, user_id, song_id
    (guess_id, guess_num, and is_correct are automatically generated)
    '''
    if not user_id:
        return
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
    print(q)
    execute(q)

def insert_song_artist(song_id,artist_id):
    '''
    inputs: song_id, artist_id
    adds a song/artist relation  
    '''
    song_id=str(song_id)
    artist_id=str(artist_id)
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
    returns: newly created genre id
    '''
    e = genre_name.replace("'", "''")
    q = f"INSERT INTO genre (genre_id, genre_name) SELECT COALESCE(MAX(genre_id), -1) + 1, '{e}' FROM genre"
    execute(q)

    q = "select genre_id from genre where genre_id = (select coalesce(max(genre_id), -1) + 1) from genre"
    res = execute(q)

    if res is not None and len(res) > 0:
        return res[0][0]
    else:
        return None

def insert_song_entry(song_id,song_name,danceability,energy,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo,\
                      album_id,album_name,release_date,
                      artist_id,artist_name,
                      genre_name=''):
    '''inserts a song and all of the associated information'''
    try:
        insert_song(song_id,song_name,danceability,energy,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo)
        insert_artist(artist_id,artist_name)
        insert_album(album_id,album_name,release_date)

        # check if you need to add a new genre for the artist
        check_genre = get_id_from_genre(genre_name)
        if not check_genre:
            if genre_name != '':
                g_id = insert_genre(genre_name)
                # isnert A_G pairing with new genre id
                if g_id is not None:
                    insert_artist_genre(artist_id,g_id)
        else:
            insert_artist_genre(artist_id,check_genre)
        
        insert_song_album(song_id,album_id)
        insert_song_artist(song_id,artist_id)
        return True
    
    except Exception as e:
        print(f'ERROR: Something went wrong when adding new SONG info: {e}')
        return False



