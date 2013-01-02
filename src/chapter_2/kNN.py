from __future__ import division
from numpy import *
import operator
import os

def createDataSet():
  group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
  labels = ['A', 'A', 'B', 'B']
  return group, labels

def classify0(x, dataSet, labels, k):
  n = dataSet.shape[0] # number of rows in dataset, each row is a point
  # find the distance vector of x from each of the other points
  dists = ((tile(x, (n, 1)) - dataSet) ** 2).sum(axis=1) ** 0.5
  # sort the distance vector by position, then count labels for first K
  # positions
  votes = map(lambda i: labels[i], dists.argsort()[0:k])
  # transform list to map of {label, count}, then sort by value reversed
  # and return the top label. This is the predicted label for the point X.
  counts = {}
  for l in set(labels):
    counts[l] = 0
  for vote in votes:
    counts[vote] += 1
  return sorted(counts.iteritems(),
    key=operator.itemgetter(1), reverse=True)[0][0]

def nlabel(s):
  if s == "largeDoses":
    return 1
  elif s == "smallDoses":
    return 0.5
  else:
    return 0
  
def file2matrix(filename):
  f = open(filename, 'rb')
  n = len(f.readlines())
  f.close()
  matrix = zeros((n, 3))
  labels = []
  index = 0
  f = open(filename, 'rb')
  for line in f.readlines():
    cols = line.strip().split('\t')
    matrix[index, :] = cols[0:3]
    labels.append(nlabel(cols[-1]))
    index += 1
  return matrix, labels

def scatterplot(xs, ys, labels):
  import matplotlib
  import matplotlib.pyplot as plt
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.scatter(xs, ys, c=array(labels))
  ax.scatter
  plt.show()

def autonorm(dataset):
  """
  Transforms all elements in the dataset as x(i,j) - min(row) / range(row).
  Returns the normalized dataset, the range and mins row matrices.
  """
  mins = dataset.min(0)
  range = dataset.max(0) - mins
  n = dataset.shape[0]
  norm = (dataset - tile(mins, (n, 1))) / tile(range, (n, 1))
  return norm, range, mins

def testClassifier(testFile, trainTestRatio):
  """ test the classifier """
  matrix, labels = file2matrix(testFile)
  normMatrix = autonorm(matrix)[0]
  n = matrix.shape[0]
  ntest = int(n * trainTestRatio)
  errorCount = 0
  for i in range(ntest):
    result = classify0(normMatrix[i, :],
      normMatrix[ntest:n, :], labels[ntest:n], 3)
    print "classifier returns: %s, actual: %s" % (result, labels[i])
    if result != labels[i]:
      errorCount += 1
  print "total error rate: ", errorCount / ntest

def classify(person, testFile):
  """ run the classifier """
  matrix, labels = file2matrix(testFile)
  normMatrix, ranges, mins = autonorm(matrix)
  result = classify0(((person - mins) / ranges), matrix, labels, 3)
  print result

def img2vector(filename):
  imgvec = zeros((1, 1024))
  f = open(filename)
  for i in range(0, 32):
    line = f.readline()
    for j in range(0, 32):
      imgvec[0, (32 * i) + j] = int(line[j])
  return imgvec

def testHandwritingClassifier():
  trainfiles = os.listdir("trainingDigits")
  n = len(trainfiles)
  trainmatrix = zeros((n, 1024))
  trainlabels = []
  for i in range(0, n):
    trainmatrix[i, :] = img2vector("trainingDigits/" + trainfiles[i])
    trainlabels.append(trainfiles[i].split('_')[0])
  testfiles = os.listdir("testDigits")
  errorCount = 0
  ntest = len(testfiles)
  for i in range(0, ntest):
    expected = testfiles[i].split('_')[0]
    actual = classify0(img2vector("testDigits/" + testfiles[i]),
      trainmatrix, trainlabels, 3)
    if (expected != actual):
      errorCount += 1
  print "#-errors:", errorCount
  print "error-rate:", errorCount / ntest

#group, labels = createDataSet()
#xlab = classify0([1,1], group, labels, 3)
#print xlab

#matrix, labels = file2matrix("datingTestSet.txt")
#print "matrix=", matrix
#print "labels=", labels
#scatterplot(matrix[:,1], matrix[:,2], labels)

#norm, range, mins = autonorm(matrix)
#print norm
#print range
#print mins

#testClassifier("datingTestSet.txt", 0.1)
#classify([10, 10000, 0.5], "datingTestSet.txt")

#img = img2vector("testDigits/5_0.txt")
#print img

testHandwritingClassifier()