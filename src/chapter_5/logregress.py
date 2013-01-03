from __future__ import division
from numpy import *

def loadDataSet():
  data = []
  labels = []
  for line in open("testSet.txt").readlines():
    linearr = line.strip().split()
    data.append((1.0, float(linearr[0]), float(linearr[1])))
    labels.append(int(linearr[2]))
  return data, labels

def sigmoid(x):
  return 1.0 / (1 + exp(-x))

def gradAscent(data, labels, alpha=0.001, iterations=500):
  datamatrix = mat(data)
  labelmatrix = mat(labels).transpose()
  n = shape(datamatrix)[1]
  weights = ones ((n, 1))
  for k in range(0, iterations):
     h = sigmoid(datamatrix * weights)
     error = labelmatrix - h
     weights = weights + (alpha * datamatrix.transpose() * error)
  return weights

def stocGradAscent0(data, labels, alpha=0.01):
  """ single pass, use one record at a time instead of entire matrix """
  datamatrix = array(data)
  m, n = shape(datamatrix)
  weights = ones(n)
  for i in range(0, m):
    h = sigmoid(sum(datamatrix[i] * weights))
    error = labels[i] - h
    weights = weights + (alpha * error * datamatrix[i])
  return weights

def stocGradAscent1(data, labels, iterations=200):
  """ multi pass, varying alpha and use random record order """
  datamatrix = array(data)
  m, n = shape(datamatrix)
  weights = ones(n)
  for j in range(0, iterations):
    dataidx = range(0, m)
    for i in range(0, m):
      alpha = 0.01 + (4 / 1.0 + j + i)
      randidx = int(random.uniform(0, len(dataidx)))
      h = sigmoid(sum(datamatrix[randidx] * weights))
      error = labels[randidx] - h
      weights = weights + (alpha * error * datamatrix[randidx])
      del(dataidx[randidx])
  return weights

def plotBestFit(weights):
  import matplotlib.pyplot as plt
  data, labels = loadDataSet()
  datamatrix = mat(data)
  x1s = []; y1s = []; x2s = []; y2s = []
  for i in range(0, shape(data)[0]):
    if int(labels[i]) == 1:
      x1s.append(datamatrix[i, 1])
      y1s.append(datamatrix[i, 2])
    else:
      x2s.append(datamatrix[i, 1])
      y2s.append(datamatrix[i, 2])
  fig = plt.figure()
  ax = fig.add_subplot(111)
  # show the scatter plots
  ax.scatter(x1s, y1s, s=30, c="red")
  ax.scatter(x2s, y2s, s=30, c="green")
  # define an arbitary x vector range from -3 to +2 step 0.1
  xs = arange(-3.0, 3.0, 0.1)
  # assuming a line w(0) + w(1)*x + w(2)*y = 0, and solving for y
  ys = -(weights[0] + (weights[1] * xs)) / weights[2]
  ax.plot(xs, ys)
  plt.xlabel('X1')
  plt.ylabel('X2')
  plt.show()

def classify(xs, weights):
  prob = sigmoid(sum(xs * weights))
  return 1.0 if prob > 0.5 else 0.0

def colicTest():
  traindata = []
  trainlabels = []
  for line in open("horseColicTraining.txt", 'rb').readlines():
    cols = line.strip().split("\t")
    features = map(lambda x: float(x), cols[0:21])
    traindata.append(features)
    trainlabels.append(float(cols[21]))
  weights = stocGradAscent1(array(traindata), trainlabels, 500)
  errorCount = 0
  numTestVecs = 0
  for line in open("horseColicTest.txt", 'rb').readlines():
    numTestVecs += 1
    cols = line.strip().split("\t")
    features = map(lambda x: float(x), cols[0:21])
    actlabel = int(classify(array(features), weights))
    if actlabel != int(cols[21]):
      errorCount += 1
  errorRate = errorCount / numTestVecs
  print "error rate=%f" % (errorRate)
  return errorRate

def multiColicTest():
  numTests = 10
  errorSum = 0.0
  for k in range(0, numTests):
    errorSum += colicTest()
  print "Average error rate=%f" % (errorSum / numTests)
    
## Gradient Ascent
#data, labels = loadDataSet()
#weights = gradAscent(data, labels)
#plotBestFit(weights.getA())

## Stochastic Gradient Ascent
#data, labels = loadDataSet()
#weights = stocGradAscent0(data, labels)
#plotBestFit(weights)

## Stochastic Gradient Ascent varying alpha and random indexes
#data, labels = loadDataSet()
#weights = stocGradAscent1(data, labels)
#plotBestFit(weights)

multiColicTest()