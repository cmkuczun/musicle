import pandas as pd

# read CSV file
df = pd.read_csv('csv/og_songs.csv')

# drop specified columns
columns_to_remove = ['album', 'album_id', 'artists', 'artist_ids', 'release_date']
df = df.drop(columns=columns_to_remove)

# save modified df back to a CSV file
df.to_csv('csv/songs.csv', index=False)