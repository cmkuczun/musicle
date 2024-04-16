import pandas as pd

# load artist_genres
artist_genres = pd.read_csv('csv/artist_genres.csv') # DONE

# load artists
artists = pd.read_csv('csv/artists.csv') # DONE

# if artist_genres artist_id not in artist_ids in artists, remove it
artist_ids = artists['artist_id'].values
print(len(artist_ids))
artist_genres = artist_genres[artist_genres['artist_id'].isin(artist_ids)]

print(len(artist_genres))

# save artist_genres
artist_genres.to_csv('csv/artist_genres.csv', index=False) # DONE