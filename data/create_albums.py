import pandas as pd
import ast

# read all songs CSV file
df = pd.read_csv('og_songs.csv')

# get pairs of album and album id from 'album' and 'album_id' columns
albums_with_ids = df[['album_id', 'album']].drop_duplicates()

# save df to new CSV file
albums_with_ids.to_csv('albums.csv', index=False)