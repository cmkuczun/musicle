import cx_Oracle
import requests

# ORACLE DB SETUP====================================================================================================
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


# API KEY FOR LAST.FM=========================================================================================================
api_key = 'YOUR_API_KEY'


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
        print(f"SUCCESS: Query executed successfully ({q}).\n")
        return res
    
    except Exception as e:
        print("ERROR: ", e)
        connection.rollback()
        return None


# INSERT QUERIES=========================================================================================================
# build query strings to insert into a table
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
    return q


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



# SEARCH QUERIES=========================================================================================================
# build query strings to search for specific data

def search_song_using_id(song_id):
    # song_id is a string
    q = 'select * from song where song_id="' + song_id + '"' 
    return q

def search_artist_using_id(artist_id):
    # artist_id is a string
    q = 'select * from artist where artist_id="' + artist_id + '"' 
    return q

def search_genre_using_id(genre_id):
    # genre_id is a number
    genre_id=str(genre_id)
    q = "select * from genre where genre_id=" + genre_id
    return q

def search_album_using_id(album_id):
    # album_id is a string
    q = 'select * from album where album_id="' + album_id + '";' 
    return q

def search_user_using_id(user_id):
    # user_id is a number
    q = 'select * from user where user_id=' + user_id + ';' 
    return q


def get_song_artist_id(song_id):
    '''get artist id(s) from song id'''
    artist_id_arr = []
    #TODO
    return artist_id_arr

def get_artist_genre_id(artist_id):
    '''get genre id(s) from artist id'''
    genre_id_arr = []
    #TODO
    return genre_id_arr

def get_song_album_id(song_id):
    '''get album id from song id'''
    album_id_arr = []
    #TODO
    return album_id_arr

def get_song_stats(song_name):
    '''get all information regarding a song, starting with song name'''


# API QUERY=========================================================================================================
# query API to get similar artists
def get_similar_artists(artist_name):
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




