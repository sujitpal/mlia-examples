from __future__ import division
from numpy import *

class TreeNode:
  def __init__(self, nameValue, numOccur, parentNode):
    self.name = nameValue
    self.count = numOccur
    self.nodeLink = None
    self.parent = parentNode
    self.children = {}

  def inc(self, numOccur):
    self.count += numOccur

  def disp(self, ind=1):
    print " "* ind, self.name, self.count
    for child in self.children.values():
      child.disp(ind + 1)

def createTree(dataSet, minSupport=1):
  headerTable = {}
  for trans in dataSet:
    for item in trans:
      headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
  headerTable = dict(filter(lambda x: x[1] >= minSupport, headerTable.items()))
  freqItemSet = set(headerTable.keys())
  if len(freqItemSet) == 0:
    return None, None
  for k in headerTable:
    headerTable[k] = [headerTable[k], None]
  recTree = TreeNode("Null", 1, None)
  for tranSet, count in dataSet.items():
    localD = {}
    for item in tranSet:
      if item in freqItemSet:
        localD[item] = headerTable[item][0]
    if len(localD) > 0:
      orderedItems = [x[0] for x in sorted(localD.items(),
        key=lambda p: p[1], reverse=True)]
      updateTree(orderedItems, recTree, headerTable, count)
  return recTree, headerTable

def updateTree(items, inTree, headerTable, count):
  if items[0] in inTree.children:
    inTree.children[items[0]].inc(count)
  else:
    inTree.children[items[0]] = TreeNode(items[0], count, inTree)
    if headerTable[items[0]][1] == None:
      headerTable[items[0]][1] = inTree.children[items[0]]
    else:
      updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
  if len(items) > 1:
    updateTree(items[1::], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):
  while nodeToTest.nodeLink != None:
    nodeToTest = nodeToTest.nodeLink
  nodeToTest.nodeLink = targetNode

def loadSimpleData():
  simpDat = [['r', 'z', 'h', 'j', 'p'],
    ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
    ['z'],
    ['r', 'x', 'n', 'o', 's'],
    ['y', 'r', 'x', 'z', 'q', 't', 'p'],
    ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
  return simpDat

def createInitSet(dataSet):
  retDict = {}
  for trans in dataSet:
    retDict[frozenset(trans)] = 1
  return retDict

def ascendTree(leafNode, prefixPath):
  if leafNode.parent != None:
    prefixPath.append(leafNode.name)
    ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePath, treeNode):
  condPats = {}
  while treeNode != None:
    prefixPath = []
    ascendTree(treeNode, prefixPath)
    if len(prefixPath) > 1:
      condPats[frozenset(prefixPath[1:])] = treeNode.count
    treeNode = treeNode.nodeLink
  return condPats

def mineTree(inTree, headerTable, minSup, prefix, freqItemList):
  bigL = [v[0] for v in sorted(headerTable.items(),
    key=lambda p: p[1])]
  for basePath in bigL:
    newFreqSet = prefix.copy()
    newFreqSet.add(basePath)
    freqItemList.append(newFreqSet)
    condPathBases = findPrefixPath(basePath, headerTable[basePath][1])
    myCondTree, myHeaderTable = createTree(condPathBases, minSup)
    if myHeaderTable != None:
      print "conditional tree for:", newFreqSet
      myCondTree.disp()
      mineTree(myCondTree, myHeaderTable, minSup, newFreqSet, freqItemList)

def main():

#  ### Tiny data for testing fpgrowth tree
#  root = TreeNode("pyramid", 9, None)
#  root.children["eye"] = TreeNode("eye", 13, None)
#  root.children["phoenix"] = TreeNode("phoenix", 3, None)
#  root.disp()

#  ### slightly larger data for testing functionality of fpgrowth
#  data = loadSimpleData()
#  #print data
#  initSet = createInitSet(data)
#  #print initSet
#  myFPTree, myHeaderTab = createTree(initSet, 3)
#  myFPTree.disp()
#  for name in myHeaderTab.keys():
#    print "prefix pattern(" + name + ")", findPrefixPath(name, myHeaderTab[name][1])
#  freqItems = []
#  mineTree(myFPTree, myHeaderTab, 3, set([]), freqItems)
#  print "frwquent items=", freqItems

  ### kosarak data (medium)
  parsedDat = [line.split() for line in open("kosarak.dat").readlines()]
  initSet = createInitSet(parsedDat)
  myFPTree, myHeaderTab = createTree(initSet, 100000)
  myFreqList = []
  mineTree(myFPTree, myHeaderTab, 100000, set([]), myFreqList)
  for itemset in myFreqList:
    print itemset

if __name__ == "__main__":
  main()
