import cx_Oracle
from .queries.oracle import execute
import logging
import pprint
from flask import session
import redis
from .cache import set_key, get_key
import time


def get_artists_from_song_id(song_id):
    query = f'''
        SELECT ar.artist_name, ar.artist_id
        FROM ARTIST ar
        JOIN SONG_ARTIST sa on ar.artist_id = sa.artist_id
        WHERE sa.song_id = '{song_id}'
    '''
    artist_list = execute(query)
    if not artist_list:
        return []
    artists = [{"name": s[0], "id": s[1], "genres": []} for s in execute(query)]

    for artist in artists:
        query = f'''
        SELECT g.genre_name
        FROM GENRE g
        JOIN ARTIST_GENRE ag on g.genre_id = ag.genre_id
        WHERE ag.artist_id = '{artist["id"]}'
        '''
        genres = execute(query)
        if genres:
            artist["genres"] = [g[0] for g in genres]
    return artists

def get_guess_list_service(data, page=0):

    # print("guess list service")
    ## COMPLEX QUERY FOR HINT MATCHING
    guess_list = []

    # make hints
    if "text" in data:
        filter_text = data["text"].lower()
    else:
        filter_text = ""

    # pprint.pprint(data)

    data = data['hints']
    hints = {
        "features" : {
            "danceability": data['danceability'],
            "energy": data['energy'],
            "speechiness": data['speechiness'],
            "acousticness": data['acousticness'],
            "instrumentalness": data['instrumentalness'],
            "liveness": data['liveness'],
            "valence": data['valence'],
            "tempo": data['tempo'],
            "mode": data['mode']
        },
        "album" : data['album'],
        "artists" : data['artists'],
        "releasedate" : data['releasedate'],
    }
    
    # print("***HINTS")
    # pprint.pprint(hints)
    # print("\n")

    query = '''
        select s.song_id, s.song_name, s.danceability, s.energy, s.loudness, s.song_mode, s.speechiness, s.acousticness, s.instrumentalness, s.liveness, s.valence, s.tempo, al.album_name, al.release_date, ar.artist_name
        from SONG s 
        JOIN SONG_ARTIST sa on s.song_id = sa.song_id
        JOIN ARTIST ar on sa.artist_id = ar.artist_id
        JOIN ARTIST_GENRE ag on ar.artist_id = ag.artist_id
        JOIN GENRE g on ag.genre_id = g.genre_id
        JOIN SONG_ALBUM sal on s.song_id = sal.song_id
        JOIN ALBUM al on sal.album_id = al.album_id'''
    
    first = True
    def add_where():
        nonlocal first
        if first:
            return "WHERE"
            first = False
        else:
            return "AND"

    if hints["features"]:
        for index, feature in enumerate(list(hints["features"].keys())):
            if hints["features"][feature]["known"] and feature != "mode":
                query += " {} s.{} BETWEEN {} * 0.95 AND {} * 1.05".format(add_where(), feature, hints["features"][feature]["value"], hints["features"][feature]["value"])
                first = False
            elif hints["features"][feature]["known"] and feature == "mode":
                query += " {} s.song_mode = {}".format(add_where(), hints['features']['mode']['value'])
                first = False
    if hints["album"]["known"]:
        query += " {} al.album_id = '{}'".format(add_where(), hints["album"]["value"])
        first = False
    if hints["releasedate"]["known"]:
        query += " {} EXTRACT(YEAR FROM al.release_date) = {} {} EXTRACT(MONTH FROM al.release_date) = {}".format(add_where(), hints["releasedate"]["value"].split("-")[2], add_where(), hints["releasedate"]["value"].split("-")[0])
        first = False
    if hints["artists"]:
        genre_list = []
        artist_list = []
        for artist in hints["artists"]:
            if artist["known"]:
                artist_list.append(artist["value"])
            else:
                if artist["genres"]:
                    for genre in artist["genres"]:
                        if genre["known"]:
                            genre_list.append(genre["value"])
        if artist_list:
            query += " {} ar.artist_id IN ('{}')".format(add_where(), "','".join(artist_list))
            first = False
        if genre_list:
            query += " {} LOWER(g.genre_name) IN ('{}')".format(add_where(), "','".join([g.lower() for g in genre_list]))
            first = False

    # add text filtering
    if filter_text != "":
        query += " {} (LOWER(s.song_name) LIKE '%{}%' OR LOWER(al.album_name) LIKE '%{}%' OR LOWER(ar.artist_name) LIKE '%{}%')".format(add_where(), filter_text, filter_text, filter_text)
        first = False
    query += " {} ROWNUM <= 25".format(add_where())

    print(query)

    # Get the first 25 distinct songs from the query
    outer_query = f"""
    with q as ({query})
    select * from q
    where song_id in (
        select distinct song_id
        from q
        where rownum <= 25
    )
    """

    # add a timestamp called start
    start = time.time()
    logging.debug(query)
    # res = execute(query)
    res = execute(outer_query)
    logging.debug(res)

    guess_list = [ {
        "song_id" : s[0],
        "song_name" : s[1],
        "danceability": s[2],
        "energy": s[3],
        "loudness": s[4],
        "mode": s[5],
        "speechiness": s[6],
        "acousticness": s[7],
        "instrumentalness": s[8],
        "liveness": s[9],
        "valence": s[10],
        "tempo": s[11],
        "song_album" : s[12],
        "song_date" : s[13].strftime("%B %Y"),
        "artists" : get_artists_from_song_id(s[0])
    } for s in res]

    unique_songs = {}

    for s in guess_list:
        song_name = s["song_name"]
        unique_songs[song_name] = {
            "song_id": s["song_id"],
            "song_name": s["song_name"],
            "danceability": s["danceability"],
            "energy": s["energy"],
            "loudness": s["loudness"],
            "mode": s["mode"],
            "speechiness": s["speechiness"],
            "acousticness": s["acousticness"],
            "instrumentalness": s["instrumentalness"],
            "liveness": s["liveness"],
            "valence": s["valence"],
            "tempo": s["tempo"],
            "song_album": s["song_album"],
            "song_date": s["song_date"],
            "artists": s["artists"]
        }

    guess_list = list(unique_songs.values())
    # print(guess_list)

    end = time.time()
    return guess_list if guess_list else []