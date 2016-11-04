# -*- coding: utf-8 -*-
from __future__ import division, print_function
from sklearn.cross_validation import train_test_split
from sklearn.metrics import *
from xgboost import XGBClassifier

import cPickle as pickle
import numpy as np
import os

DATA_DIR = "../../data/student-alcohol"

dataset = np.loadtxt(os.path.join(DATA_DIR, "merged-data.csv"), 
                     delimiter=";")
X = dataset[:, 0:-1]
y = dataset[:, -1]

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.3, 
                                                random_state=42)

clf = XGBClassifier()
clf.fit(Xtrain, ytrain, early_stopping_rounds=10, eval_metric="logloss",
        eval_set=[(Xtest, ytest)], verbose=True)

y_ = clf.predict(Xtest)

print("Accuracy: {:.3f}".format(accuracy_score(ytest, y_)))
print()
print("Confusion Matrix")
print(confusion_matrix(ytest, y_))
print()
print("Classification Report")
print(classification_report(ytest, y_))

with open(os.path.join(DATA_DIR, "model.pkl"), "wb") as fclf:
    pickle.dump(clf, fclf)
