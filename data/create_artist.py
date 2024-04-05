import pandas as pd
import ast

df = pd.read_csv('songs.csv')

# convert string to list
df['artists'] = df['artists'].apply(lambda x: ast.literal_eval(x))

# expand artist arrays
df = df.explode('artists')

# convert type of artist back to string!
df['artists'] = df['artists'].astype(str)
df = df.rename(columns={'artists': 'artist'})

# keep specified columns
columns_to_keep = ['id', 'artist']
df = df[columns_to_keep]

# save modified DataFrame back to CSV file
df.to_csv('artists.csv', index=False)