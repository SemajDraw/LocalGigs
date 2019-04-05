"""
@author James Ward C12404762

created 11/02/2019

"""
from Evaluation import RecommenderEvaluation, EvaluatorPreProcessing


class EvaluateAlgorithm:

    def __init__(self, algorithm, name):
        self.algorithm = algorithm
        self.name = name

    def evaluate(self, evaluationData, doTopN, n=10, verbose=True):
        RE = RecommenderEvaluation.RecommenderEvaluation()
        metrics = {}

        # Compute the accuracy of the algo
        if verbose:
            print("Evaluating accuracy...")
        self.algorithm.fit(evaluationData.getTrainSet())
        predictions = self.algorithm.test(evaluationData.getTestSet())
        metrics["RMSE"] = RE.RMSE(predictions)
        metrics["MAE"] = RE.MAE(predictions)

        if doTopN:
            # Evaluate top-10 with Leave One Out testing
            if verbose:
                print("Evaluating top-N with leave_one_out....")

            self.algorithm.fit(evaluationData.getLOOTrainSet())
            leftOutPredictions = self.algorithm.test(evaluationData.getLOOTestSet())

            # Generate predictions for all ratings not in the training set
            allPredictions = self.algorithm.test(evaluationData.getLOOAntiTestSet())

            # Compute top 10 recommendations for each user
            topNPredicted = RE.getTopN(allPredictions, n)

            if verbose:
                print("Computing hit-rate and rank metrics....")

            # See how often we recommended a movie the user actually rated
            metrics["HR"] = RE.hitRate(topNPredicted, leftOutPredictions)

            # See how often we recommended a movie the user actually liked
            metrics["cHR"] = RE.cumulativeHitRate(topNPredicted, leftOutPredictions)

            # Compute ARHR
            metrics["ARHR"] = RE.averageReciprocalHitRank(topNPredicted, leftOutPredictions)

            # Evaluate the recommendations using the full training set
            if verbose:
                print("Computing recommendations with full dataset....")

            self.algorithm.fit(evaluationData.getFullTrainSet())
            allPredictions = self.algorithm.test(evaluationData.getFullAntiTestSet())
            topNPredicted = RE.getTopN(allPredictions, n)

            if verbose:
                print("Analyzing coverage, diversity, and novelty....")

            # Print the user coverage with a minimum predicted rating of 1.0:
            metrics["Coverage"] = RE.userCoverage(topNPredicted, evaluationData.getFullTrainSet().n_users,
                                                  ratingThreshold=1.0)
            # Measure the diversity of recommendations:
            """TOO COMPUTATIONALY INTENSIVE FOR MY MACHINE"""
            # metrics["Diversity"] = RE.diversity(topNPredicted, evaluationData.getSimilarities())

            # Measure the novelty (average popularity rank of recommendations):
            metrics["Novelty"] = RE.novelty(topNPredicted, evaluationData.getPopularityRankings())

        if verbose:
            print("Analysis complete.")

        return metrics

    def getName(self):
        return self.name

    def getAlgorithm(self):
        return self.algorithm
