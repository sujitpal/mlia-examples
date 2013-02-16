# copy of github version
from __future__ import division
from numpy import *

class optStruct:
  """ parameter holder """
  def __init__(self, dataMatIn, classLabels, C, toler, kTup):
    self.X = dataMatIn
    self.labelMat = classLabels
    self.C = C
    self.tol = toler
    self.m = shape(dataMatIn)[0]
    self.alphas = mat(zeros((self.m,1)))
    self.b = 0
    self.eCache = mat(zeros((self.m,2))) #first column is valid flag
    self.K = mat(zeros((self.m,self.m)))
    for i in range(self.m):
      self.K[:,i] = kernelTrans(self.X, self.X[i,:], kTup)

def loadDataSet(filename):
  datamatrix = []
  labelmatrix = []
  for line in open(filename).readlines():
    cols = line.strip().split("\t")
    datamatrix.append((float(cols[0]), float(cols[1])))
    labelmatrix.append(float(cols[2]))
  return datamatrix, labelmatrix

def selectJrand(i, m):
  j=i #we want to select any J not equal to i
  while (j == i):
    j = int(random.uniform(0, m))
  return j

def clipAlpha(aj,H,L):
  if aj > H:
    aj = H
  if L > aj:
    aj = L
  return aj

def smoSimple(dataMatIn, classLabels, C, toler, maxIter):
  dataMatrix = mat(dataMatIn)
  labelMat = mat(classLabels).T
  b = 0
  m, n = shape(dataMatrix)
  alphas = mat(zeros((m, 1)))
  iter = 0
  while iter < maxIter:
    alphaPairsChanged = 0
    for i in range(m):
      fXi = float(multiply(alphas, labelMat).T * \
        (dataMatrix * dataMatrix[i, :].T)) + b
      Ei = fXi - float(labelMat[i]) #if checks if an example violates KKT conditions
      if ((labelMat[i] * Ei < -toler) and (alphas[i] < C)) or \
          ((labelMat[i] * Ei > toler) and (alphas[i] > 0)):
        j = selectJrand(i,m)
        fXj = float(multiply(alphas, labelMat).T * \
          (dataMatrix * dataMatrix[j, :].T)) + b
        Ej = fXj - float(labelMat[j])
        alphaIold = alphas[i].copy()
        alphaJold = alphas[j].copy();
        if (labelMat[i] != labelMat[j]):
          L = max(0, alphas[j] - alphas[i])
          H = min(C, C + alphas[j] - alphas[i])
        else:
          L = max(0, alphas[j] + alphas[i] - C)
          H = min(C, alphas[j] + alphas[i])
        if L==H:
          print "L==H"
          continue
        eta = 2.0 * dataMatrix[i, :] * dataMatrix[j, :].T - \
          dataMatrix[i, :] * dataMatrix[i, :].T - \
          dataMatrix[j, :] * dataMatrix[j, :].T
        if eta >= 0:
          print "eta>=0"
          continue
        alphas[j] -= labelMat[j] * (Ei - Ej) / eta
        alphas[j] = clipAlpha(alphas[j], H, L)
        if (abs(alphas[j] - alphaJold) < 0.00001):
          print "j not moving enough"
          continue
        # update i by the same amount as j
        # the update is in the oppostie direction
        alphas[i] += labelMat[j] * labelMat[i] * (alphaJold - alphas[j])
        b1 = b - Ei - labelMat[i] * (alphas[i] - alphaIold) * \
          dataMatrix[i, :] * dataMatrix[i, :].T - \
          labelMat[j] * (alphas[j] - alphaJold) * \
          dataMatrix[i, :] * dataMatrix[j, :].T
        b2 = b - Ej - labelMat[i]* (alphas[i] - alphaIold) * \
          dataMatrix[i, :] * dataMatrix[j, :].T - \
          labelMat[j] * (alphas[j] - alphaJold) * \
          dataMatrix[j, :] * dataMatrix[j, :].T
        if (0 < alphas[i]) and (C > alphas[i]):
          b = b1
        elif (0 < alphas[j]) and (C > alphas[j]):
          b = b2
        else:
          b = (b1 + b2)/2.0
        alphaPairsChanged += 1
        print "iter: %d i:%d, pairs changed %d" % (iter, i, alphaPairsChanged)
    if alphaPairsChanged == 0:
      iter += 1
    else:
      iter = 0
    print "iteration number: %d" % iter
  return b,alphas


def calcEk(oS, k):
  fXk = float(multiply(oS.alphas, oS.labelMat).T * oS.K[:, k] + oS.b)
  Ek = fXk - float(oS.labelMat[k])
  return Ek

def selectJ(i, oS, Ei):         #this is the second choice -heurstic, and calcs Ej
  maxK = -1; maxDeltaE = 0; Ej = 0
  oS.eCache[i] = [1,Ei]  #set valid #choose the alpha that gives the maximum delta E
  validEcacheList = nonzero(oS.eCache[:,0].A)[0]
  if (len(validEcacheList)) > 1:
    for k in validEcacheList:   #loop through valid Ecache values and find the one that maximizes delta E
      if k == i:
        continue #don't calc for i, waste of time
      Ek = calcEk(oS, k)
      deltaE = abs(Ei - Ek)
      if (deltaE > maxDeltaE):
        maxK = k; maxDeltaE = deltaE
        Ej = Ek
    return maxK, Ej
  else:   #in this case (first time around) we don't have any valid eCache values
    j = selectJrand(i, oS.m)
    Ej = calcEk(oS, j)
  return j, Ej

def updateEk(oS, k):#after any alpha has changed update the new value in the cache
  Ek = calcEk(oS, k)
  oS.eCache[k] = [1,Ek]

def innerL(i, oS):
  Ei = calcEk(oS, i)
  if ((oS.labelMat[i]*Ei < -oS.tol) and \
      (oS.alphas[i] < oS.C)) or \
      ((oS.labelMat[i]*Ei > oS.tol) and \
      (oS.alphas[i] > 0)):
    j,Ej = selectJ(i, oS, Ei) #this has been changed from selectJrand
    alphaIold = oS.alphas[i].copy()
    alphaJold = oS.alphas[j].copy();
    if (oS.labelMat[i] != oS.labelMat[j]):
      L = max(0, oS.alphas[j] - oS.alphas[i])
      H = min(oS.C, oS.C + oS.alphas[j] - oS.alphas[i])
    else:
      L = max(0, oS.alphas[j] + oS.alphas[i] - oS.C)
      H = min(oS.C, oS.alphas[j] + oS.alphas[i])
    if L==H:
      print "L==H"
      return 0
    eta = 2.0 * oS.K[i,j] - oS.K[i,i] - oS.K[j,j] #changed for kernel
    if eta >= 0:
      print "eta>=0"
      return 0
    oS.alphas[j] -= oS.labelMat[j] * (Ei - Ej) / eta
    oS.alphas[j] = clipAlpha(oS.alphas[j], H, L)
    updateEk(oS, j) #added this for the Ecache
    if (abs(oS.alphas[j] - alphaJold) < 0.00001):
      print "j not moving enough"
      return 0
    oS.alphas[i] += oS.labelMat[j] * oS.labelMat[i] * \
      (alphaJold - oS.alphas[j]) #update i by the same amount as j
    updateEk(oS, i) #added this for the Ecache                    #the update is in the oppostie direction
    b1 = oS.b - Ei - oS.labelMat[i] * \
      (oS.alphas[i] - alphaIold) * oS.K[i,i] - \
      oS.labelMat[j] * (oS.alphas[j] - alphaJold) * \
      oS.K[i,j]
    b2 = oS.b - Ej - oS.labelMat[i] * \
      (oS.alphas[i] - alphaIold) * oS.K[i,j] - \
      oS.labelMat[j] * (oS.alphas[j] - alphaJold) * \
      oS.K[j,j]
    if 0 < oS.alphas[i] and oS.C > oS.alphas[i]:
      oS.b = b1
    elif 0 < oS.alphas[j] and oS.C > oS.alphas[j]:
      oS.b = b2
    else:
      oS.b = (b1 + b2) / 2.0
    return 1
  else: return 0

def smoP(dataMatIn, classLabels, C, toler, maxIter,kTup=('lin', 0)):    #full Platt SMO
  oS = optStruct(mat(dataMatIn),
    mat(classLabels).T, C, toler, kTup)
  iter = 0
  entireSet = True; alphaPairsChanged = 0
  while (iter < maxIter) and ((alphaPairsChanged > 0) or (entireSet)):
    alphaPairsChanged = 0
    if entireSet:   #go over all
      for i in range(oS.m):
        alphaPairsChanged += innerL(i,oS)
      print "fullSet, iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
      iter += 1
    else:#go over non-bound (railed) alphas
      nonBoundIs = nonzero((oS.alphas.A > 0) * (oS.alphas.A < C))[0]
      for i in nonBoundIs:
        alphaPairsChanged += innerL(i,oS)
        print "non-bound, iter: %d i:%d, pairs changed %d" % (iter,i,alphaPairsChanged)
        iter += 1
    if entireSet: entireSet = False #toggle entire set loop
    elif (alphaPairsChanged == 0): entireSet = True
    print "iteration number: %d" % iter
  return oS.b,oS.alphas

def calcWs(alphas, dataArr, classLabels):
  X = mat(dataArr)
  labelMat = mat(classLabels).T
  m,n = shape(X)
  w = zeros((n,1))
  for i in range(m):
    # alpha == 0 will be ignored in this calculation
    # only non-zero alpha (support vector) will be
    # considered
    w += multiply(alphas[i] * labelMat[i], X[i,:].T)
  return w

def kernelTrans(X, A, kTup):
  m,n = shape(X)
  K = mat(zeros((m,1)))
  if kTup[0] == "lin":
    K = X * A.T   #linear kernel
  elif kTup[0] == "rbf":
    for j in range(m):
      deltaRow = X[j,:] - A
      K[j] = deltaRow * deltaRow.T
    K = exp(K / (-1 * kTup[1]**2))
  else: raise NameError('Unrecognized kernel')
  return K

def testRbf(k1=1.3):
  dataArr, labelArr = loadDataSet('testSetRBF.txt')
  b, alphas = smoP(dataArr, labelArr, 200, 0.0001, 10000, ('rbf', k1)) #C=200 important
  datMat = mat(dataArr)
  labelMat = mat(labelArr).T
  svInd = nonzero(alphas.A > 0)[0]
  sVs = datMat[svInd] #get matrix of only support vectors
  labelSV = labelMat[svInd];
  print "there are %d Support Vectors" % shape(sVs)[0]
  m = shape(datMat)[0]
  errorCount = 0
  for i in range(m):
    kernelEval = kernelTrans(sVs, datMat[i,:], ('rbf', k1))
    predict = kernelEval.T * multiply(labelSV, alphas[svInd]) + b
    if sign(predict) != sign(labelArr[i]):
      errorCount += 1
  print "the training error rate is: %f" % (float(errorCount)/m)
  dataArr, labelArr = loadDataSet('testSetRBF2.txt')
  errorCount = 0
  datMat = mat(dataArr)
  labelMat = mat(labelArr).T
  m = shape(datMat)[0]
  for i in range(0, m):
    kernelEval = kernelTrans(sVs, datMat[i,:], ('rbf', k1))
    predict= kernelEval.T * multiply(labelSV, alphas[svInd]) + b
    if sign(predict) != sign(labelArr[i]):
      errorCount += 1
  print "the test error rate is: %f" % (float(errorCount)/m)

def img2vector(filename):
  """ from chapter 2 knn.py """
  imgvec = zeros((1, 1024))
  f = open(filename)
  for i in range(0, 32):
    line = f.readline()
    for j in range(0, 32):
      imgvec[0, (32 * i) + j] = int(line[j])
  return imgvec

def loadImages(dirName):
  from os import listdir
  hwLabels = []
  trainingFileList = listdir(dirName)
  m = len(trainingFileList)
  trainingMat = zeros((m,1024))
  for i in range(m):
    fileNameStr = trainingFileList[i]
    fileStr = fileNameStr.split('.')[0]
    classNumStr = int(fileStr.split('_')[0])
    if classNumStr == 9:
      hwLabels.append(-1)
    else:
      hwLabels.append(1)
    trainingMat[i,:] = img2vector('%s/%s' % (dirName, fileNameStr))
  return trainingMat, hwLabels

def testDigits(kTup=('rbf', 10)):
  dataArr, labelArr = loadImages('trainingDigits')
  b, alphas = smoP(dataArr, labelArr, 200, 0.0001, 10000, kTup)
  datMat = mat(dataArr)
  labelMat = mat(labelArr).T
  svInd = nonzero(alphas.A > 0)[0]
  sVs = datMat[svInd]
  labelSV = labelMat[svInd];
  print "there are %d Support Vectors" % shape(sVs)[0]
  m = shape(datMat)[0]
  errorCount = 0
  for i in range(0, m):
    kernelEval = kernelTrans(sVs, datMat[i, :], kTup)
    predict = kernelEval.T * multiply(labelSV, alphas[svInd]) + b
    if sign(predict) != sign(labelArr[i]):
      errorCount += 1
  print "the training error rate is: %f" % (float(errorCount)/m)
  dataArr, labelArr = loadImages('testDigits')
  errorCount = 0
  datMat = mat(dataArr); labelMat = mat(labelArr).transpose()
  m = shape(datMat)[0]
  for i in range(m):
    kernelEval = kernelTrans(sVs, datMat[i, :], kTup)
    predict = kernelEval.T * multiply(labelSV, alphas[svInd]) + b
    if sign(predict) != sign(labelArr[i]):
      errorCount += 1
  print "the test error rate is: %f" % (float(errorCount)/m)

## Load the data
#data, labels = loadDataSet("testSet.txt")
#print data
#print labels

## run simplified SMO
#b, alphas = smoSimple(data, labels, 0.6, 0.001, 40)
#print "b=", b
#print "#-support vectors=", shape(alphas[alphas > 0])
#print "points that are support vectors"
#for i in range(0, 100):
#  if alphas[i] > 0.0:
#    print data[i], labels[i]

## run full SMO
#b, alphas = smoP(data, labels, 0.6, 0.001, 40)
#print "b=", b
#print "#-support vectors=", shape(alphas[alphas > 0])
#print "points that are support vectors"
#for i in range(0, 100):
#  if alphas[i] > 0.0:
#    print data[i], labels[i]
#
## Find the w values for the hyperplane
#ws = calcWs(alphas, data, labels)
##print ws
#
## classify something (frex the first record)
#y = (mat(data[0]) * mat(ws)) + b
#actlabel = 1.0 if y > 0 else -1.0
#print "expected=", labels[0], "actual=", actlabel

## Test for radial basis function kernel transformation
#testRbf()

## Test for handwriting recognition (binary, rbf)
testDigits()