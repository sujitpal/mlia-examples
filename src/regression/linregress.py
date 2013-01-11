from __future__ import division
from numpy import *

def loadDataSet(filename):
  data = []
  labels = []
  for line in open(filename).readlines():
    cols = line.strip().split("\t")
    data.append(map(lambda x: float(x), cols[:-1]))
    labels.append(float(cols[-1]))
  return data, labels

def regress(xs, ys):
  xmat = mat(xs)
  ymat = mat(ys).T
  xTx = xmat.T * xmat
  if linalg.det(xTx) == 0:
    print "singular matrix, cannot invert"
    return
  return xTx.I * (xmat.T * ymat)

def plot(xmat, ymat):
  import matplotlib.pyplot as plt
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.scatter(xmat[:, 1].flatten().A[0], ymat.T[:, 0].flatten().A[0])
  xcopy = xmat.copy()
  xcopy.sort(0)
  yhat = xcopy * ws
  ax.plot(xcopy[:, 1], yhat)
  plt.show()

def lwlr(testPoint, xs, ys, k=1.0):
  xmat = mat(xs)
  ymat = mat(ys).T
  m = shape(xmat)[0]
  weights = mat(eye((m)))
  for j in range(0, m):
    diffMat = testPoint - xmat[j, :]
    weights[j, j] = exp(diffMat * diffMat.T / (-2.0 * k**2))
  xTx = xmat.T * (weights * xmat)
  if linalg.det(xTx) == 0.0:
    print "singular matrix, can't invert"
    return
  ws = xTx.I * (xmat.T * (weights * ymat))
  return testPoint * ws

def lwlrTest(testArr, xs, ys, k=1.0):
  m = shape(testArr)[0]
  yhat = zeros(m)
  for i in range(0, m):
    yhat[i] = lwlr(testArr[i], xs, ys, k)
  return yhat

def plot2(xs, ys, yhat):
  import matplotlib.pyplot as plt
  xmat = mat(xs)
  ymat = mat(ys)
  artInd = xmat[:, 1].argsort(0)
  xsort = xmat[artInd][:, 0, :]
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.plot(xsort[:, 1], yhat[artInd])
  ax.scatter(xmat[:,1].flatten().A[0], ymat.T.flatten().A[0],
    s=2, c='red')
  plt.show()

def rssError(ys, yHat):
  return ((ys - yHat)**2).sum()

def ridgeRegress(xmat, ymat, lam=0.2):
  """ wHat = (X.T*X + lambda*I).I*X.T*y """
  xTx = xmat.T * xmat
  denom = xTx + eye(shape(xmat)[1]) * lam
  if linalg.det(denom) == 0.0:
    print "singular matrix, can't invert"
    return
  return denom.I * (xmat.T * ymat)

def ridgeTest(xs, ys):
  """ return weights for 30 different values of lambda """
  xmat = mat(xs)
  ymat = mat(ys).T
  ymean = mean(ymat, 0)
  ymat = ymat - ymean
  xmean = mean(xmat, 0)
  xVar = var(xmat, 0)
  xmat = (xmat - xmean) / xVar
  numTestPts = 30
  wmat = zeros((numTestPts, shape(xmat)[1]))
  for i in range(0, numTestPts):
    ws = ridgeRegress(xmat, ymat, exp(i - 10))
    wmat[i, :] = ws.T
    print "iter=", i, "weights=", wmat[i, :]
  return wmat

def plot3(rws):
  import matplotlib.pyplot as plt
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.plot(rws)
  plt.show()

def regularize(xmat):
  inmat = xmat.copy()
  inmeans = mean(inmat, 0)
  invar = var(inmat, 0)
  return (inmat - inmeans) / invar

def stageWise(xs, ys, epsilon=0.01, iterations=100):
  xmat = mat(xs)
  ymat = mat(ys).T
  ymean = mean(ymat, 0)
  ymat = ymat - ymean
  xmat = regularize(xmat)
  m, n = shape(xmat)
  returnMat = zeros((iterations,n))
  ws = zeros((n,1))
  wsTest = ws.copy()
  wsMax = ws.copy()
  for i in range(0, iterations):
    print ws.T
    lowestError = inf;
    for j in range(0, n):
      for sign in [-1,1]:
        wsTest = ws.copy()
        wsTest[j] += epsilon * sign
        ytest = xmat * wsTest
        rssE = rssError(ymat.A, ytest.A)
        if rssE < lowestError:
          lowestError = rssE
          wsMax = wsTest
    ws = wsMax.copy()
    returnMat[i, :] = ws.T
  return returnMat

def crossValidation(xs, ys, nvalidations=10):
  m = len(ys)
  indexList = range(0, m)
  errorMat = zeros((nvalidations,30))
  for i in range(nvalidations):
    trainX = []
    trainY = []
    testX = []
    testY = []
    random.shuffle(indexList)
  for j in range(0, m):
    if j < m * 0.9:
      trainX.append(xs[indexList[j]])
      trainY.append(ys[indexList[j]])
    else:
      testX.append(xs[indexList[j]])
      testY.append(ys[indexList[j]])
  wMat = ridgeTest(trainX, trainY)
  for k in range(0, 30):
    matTestX = mat(testX)
    matTrainX = mat(trainX)
    meanTrain = mean(matTrainX, 0)
    varTrain = var(matTrainX, 0)
    matTestX = (matTestX - meanTrain) / varTrain
    yEst = matTestX * mat(wMat[k,:]).T + mean(trainY)
    errorMat[i, k] = rssError(yEst.T.A, array(testY))
  meanErrors = mean(errorMat, 0)
  minMean = float(min(meanErrors))
  bestWeights = wMat[nonzero(meanErrors == minMean)]
  xMat = mat(xs)
  yMat=mat(ys).T
  meanX = mean(xMat, 0)
  varX = var(xMat, 0)
  unReg = bestWeights / varX
  print "the best model from Ridge Regression is:\n", unReg
  print "with constant term: ", -1 * sum(multiply(meanX, unReg)) + mean(yMat)

### test data
#xs, ys = loadDataSet("ex0.txt")
##print "xs=", xs
##print "ys=", ys
#ws = regress(xs, ys)
##print "ws=", ws
#xmat = mat(xs)
#ymat = mat(ys)
#yhat = xmat * ws
##plot(xmat, ymat)
## compute correlation coefficient
##print corrcoef(yhat.T, ymat)
#
### estimate for a single point on dataset
#print "yhat(k=1.0)=", lwlr(xs[0], xs, ys, 1.0)
#print "yhat(k=0.001)=", lwlr(xs[0], xs, ys, 0.001)
#
### estimate for all points in dataset
##yhat = lwlrTest(xs, xs, ys)
#yhat = lwlrTest(xs, xs, ys, 0.01)
##yhat = lwlrTest(xs, xs, ys, 0.003)
#plot2(xs, ys, yhat)

## predicting abalone age
#xs, ys = loadDataSet("abalone.txt")

## check error using different kernel size on test data
## vary "k"
#yHat01 = lwlrTest(xs[0:99], xs[0:99], ys[0:99], 0.1)
#print "error(0:99, .1)=", rssError(ys[0:99], yHat01)
#yHat1 = lwlrTest(xs[0:99], xs[0:99], ys[0:99], 1)
#print "error(0:99, 1)=", rssError(ys[0:99], yHat1)
#yHat10 = lwlrTest(xs[0:99], xs[0:99], ys[0:99], 10)
#print "error(0:99, 10)=", rssError(ys[0:99], yHat10)
#
#yHat01 = lwlrTest(xs[100:199], xs[100:199], ys[100:199], 0.1)
#print "error(100:199, .1)=", rssError(ys[0:99], yHat01)
#yHat1 = lwlrTest(xs[100:199], xs[100:199], ys[100:199], 1)
#print "error(100:199, 1)=", rssError(ys[0:99], yHat1)
#yHat10 = lwlrTest(xs[100:199], xs[100:199], ys[100:199], 10)
#print "error(100:199, 10)=", rssError(ys[0:99], yHat10)

## vary lambda
#ridgeWeights = ridgeTest(xs, ys)
#plot3(ridgeWeights)

#stageWeights = stageWise(xs, ys, 0.01, 200)
#plot3(stageWeights)

## compare results with standard regression
#standardWeights = regress(xs, ys)
#plot3(standardWeights)

## lego prices
xs, ys = loadDataSet("legoPrices.txt")
# add the w0 coeff (always 1)
#m, n = shape(xs)
#xs1 = mat(ones((m,n+1)))
#xs1[:, 1:5] = mat(xs)
#ws = regress(xs1, ys)
#for i in range(0, m):
#  actY = ys[i]
#  predY = xs1[i] * ws
#  print actY, predY

# run cross validation
#crossValidation(xs, ys)

# running the ridge test shows that coeff 4 is
# most important
ridgeTest(xs, ys)