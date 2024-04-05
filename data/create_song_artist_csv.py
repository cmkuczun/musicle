import pandas as pd
import ast

# read in og csv file
df = pd.read_csv('og_songs.csv')

# convert string representation of list to actual list for 'artist_ids' col
df['artist_ids'] = df['artist_ids'].apply(lambda x: ast.literal_eval(x))

# init empty list to store rows
rows = []

# iterate through each row in the df
for _, row in df.iterrows():
    # Retrieve the song_id and associated artist_ids
    song_id = row['id']
    artist_ids = row['artist_ids']
    
    # Create a row for each artist_id and associate it with the song_id
    for artist_id in artist_ids:
        rows.append({
            'song_id': song_id,
            'artist_id': artist_id
        })

# create df
result_df = pd.DataFrame(rows)

# save df to as csv file
result_df.to_csv('song_artists.csv', index=False)
