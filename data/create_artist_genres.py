import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from spotify_secrets import CLIENT_ID, CLIENT_SECRET
from tqdm import tqdm
import csv


# Spotipy Client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_artists_genres(artist_ids):
    try:
        artists = sp.artists(artist_ids)
        genres = {}
        for artist in artists['artists'][:1]:
            genres[artist['id']] = artist['genres']
        return genres
    except spotipy.SpotifyException as _:
        return {}


def get_artist_ids(n=100):
    df = pd.read_csv('csv/artists.csv')
    artist_ids = list(set(df['artist_id'].tolist()))
    artist_ids.sort()
    artist_ids = [artist_ids[i:i + n] for i in range(0, len(artist_ids), n)] 
    return artist_ids


def get_genre_dict():
    df = pd.read_csv('csv/genres.csv')
    genre_dict = {}
    for _,row in df.iterrows():
        genre_dict[row['genre']] = row['id']
    return genre_dict


if __name__ == '__main__':
    n = 50
    artist_ids = get_artist_ids(n)
    print(f"Getting genres for {len(artist_ids)*n + len(artist_ids[-1])} artists...")

    genre_dict = get_genre_dict()
    def genres_to_ids(genres):
        return [genre_dict[genre] for genre in genres if genre in genre_dict]

    csv_file = "csv/artist_genres.csv"
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["artist_id", "genre_id"])
    
        for artist_ids_chunk in tqdm(artist_ids[:1]):
            g = get_artists_genres(artist_ids_chunk)
            for artist_id, genres in g.items():
                for genre_id in genres_to_ids(genres):
                    writer.writerow([artist_id, genre_id])
    
    print('Done!')