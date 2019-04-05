"""
@author James Ward C12404762

created 11/02/2019

"""
from surprise.model_selection import train_test_split, LeaveOneOut
from surprise import Dataset, Reader
import pandas as pd


class EvaluatorPreProcessing:

    def __init__(self, dataset, popularityRanks):

        self.popularity = popularityRanks

        # Build a training set from all of the data
        self.fullTrainSet = dataset.build_full_trainset()
        self.fullAntiTestSet = self.fullTrainSet.build_anti_testset()

        #  Build a 75% 25% train test split
        self.trainSet, self.testSet = train_test_split(dataset, test_size=.25, random_state=1)

        # Build a leave_one_out train test split for evaluating top N recommendations
        # Build an anti_test_set for generating predictions
        LOO = LeaveOneOut(n_splits=1, random_state=1)
        for train, test in LOO.split(dataset):
            self.LOOTrain = train
            self.LOOTest = test

        self.LOOAntiTestSet = self.LOOTrain.build_anti_testset()

        # Compute the similarity matrix between artists
        """ONLY NECESSARY FOR CALCULATING DIVERSITY"""
        # self.simsAlgo = KNNBaseline(
        #     sim_options={'name': 'cosine', 'user_based': False})
        # self.simsAlgo.fit(self.fullTrainSet)

    def getFullTrainSet(self):
        return self.fullTrainSet

    def getFullAntiTestSet(self):
        return self.fullAntiTestSet

    def getAntiTestSetForUser(self, user):
        trainset = self.fullTrainSet
        fill = trainset.global_mean
        anti_testset = []
        u = trainset.to_inner_uid(str(user))
        user_items = set([j for (j, _) in trainset.ur[u]])
        anti_testset += [(trainset.to_raw_uid(u), trainset.to_raw_iid(i), fill) for
                         i in trainset.all_items() if
                         i not in user_items]
        return anti_testset

    def getFullTestSetForUser(self):

        column_names = ['user', 'artist', 'track_count']
        npdf = pd.read_csv("../Dataset/02d63991838c76696f4f9a76da3c1871.csv", sep=',', names=column_names, encoding="utf8")

        reader = Reader(rating_scale=(1, 10))

        userData = Dataset.load_from_df(npdf[['user', 'artist', 'track_count']], reader)

        trainset = userData
        # fill = trainset
        # anti_testset = []
        # u = trainset.index(0)
        # user_items = set([j for (j, _) in trainset.ur[u]])
        # anti_testset += [(trainset.to_raw_uid(u), trainset.to_raw_iid(i), fill) for
        #                  i in trainset.all_items() if
        #                  i not in user_items]
        return trainset

    def getTrainSet(self):
        return self.trainSet

    def getTestSet(self):
        return self.testSet

    def getLOOTrainSet(self):
        return self.LOOTrain

    def getLOOTestSet(self):
        return self.LOOTest

    def getLOOAntiTestSet(self):
        return self.LOOAntiTestSet

    def getSimilarities(self):
        return self.simsAlgo

    def getPopularityRankings(self):
        return self.popularity
