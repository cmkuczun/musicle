import cx_Oracle
import requests

# CONNECT TO ORACLE DB====================================================================================================
connection = cx_Oracle.connect("guest", "guest", "localhost:1521/xe")
# create cursor
cursor = connection.cursor()

# API KEY FOR LAST.FM=========================================================================================================
api_key = 'YOUR_API_KEY'


# EXECUTE QUERIES=========================================================================================================
def execute(q):
    try:
        cursor.execute(q)
        connection.commit()
        print("SUCCESS: query executed successfully")

        # fetch results
        for row in cursor:
            print(row)
    except Exception as e:
        print("ERROR: ", e)
        connection.rollback()


# INSERT QUERIES=========================================================================================================
# build query strings to insert into a table
def insert_song(args):
    '''
    song_id int primary key,
    title varchar(200),
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
    song_id,title,danceability,energy,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo = args
    q = 'INSERT INTO song VALUES (' + song_id + ', ' + title + ', ' + danceability + ', ' + energy + ', ' + loudness + ', ' + mode + ', ' + speechiness + ', ' + acousticness + ', ' + instrumentalness + ', ' + liveness + ', ' + valence + ', ' + tempo + ');'
    return q


def insert_custom_puzzle(args):
    '''
    cp_id int primary key auto_increment,
    user_id int,
    song_id int
    '''
    cp_id,user_id,song_id=args
    q = 'INSERT INTO custom_puzzle VALUES (' + cp_id + ', ' + user_id + ', ' + song_id + ');'
    return q


def insert_daily_puzzle(args):
    '''
    dp_id int primary key auto_increment,
    song_id int,
    dp_date date
    '''  
    dp_id,song_id,dp_date = args
    q = 'INSERT INTO daily_puzzle VALUES (' + dp_id + ', ' + song_id + ', ' + dp_date + ');'
    return q


def insert_guess(args):
    '''
    guess_id int primary key auto_increment,
    puzzle_id int,
    user_id int,
    song_id int,
    is_correct boolean,
    '''
    guess_id,puzzle_id,user_id,song_id,is_correct = args
    q = 'INSERT INTO daily_guess VALUES (' + guess_id + ', ' + puzzle_id + ', ' + user_id + ', ' + song_id + ', ' + is_correct + ');'
    return q


def insert_song_artist(args):
    '''
    song_id int,
    artist_id int    '''
    song_id,artist_id = args
    q = 'INSERT INTO song_artist VALUES (' + song_id + ', ' + artist_id + ');'
    return q


def insert_song_album(args):
    '''
    song_id int,
    album_id int
    '''
    song_id,album_id = args
    q = 'INSERT INTO song_album VALUES (' + song_id + ', ' + album_id + ');'
    return q


def insert_artist_genre(args):
    '''
    genre_id int,
    artist_id int
    '''
    genre_id,artist_id = args
    q = 'INSERT INTO artist_genre VALUES (' + genre_id + ', ' + artist_id + ');'
    return q


def insert_genre(args):
    '''
    genre_id int primary key auto_increment,
    genre varchar(100)
    '''
    genre_id,genre = args
    q = 'INSERT INTO genre VALUES (' + genre_id + ', ' + genre + ');'
    return q


def insert_user(args):
    '''
    user_id int primary key auto_increment,
    username varchar(50),
    password varchar(100)
    '''
    user_id,username,password = args
    q = 'INSERT INTO user VALUES (' + user_id + ', ' + username + ', ' + password + ');'
    return q


def insert_album(args):
    '''
    album_id int primary key,
    album_name varchar(100),
    release_date date
    '''
    album_id,album_name,release_date = args

    # parse date
    release_date = 'TO_DATE(' + release_date + ', "YYYY-MM-DD")'
    q = 'INSERT INTO album VALUES (' + album_id + ', ' + album_name + ', ' + release_date + ');'
    return q


def insert_artist(args):
    '''
    artist_id int primary key,
    artist_name varchar(100)
    '''
    artist_id,artist_name = args
    q = 'INSERT INTO artist VALUES (' + artist_id + ', ' + artist_name + ');'
    return q


# SEARCH QUERIES=========================================================================================================
# build query strings to search for specific data

def search_song_using_id(song_id):
    # song_id is a string
    q = 'select * from song where song_id="' + song_id + '";' 
    return q

def search_artist_using_id(artist_id):
    # artist_id is a string
    q = 'select * from artist where artist_id="' + artist_id + '";' 
    return q

def search_genre_using_id(genre_id):
    # genre_id is a number
    q = 'select * from genre where genre_id=' + genre_id + ';' 
    return q

def search_album_using_id(album_id):
    # album_id is a string
    q = 'select * from album where album_id="' + album_id + '";' 
    return q

def search_user_using_id(user_id):
    # user_id is a number
    q = 'select * from user where user_id=' + user_id + ';' 
    return q

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

