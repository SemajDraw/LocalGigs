import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix

# Set larger console display
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 5000)

column_names = ['user', 'artist', 'track_count']
cleaned_df = pd.read_csv('../Dataset/CleanedDataset.csv', sep=',', names=column_names, encoding="utf8")

# train_df = pd.read_csv('../Dataset/TrainDataset.csv', sep=',', names=column_names, encoding="utf8")

# test_df = pd.read_csv('../Dataset/TestDataset.csv', sep=',', names=column_names, encoding="utf8")


def one_hot_encode(df):
    pass
    # for index, row in df.iterrows
    # one_hot_df = pd.concat([df, pd.get_dummies(df['artist'])], axis=1)

    # one_hot_df.drop()
    # numUsers, num_features = feature_count_dataset(df)
    # feature_matrix = lil_matrix((df.shape[0], num_features)).astype('float32')
    # label_matrix = []
    # rowNum = 0
    # for index, row in df.iterrows():
    #     feature_matrix[rowNum, int(row['user'])-1] = 1
    #     feature_matrix[rowNum, int(numUsers) + int(row['artist']) - 1] = 1
    #     if int(row['rating']) >= 4:
    #         label_matrix.append(1)
    #     else:
    #         label_matrix.append(0)
    #     rowNum += 1
    #
    # label_matrix = np.array(label_matrix).astype('float32')
    # return feature_matrix, label_matrix


def feature_count_dataset(df):
    numUsers = df['user'].nunique
    print(numUsers)
    numArtists = df['artist'].nunique

    return numUsers, numUsers + numArtists


def unique_artist_user(df):
    users = df.user.unique()
    artists = df.artist.unique()

    return users, artists
