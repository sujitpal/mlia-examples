from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from operator import itemgetter
from scipy.io import loadmat
from sklearn.svm import SVC
from sklearn.metrics.pairwise import rbf_kernel
from sklearn.metrics import accuracy_score

def plot_data(X, y):
    # two scatter plots of subsets of X based on value of y
    Xneg = X[np.where(y == 0)[0], :]
    Xpos = X[np.where(y == 1)[0], :]
    plt.scatter(Xneg[:, 0], Xneg[:, 1], c='r')
    plt.scatter(Xpos[:, 0], Xpos[:, 1], c='c')
    
def visualize_boundary(X, y, clf):
    # Code adapted from:
    # http://stackoverflow.com/questions/22294241/plotting-a-decision-boundary-separating-2-classes-using-matplotlibs-pyplot
    plot_data(X, y)
    step = 0.01
    x0 = np.arange(np.min(X[:, 0]) - step, np.max(X[:, 0]) + step, step)
    x1 = np.arange(np.min(X[:, 1]) - step, np.max(X[:, 1]) + step, step)    
    X0, X1 = np.meshgrid(x0, x1)
    Z = clf.predict(np.c_[X0.ravel(), X1.ravel()])
    Z = Z.reshape(X0.shape)
    plt.contour(X0, X1, Z, levels=[0.0])
    plt.title("SVC (kernel=%s, c=%d)" % (clf.kernel, clf.C))    

def compute_gamma(sigma):
    return (1.0 / (2.0 * np.power(sigma, 2)))
    

# Load and Visualize dataset 1
data = loadmat("../../data/mlpas/ex6data1.mat")

X = data["X"]
y = data["y"]
plot_data(X, y)
plt.show()

# Train linear SVM
for c in [1.0, 100.0, 1000.0]:
    clf = SVC(C=c, kernel="linear")
    clf.fit(X, np.ravel(y))
    visualize_boundary(X, y, clf)
    plt.show()

# Implement Gaussian Kernel (aka RBF kernel)
x = np.matrix([1, 2, 1])
y = np.matrix([0, 4, -1])
sigma = 2.0 # gamma is 1/2*sigma^2
k_xy = rbf_kernel(x, y, gamma=compute_gamma(sigma))
print k_xy

# Load and Visualizing Dataset 2
data = loadmat("../../data/mlpas/ex6data2.mat")
X = data["X"]
y = data["y"]
plot_data(X, y)
plt.show()

# Train SVM with RBF kernel
sigma = 0.1
clf = SVC(C=1.0, gamma=compute_gamma(sigma), kernel='rbf')
clf.fit(X, y.ravel())
visualize_boundary(X, y, clf)
plt.show()

# Load and visualize Dataset 3
data = loadmat("../../data/mlpas/ex6data3.mat")
X = data["X"]
y = data["y"]
Xval = data["Xval"]
yval = data["yval"]
plot_data(X, y)
plt.show()

clf_scores = []
for c in [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]:
    for sigma in [0.01, 0.03, 0.1, 0.3, 1, 3, 10, 30]:
        clf = SVC(C=c, gamma=compute_gamma(sigma), kernel='rbf')
        clf.fit(X, y.ravel())
        ypred = clf.predict(Xval)
        accuracy = accuracy_score(yval, ypred)
        clf_scores.append((c, sigma, accuracy))
print "best estimator:", sorted(clf_scores, key=itemgetter(2), reverse=True)[0]        

clf = SVC(C=1.0, gamma=compute_gamma(0.1), kernel='rbf')
clf.fit(X, y.ravel())
visualize_boundary(X, y, clf)
