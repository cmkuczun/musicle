import pandas as pd
import ast

# read all songs CSV file
df = pd.read_csv('og_songs.csv')

# convert string representation of list to actual list for 'artists' and 'artist_ids' cols
df['artists'] = df['artists'].apply(lambda x: ast.literal_eval(x))
df['artist_ids'] = df['artist_ids'].apply(lambda x: ast.literal_eval(x))

# initialize empty df to store exploded rows
exploded_rows = []

# explore df based on artists/artist_ids
for _, row in df.iterrows():
    artists = row['artists']
    artist_ids = row['artist_ids']
    # multiple IDs for one artist
    if len(artists) != len(artist_ids):
       # unmatching number of artists and artist IDs, create a row for each artist
        num_artists = min(len(artists), len(artist_ids))
        for i in range(num_artists):
            exploded_rows.append({
                'artist': artists[i],
                'artist_id': artist_ids[i]
            })
    else:
        # matching number of artists and artist IDs, create a row for each artist
        for artist, artist_id in zip(artists, artist_ids):
            exploded_rows.append({
                'artist': artist,
                'artist_id': artist_id
            })

# create df from exploded rows
exploded_df = pd.DataFrame(exploded_rows)

# save df to new CSV file
exploded_df.to_csv('artists.csv', index=False)