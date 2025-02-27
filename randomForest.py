from decisionTree import decisionTree
import numpy as np
import random

class randomForest:
    """
    This class is an implementation of the random forest ensemble method
    using the decision tree class which has already been implemented. In every bagging round
    50% of the dataset is selected for training of the base estimator and all the base estimators'
    prediction is counted through a vote and the majority class is predicted as the final prediction
    """
    def __init__(self, type="classification", n_trees=50, max_depth=30, min_samples_leaf=10):
        self.n_trees = n_trees
        self.type = type
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.dts = []
        return
    def sample(self, features, labels):
        #sampling is done randomely from the set of features with repetitions where 50% of the data set is sampled
        l = features.shape[0]
        select = random.sample(range(l), int(0.5*l))
        return features[select], labels[select]
    def train(self, features, labels):
        #this method creates n_trees number of base estimators which are trained on the bag set of features after which the majority class is marqued as the prediction
        for i in range(self.n_trees):
            tree = decisionTree(type = self.type, max_depth=self.max_depth, min_samples_leaf=self.min_samples_leaf)
            f1, l1 = self.sample(features, labels)
            tree.train(f1, l1)
            self.dts.append(tree)
        return
    def voting(self, preds):
        p = []
        for i in range(len(preds[0])):
            votes = []
            for j in range(self.n_trees):
                votes.append(preds[j][i])
            pred_classes, pred_counts = np.unique(votes, return_counts=True)
            prediction = pred_classes[np.argmax(pred_counts)]
            print(prediction)
            p.append(prediction)
        return p

    def predict(self, features):
        preds = []
        for i in range(self.n_trees):
            preds.append(self.dts[i].predict(features))
        pred = self.voting(preds)
        return pred
