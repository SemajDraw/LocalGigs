# This file cretes a useable dataset from the #nowplaying dataset
import pandas as pd

# Set larger console display
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 5000)

# Read dataset and label columns
column_names = ['user', 'artist', 'track', 'playlist']
df = pd.read_csv('data/playlist_ds.csv', sep=',', names=column_names)

# Aggregate dataset by user and artist
target_df = df.groupby(['user', 'artist']).count()

# Drop the redundant playlist name column
target_df = target_df.drop('playlist', axis=1)

# Export dataframe to CSV
target_df.to_csv('data/my.csv', sep=',')
print(target_df)
