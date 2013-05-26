from __future__ import division

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cross_validation import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import RidgeClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

N_TRAIN_ROWS = 139
N_FEATURES = 204355
N_FOLDS = 10

ethCode = {
  "CEU": 0, "GIH": 1, "JPT": 2, "ASW": 3, "YRI": 4
}

def load(filename, numInstances, numFeatures):
  headerLines = 3
  ftrain = open(filename, 'rb')
  X = np.zeros((numInstances, numFeatures))
  y = np.zeros((numInstances,))
  i = 0
  for line in ftrain:
    i += 1
    if i <= headerLines:
      continue
    line = line.strip()
    cols = line.split("\t")
    y[i - headerLines - 1] = ethCode[cols[0]]
    for j in range(1, len(cols) - 1):
      if cols[j] == "1":
        X[i - headerLines - 1, j] = cols[j]
  ftrain.close()
  return X, y

def evaluate(X, y, nfolds, clf, nfeats, clfname, scoreFunc):
  kfold = KFold(X.shape[0], n_folds=nfolds)
  acc = 0
  i = 0
  print("%s (#-features=%d)..." % (clfname, nfeats))
  for train, test in kfold:
    i += 1
    Xtrain, Xtest, ytrain, ytest = X[test], X[train], y[test], y[train]
    clf.fit(Xtrain, ytrain)
    ypred = clf.predict(Xtest)
    score = accuracy_score(ytest, ypred)
    print "  Fold #%d, accuracy=%f" % (i, score)
    acc += score
  acc /= nfolds
  print "## %s (#-features=%d) accuracy=%f" % (clfname, nfeats, acc)
  return acc

def plot(accuracies, xvals, legends):
  fig = plt.figure()
  ax = fig.add_subplot(111)
  cm = [color + marker
    for color in ["b", "g", "r", "c", "m", "y", "b"]
    for marker in ["o", "D"]]
  for i in range(0, accuracies.shape[0]):
    ax.plot(xvals, accuracies[i, :], color=cm[i][0], 
      marker=cm[i][1], label=legends[i])
  plt.xlabel("#-Features")
  plt.ylabel("Accuracy")
  plt.title("Accuracy vs #-Features for different classifiers")
  ax.set_xscale("log")
  box = ax.get_position()
  ax.set_position([box.x0, box.y0 + box.height * 0.3,
    box.width, box.height * 0.7])
  ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15),
    fancybox=True, shadow=True, ncol=3)
  plt.show()
  
def main():
  X, y = load("genestrain.tab", N_TRAIN_ROWS, N_FEATURES)
  nFeatures = np.array([N_FEATURES, 50000, 5000, 500, 50, 10])
  clfs = [
    BernoulliNB(),
    MultinomialNB(),
    GaussianNB(),
    DecisionTreeClassifier(),
    RandomForestClassifier(n_estimators=10),
    OneVsRestClassifier(LinearSVC(random_state=0)),
    OneVsRestClassifier(LogisticRegression()),
    OneVsRestClassifier(SGDClassifier()),
    OneVsRestClassifier(RidgeClassifier()),
  ]
  clfnames = map(lambda x: type(x).__name__
    if type(x).__name__ != 'OneVsRestClassifier'
    else type(x.estimator).__name__, clfs)
  scoreFuncs = [chi2, f_classif]
  accuracies = np.zeros((len(clfs), len(nFeatures), len(scoreFuncs)))
  for k in range(0, len(scoreFuncs)):
    Xtrunc = X.copy()
    for j in range(0, len(nFeatures)):
      if nFeatures[j] != N_FEATURES:
        featureSelector = SelectKBest(score_func=scoreFuncs[k], k=nFeatures[j])
        Xtrunc = featureSelector.fit_transform(X, y)
      for i in range(0, len(clfs)):
        accuracies[i, j, k] = evaluate(Xtrunc, y, N_FOLDS, clfs[i],
          nFeatures[j], clfnames[i], scoreFuncs[k])
  # print out accuracy matrix
  for k in range(0, len(scoreFuncs)):
    for i in range(0, len(clfs)):
      print "%22s " % clfnames[i],
      for j in range(0, accuracies.shape[1]):
        print "%5.3f" % accuracies[i, j, k],
      print
    plot(accuracies[:, :, k], nFeatures, clfnames)

if __name__ == "__main__":
  main()
