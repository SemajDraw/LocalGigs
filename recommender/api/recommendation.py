from scipy.spatial.distance import cosine
from surprise import SVD
import pandas as pd
from . import pre_processing


def generate_recommendations(query_dict):

    print("IN")
    pp = pre_processing.PreProcessing(query_dict)
    dataset, fav_artists = pp.process_data()
    SVD_model = train_fit_model(dataset)

    recommended_df_list = []
    for artist in fav_artists:
        try:
            print(artist)
            recommended_df_list.append(get_top_similarities(artist, SVD_model))
        except KeyError:
            pass

    return build_artist_list(fav_artists, recommended_df_list)


def train_fit_model(dataset):
    """Builds and fits the model from the surprise dataset"""
    print("Training model...")
    trainset = dataset.build_full_trainset()
    SVD_algo = SVD(n_epochs=5)
    SVD_algo.fit(trainset)
    print("Model trained...")
    return SVD_algo


def build_artist_list(fav_artists, recommended_df_list):
    recommeded_df = pd.concat(recommended_df_list)
    recommeded_df.sort_values('vector cosine distance', ascending=True, inplace=True)
    recommeded_df.drop_duplicates('artist', keep='first', inplace=True)
    for artist in fav_artists:
        recommeded_df = recommeded_df[recommeded_df.artist != artist]

    top_100_recs = recommeded_df.head(100)
    fav_artists.extend(list(top_100_recs['artist'].unique()))
    return fav_artists


def get_vector_by_artist(artist, trained_model):
    """Returns the latent features of an artist in the form of a numpy array"""
    artist_row_idx = trained_model.trainset._raw2inner_id_items[artist]
    return trained_model.qi[artist_row_idx]


def cosine_distance(vector_a, vector_b):
    """Returns a float indicating the similarity between two vectors"""
    return cosine(vector_a, vector_b)


def display(similarity_table):
    """Builds a DataFrame and returns the top 10 entries,
        the first entry is always the artist that is being searched
        for as its distance from itself is 0 so it is removed"""

    similarity_table = pd.DataFrame(
        similarity_table,
        columns=['vector cosine distance', 'artist']
    ).sort_values('vector cosine distance', ascending=True)
    return similarity_table.iloc[1:10]


def get_top_similarities(artist, model):
    """Builds a similarity table of one artists to all other artists
        using the cosine distance of each artists vector"""

    artist_vector = get_vector_by_artist(artist, model)
    similarity_table = []

    # Iterate over every possible artist and calculate similarity
    for other_artist in model.trainset._raw2inner_id_items.keys():
        other_artist_vector = get_vector_by_artist(other_artist, model)

        # Get the second artists vector, and calculate distance
        similarity_score = cosine_distance(other_artist_vector, artist_vector)
        similarity_table.append((similarity_score, other_artist))

    return display(sorted(similarity_table))

