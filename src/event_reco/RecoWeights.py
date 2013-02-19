from __future__ import division

import math

import numpy as np
import pandas as pd

from sklearn.cross_validation import KFold
from sklearn.linear_model import SGDClassifier

def train():
  """
  Trains a classifier on the entire (modified) training dataset.
  Since our objective is to predict only interested users, we
  only consider the outcome 1=interested and 0=not.
  """
  trainDf = pd.read_csv("../NewData/train.csv")
  X = np.matrix(pd.DataFrame(trainDf, index=None,
    columns=["invited", "user_reco", "evt_p_reco", "evt_c_reco",
    "user_pop", "frnd_infl", "evt_pop"]))
  y = np.array(trainDf.interested)
  clf = SGDClassifier(loss="log", penalty="l2")
  clf.fit(X, y)
  return clf

def validate():
  """
  Runs a 10-fold cross validation on the classifier, reporting
  accuracy.
  """
  trainDf = pd.read_csv("../NewData/train.csv")
  X = np.matrix(pd.DataFrame(trainDf, index=None,
    columns=["invited", "user_reco", "evt_p_reco", "evt_c_reco",
    "user_pop", "frnd_infl", "evt_pop"]))
  y = np.array(trainDf.interested)
  nrows = len(trainDf)
  kfold = KFold(nrows, 10)
  avgAccuracy = 0
  run = 0
  for train, test in kfold:
    Xtrain, Xtest, ytrain, ytest = X[train], X[test], y[train], y[test]
    clf = SGDClassifier(loss="log", penalty="l2")
    clf.fit(Xtrain, ytrain)
    accuracy = 0
    ntest = len(ytest)
    for i in range(0, ntest):
      yt = clf.predict(Xtest[i, :])
      if yt == ytest[i]:
        accuracy += 1
    accuracy = accuracy / ntest
    print "accuracy (run %d): %f" % (run, accuracy)
    avgAccuracy += accuracy
    run += 1
  print "Average accuracy", (avgAccuracy / run)

def test(clf):
  """
  Reads the X values from the dataframe provided, then uses the
  trained classifier to write an array of outcomes.
  """
  origTestDf = pd.read_csv("../Data/test.csv")
  users = origTestDf.user
  events = origTestDf.event
  testDf = pd.read_csv("../NewData/test.csv")
  fout = open("../NewData/result.csv", 'wb')
  fout.write(",".join(["user", "event", "outcome", "dist"]) + "\n")
  nrows = len(testDf)
  Xp = np.matrix(testDf)
  yp = np.zeros((nrows, 2))
  for i in range(0, nrows):
    xp = Xp[i, :]
    yp[i, 0] = clf.predict(xp)
    yp[i, 1] = clf.decision_function(xp)
    fout.write(",".join(map(lambda x: str(x), 
      [users[i], events[i], yp[i, 0], yp[i, 1]])) + "\n")
  fout.close()

def main():
#  validate()
  clf = train()
  test(clf)

if __name__ == "__main__":
  main()