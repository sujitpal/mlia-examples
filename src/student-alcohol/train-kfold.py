# -*- coding: utf-8 -*-
from __future__ import division, print_function
from sklearn.cross_validation import train_test_split, KFold
from sklearn.metrics import *
from xgboost import XGBClassifier
import numpy as np
import cPickle as pickle

import os

DATA_DIR = "../../data/student-alcohol"

dataset = np.loadtxt(os.path.join(DATA_DIR, "merged-data.csv"), 
                     delimiter=";")
X = dataset[:, 0:-1]
y = dataset[:, -1]

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.3, 
                                                random_state=42)

kfold = KFold(Xtrain.shape[0], n_folds=10, random_state=42)
best_model = None
best_score = 0.0
for curr_fold, (train_cv, test_cv) in enumerate(kfold):
    Xtrain_cv, Xtest_cv, ytrain_cv, ytest_cv = \
        Xtrain[train_cv], Xtrain[test_cv], ytrain[train_cv], ytrain[test_cv]
    clf = XGBClassifier()
    clf.fit(Xtrain_cv, ytrain_cv)
    score = clf.score(Xtest_cv, ytest_cv)
    print("Fold {:d}, score: {:.3f}".format(curr_fold, score))
    if score > best_score:
        best_score = score
        best_model = clf

y_ = best_model.predict(Xtest)
print("Accuracy: {:.3f}".format(accuracy_score(ytest, y_)))
print()
print("Confusion Matrix")
print(confusion_matrix(ytest, y_))
print()
print("Classification Report")
print(classification_report(ytest, y_))

with open(os.path.join(DATA_DIR, "best-model.pkl"), "wb") as fmod:
    pickle.dump(best_model, fmod)
