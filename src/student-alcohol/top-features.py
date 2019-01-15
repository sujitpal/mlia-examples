# -*- coding: utf-8 -*-
from __future__ import division, print_function

import numpy as np
import cPickle as pickle
import matplotlib.pyplot as plt

import os

DATA_DIR = "../../data/student-alcohol"

with open(os.path.join(DATA_DIR, "model.pkl"), "rb") as fclf:
    clf = pickle.load(fclf)

important_features = clf.feature_importances_

colnames = []
fcolnames = open(os.path.join(DATA_DIR, "merged-colnames.txt"), "rb")
for line in fcolnames:
    colnames.append(line.strip())
fcolnames.close()
colnames = colnames[0:-1]

# feature importances
plt.figure(figsize=(20, 10))
plt.barh(range(len(important_features)), important_features)
plt.xlabel("importance")
plt.ylabel("features")
plt.yticks(np.arange(len(colnames))+0.35, colnames)
plt.show()

# list of top features
print("Top features")
top_features = np.argsort(important_features)[::-1][0:15]
for i in range(15):
    idx = top_features[i]
    print("\t{:.3f}\t{:s}".format(important_features[idx], colnames[idx]))

# distribution of top features with output
dataset = np.loadtxt(os.path.join(DATA_DIR, "merged-data.csv"), delimiter=";")
X = dataset[:, 0:-1]
y = dataset[:, -1]

colors = ["lightgray", "r"]
fig, axes = plt.subplots(5, 3, figsize=(20, 10))
axes = np.ravel(axes)
for i in range(15):
    idx = top_features[i]
    xvals = X[:, idx]
    xvals_nalc = xvals[np.where(y == 0)[0]]
    xvals_alc = xvals[np.where(y == 1)[0]]
    num_xvals = np.unique(xvals).shape[0]
    if num_xvals <= 2:
        nbins = 2
    elif num_xvals <= 5:
        nbins = 5
    else:
        nbins = 10
    axes[i].hist([xvals_nalc, xvals_alc], bins=nbins, normed=False, 
                 histtype="bar", stacked=True, color=colors)
    axes[i].set_title(colnames[idx])
    axes[i].set_xticks([])
    axes[i].set_yticks([])
plt.xticks([])
plt.yticks([])
plt.tight_layout()
plt.show()
    