"""
@author James Ward C12404762

created 11/02/2019

"""
from Evaluation import EvaluatorPreProcessing, EvaluateAlgorithm


class Evaluator:

    algorithms = []

    def __init__(self, dataset, popularityRanks):
        ed = EvaluatorPreProcessing.EvaluatorPreProcessing(dataset, popularityRanks)
        self.dataset = ed

    def addAlgorithm(self, algorithm, name):
        alg = EvaluateAlgorithm.EvaluateAlgorithm(algorithm, name)
        self.algorithms.append(alg)

    def evaluate(self, doTopN):
        results = {}
        for algorithm in self.algorithms:
            print("Evaluating ", algorithm.getName(), "....")
            results[algorithm.getName()] = algorithm.evaluate(self.dataset, doTopN)

        # Print results
        print("\n")

        if doTopN:                                              # {:<10}
            print("{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}".format(
                "Algorithm", "RMSE", "MAE", "HR", "cHR", "ARHR", "Coverage", "Novelty"))
                                                                # "Diversity",^^^
            for (name, metrics) in results.items():
                                                        # {:<10.4f}
                print("{:<10} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f} {:<10.4f}".format(
                    name, metrics["RMSE"], metrics["MAE"], metrics["HR"], metrics["cHR"], metrics["ARHR"],
                    metrics["Coverage"], metrics["Novelty"]))
                    # metrics["Diversity"],^^^
        else:
            print("{:<10} {:<10} {:<10}".format("Algorithm", "RMSE", "MAE"))
            for (name, metrics) in results.items():
                print("{:<10} {:<10.4f} {:<10.4f}".format(name, metrics["RMSE"], metrics["MAE"]))

        print("\nLegend:\n")
        print("RMSE:      Root Mean Squared Error. Lower values mean better accuracy.")
        print("MAE:       Mean Absolute Error. Lower values mean better accuracy.")
        if doTopN:
            print("HR:        Hit Rate; how often we are able to recommend a left-out rating. Higher is better.")
            print(
                "cHR:       Cumulative Hit Rate; hit rate, confined to ratings above a certain threshold. Higher is better.")
            print(
                "ARHR:      Average Reciprocal Hit Rank - Hit rate that takes the ranking into account. Higher is better.")
            print(
                "Coverage:  Ratio of users for whom recommendations above a certain threshold exist. Higher is better.")
            print(
                "Diversity: 1-S, where S is the average similarity score between every possible pair of recommendations")
            print("           for a given user. Higher means more diverse.")
            print("Novelty:   Average popularity rank of recommended items. Higher means more novel.")

    def sampleTopNRecs(self, testUser, k=15):

        for algo in self.algorithms:
            print("\nUsing recommender ", algo.getName())

            print("\nBuilding recommendation model...")
            trainSet = self.dataset.getFullTrainSet()
            algo.getAlgorithm().fit(trainSet)

            print("Computing recommendations...")
            testSet = self.dataset.getAntiTestSetForUser(testUser)

            predictions = algo.getAlgorithm().test(testSet)

            recommendations = []

            print("\nWe recommend:")
            for user, artist, actualTrackCount, estimatedTrackCount, _ in predictions:
                recommendations.append((artist, estimatedTrackCount))

            recommendations.sort(key=lambda x: x[1], reverse=True)

            for row in recommendations[:k]:
                print(row)

    def sampleTopUserNRecs(self, k=15):

        for algo in self.algorithms:
            print("\nUsing recommender ", algo.getName())

            print("\nBuilding recommendation model...")
            trainSet = self.dataset.getFullTrainSet()
            algo.getAlgorithm().fit(trainSet)

            print("Computing recommendations...")
            testSet = self.dataset.getFullTestSetForUser()

            print(testSet)

            predictions = algo.getAlgorithm().test(testSet)

            recommendations = []

            print("\nWe recommend:")
            for user, artist, actualTrackCount, estimatedTrackCount, _ in predictions:
                recommendations.append((artist, estimatedTrackCount))

            recommendations.sort(key=lambda x: x[1], reverse=True)

            for row in recommendations[:k]:
                print(row)
