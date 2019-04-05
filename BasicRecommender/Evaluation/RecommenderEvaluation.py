"""
@author James Ward C12404762

created 09/02/2019

"""
import itertools
from surprise import accuracy
from collections import defaultdict


class RecommenderEvaluation:

    def RMSE(self, predictions):
        return accuracy.rmse(predictions, verbose=False)

    def MAE(self, predictions):
        return accuracy.mae(predictions, verbose=False)

    # Gets the top N = 10 predictions for each user
    def getTopN(self, predictions, n=10, minimumTrackCount=2):
        topN = defaultdict(list)

        for user, artist, actualTrackCount, predictedTrackCount, _ in predictions:
            if predictedTrackCount >= minimumTrackCount:
                topN[str(user)].append((str(artist), predictedTrackCount))

        for user, trackCount in topN.items():
            trackCount.sort(key=lambda x: x[1], reverse=True)
            topN[str(user)] = trackCount[:n]

        return topN

    def hitRate(self, topNPredictions, leftOutPredictions):
        hits = 0
        total = 0

        # For each users artist track count left out
        for leftOut in leftOutPredictions:
            user = leftOut[0]
            leftOutArtist = leftOut[1]

            # Is the left out prediction in the top N predictions for the user
            hit = False
            for artist, predictedTrackCount in topNPredictions[str(user)]:
                if str(leftOutArtist) == str(artist):
                    hit = True
                    break
            if hit :
                hits += 1

            total += 1

        # Return the overall precision
        return hits/total

    def cumulativeHitRate(self, topNPredictions, leftOutPredictions, trackCountCutOff=0):
        hits = 0
        total = 0

        # For each users artist track count left out
        for user, leftOutArtist, actualTrackCount, estimatedTrackCount, _ in leftOutPredictions:
            # Only look at the ability to recommend artist the user actually likes
            if actualTrackCount >= trackCountCutOff:
                # Check if it is in the top N predictions for the user
                hit = False
                for artist, predictedTrackCount in topNPredictions[str(user)]:
                    if str(leftOutArtist) == artist:
                        hit = True
                        break
                if hit :
                    hits += 1

                total += 1

        # Return the overall precision
        return hit/total

    def trackCountHitRate(self, topNPredicted, leftOutPredictions):
        hits = defaultdict(float)
        total = defaultdict(float)

        # For each users artist track count left out
        for user, leftOutArtist, actualTrackCount, estimatedTrackCount, _ in leftOutPredictions:
            # Check if it is in the top N predictions for the user
            hit = False
            for artist, predictedTrackCount in topNPredicted[str(user)]:
                if str(leftOutArtist) == artist:
                    hit = True
                    break
            if (hit) :
                hits[actualTrackCount] += 1

            total[actualTrackCount] += 1

        # Compute overall precision
        for trackCount in sorted(hits.keys()):
            print(trackCount, hits[trackCount] / total[trackCount])

    def averageReciprocalHitRank(self, topNPredicted, leftOutPredictions):
        summation = 0
        total = 0

        # For each users artist track count left out
        for user, leftOutArtist, actualTrackCount, estimatedTrackCount, _ in leftOutPredictions:
            # Is it in the predicted top N for this user?
            hitRank = 0
            rank = 0
            for artist, predictedTrackCount in topNPredicted[str(user)]:
                rank = rank + 1
                if str(leftOutArtist) == artist:
                    hitRank = rank
                    break
            if hitRank > 0:
                summation += 1.0 / hitRank

            total += 1

        return summation / total

    # What percentage of users have at least one accurate recommendation
    def userCoverage(self, topNPredicted, numUsers, ratingThreshold=0):
        hits = 0
        for user in topNPredicted.keys():
            hit = False
            for artist, predictedTrackCount in topNPredicted[user]:
                if predictedTrackCount >= ratingThreshold:
                    hit = True
                    break
            if hit:
                hits += 1

        return hits / numUsers

    def diversity(self, topNPredicted, simsAlgo):
        n = 0
        total = 0
        simsMatrix = simsAlgo.compute_similarities()
        for user in topNPredicted.keys():
            pairs = itertools.combinations(topNPredicted[user], 2)
            for pair in pairs:
                artist1 = pair[0][0]
                artist2 = pair[1][0]
                innerID1 = simsAlgo.trainset.to_inner_iid(str(artist1))
                innerID2 = simsAlgo.trainset.to_inner_iid(str(artist2))
                similarity = simsMatrix[innerID1][innerID2]
                total += similarity
                n += 1

        sim = total / n
        return 1-sim

    def novelty(self, topNPredicted, rankings):
        n = 0
        total = 0
        for user in topNPredicted.keys():
            for rating in topNPredicted[user]:
                artist = rating[0]
                rank = rankings[artist]
                total += rank
                n += 1
        return total / n
