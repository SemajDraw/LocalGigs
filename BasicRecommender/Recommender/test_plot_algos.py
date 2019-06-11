"""
@author James Ward C12404762

created 11/02/2019

"""
from Recommender import NowPlaying
from plotly.offline import plot
import plotly.graph_objs as go

from Evaluation import Evaluator
from surprise import SVD, SVDpp, SlopeOne, NMF, NormalPredictor, KNNBaseline, \
    KNNBasic, KNNWithMeans, KNNWithZScore, BaselineOnly, CoClustering
from surprise.model_selection.validation import cross_validate
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


# Load the dataset and the popularity ranks for the recommenders
train_data = loadNowPlayingDataset()


# Visualizing the data
""" THE PLOTTING METHODS REQUIRE A PANDAS DF FOR TRAIN DATA"""
def plot_districbution_of_artist_ratings():
    rating_data = train_data['track_count'].value_counts().sort_index(ascending=False)
    rating_data.pop(0)
    # Create trace
    trace = go.Bar(x =  rating_data.index,
                   text = ['{:.1f} %'.format(val) for val in (rating_data.values / train_data.shape[0] * 100)],
                   textposition = 'auto',
                   textfont = dict(color='#000000'),
                   y = rating_data.values,
                   )
    # Create layout
    layout = dict(title = 'Distribution Of Artist Ratings',
                  xaxis = dict(title = 'Rating'),
                  yaxis = dict(title = 'Count'))
    # Create plot
    fig = go.Figure(data=[trace], layout=layout)
    plot(fig)


def plot_distribution_of_user_rating_pattern():
    rating_data = train_data.groupby('user')['track_count'].count().clip(upper=1000)
    # Create trace
    trace = go.Histogram(x=rating_data.values,
                         name='Ratings',
                         xbins=dict(start=0, end=1000, size=20))

    # Create layout
    layout = dict(title='Distribution Of Number of Ratings Per User',
                  xaxis=dict(title='Ratings Per User'),
                  yaxis=dict(title='User Count'),
                  bargap=0.2)
    # Create plot
    fig = go.Figure(data=[trace], layout=layout)
    plot(fig)


# Cross validate algorithms and retrieve their RMSE score, test and train time
def cross_validate_algos():
    benchmark = []
    # Iterate over all algorithms
    for algorithm in [SVD(), SVDpp(), SlopeOne(), NMF(), NormalPredictor(), KNNBaseline(),
                      KNNBasic(), KNNWithMeans(), KNNWithZScore(), BaselineOnly(), CoClustering()]:
        print(str(algorithm))
        # Perform cross validation
        results = cross_validate(algorithm, train_data, measures=['RMSE'], cv=3, verbose=False)
        print('Finished cross validation')
        # Get results & append algorithm name
        tmp = pd.DataFrame.from_dict(results).mean(axis=0)
        tmp = tmp.append(pd.Series([str(algorithm).split(' ')[0].split('.')[-1]], index=['Algorithm']))
        benchmark.append(tmp)

    benchmarked_algos = pd.DataFrame(benchmark).set_index('Algorithm').sort_values('test_rmse')
    print(benchmarked_algos.head())
    benchmarked_algos.to_csv('../Dataset/BenchmarkedAlgos.csv', sep=',')


# print("Training the SVD model...")
# #  Build full train set from train data
# trainset = train_data.build_full_trainset()
#
# # Instantiate SVD algorithm
# SVD_algo = SVD(n_epochs=5)
#
# # Fit the SVD model with the training dataset
# print("Fitting the SVD model...")
# SVD_algo.fit(trainset)



# plot_districbution_of_artist_ratings()
# plot_distribution_of_user_rating_pattern()
cross_validate_algos()