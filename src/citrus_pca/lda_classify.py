from sklearn.cross_validation import train_test_split, KFold
from sklearn.lda import LDA
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

DATA_DIR = "../../data/citrus_pca"

cvdf = pd.read_csv(os.path.join(DATA_DIR, "Citrus_Varieties.txt"))
y_species = np.asarray(cvdf["class"])
y_plant = np.asarray(cvdf["plant"])
X = np.matrix(cvdf[cvdf.columns[3:]])

wavelengths = np.loadtxt(os.path.join(DATA_DIR, "Citrus_Varieties_Wavelengths.txt"))

# Reduce to 2 dimensions and visualize
scaler = StandardScaler()
Xscaled = scaler.fit_transform(X)

U, s, V = np.linalg.svd(Xscaled)
Ured = U[:, 0:2]
Sred = np.diag(s[0:2])
Xproj = np.dot(Ured, Sred)

species_ids = np.unique(y_species)
print "species_ids:", species_ids
colors = ['b', 'g', 'r', 'c', 'm', 'y']
i = 0
for species_id in species_ids:
    Xpart = Xproj[np.where(y_species == species_id)[0], :]
    plt.scatter(Xpart[:, 0], Xpart[:, 1], color=colors[i])
    i = i + 1
plt.title("Citrus Species (first 2 Principal Components)")
plt.xlabel("X0")
plt.ylabel("X1")
plt.show()

# Perform multiclass LDA 
Xtrain, Xtest, ytrain, ytest = train_test_split(Xscaled, y_species, 
                                                test_size=0.25, random_state=42)
clf = LDA(len(species_ids))
clf.fit(Xtrain, ytrain)
ypred = clf.predict(Xtest)
print "LDA Accuracy Score: %.3f" % (accuracy_score(ypred, ytest))

# What varieties are most spectrally similar?
corr = np.corrcoef(clf.means_)
plt.imshow(corr, interpolation="nearest", cmap=plt.cm.cool)
plt.xticks(np.arange(len(species_ids)), species_ids, rotation=45)
plt.yticks(np.arange(len(species_ids)), species_ids)
plt.colorbar()
plt.show()

# Find LDA classifier accuracy using cross validation
kfold = KFold(Xscaled.shape[0], 10)
scores = []
for train, test in kfold:
    Xtrain, Xtest, ytrain, ytest = Xscaled[train], Xscaled[test], \
        y_species[train], y_species[test]
    clf = LDA(len(species_ids))
    clf.fit(Xtrain, ytrain)
    ypred = clf.predict(Xtest)
    scores.append(accuracy_score(ypred, ytest))
print "LDA accuracy predicting species: %.3f" % (1.0 * sum(scores) / len(scores))

# Find LDA classifier accuracy for predicting specific plants
kfold = KFold(Xscaled.shape[0], 10)
scores = []
for train, test in kfold:
    Xtrain, Xtest, ytrain, ytest = Xscaled[train], Xscaled[test], \
        y_plant[train], y_plant[test]
    clf = LDA(len(species_ids))
    clf.fit(Xtrain, ytrain)
    ypred = clf.predict(Xtest)
    scores.append(accuracy_score(ypred, ytest))
print "LDA accuracy predicting plants: %.3f" % (1.0 * sum(scores) / len(scores))
