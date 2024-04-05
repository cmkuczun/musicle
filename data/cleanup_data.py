import pandas as pd

# Read the CSV file
df = pd.read_csv('tracks_features.csv')

# Drop the specified columns
columns_to_remove = ['track_number', 'disc_number', 'explicit', 'key', 'duration_ms', 'time_signature', 'year']
df = df.drop(columns=columns_to_remove)

# Save the modified DataFrame back to a CSV file
df.to_csv('songs.csv', index=False)
