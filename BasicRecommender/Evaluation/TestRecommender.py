"""
@author James Ward C12404762

created 09/02/2019

"""
from Recommender import NowPlaying
from Evaluation import RecommenderEvaluation
from surprise import SVD, KNNBaseline
from surprise.model_selection import train_test_split, LeaveOneOut

NP = NowPlaying.NowPlaying()
RE = RecommenderEvaluation.RecommenderEvaluation

print("Loading the NowPlaying dataset....")
dataset = NP.loadNowPlaying()

print('\nComputing artist popularity rankings so novelty can be measured....')
popularityRank = NP.getPopularityRanks()

print('\nComputing artist similarities so the diversity can be measured....')
fullTrainSet = dataset.build_full_trainset()
# sim_options = {'name': 'pearson_baseline', 'user_based': False}
# simAlgo = KNNBaseline(sim_options=sim_options)
# simAlgo.fit(fullTrainSet)

print('\nCreating train test split....')
trainSet, testSet = train_test_split(dataset, test_size=.25, random_state=1)

print('\nBuilding SVD recommendation model....')
svdAlgo = SVD(random_state=10)
svdAlgo.fit(trainSet)

print('\nComputing recommendations....')
predictions = svdAlgo.test(testSet)

print("\nEvaluating the accuracy of the model....")
print("RMSE: ", RE.RMSE(predictions))
print("MAE: ", RE.MAE(predictions))

print("\nEvaluating top-10 recommendations....")
# Set aside one artist track count per user for testing
leaveOneOut = LeaveOneOut(n_splits=1, random_state=1)

for trainSet, testSet in leaveOneOut.split(dataset):
    print("Computing recommendations for leave one out....")

    # Train the model with the training data minus 1 entry per user
    svdAlgo.fit(trainSet)

    # Predict track count for the left out entry
    print("Predict ratings for leave one out set....")
    leaveOnePredictions = svdAlgo.test(testSet)

    # Build predictions for all the track counts not in the training set
    print("Predict all missing track counts....")
    largeTestSet = trainSet.build_anti_testset()
    allPredictions = svdAlgo.test(largeTestSet)

    # Compute the top 10 recommendations for each user
    print("Compute the top 10 recommendations for each user....")
    topNPredictions = RE.getTopN(allPredictions, n=10)

    # See how often we recommended an artist the user already liked
    print("\nHit Rate: ", RE.hitRate(topNPredictions, leaveOnePredictions))

    # Break down hit rate by rating value
    print("\ntcHR (Track Count Hit Rate): ")
    RE.trackCountHitRate(topNPredictions, leaveOnePredictions)

    # Check how often an artist with at at least two tracks was recommended
    print("\ncHR (Cummulative Hit Rate, Track Count >= 1): ",
          RE.cumulativeHitRate(topNPredictions, leaveOnePredictions, 1))

    print("\nARHR (Average Reciprocal Hit Rank): ",
          RE.averageReciprocalHitRank(topNPredictions, leaveOnePredictions))

print("\nComputing complete recommendations, all inclusive....")
svdAlgo.fit(fullTrainSet)
largeTestSet = fullTrainSet.build_anti_testset()
allPredictions = svdAlgo.test(largeTestSet)
topNPredictions = RE.getTopN(allPredictions, n=10)

# Print user coverage with a minimum predicted track count of 1
print("\nUser Coverage: ", RE.userCoverage(
    topNPredictions, fullTrainSet.n_users, ratingThreshold=1))

# Measure the diversity of the recommendations
# print("\nDiversity: ", RE.diversity(topNPredictions, simAlgo))

# Measure novelty (average popularity rank of recommendations):
print("\nNovelty (average popularity rank): ", RE.novelty(topNPredictions, popularityRank))


