# -*- coding: utf-8 -*-
from __future__ import division, print_function
from sklearn import grid_search
from sklearn.cross_validation import train_test_split
from sklearn.metrics import *
from xgboost import XGBClassifier

import numpy as np
import os

DATA_DIR = "../../data/student-alcohol"

dataset = np.loadtxt(os.path.join(DATA_DIR, "merged-data.csv"), delimiter=";")
X = dataset[:, 0:-1]
y = dataset[:, -1]

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.3, 
                                                random_state=42)

clf = XGBClassifier()
parameters = {
    "learning_rate": [0.001, 0.01, 0.1, 1.0],
    "n_estimators" : [50, 100, 250, 500],
    "max_depth"    : [3, 5, 10]
}
gs = grid_search.GridSearchCV(clf, parameters, verbose=True)
gs.fit(Xtrain, ytrain)

y_ = gs.predict(Xtest)

print("Accuracy: {:.3f}".format(accuracy_score(ytest, y_)))
print()
print("Confusion Matrix")
print(confusion_matrix(ytest, y_))
print()
print("Classification Report")
print(classification_report(ytest, y_))

print("Best parameters:")
best_params = gs.get_params()
for k in parameters.keys():
    print("\t{:s}: {:.3f}".format(k, best_params["estimator__" + k]))

with open(os.path.join(DATA_DIR, "best-model-gs.pkl"), "wb") as fmod:
    pickle.dump(best_model, fmod)
