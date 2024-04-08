import os
import csv
import pandas as pd


# load csv files
albums = pd.read_csv('csv/albums.csv') # DONE
artists = pd.read_csv('csv/artists.csv') # DONE
songs = pd.read_csv('csv/songs.csv') # DONE
song_artists = pd.read_csv('csv/song_artists.csv') # DONE
song_albums = pd.read_csv('csv/song_albums.csv') # DONE
artist_genres = pd.read_csv('csv/artist_genres.csv') # DONE
    
# find difference between set of artist_ids in artists and artist_ids in genres
artist_ids = set(artists['artist_id'].tolist())
genre_artist_ids = set(artist_genres['artist_id'].tolist())
to_eradicate = artist_ids - genre_artist_ids

# only keep rows from artists that do not an artist_id in to_eradicate
artists = artists[~artists['artist_id'].isin(to_eradicate)]

# remove rows from song_artists that have no artist_id in artists
song_artists = song_artists[song_artists['artist_id'].isin(artists['artist_id'])]

# remove rows from artist_genres that have no artist_id in artists
artist_genres = artist_genres[artist_genres['artist_id'].isin(artists['artist_id'])]

# remove the song rows from song_albums that have no artist_id in song_artists
song_albums = song_albums[song_albums['song_id'].isin(song_artists['song_id'])]

# remove the album rows from albums that have no song_id in song_albums
albums = albums[albums['album_id'].isin(song_albums['album_id'])]

# remove the song rows from songs that have no song_id in song_albums
songs = songs[songs['id'].isin(song_albums['song_id'])]

# now, rewrite all the csv's!
albums.to_csv('csv/albums.csv', index=False)
artists.to_csv('csv/artists.csv', index=False)
songs.to_csv('csv/songs.csv', index=False)
song_artists.to_csv('csv/song_artists.csv', index=False)
song_albums.to_csv('csv/song_albums.csv', index=False)
artist_genres.to_csv('csv/artist_genres.csv', index=False)
