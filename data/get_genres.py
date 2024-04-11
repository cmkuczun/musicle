import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# load genres.txt file
genres = pd.read_csv('genres.txt', header=None)
# there are no columns
genres.columns = ['genre']
# for each row, split by first space and take second element
genres['genre'] = genres['genre'].apply(lambda x: x.split(' ')[1:])
#extract only the genre column
genres = genres['genre']

# combine each row into single string
genres = genres.str.join(' ')
# for each genre, make it lowercase
genres = genres.apply(lambda x: x.lower())
# write to genres.csv, creating new id column for each genre
genres.to_csv('genres.csv', index_label='id', header=True)
