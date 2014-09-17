from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from scipy.io import loadmat
from scipy.stats import multivariate_normal
from sklearn.metrics import f1_score

def plot_contours(X):
    x0_coords = np.linspace(np.min(X[:, 0]), np.max(X[:, 0]), 100)
    x1_coords = np.linspace(np.min(X[:, 1]), np.max(X[:, 1]), 100)
    X0, X1 = np.meshgrid(x0_coords, x1_coords)
    Z = multivariate_normal.pdf(np.vstack((X0.ravel(), X1.ravel())).T, mu, sigma2)
    plt.contour(X0, X1, Z.reshape(X0.shape), np.power(10.0, np.arange(-20, 0, 3)))
    
    

# Load data and visualize
data = loadmat("../../data/mlpas/ex8data1.mat")
X = data["X"]
#plt.scatter(X[:, 0], X[:, 1])
#plt.xlabel("Latency (ms)")
#plt.ylabel("Thruput (mb/s)")
#plt.show()

# Model data distribution
mu = np.mean(X, axis=0)
sigma2 = np.cov(X, rowvar=0)
p = multivariate_normal.pdf(X, mu, sigma2)

Xval = data["Xval"]
yval = data["yval"]

# Cross-validation to find best threshold epsilon
pval = multivariate_normal.pdf(Xval, mu, sigma2)
best_epsilon = None
best_f1 = 0
for epsilon in np.linspace(np.min(pval), np.max(pval), 1000):
    ypred = (pval < epsilon).astype(float)
    f1 = f1_score(yval, ypred)
    if f1 > best_f1:
        best_f1 = f1
        best_epsilon = epsilon
print "Best epsilon:", best_epsilon
print "Best F1 score:", best_f1

# Find outliers in training set and plot
outliers = np.where(p < best_epsilon)[0]
print "Outliers:\n", outliers

plt.scatter(X[:, 0], X[:, 1])
plot_contours(X)
plt.scatter(X[outliers, 0], X[outliers, 1], marker='o', s=10, color='r')
plt.xlabel("Latency (ms)")
plt.ylabel("Thruput (mb/s)")
plt.show()

# Repeat on larger dataset
data = loadmat("../../data/mlpas/ex8data2.mat")
X = data["X"]
Xval = data["Xval"]
yval = data["yval"]

mu = np.mean(X, axis=0)
sigma2 = np.cov(X, rowvar=0)
p = multivariate_normal.pdf(X, mu, sigma2)

pval = multivariate_normal.pdf(Xval, mu, sigma2)
best_epsilon = None
best_f1 = 0
for epsilon in np.linspace(np.min(pval), np.max(pval), 1000):
    ypred = (pval < epsilon).astype(float)
    f1 = f1_score(yval, ypred)
    if f1 > best_f1:
        best_f1 = f1
        best_epsilon = epsilon

print "Best epsilon (large dataset):", best_epsilon
print "Best F1 score (large dataset):", best_f1

outliers = np.where(p < best_epsilon)[0]
print "outliers:\n", outliers
