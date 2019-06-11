# This file cretes a useable dataset from the #nowplaying dataset
import pandas as pd

# Set larger console display
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 5000)


column_names = ['user', 'artist', 'track_count', 'playlist']
def base_dateset():
    df = pd.read_csv('data/playlist_ds.csv', sep=',', names=column_names)

    # Aggregate dataset by user and artist
    target_df = df.groupby(['user', 'artist']).count()

    # Drop the redundant playlist name column
    target_df = target_df.drop('playlist', axis=1)

    # Export dataframe to CSV
    target_df.to_csv('Dataset/AggregatedDataset.csv', sep=',')
    print(target_df)


def user_dataset():
    df = pd.read_csv('../Dataset/CleanedDataset.csv', sep=',', names=column_names)
    users = df.user.unique()

    users_df = pd.DataFrame(users, columns=['user'])

    print(users_df.head())

    users_df.to_csv('../Dataset/UsersDataset.csv', sep=',', header=False)


def artist_dataset():
    df = pd.read_csv('../Dataset/CleanedDataset.csv', sep=',', names=column_names)
    artists = df.artist.unique()
    artists.sort()

    artists_df = pd.DataFrame(artists, columns=['artist'])

    print(artists_df.head())

    artists_df.to_csv('../Dataset/ArtistsDataset.csv', sep=',', header=False)


def id_track_count():
    df = pd.read_csv('../Dataset/CleanedDataset.csv', sep=',', names=column_names)
    user_df = pd.read_csv('../Dataset/UsersDataset.csv', sep=',', names=['id', 'user'], index_col='user')
    artist_df = pd.read_csv('../Dataset/ArtistsDataset.csv', sep=',', names=['id', 'artist'], index_col='artist')

    # Create a user and artist series from the dataframe
    user_series = df['user']
    artist_series = df['artist']

    # Create mapping dictionaries from the dataframe
    user_df_dict = user_df.to_dict()
    artist_df_dict = artist_df.to_dict()

    # Extract user and artist dictionaries
    user_dict = user_df_dict['id']
    artist_dict = artist_df_dict['id']

    # Map users and artists ids to the main dataframe
    mapped_users = user_series.map(user_dict)
    mapped_artists = artist_series.map(artist_dict)

    # Create the ID dataframe
    mapped_df = pd.concat([mapped_users, mapped_artists, df['track_count']], axis=1,
                          names=['user', 'artist', 'track_count'])

    mapped_df.set_index('user', inplace=True)
    mapped_df.to_csv('../Dataset/UserArtistIDDataset.csv', sep=',', header=False)


df = pd.read_csv('../Dataset/CleanedDataset.csv', sep=',', names=['user', 'artist', 'track_count'])
user_df = pd.read_csv('../Dataset/UsersDataset.csv', sep=',', names=['id', 'user'], index_col='user')
artist_df = pd.read_csv('../Dataset/ArtistsDataset.csv', sep=',', names=['id', 'artist'], index_col='artist')


def replace_id(x):
    return artist_df[artist_df['artist']==x].artist.values[0]


artist_to_id = df.artist.map(replace_id)

id_track_count()
