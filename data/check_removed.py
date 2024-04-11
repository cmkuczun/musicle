import pandas as pd

# load in og_songs.csv
og_songs = pd.read_csv('csv/og_songs.csv')

# load in songs.csv
songs = pd.read_csv('csv/songs.csv')

# count number of unique 'id' in og_songs
og_songs_unique = og_songs['id'].nunique()

# count number of unique 'id' in songs
songs_unique = songs['id'].nunique()

# subtract the two counts
diff = og_songs_unique - songs_unique
print(f'{diff} songs were removed from original dataset!!')