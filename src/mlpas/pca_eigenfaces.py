from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from scipy.io import loadmat
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def plot_line(p1, p2):
    xs = [p1[0], p2[0]]
    ys = [p1[1], p2[1]]
    plt.plot(xs, ys, "-k", linewidth=2)
    
def project_data(U, s, k):
    Ured = U[:, 0:k]
    Sred = np.diag(s[0:k])
    return np.dot(Ured, Sred)
    
def recover_data(Xred, V, k):
    Vred = V[0:k, :]
    return np.dot(Xred, Vred)
    
def display_faces(X, k, title):
    pixwidth = int(np.sqrt(k))
    fig, ax = plt.subplots(10, 10)    
    for i in range(10):
        for j in range(10):
            idx = (i * 10) + j
            img = np.reshape(X[idx, :], (pixwidth, pixwidth)).T
            ax[i, j].set_axis_off()
            ax[i, j].imshow(img, aspect="auto", cmap="gray")
    plt.show()
    

# Load and visualize 2 dimensional example data
data = loadmat("../../data/mlpas/ex7data1.mat")
X = data["X"]

# Normalize features (so mean of each feature is 0 and std dev is 1)
scaler = StandardScaler()
Xscaled = scaler.fit_transform(X)

# Compute covariance matrix for X, then run SVD on it to get the eigenvalues
# and eigenvectors
Sigma = np.cov(Xscaled, rowvar=0, bias=1)
U, s, V = np.linalg.svd(Sigma)

print "Eigenvalues=", s
print "Top Eigenvectors=", U[:, 0]
print "fraction of variance explained", s / np.cumsum(s)[-1]

# Visualize
plt.scatter(Xscaled[:, 0], Xscaled[:, 1])
mu = np.mean(Xscaled, axis=0)
plot_line(mu, mu + 1.5 * s[0] * U[:, 0])
plot_line(mu, mu + 1.5 * s[1] * U[:, 1])
plt.xlabel("Xscaled[0]")
plt.ylabel("Xscaled[1]")
plt.axes().set_aspect("equal")
plt.show()

# Project original data to k dimensions
k = 1
print "rec#1 (original):", Xscaled[0, :]
U, s, V = np.linalg.svd(Xscaled, full_matrices=False)
Xprojected = project_data(Xscaled, U, k).reshape((50, 1))
print "rec#1 (projected):", Xprojected[0, :]
Xrecovered = recover_data(Xprojected, V, k)
print "rec#1 (recovered):", Xrecovered[0, :]

# Load faces dataset
faces = loadmat("../../data/mlpas/ex7faces.mat")
X = faces["X"]
display_faces(X, 1024, "Original")

# Decompose images to have top 36 (6 x 6) pixels
U, s, V = np.linalg.svd(X, full_matrices=False)
Xprojected = project_data(U, s, 100)
display_faces(Xprojected, 100, "Projected to top 100")
Xrecovered = recover_data(Xprojected, V, 100)
display_faces(Xrecovered, 1024, "Recovered from top 100")

# Plot percentage of variance explained
xs = range(s.shape[0])
ys = (100.0 * s**2) / np.cumsum(s**2)
plt.plot(xs[0:100], ys[0:100], "b-")
plt.xlabel("K")
plt.ylabel("Percentage of Variance Explained")
plt.show()

# Reduce Bird Image data to 2 dimensions using PCA for visualization
A = plt.imread("../../data/mlpas/ex7_bird_small.png")
A = A / 255
X = np.reshape(A, (A.shape[0] * A.shape[1], 3))
Xscaled = scaler.fit_transform(X)

# Cluster the pixels into 16 clusters
kmeans = KMeans(n_clusters=16)
kmeans.fit(X)
labels = kmeans.labels_

# SVD Decompose to reduce to 2 dimensions and visualize
U, s, V = np.linalg.svd(Xscaled, full_matrices=False)
Xprojected = project_data(U, s, 2)
# sample 1000 random points from each record
sel = np.random.random_integers(0, Xscaled.shape[0], 1000)
Xproj_sampled = Xprojected[sel]
colors = labels[sel]

plt.scatter(Xproj_sampled[:, 0], Xproj_sampled[:, 1], c=colors)
plt.show()

