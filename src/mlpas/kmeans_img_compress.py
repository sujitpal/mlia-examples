from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from scipy.io import loadmat
from sklearn.cluster import KMeans

def plot_clusters(X, y, centroids, K, i):
    colors = ["r", "m", "c"]
    for k in range(0, K):
        Xsub = X[np.where(y == k)[0], :]
        plt.scatter(Xsub[:, 0], Xsub[:, 1], c=colors[k], marker="o")
        plt.scatter(centroids[k][0], centroids[k][1], color='k', marker="+", s=300) 
    plt.xlabel("X[:, 0]")
    plt.ylabel("X[:, 1]")
    plt.title("KMeans Clusters (iteration=%d)" % (i))
    plt.show()
    
def recover_image(X, centroids, labels):
    # replace wach X with the corresponding centroid it belongs to.
    return centroids[labels, :]

def plot_image_subplot(X, title, nrows, ncols, plot_num):
    ax = plt.subplot(nrows, ncols, plot_num)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    plt.imshow(X)
    plt.title(title)


data = loadmat("../../data/mlpas/ex7data2.mat")
X = data["X"]

# Run KMeans with specified parameters
K = 3
init_centroids = np.matrix("2 2; 5 1; 7 4")
kmeans = KMeans(n_clusters=K, n_init=1, init=init_centroids)
kmeans.fit(X)

# Visualize
plot_clusters(X, kmeans.labels_, kmeans.cluster_centers_, K, 10)
labels = kmeans.labels_
print "Closest centroid for first 3 points:", labels[0:3]

# Plot inertia of KMeans, varying the number of iterations
xs = range(1, 11)
ys = []
for curr_iter in xs:
    kmeans = KMeans(n_clusters=K, n_init=1, max_iter=curr_iter, 
                    init=init_centroids)
    kmeans.fit(X)
#    plot_clusters(X, kmeans.labels_, kmeans.cluster_centers_, K, curr_iter)
    ys.append(kmeans.inertia_)
plt.plot(xs, ys, "b-")
plt.xlabel("Number of iterations")
plt.ylabel("Inertia of resulting clusters")
plt.show()

# Image compression with KMeans
# By clustering the colors into a fixed set of smaller colors, the original
# X matrix of pixels can be approximated by a smaller set of centroids and 
# labels, from which the approximate X can be recovered (see recover_image).

# Load image from .mat file
Xorig = plt.imread("../../data/mlpas/ex7_bird_small.png")
Xorig / 255
img_size = Xorig.shape[0]
X = np.reshape(Xorig, (img_size * img_size, 3))

# Run KMeans with different values of K (compression levels) and plot
# resulting image (first one is the original image)
plot_image_subplot(Xorig, "Original", 2, 2, 1)
plot_num = 1
for k in [16, 8, 4]:
    kmeans = KMeans(n_clusters=16, max_iter=10, init="random")
    kmeans.fit(X)
    Xrecover = recover_image(X, kmeans.cluster_centers_, kmeans.labels_)
    Xrecover = np.reshape(Xrecover, (img_size, img_size, 3))
    plot_num += 1
    plot_image_subplot(Xrecover, "Compressed (%d colors)" % (k), 2, 2, plot_num)    
plt.show()
