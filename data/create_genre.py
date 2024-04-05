import pandas as pd
import ast
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import requests
from requests.exceptions import ReadTimeout

# initialize spotipy with credentials
client_credentials_manager = SpotifyClientCredentials(client_id='ea510748c3294667abf66e27cc3a117d', \
                                                      client_secret='332a40248c564cc5ad4d6c0160a62aff')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# TODO: REMOVE SECRET KEY BEFORE PUSHING TO GITHUB


timed_out = []
# query API for genre
def get_artist_genre(artist_name, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            # Query Spotify API to get artist info
            results = sp.search(q='artist:' + artist_name, type='artist')

            # Extract genre information
            if 'artists' in results and 'items' in results['artists'] and results['artists']['items']:
                genres = results['artists']['items'][0]['genres']
                return genres
            else:
                return None
        except ReadTimeout:
            retries += 1
            timed_out.append(artist_name)
    return None
    

df = pd.read_csv('songs.csv')

# convert string to list
df['artists'] = df['artists'].apply(lambda x: ast.literal_eval(x))

# expand artist arrays
df = df.explode('artists')

# convert type of artist back to string!
df['artists'] = df['artists'].astype(str)
df = df.rename(columns={'artists': 'artist'})

# create new df!
artist_genre_df = pd.DataFrame(columns=['artist', 'genre'])

# NOW, must get genre id for each artist 
# query the spotify api for each artist's genre in the df
for a in df['artist'].unique():
    genres = get_artist_genre(a)
    print(f"got {genres} for {a}")
    # if genre info available, append artist-genre pairs to df
    if genres:
        for genre in genres:
            artist_genre_df = pd.concat([artist_genre_df, \
                                         pd.DataFrame({'artist': [a], \
                                                       'genre': [genre]})])


# save modified DataFrame back to CSV file
artist_genre_df.to_csv('genres.csv', index=False)