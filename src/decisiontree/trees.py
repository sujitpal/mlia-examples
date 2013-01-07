from __future__ import division
from math import log
import operator

def createDataSet():
  return [[1, 1, "yes"],
    [1, 1, "yes"],
    [1, 0, "no"],
    [0, 1, "no"],
    [0, 1, "no"]], ["no surfacing", "flippers"]

def entropy(dataset):
  n = len(dataset)
  labelCounts = {}
  for featVec in dataset:
    currlabel = featVec[-1]
    if currlabel not in labelCounts.keys():
      labelCounts[currlabel] = 0
    labelCounts[currlabel] += 1
  entropy = 0.0
  for key in labelCounts:
    prob = labelCounts[key] / n
    entropy -= prob * log(prob, 2)
  return entropy

def splitDataSet(dataset, axis, value):
  result = []
  for vec in dataset:
    if vec[axis] == value:
      result.append(
        map(lambda (i,x): x,
        filter(lambda (i,x): i != axis,
        enumerate(vec))))
  return result

def chooseBestFeatureToSplit(dataset):
  baseEntropy = entropy(dataset)
  bestInfoGain = 0
  bestFeature = -1
  for i in range(0, len(dataset[0])-1):
    newEntropy = 0
    for value in set([x[i] for x in dataset]):
      subdataset = splitDataSet(dataset, i, value)
      prob = len(subdataset) / len(dataset)
      newEntropy += prob * entropy(subdataset)
    infoGain = baseEntropy - newEntropy
    if infoGain > bestInfoGain:
      bestInfoGain = infoGain
      bestFeature = i
  return bestFeature

def majorityCount(votes):
  """
  If we run out of attributes and the branch contains more than
  one class, then we assign the class for the branch using the
  majority class in that branch.
  """
  classCount = {}
  for vote in votes:
    if vote not in classCount.keys():
      classCount[vote] = 0
    classCount[vote] += 1
  return sorted(classCount.iteritems(),
    key=operator.itemgetter(1), reverse=True)[0][0]

def createTree(dataset, labels):
  classList = [x[-1] for x in dataset]
  if classList.count(classList[0]) == len(classList):
    # if branch contains single class, it can't be split further
    return classList[0]
  if len(dataset[0]) == 1:
    # if no more attributes remain, the splitting can't continue
    # so we choose the majority label as the branch label in this case
    return majorityCount(classList)
  bestFeat = chooseBestFeatureToSplit(dataset)
  bestFeatLabel = labels[bestFeat]
  tree = {bestFeatLabel: {}}
  del(labels[bestFeat])
  for value in set([x[bestFeat] for x in dataset]):
    sublabels = labels[:]
    tree[bestFeatLabel][value] = createTree(
      splitDataSet(dataset, bestFeat, value), sublabels)
  return tree

def retrieveTree(i):
  listOfTrees =[{'no surfacing': {
    0: 'no', 1: {
      'flippers': {
        0: 'no', 1: 'yes'
      }
    }}},
    {'no surfacing': {
      0: 'no', 1: {
        'flippers': {
          0: {
            'head': {
              0: 'no', 1: 'yes'
            }
          }, 1: 'no'
    }}}}
  ]
  return listOfTrees[i]

def classify(tree, labels, testVec):
  first = tree.keys()[0]
  rest = tree[first]
  featIndex = labels.index(first)
  for key in rest.keys():
    if testVec[featIndex] == key:
      if type(rest[key]).__name__ == "dict":
        classLabel = classify(rest[key], labels, testVec)
      else:
        classLabel = rest[key]
  return classLabel

def storeTree(tree, filename):
  import pickle
  f = open(filename, 'wb')
  pickle.dump(tree, f)
  f.close()

def loadTree(filename):
  import pickle
  f = open(filename, 'rb')
  return pickle.load(f)

#data, labels = createDataSet()
##print entropy(data)
##print splitDataSet(data, 0, 1)
##print splitDataSet(data, 0, 0)
##print chooseBestFeatureToSplit(data)
#labels_copy = labels[:]
#tree = createTree(data, labels_copy)
#print "tree=", tree
#print "tree.classify([1,0])=", classify(tree, labels, [1,0])
#print "tree.classify([1,1])=", classify(tree, labels, [1,1])
#storeTree(tree, "classifier.pkl")
#xtree = loadTree("classifier.pkl")
#print "xtree.classify([1,0])=", classify(xtree, labels, [1,0])
#print "xtree.classify([1,1])=", classify(xtree, labels, [1,1])

# contact lenses data
import treeplotter
f = open("lenses.txt", 'rb')
lenses = [line.strip().split('\t') for line in f.readlines()]
labels = ["age", "prescript", "astigmatic", "tearRate"]
labels_copy = labels[:]
tree = createTree(lenses, labels_copy)
#treeplotter.createPlot(tree)
print classify(tree, labels, ["young", "myope", "yes", "reduced"])
f.close()
