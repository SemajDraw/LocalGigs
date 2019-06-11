"""
@author James Ward C12404762

created 09/02/2019

"""
from surprise import Dataset, Reader
from collections import defaultdict
import pandas as pd
import csv


class NowPlaying(object):

    dataset_path = "../Dataset/100kDataset.csv"

    def loadNowPlaying(self):

        column_names = ['user', 'artist', 'track_count']
        npdf = pd.read_csv(self.dataset_path, sep=',', names=column_names, encoding="utf8")

        reader = Reader(rating_scale=(1, 10))

        nowPlayingDataset = Dataset.load_from_df(npdf[['user', 'artist', 'track_count']], reader)

        return nowPlayingDataset

    # def getPopularityRanks(self):
    #     ratings = defaultdict(int)
    #     rankings = defaultdict(str)
    #     with open(self.dataset_path, newline='\n', encoding='utf8') as dataset:
    #         ratingReader = csv.reader(dataset)
    #         next(ratingReader)
    #         for row in ratingReader:
    #             artist = str(row[1])
    #             ratings[artist] += 1
    #     rank = 1
    #     for artist, occuranceCount in sorted(ratings.items(), key=lambda x: x[1], reverse=True):
    #         rankings[artist] = rank
    #         rank += 1
    #     return rankings




