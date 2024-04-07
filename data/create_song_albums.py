import pandas as pd
import ast

# read all songs CSV file
df = pd.read_csv('og_songs.csv')

# get pairs of song id and album id
albums_with_ids = df[['id', 'album_id']].drop_duplicates()

# rename id to song_id
albums_with_ids.rename(columns={'id': 'song_id'}, inplace=True)

# save df to new CSV file
albums_with_ids.to_csv('song_albums.csv', index=False)