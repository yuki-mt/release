import numpy as np
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.neighbors import NearestNeighbors
from multiprocessing import Pool
import os
from typing import List
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import StratifiedKFold


class NearestNeighborsFeats(BaseEstimator, ClassifierMixin):
    def __init__(self, n_jobs, k_list, metric, n_classes=None, n_neighbors=None, eps=1e-6):
        self.n_jobs = n_jobs
        self.k_list = k_list  # List of number of neighbors to check
        self.metric = metric

        if n_neighbors is None:
            self.n_neighbors = max(k_list)
        else:
            self.n_neighbors = n_neighbors

        self.eps = eps
        self.n_classes_ = n_classes

    def fit(self, X, y):
        self.NN = NearestNeighbors(n_neighbors=max(self.k_list),
                                   metric=self.metric,
                                   n_jobs=1,
                                   algorithm='brute' if self.metric=='cosine' else 'auto')
        self.NN.fit(X)
        self.y_train = y
        self.n_classes = np.unique(y).shape[0] if self.n_classes_ is None else self.n_classes_

    def predict(self, X):
        if self.n_jobs == 1:
            test_feats = []
            for i in range(X.shape[0]):
                test_feats.append(self._get_features_for_one(X[i:i + 1]))
        else:
            with Pool(processes=self.n_jobs) as pool:
                data = [X[i:i + 1] for i in range(X.shape[0])]
                test_feats = pool.map(self._get_features_for_one, data)

        return np.vstack(test_feats)

    def _get_features_for_one(self, x):
        NN_output = self.NN.kneighbors(x)
        neighs = NN_output[1][0]
        neighs_dist = NN_output[0][0]
        neighs_y = self.y_train[neighs]

        return_list = []

        """
        Fraction of objects of every class.
        """
        for k in self.k_list:
            bincount = np.bincount(neighs_y[:k])
            bincount = np.append(bincount, np.zeros(self.n_classes - len(bincount)))
            feats = []
            for i in range(self.n_classes):
                feats.append(bincount[i] / k)

            assert len(feats) == self.n_classes
            return_list += [feats]

        """
        Same label streak: the largest number N,
        such that N nearest neighbors have the same label.
        """
        a = np.where(neighs_y == neighs_y[0])[0]
        feats = [a[a == range(len(a))][-1] + 1]
        assert len(feats) == 1
        return_list += [feats]

        '''
        Minimum distance to objects of each class
        Find the first instance of a class and take its distance as features.
        If there are no neighboring objects of some classes, set distance to that class to be 999.
        '''
        feats = []
        for c in range(self.n_classes):
            feats.append(np.min(np.where(neighs_y == c, neighs_dist, 999)))

        assert len(feats) == self.n_classes
        return_list += [feats]

        '''
        Minimum *normalized* distance to objects of each class
        If there are no neighboring objects of some classes, set distance to that class to be 999.
        '''
        feats = []
        closest_dist = np.min(neighs_dist)
        norm_dist = neighs_dist / (closest_dist + self.eps)
        for c in range(self.n_classes):
            dists = norm_dist[neighs_y == c]
            if len(dists) > 0:
                feats.append(dists.min())
            else:
                feats.append(999)

        assert len(feats) == self.n_classes
        return_list += [feats]

        '''
        - Distance to Kth neighbor
        - Distance to Kth neighbor normalized by distance to the first neighbor
        '''
        for k in self.k_list:
            feat_51 = neighs_dist[k - 1]
            feat_52 = feat_51 / (neighs_dist[0] + self.eps)
            return_list += [[feat_51, feat_52]]

        '''
        Mean distance to neighbors of each class for each K from `k_list`
        For each class select the neighbors of that class among K nearest neighbors
        and compute the average distance to those objects

        If there are no objects of a certain class among K neighbors, set mean distance to 999
        '''
        for k in self.k_list:
            feats = []
            for c in range(self.n_classes):
                dists = neighs_dist[:k][neighs_y[:k] == c]
                if len(dists) > 0:
                    feats.append(dists.sum() / (len(dists) + self.eps))
                else:
                    feats.append(999)

            assert len(feats) == self.n_classes
            return_list += [feats]

        knn_feats = np.hstack(return_list)

        assert knn_feats.shape == (239,) or knn_feats.shape == (239, 1)
        return knn_feats


def get_test_feature(X: np.ndarray, y: np.ndarray, k_list: List[int] = [3, 8]):
    os.makedirs('data', exist_ok=True)
    for metric in ['minkowski', 'cosine']:
        NNF = NearestNeighborsFeats(n_jobs=4, k_list=k_list, metric=metric)
        NNF.fit(X, y)
        test_knn_feats = NNF.predict(X)
        np.save(f'data/knn_feats_{metric}_test.npy', test_knn_feats)

def get_train_feature(X: np.ndarray, y: np.ndarray, k_list: List[int] = [3, 8]):
    for metric in ['minkowski', 'cosine']:
        skf = StratifiedKFold(n_splits=5, random_state=123, shuffle=True)
        NNF = NearestNeighborsFeats(n_jobs=4, k_list=k_list, metric=metric)
        preds = cross_val_predict(NNF, X, y, cv=skf)
        np.save(f'data/knn_feats_{metric}_train.npy', preds)
