from __future__ import division

import math

import glob
import numpy as np
import pandas as pd
import scipy.io as sio
import sklearn.cross_validation as scv
from sklearn.ensemble import RandomForestRegressor
import sklearn.linear_model as slm

def getX(fpattern):
  """
  Concatenates all the MatrixMarket files into one large X matrix
  """
  print "...(getting X)"
  fnames = sorted([fname for fname in glob.glob(fpattern)])
  vectors = map(lambda fname: sio.mmread(open(fname, 'rb')), fnames)
  nrows = np.shape(vectors[0])[0]
  for vector in vectors:
    nrows = np.shape(vector)[0]
  X = np.zeros((nrows, 1))
  for vector in vectors:
    X = np.hstack((X, vector.todense()))
  X = X[:, 1:]
  print "X.shape=", np.shape(X)
  return X
    
def getY(fin):
  """
  Reads the outcome (normalized salary) from training file.
  """
  print "...(getting y)"
  df = pd.read_csv(fin)
  sal_norm = df.SalaryNormalized
  nrows = len(sal_norm)
  y = np.zeros((nrows))
  for i in range(0, nrows):
    y[i] = sal_norm[i]
  print "y.shape=", np.shape(y)
  return y

def getIds(fin):
  """
  Reads the job ID from the training file.
  """
  print "...(getting ids)"
  df = pd.read_csv(fin)
  return df.Id

def train():
  X = getX("../data/Train.*.mtx")
  y = getY("../data/Train.csv")
  reg = slm.LinearRegression()
  reg.fit(X, y)
  return reg

def cross_validate():
  X = getX("../data/Train.*.mtx")
  y = getY("../data/Train.csv")
  nrows = np.shape(X)[0]
  kfold = scv.KFold(nrows, 10)
  amae = 0
  run = 0
  for train, test in kfold:
    Xtrain, Xtest, ytrain, ytest = X[train], X[test], y[train], y[test]
#    reg = slm.LinearRegression().fit(Xtrain, ytrain)
#    reg = slm.Ridge().fit(Xtrain, ytrain)
#    reg = slm.ElasticNet(alpha=0.1).fit(Xtrain, ytrain)
#    reg = slm.SGDRegressor().fit(Xtrain, ytrain)
#    reg = slm.ARDRegression(n_iter=10).fit(Xtrain, ytrain)
#    reg = svm.SVR(C=1.0, epsilon=0.2).fit(Xtrain, ytrain)
    reg = RandomForestRegressor(n_estimators=50,
      verbose=2, n_jobs=1, min_samples_split=30, random_state=3465343)
    ntest = len(ytest)
    mae = 0
    for i in range(0, ntest):
      yt = reg.predict(Xtest[i, :])
      mae += math.fabs(yt - ytest[i])
    mae = mae / ntest
    print "Mean Abs Error (run %d) = %f" % (run, mae)
    run += 1
    amae += mae
    break
  print "MAE =", (amae / run)

def test(reg):
  X = getX("../data/Valid.*.mtx")
  y = reg.predict(X)
  ids = getIds("../data/Valid.csv")
  fout = open("../data/result.csv", 'wb')
  fout.write(",".join(["Id", "SalaryNormalized"]) + "\n")
  for i in range(0, np.shape(y)[0]):
    fout.write(",".join([str(ids[i]), str(y[i])]) + "\n")
  fout.close()

def main():
  cross_validate()
#  reg = train()
#  test(reg)

if __name__ == "__main__":
  main()
