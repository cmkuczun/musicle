from .queries.oracle import execute
from .queries.inserts import insert_guess, insert_puzzle
from .queries.current import get_song_stats
from datetime import date
from .queries import *
import logging
import random


def get_config_from_puzzle_id_service(puzzle_id):
    ## build config json *** see model in fe *** from song_id of puzzle (json processing)
    ## this will also be useful for the load_empty_config function in the fe
    song_id = execute(f"SELECT song_id FROM PUZZLE WHERE puzzle_id = {puzzle_id}")[0][0]

    print("SONGID in config from puzzle:", song_id)
    if song_id:
        return get_blank_config_from_song_id_service(song_id)
    return {}

def get_blank_config_from_song_id_service(song_id):
    ## build initial BLANK config from DB using song_id to retrieve all information
    stats = get_song_stats(song_id)
    config = {}
    config['danceability'] = {'known': False, 'value': stats['danceability']}
    config['energy'] = {'known': False, 'value': stats['energy']}
    config['speechiness'] = {'known': False, 'value': stats['speechiness']}
    config['acousticness'] = {'known': False, 'value': stats['acousticness']}
    config['instrumentalness'] = {'known': False, 'value': stats['instrumentalness']}
    config['liveness'] = {'known': False, 'value': stats['liveness']}
    config['valence'] = {'known': False, 'value': stats['valence']}
    config['tempo'] = {'known': False, 'value': stats['tempo']}
    config['loudness'] = {'known': False, 'value': stats['loudness']}
    config['mode'] = {'known': False, 'value': stats['song_mode']}

    config['album'] = {'known': False, 'value': stats['album']['album_id'], 'name': stats['album']['album_name']}

    dt = stats['album']['release_date']
    dt = dt.strftime("%m-%d-%Y")
    config['releasedate'] = {'known': False, 'value': dt}

    config_artists = []
    for a in stats['artists']:
        desired_a = {
                        "known": False,
                        "value": a["artist_id"],
                        "name": a["artist_name"],
                        "genres": [] 
                    }
        for genre_id, genre_name in a["genres"].items():
            desired_a["genres"].append({"known": False, "value": genre_name})
        config_artists.append(desired_a)
    config['artists'] = config_artists

    config['title'] = {'known': False, 'value': stats['song name']}

    return config


def insert_guess_service(user_id, puzzle_id, song_id, guess_num, correct):
    ## insert the guess (dummmy easy)
    if user_id:
        print(user_id)
        insert_guess(puzzle_id, user_id, song_id)
    return True
    


def check_correct_service(song_id, puzzle_id):
    ## check if puzzle's song_id == guessed song_id
    query = f'''SELECT song_id FROM PUZZLE where puzzle_id = {puzzle_id}'''
    res = execute(query)[0]

    print("res in correct service", res)
    res = res[0]
    if res == song_id:
        return True
    return False

def set_known_to_true_utility(d):
    if isinstance(d, dict):  # Check if the item is a dictionary
        for key, value in d.items():
            if isinstance(value, dict):  # If the value is a dictionary, recurse into it
                set_known_to_true_utility(value)
            elif isinstance(value, list):  # If the value is a list, iterate through its elements
                for item in value:
                    set_known_to_true_utility(item)
            if 'known' in d:  # Check if 'known' is a key in the dictionary
                d['known'] = True  # Set 'known' to True
    return d

def diff_configs_service(current, answer, song_id):
    ## COMPLEX - need to loop through 3 configs to build one that has the correct updates
    '''
    iterate through three parallel dictionaries, current, answer, guess. 
    every item in the dictionaries has two attributes, known and value. 
    for any attribute, if known is False in current and value in guess == value in answer, update known to be True in result_dict. 
    if known is True in current, known is True in result_dict. otherwise, known is False'''
    logging.debug(current)
    guess = get_blank_config_from_song_id_service(song_id)
    result = {}

    # print("current", current)
    # print("answer", answer)
    # print("guess", guess)

    for k, v in current.items():
        if k == "artists":
            # get all genres guessed
            unique_genres = set()
            artistas = set()
            # Loop through each artist in the list
            for artist in guess[k]:
                for genre in artist["genres"]:
                    unique_genres.add(genre['value'])
                artistas.add(artist["name"])
            for artist in current[k]:
                for genre in artist["genres"]:
                    if genre['value'] in unique_genres:
                        genre['known'] = True
                if artist["name"] in artistas:
                    artist["known"] = True

        elif k == "releasedate":
            curdat = current[k]["value"].split("-")
            curmon, curyear = curdat[0], curdat[2]
            gdat = guess[k]["value"].split("-")
            gmon, gyear = gdat[0], gdat[2]
            if gmon == curmon and gyear == curyear:
                current[k]["known"] = True
        elif isinstance(current[k]["value"], str):
            if not current[k]["known"] and guess[k]["value"] == current[k]["value"]:
                current[k]["known"] = True
        else:
            if not current[k]["known"] and guess[k]["value"] < current[k]["value"] * 1.15 and guess[k]["value"] > current[k]["value"] * .85:
                current[k]["known"] = True
            if k == "loudness":
                print(current[k], guess[k])


    print("first method:", current)
    return current


def create_user_puzzle_service(start_date, end_date, genres, user_id):
    # get song id that matches the params
    genre_list = ', '.join(f"'{genre}'" for genre in genres)
    start_date = str(start_date) + '-01-01'
    end_date = str(end_date) +  '-12-31'
    print(start_date, end_date)

    # SQL to get a song ID that matches the parameters
    query = f"""
    
    SELECT DISTINCT s.song_id, g.genre_name, sar.artist_id
    FROM SONG s
    JOIN song_album sa ON s.song_id = sa.song_id
    JOIN album a ON a.album_id = sa.album_id
    JOIN song_artist sar ON s.song_id = sar.song_id
    JOIN artist_genre ag ON sar.artist_id = ag.artist_id
    JOIN genre g ON ag.genre_id = g.genre_id
    WHERE a.release_date BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
    AND g.genre_name IN ({genre_list})
    AND rownum <= 25
    
    """
    

    res = execute(query)

    print(res, query)

    if not res:
        print("No song matches the criteria.")
        return -1, {}

    song_list = res
    # select random value from song_list
    print(song_list)
    song_id_for_puzzle = random.choice(song_list)[0]

    #song_id_for_puzzle = res[0][0]
    print(f"Selected song ID for puzzle: {song_id_for_puzzle} for user {user_id} ")


    puzzle_id = insert_puzzle(song_id_for_puzzle, user_id, date.today().strftime("%Y-%m-%d"))

    print(puzzle_id)
    config = get_blank_config_from_song_id_service(song_id_for_puzzle)
    config = get_config_from_puzzle_id_service(puzzle_id)

    return puzzle_id, config


def get_puzzle_from_date_service(date):
    return get_todays_puzzle_service()
    
    ## NOTE (CHECK) Process date, error check if date does not [yet] have a puzzle
    ## returns: False if no puzzle exists yet, puzzle_id & song_id if it does exist
    q = f"SELECT puzzle_id, song_id FROM PUZZLE WHERE user_id IS NULL AND puzzle_date = TO_DATE('{date}', 'YYYY-MM-DD') AND ROWNUM <= 1"
    res = execute(q)
    print(q)
    if not res:
        return 0, {}
    puzzle_id = res[0][0]
    song_id = res[0][1]
    if puzzle_id is None and song_id is None: 
        return False
    return puzzle_id, get_blank_config_from_song_id_service(song_id)

def get_todays_puzzle_service():
    todays_date = date.today().strftime("%Y-%m-%d")
    q = f"SELECT puzzle_id, song_id FROM PUZZLE WHERE user_id IS NULL AND puzzle_date = TO_DATE('{todays_date}', 'YYYY-MM-DD') AND ROWNUM <= 1"
    res = execute(q)
    print(q)
    if not res:
        return 0, {}
    puzzle_id = res[0][0]
    song_id = res[0][1]
    if puzzle_id is None and song_id is None: 
        return False
    return puzzle_id, get_blank_config_from_song_id_service(song_id)

# cursor.execute("SELECT * FROM SONG")
# users = cursor.fetchmany(40)
# # convert users to json object
# users = [dict(zip([column[0] for column in cursor.description], row)) for row in users]
# print(users)

def get_recent_puzzles_service(user_id):
    res = load_user_recent_games(user_id)

    # print("res", res)
    return list(res)
