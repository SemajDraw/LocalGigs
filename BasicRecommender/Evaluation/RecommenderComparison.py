"""
@author James Ward C12404762

created 11/02/2019

"""
from Recommender import NowPlaying
from surprise import SVD, SVDpp, NormalPredictor
import random
import numpy as np
from Evaluation import Evaluator


def loadNowPlayingDataset():
    NP = NowPlaying.NowPlaying()
    print('Loading NowPlaying Dataset....')
    dataset = NP.loadNowPlaying()
    print('\nComputing the popularity of each artist so novelty can be measured....')
    popularity = NP.getPopularityRanks()
    return dataset, popularity


np.random.seed(0)
random.seed(0)

# Load the dataset and the popularity ranks for the recommenders
dataset, popularityRanks = loadNowPlayingDataset()

# Instantiate the evaluator to evaluate the performance of the algos
evaluator = Evaluator.Evaluator(dataset, popularityRanks)

# Build an SVD model and evaluate it
svdAlgo = SVD(random_state=10)
evaluator.addAlgorithm(svdAlgo, "SVD")

# Build an SVD++ model and evaluate it
svdppAlgo = SVDpp(random_state=10)
evaluator.addAlgorithm(svdAlgo, "SVD++")

# Make some random recommendations
random = NormalPredictor()
evaluator.addAlgorithm(random, "Random")

# Begin
evaluator.evaluate(True)
