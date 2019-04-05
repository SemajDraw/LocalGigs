"""
@author James Ward C12404762

created 11/02/2019

"""
from Recommender import NowPlaying
from Evaluation import Evaluator
from surprise import SVD, SVDpp, dump
from surprise import Dataset, Reader
from collections import defaultdict
import random
import numpy as np
from scipy.spatial.distance import cosine
import pandas as pd


np.random.seed(0)
random.seed(0)


def loadNowPlayingDataset():
    NP = NowPlaying.NowPlaying()
    print('Loading NowPlaying Dataset....')
    dataset = NP.loadNowPlaying()
    # print('\nComputing the popularity of each artist so novelty can be measured....')
    # popularity = NP.getPopularityRanks()
    return dataset#, popularity


def evaluate_svd_algos(dataset, popularityRanks):
    # Instantiate the evaluator to evaluate the performance of the algos
    evaluator = Evaluator.Evaluator(dataset, popularityRanks)

    # Build an SVD++ model
    print("Building SVD++ predictive model....")
    svdppAlgo = SVDpp(random_state=10)
    evaluator.addAlgorithm(svdppAlgo, "SVD++")

    # Build an SVD++ model
    print("Building SVD predictive model....")
    svdAlgo = SVD(random_state=10)
    evaluator.addAlgorithm(svdAlgo, "SVD")

    # Evaluate the algorithms
    evaluator.evaluate(True)

    user = ""
    while user != "exit":
        user = input("\nEnter a user id: ")
        if user == "exit":
            exit()
        evaluator.sampleTopNRecs(user)


def get_top_n(predictions, n=10):
    '''Return the top-N recommendation for each user from a set of predictions.

    Args:
        predictions(list of Prediction objects): The list of predictions, as
            returned by the test method of an algorithm.
        n(int): The number of recommendation to output for each user. Default
            is 10.

    Returns:
    A dict where keys are user (raw) ids and values are lists of tuples:
        [(raw item id, rating estimation), ...] of size n.
    '''

    # First map the predictions to each user.
    top_n = defaultdict(list)
    for uid, iid, true_r, est, _ in predictions:
        top_n[uid].append((iid, est))

    # Then sort the predictions for each user and retrieve the k highest ones.
    for uid, user_ratings in top_n.items():
        user_ratings.sort(key=lambda x: x[1], reverse=True)
        top_n[uid] = user_ratings[:n]

    return top_n


def get_vector_by_artist(artist, trained_model: SVD):
    """Returns the latent features of an artist in the form of a numpy array"""
    artist_row_idx = trained_model.trainset._raw2inner_id_items[artist]
    return trained_model.qi[artist_row_idx]


def cosine_distance(vector_a, vector_b):
    """Returns a float indicating the similarity between two vectors"""
    return cosine(vector_a, vector_b)


def display(similarity_table):
    similarity_table = pd.DataFrame(
        similarity_table,
        columns=['vector cosine distance', 'artist']
    ).sort_values('vector cosine distance', ascending=True)
    return similarity_table.iloc[1:10]


def get_top_similarities(artist, model):
    """Returns the top 5 most similar artists to a specified artist

    This function iterates over every possible artist in the dataset and calculates
    distance between `artist` vector and provided artist's vector.
    """

    # Get the first movie vector
    artist_vector = get_vector_by_artist(artist, model)
    similarity_table = []

    # Iterate over every possible artist and calculate similarity
    for other_artist in model.trainset._raw2inner_id_items.keys():
        other_artist_vector = get_vector_by_artist(other_artist, model)

        # Get the second movie vector, and calculate distance
        similarity_score = cosine_distance(other_artist_vector, artist_vector)
        similarity_table.append((similarity_score, other_artist))

    # sort movies by ascending similarity
    return display(sorted(similarity_table))


# Load the dataset and the popularity ranks for the recommenders
train_data = loadNowPlayingDataset()

print("Training the SVD model...")
#  Build full train set from train data
trainset = train_data.build_full_trainset()

# Instantiate SVD algorithm
SVD_algo = SVD(n_epochs=5)

# Fit the SVD model with the training dataset
print("Fitting the SVD model...")
SVD_algo.fit(trainset)

# Dump/store algo
# dump.dump('../Models/SVDpp5epochs', algo=SVD_algo)

var = ''
while var != exit:
    fav_list = ['Fuzz', 'Pond', 'RJD2', 'Flume', 'Hozier', 'ZZ Top', 'Battles', 'Nirvana', 'Pantera', 'The Who',
                'Bee Gees', 'Bon Jovi', 'Megadeth', 'Allah-Las', 'Bob Dylan', 'Etherwood', 'Jax Jones', 'Metallica',
                'Pearl Jam', 'The Clash', 'The Doors', 'The Kinks', 'The Kooks', 'Ty Segall', 'Pink Floyd',
                'David Bowie', 'Iron Maiden', 'James Brown', 'Labi Siffre', 'Mac DeMarco', 'Night Beats', 'Ray Charles',
                'Royal Blood', 'Tame Impala', 'The Animals', 'The Beatles', 'Bill Withers', 'Dire Straits',
                'Eric Clapton', 'Hybrid Minds', 'Jimi Hendrix', 'Led Zeppelin', 'Thee Oh Sees', 'Van Morrison',
                'Wu-Tang Clan', 'Black Sabbath', "Guns N' Roses", 'Kings of Leon', 'Arctic Monkeys', 'Paul McCartney',
                'The Beach Boys', 'The Black Keys', 'The Budos Band', 'Fred V & Grafix', 'Greta Van Fleet',
                'System Of A Down', 'The Dead Weather', 'The White Stripes', 'Bass Drum of Death', 'The Gaslamp Killer',
                'The Rolling Stones', 'A Tribe Called Quest', 'Red Hot Chili Peppers', 'The Mamas & The Papas',
                'Queens of the Stone Age', 'Bob Marley & The Wailers', 'Rage Against The Machine',
                'Unknown Mortal Orchestra', 'Creedence Clearwater Revival', 'The Brian Jonestown Massacre',
                'King Gizzard & The Lizard Wizard']

    try:
        print('Get similarities')
        recommended_df_list = []
        for artist in fav_list:
            try:
                print(artist)
                recommended_df_list.append(get_top_similarities(artist, SVD_algo))
            except KeyError:
                pass

        print('Get favourites')
        recommeded_df = pd.concat(recommended_df_list)
        recommeded_df.sort_values('vector cosine distance', ascending=True, inplace=True)
        recommeded_df.drop_duplicates('artist', keep='first', inplace=True)
        for artist in fav_list:
            print(artist)
            recommeded_df = recommeded_df[recommeded_df.artist != artist]

        top_100_recs = recommeded_df.head(100)
        print(top_100_recs)
        fav_list.extend(list(top_100_recs['artist'].unique()))

        print('Recommended artists: ', fav_list)

        var = input('Pleae enter an artist: ')
    except KeyError:
        pass
