from sklearn.cross_validation import KFold
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import random

DATA_DIR = "../../data/citrus_pca"

def plot_by_class(X, y, w):
    """Plot reflectance across wavelengths for citrus vs non-citrus"""
    viz_df = pd.DataFrame()
    viz_df["wavelength"] = w
    colnames = {1: "citrus", 2: "noncit"}
    for yval in range(1,3):
        Xc = X[np.where(y == yval)[0], :]
        xmin = np.min(Xc, axis=0)
        xavg = np.mean(Xc, axis=0)
        xmax = np.max(Xc, axis=0)
        viz_df[colnames[yval] + "_min"] = xmin.T
        viz_df[colnames[yval] + "_avg"] = xavg.T
        viz_df[colnames[yval] + "_max"] = xmax.T
    plt.subplot(211)
    viz_df.plot(x="wavelength", y=["citrus_min", "citrus_avg", "citrus_max"],
                title="Citrus Plants", style=["r--", "b", "g--"])
    plt.xticks([])
    plt.xlabel("")
    plt.ylabel("reflectance")
    plt.subplot(212)
    viz_df.plot(x="wavelength", y=["noncit_min", "noncit_avg", "noncit_max"],
                title="Non-Citrus Plants", style=["r--", "b", "g--"])
    plt.ylabel("reflectance")
    plt.show()
    
def plot_random_plants(X, y, w, n):
    """Plot reflectance vs wavelengths for n random plants"""
    viz_df = pd.DataFrame()
    viz_df["wavelength"] = w
    # generate n random plant ids
    plant_ids = set()
    num_unique = len(np.unique(y))
    while len(plant_ids) < n:
        plant_ids.add(int(num_unique * random.random()))
    # for each plant plot mean value of wavelengths
    plant_ids_lst = list(plant_ids)
    pcols = []
    for i in range(n):
        Xp = X[np.where(y == plant_ids_lst[i])[0], :]
        xavg = np.mean(Xp, axis=0)
        pcols.append("p" + str(i))
        viz_df["p" + str(i)] = xavg.T
    viz_df.plot(x="wavelength", y=pcols, title="Mean for %d random plants" % (n))
    plt.ylabel("reflectance")        
    plt.show()
    
def plot_correlations_as_heatmap(X):
    """Plots heatmap from blue (low) to pink (high)"""
    corr = np.corrcoef(X)
    plt.imshow(corr, interpolation="nearest", cmap=plt.cm.cool)
    plt.xticks(())
    plt.yticks(())
    plt.title("Correlation Matrix")
    plt.colorbar()
    plt.show()
    
def plot_fraction_of_variance_explained(s, n):
    """Plot the first n values of eigenvalue s as fraction of total"""
    fve = s / np.cumsum(s)[-1]
    plt.plot(np.arange(len(fve))[0:n], fve[0:n])
    plt.title("Eigenvalue Decay")
    plt.xlabel("Principal Eigenvalues")
    plt.ylabel("Fraction of Variance Explained")
    plt.show()
    return fve
    
def project_data(X, U, k):
    Ured = U[:, 0:k]
    Sred = np.diag(s[0:k])
    return np.dot(Ured, Sred)

def recover_data(Xred, V, k):
    Vred = V[0:k, :]
    return np.dot(Xred, Vred)
    
def plot_scatter_plots(X, y, title):
    pairs = [(0, 1), (1, 2), (0, 2)]
    Xparts = [X[np.where(y == 1)[0], :], X[np.where(y == 2)[0], :]]
    for i in range(len(pairs)):
        plt.subplot(1, 3, i + 1)
        for j in range(len(Xparts)):
            ecol = 'b' if j == 0 else 'r'
            plt.scatter(Xparts[j][:, pairs[i][0]], Xparts[j][:, pairs[i][1]], 
                        s=10, edgecolors=ecol, facecolors='none')
        if i == 1:
            plt.title(title)
        plt.xlabel("X" + str(pairs[i][0]))
        plt.ylabel("X" + str(pairs[i][1]))
        plt.xticks(())
        plt.yticks(())
        i = i + 1
    plt.show()

def evaluate_classification(X, y):
    """Evaluate classifier using 10 fold cross validation"""
    kfold = KFold(X.shape[0], 3)
    scores = []
    for train, test in kfold:
        Xtrain, Xtest, ytrain, ytest = X[train], X[test], y_class[train], y_class[test]
        clf = SVC()  # rbf kernel default
        clf.fit(Xtrain, ytrain)
        ypred = clf.predict(Xtest)
        scores.append(accuracy_score(ypred, ytest))
    return 1.0 * sum(scores) / len(scores)
    

cid_df = pd.read_csv(os.path.join(DATA_DIR, "Citrus_Identification_Data.txt"))
y_class = np.asarray(cid_df["class"])
y_plant = np.asarray(cid_df["plant"])
X = np.matrix(cid_df[cid_df.columns[3:]])  # capture the bNNN cols (representing wavelengths)

wavelengths = np.loadtxt(os.path.join(DATA_DIR, "Citrus_Identification_Wavelengths.txt"))

# How many classes?
print "#-classes:", len(np.unique(y_class))
print "#-plants:", len(np.unique(y_plant))

# Plot reflectance vs wavelength for citrus vs non-citrus plants
plot_by_class(X, y_class, wavelengths)

## Plot Reflectace vs Wavelengths for 10 random plants on same chart
plot_random_plants(X, y_plant, wavelengths, 10)

# plot heat map of correlations between features
scaler = StandardScaler()
Xscaled = scaler.fit_transform(X)
plot_correlations_as_heatmap(Xscaled)

# Perform a PCA on the (scaled) matrix
U, s, V = np.linalg.svd(Xscaled)

# Plot eigenvalue decay (as fraction of variance explained)
fve = plot_fraction_of_variance_explained(s, 50)

# Project dataset onto first k components
k = 10
print "Variance explained with %d principal components = %0.3f" % (k, np.sum(fve[0:k]))

# Project Xscaled to first k dimensions
Xprojected = project_data(Xscaled, U, k)
plot_by_class(Xprojected, y_class, np.arange(k))

# Scatter plot between 1/2. 2/3, 1/3
plot_scatter_plots(Xscaled, y_class, "Original Data")
plot_scatter_plots(Xprojected, y_class, "Projected Data")

# Train classifier on original data with 10-fold cross validation
score_orig = evaluate_classification(Xscaled, y_class)
score_pca = evaluate_classification(Xprojected, y_class)
print "Classification accuracy: original: %.3f, after PCA: %.3f" % (score_orig, score_pca)
# score moves up from 0.84 to 0.86
