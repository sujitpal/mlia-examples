from __future__ import division
from numpy import *

def loadDataSet(filename, delim="\t"):
  f = open(filename)
  lines = [line.strip().split(delim) for line in f.readlines()]
  data = [map(lambda x: float(x), line) for line in lines]
  return matrix(data)

def pca(datamatrix, topNFeat=999999):
  print datamatrix
  meanVals = mean(datamatrix, axis=0)
  meanRemoved = datamatrix - meanVals
  covMat = cov(meanRemoved, rowvar=0)
  eigVals, eigVects = linalg.eig(mat(covMat))
  eigValInd = argsort(eigVals)
  eigValInd = eigValInd[:-(topNFeat-1):-1]
  redEigVects = eigVects[:, eigValInd]
  lowDDataMatrix = meanRemoved * redEigVects
  reconMatrix = (lowDDataMatrix * redEigVects.T) + meanVals
  return lowDDataMatrix, reconMatrix

def plot(dataMat, reconMat):
  import matplotlib
  import matplotlib.pyplot as plt
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.scatter(dataMat[:, 0].flatten().A[0], dataMat[:, 1].flatten().A[0],
    marker='^', s=90)
  ax.scatter(reconMat[:, 0].flatten().A[0], reconMat[:, 1].flatten().A[0],
    marker="o", s=50, c="red")
  plt.show()

def replaceNaNWithMean(dataMat):
  numFeat = shape(dataMat)[1]
  for i in range(0, numFeat):
    meanVal = mean(dataMat[nonzero(~isnan(dataMat[:, i].A))[0], i])
    dataMat[nonzero(isnan(dataMat[:, i].A))[0], i] = meanVal
  return dataMat

def plot_eigenValues(eigenVals, ylim=-1):
  import matplotlib
  import matplotlib.pyplot as plt
  fig = plt.figure()
  ax = fig.add_subplot(111)
  xs = []
  ys = []
  rmax = len(eigenVals) if ylim == -1 else ylim
  for i in range(0, rmax):
    xs.append(i)
    ys.append(eigenVals[i])
  ax.plot(xs, ys, c="b")
  plt.show()
  
#dataMat = loadDataSet("testSet.txt")
##print dataMat
#dataMat = replaceNaNWithMean(dataMat)
#lowDMat, reconMat = pca(dataMat, 1)
#print lowDMat
#plot(dataMat, reconMat)

dataMat = loadDataSet("secom.data", " ")
#print dataMat
dataMat = replaceNaNWithMean(dataMat)

### calculate eigenvalue and eigenvectors
#meanVals = mean(dataMat, axis=0)
#meanRemoved = dataMat - meanVals
#covMat = cov(meanRemoved, rowvar=0)
#eigVals, eigVecs = linalg.eig(mat(covMat))
#plot_eigenValues(eigVals, 20)

# since 96% of the variance contained in first 6 comps
lowDMat, reconMat = pca(dataMat, 6)
print "shape(dataMat)=", shape(dataMat)
print "shape(lowDMat)=", shape(lowDMat)
print "shape(reconMat)=", shape(reconMat)
