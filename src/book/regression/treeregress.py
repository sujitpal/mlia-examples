from __future__ import division
from numpy import *

class TreeNode():
  def __init__(self, feat, val, right, left):
    featureToSplitOn = feat
    valueOfSplit = val
    rightBranch = right
    leftBranch = left

def loadDataSet(filename):
  data = []
  for line in open(filename).readlines():
    data.append(map(lambda x: float(x), line.strip().split("\t")))
  return data

def binSplitDataSet(dataset, feature, value):
  mat0 = dataset[nonzero(dataset[:, feature] > value)[0], :][0]
  mat1 = dataset[nonzero(dataset[:, feature] <= value)[0], :][0]
  return mat0, mat1

def modelErr(dataSet):
    ws,X,Y = linearSolve(dataSet)
    yHat = X * ws
    return sum(power(Y - yHat,2))

def regLeaf(dataSet):
  return mean(dataSet[:, -1])

def regErr(dataSet):
  return var(dataSet[:, -1]) * shape(dataSet)[0]

def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1,4)):
  tolS = ops[0]
  tolN = ops[1]
  # if all the target variables are the same value: quit and return value
  if len(set(dataSet[:, -1].T.tolist()[0])) == 1: #exit cond 1
    return None, leafType(dataSet)
  m, n = shape(dataSet)
  # the choice of the best feature is driven by Reduction in RSS error from mean
  S = errType(dataSet)
  bestS = inf
  bestIndex = 0
  bestValue = 0
  for featIndex in range(n-1):
    for splitVal in set(dataSet[:, featIndex]):
      mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
      if shape(mat0)[0] < tolN or shape(mat1)[0] < tolN:
        continue
      newS = errType(mat0) + errType(mat1)
      if newS < bestS:
        bestIndex = featIndex
        bestValue = splitVal
        bestS = newS
  # if the decrease (S-bestS) is less than a threshold don't do the split
  if (S - bestS) < tolS:
    return None, leafType(dataSet) #exit cond 2
  mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
  if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):  #exit cond 3
    return None, leafType(dataSet)
  return bestIndex,bestValue  #returns the best feature to split on
                              #and the value used for that split

def createTree(dataset, leafType=regLeaf, errType=regErr, ops=(1,4)):
  feat, val = chooseBestSplit(dataset, leafType, errType, ops)
  if feat == None:
    return val
  retTree = {}
  retTree["spInd"] = feat
  retTree["spVal"] = val
  lset, rset = binSplitDataSet(dataset, feat, val)
  retTree["left"]= createTree(lset, leafType, errType, ops)
  retTree["right"]= createTree(rset, leafType, errType, ops)
  return retTree

def isTree(obj):
  return type(obj).__name__ == "dict"

def getMean(tree):
  if isTree(tree["right"]):
    tree["right"] = getMean(tree["right"])
  if isTree(tree["left"]):
    tree["left"] = getMean(tree["left"])
  return (tree["left"] + tree["right"]) / 2

def prune(tree, testData):
  if shape(testData)[0] == 0:
    return getMean(tree)
  if isTree(tree['right']) or isTree(tree['left']):
    lSet, rSet = binSplitDataSet(testData, tree["spInd"], tree["spVal"])
  if isTree(tree['left']):
    tree['left'] = prune(tree['left'], lSet)
  if isTree(tree['right']):
    tree['right'] = prune(tree['right'], rSet)
  if not isTree(tree['left']) and not isTree(tree['right']):
    lSet, rSet = binSplitDataSet(testData, tree["spInd"], tree["spVal"])
    errorNoMerge = sum(power(lSet[:,-1] - tree['left'],2)) + \
      sum(power(rSet[:,-1] - tree['right'],2))
    treeMean = (tree['left'] + tree['right']) / 2.0
    errorMerge = sum(power(testData[:, -1] - treeMean, 2))
    if errorMerge < errorNoMerge:
      print "merging"
      return treeMean
    else: return tree
  else:
    return tree

def linearSolve(data):
  m, n = shape(data)
  X = mat(ones((m, n)))
  Y = mat(ones((m, 1)))
  X[:, 1:n] = data[:, 0:n-1]
  Y = data[:, -1]
  xTx = X.T * X
  if linalg.det(xTx) == 0.0:
    raise NameError("singular matrix, can't invert, " +
      "try increasing second value of ops")
  ws = xTx.I * (X.T * Y)
  return ws, X, Y

def modelLeaf(data):
  ws, X, Y = linearSolve(data)
  return ws

def modelErr(data):
  ws, X, Y = linearSolve(data)
  yHat = X * ws
  return sum(power(Y - yHat, 2))

def regTreeEval(model, data):
  return float(model)

def modelTreeEval(model, data):
  n = shape(data)[1]
  X = mat(ones((1, n + 1)))
  X[:, 1:n+1] = data
  return float(X * model)

def treeForecast(tree, data, modelEval=regTreeEval):
  if not isTree(tree):
    return modelEval(tree, data)
  if data[tree["spInd"]] > tree["spVal"]:
    if isTree(tree["left"]):
      return treeForecast(tree["left"], data, modelEval)
    else:
      return modelEval(tree["left"], data)
  else:
    if isTree(tree["right"]):
      return treeForecast(tree["right"], data, modelEval)
    else:
      return modelEval(tree["right"], data)

def createForecast(tree, testData, modelEval=regTreeEval):
  m = len(testData)
  yHat = mat(zeros((m, 1)))
  for i in range(0, m):
    yHat[i, 0] = treeForecast(tree, testData[i], modelEval)
  return yHat

def main():
  #testMat = amat(eye(4))
  #print testMat
  #mat0, mat1 = binSplitDataSet(testMat, 1, 0.5)
  #print "mat0=", mat0
  #print "mat1=", mat1

  #tree = createTree(mat(loadDataSet("ex00.txt")))
  #print tree
  #tree2 = createTree(mat(loadDataSet("ex0.txt")))
  #print tree2
  #tree3 = createTree(mat(loadDataSet("ex0.txt")), ops=[0, 1])
  #print tree3

  # first call creates many leaves, second creates 2
  #tree4 = createTree(mat(loadDataSet("ex2.txt")))
  #print tree4
  #tree5 = createTree(mat(loadDataSet("ex2.txt")), ops=[10000, 4])
  #print tree5

  #tree6 = createTree(mat(loadDataSet("ex2.txt")), ops=[0, 1])
  #testData = mat(loadDataSet("ex2test.txt"))
  #prune(tree6, testData)
  #print tree6

  ## model trees
  #datamatrix = mat(loadDataSet("exp2.txt"))
  #tree7 = createTree(datamatrix, modelLeaf, modelErr, (1, 10))
  #print tree7

  ## bike speeds
  trainmatrix = mat(loadDataSet("bikeSpeedVsIq_train.txt"))
  testmatrix = mat(loadDataSet("bikeSpeedVsIq_test.txt"))
  # reg tree
  tree = createTree(trainmatrix, ops=(1, 20))
  yHat = createForecast(tree, testmatrix[:, 0])
  print "r-squared(reg)=", corrcoef(yHat, testmatrix[:, 1], rowvar=0)[0, 1]
  # model tree
  mtree = createTree(trainmatrix, modelLeaf, modelErr, (1, 20))
  yHat = createForecast(mtree, testmatrix[:, 0], modelTreeEval)
  print "r-squared(model)=", corrcoef(yHat, testmatrix[:, 1], rowvar=0)[0, 1]
  # linear solver
  ws, X, Y = linearSolve(trainmatrix)
  for i in range(shape(testmatrix)[0]):
    yHat[i] = testmatrix[i,0] * ws[1,0] + ws[0,0]
  print "r-squared(lin)=", corrcoef(yHat, testmatrix[:, 1], rowvar=0)[0, 1]

if __name__ == "__main__":
  main()
  