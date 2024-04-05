import pandas as pd

# read CSV file
df = pd.read_csv('tracks_features.csv')

# drop specified columns
columns_to_remove = ['track_number', 'disc_number', 'explicit', 'key', 'duration_ms', 'time_signature', 'year']
df = df.drop(columns=columns_to_remove)

# save modified df back to a CSV file
df.to_csv('og_songs.csv', index=False)
