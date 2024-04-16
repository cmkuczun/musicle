import pandas as pd

# ARTISTS: REMOVE DUPLICATES
# load csv
artists = pd.read_csv('csv/artists.csv')

# remove duplicates from artists
artists = artists.drop_duplicates(subset='artist_id')

# rewrite csv
artists.to_csv('csv/artists.csv', index=False)

# ALBUMS: ADD RELEASE_DATE COL TO END OF EACH ROW FROM OG_SONGS
# load csv
albums = pd.read_csv('csv/albums.csv')
og_songs = pd.read_csv('csv/og_songs.csv')

# add release_date column to albums
albums['release_date'] = og_songs['release_date']

# rewrite csv
albums.to_csv('csv/albums.csv', index=False)

# SONG_ALBUM: ENSURE THAT ALBUM_ID IS IN ALBUMS
# load csv
song_albums = pd.read_csv('csv/song_albums.csv')

# remove rows from song_albums that have no album_id in albums
song_albums = song_albums[song_albums['album_id'].isin(albums['album_id'])]

# rewrite csv
song_albums.to_csv('csv/song_albums.csv', index=False)

# SONG_ARTISTS: ENSURE THAT ARTIST_ID IS IN ARTISTS
# load csv
song_artists = pd.read_csv('csv/song_artists.csv')

# remove rows from song_artists that have no artist_id in artists
song_artists = song_artists[song_artists['artist_id'].isin(artists['artist_id'])]

# rewrite csv
song_artists.to_csv('csv/song_artists.csv', index=False)

print('modified: albums, song_algums, song_artist, artists')