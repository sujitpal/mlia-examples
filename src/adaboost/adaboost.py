from __future__ import division
from numpy import *

def loadSimpleData():
  data = matrix([[ 1. , 2.1],
    [ 2. , 1.1],
    [ 1.3, 1. ],
    [ 1. , 1. ],
    [ 2. , 1. ]])
  labels = [1.0, 1.0, -1.0, -1.0, 1.0]
  return data, labels

def stumpClassify(datamatrix, dims, threshold, threshfunc):
  result = ones((shape(datamatrix)[0], 1))
  if threshfunc == "lt":
    result[datamatrix[:, dims] <= threshold] = -1
  else:
    result[datamatrix[:, dims] > threshold] = -1
  return result

def buildStump(data, labels, D):
  datamatrix = mat(data)
  labelmatrix = mat(labels).T
  m, n = shape(datamatrix)
  steps = 10.0
  bestStump = {}
  bestClassEst = mat(zeros((m, 1)))
  minError = inf
  for i in range(0, n):
    rangemin = datamatrix[:, i].min()
    rangemax = datamatrix[:, i].max()
    stepSize = (rangemax - rangemin) / steps
    for j in range(-1, int(steps) + 1):
      for threshfunc in ["lt", "gt"]:
        threshold = rangemin + (float(j) * stepSize)
        predicted = stumpClassify(datamatrix, i, threshold, threshfunc)
        errors = mat(ones((m, 1)))
        errors[predicted == labelmatrix] = 0
        weightedError = D.T * errors
#        print "split: dim %d, thresh %.2f, func: %s, weighted error: %.3f" % \
#          (i, threshold, threshfunc, weightedError)
        if weightedError < minError:
          minError = weightedError
          bestClassEst = predicted.copy()
          bestStump["dim"] = i
          bestStump["thresh"] = threshold
          bestStump["ineq"] = threshfunc
  return bestStump, minError, bestClassEst

def adaboostTrainDs(data, labels, iterations=40):
  weakClassifiers = []
  m = shape(data)[0]
  D = mat(ones((m,1))/m)
  aggClassEst = mat(zeros((m,1)))
  for i in range(iterations):
    bestStump, error, classEst = buildStump(data, labels, D)
    print "D:",D.T
    alpha = float(0.5 * log((1.0 - error) / max(error, 1e-16)))
    bestStump['alpha'] = alpha
    weakClassifiers.append(bestStump)
    print "classEst:", classEst.T
    expon = multiply(-1 * alpha * mat(labels).T, classEst)
    D = multiply(D, exp(expon))
    D = D / D.sum()
    aggClassEst += alpha * classEst
    print "aggClassEst:", aggClassEst.T
    aggErrors = multiply(sign(aggClassEst) != mat(labels).T, ones((m,1)))
    errorRate = aggErrors.sum() / m
    print "total error:", errorRate
    print "---"
    if errorRate == 0.0:
      break
  return weakClassifiers, aggClassEst

def adaboostClassify(data, classifiers):
  datamatrix = mat(data)
  m = shape(datamatrix)[0]
  aggClassEst = mat(zeros((m, 1)))
  for i in range(0, len(classifiers)):
    classEst = stumpClassify(datamatrix, classifiers[i]["dim"],
      classifiers[i]["thresh"], classifiers[i]["ineq"])
    aggClassEst += classifiers[i]['alpha'] * classEst
    print aggClassEst
  return sign(aggClassEst)

def loadDataSet(filename):
  data = []
  labels = []
  for line in open(filename, 'rb').readlines():
    cols = line.strip().split("\t")
    data.append(map(lambda x: float(x), cols[:-1]))
    labels.append(float(cols[-1]))
  return data, labels

def plotROC(predicted, labels):
  import matplotlib.pyplot as plt
  cur = (1.0, 1.0)
  ysum = 0.0
  numPos = sum(array(labels) == 1.0)
  ystep = 1 / float(numPos)
  xstep = 1 / float(len(labels) - numPos)
  sortedIndices = predicted.argsort()
  fig = plt.figure()
  fig.clf()
  ax = plt.subplot(111)
  for index in sortedIndices.tolist()[0]:
    if labels[index] == 1.0:
      delX = 0;
      delY = ystep;
    else:
      delX = xstep
      delY = 0
      ysum += cur[1]
    ax.plot([cur[0], cur[0] - delX], [cur[1], cur[1] - delY], c='b')
    cur = (cur[0] - delX, cur[1] - delY)
  ax.plot([0,1], [0,1],'b--')
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.title('ROC curve for AdaBoost Horse Colic Detection System')
  ax.axis([0, 1, 0, 1])
  plt.show()
  print "AUC: ", ysum * xstep

### Testing basic functionality
#data, labels = loadSimpleData()
#D = mat(ones((5, 1))) / 5
#bestStump, minError, bestClassEst = buildStump(data, labels, D)
#print "bestStump=", bestStump
#classifiers = adaboostTrainDs(data, labels, 10)
#print classifiers
#print "result=", adaboostClassify([[0,0], [5,5]], classifiers)

## Horse colic dataset
traindata, trainlabels = loadDataSet("horseColicTraining2.txt")
classifiers, aggClassEst = adaboostTrainDs(traindata, trainlabels, 10)

testdata, testlabels = loadDataSet("horseColicTest2.txt")
predictions = adaboostClassify(testdata, classifiers)
errors = mat(ones((len(testdata), 1)))
print "# misclassified:", errors[predictions != mat(testlabels).T].sum()

plotROC(aggClassEst.T, trainlabels)


