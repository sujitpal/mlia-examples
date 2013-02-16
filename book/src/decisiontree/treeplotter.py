import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
  createPlot.ax1.annotate(nodeTxt, xy=parentPt,
    xycoords='axes fraction',
    xytext=centerPt, textcoords='axes fraction',
    va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

def getNumLeafs(tree):
  numLeafs = 0
  firstStr = tree.keys()[0]
  secondDict = tree[firstStr]
  for key in secondDict.keys():
    if type(secondDict[key]).__name__ == "dict":
      numLeafs += getNumLeafs(secondDict[key])
    else:
      numLeafs += 1
  return numLeafs

def getTreeDepth(tree):
  maxDepth = 0
  firstStr = tree.keys()[0]
  secondDict = tree[firstStr]
  for key in secondDict.keys():
    if type(secondDict[key]).__name__=='dict':
      thisDepth = 1 + getTreeDepth(secondDict[key])
    else:
      thisDepth = 1
  if thisDepth > maxDepth:
    maxDepth = thisDepth
  return maxDepth

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

def plotMidText(centerPt, parentPt, textString):
  xmid = ((parentPt[0] - centerPt[0]) / 2.0) + centerPt[0]
  ymid = ((parentPt[1] - centerPt[1]) / 2.0) + centerPt[1]
  createPlot.ax1.text(xmid, ymid, textString)

def plotTree(myTree, parentPt, nodeTxt):
  numLeafs = getNumLeafs(myTree)
  getTreeDepth(myTree)
  firstStr = myTree.keys()[0]
  cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW,\
    plotTree.yOff)
  plotMidText(cntrPt, parentPt, nodeTxt)
  plotNode(firstStr, cntrPt, parentPt, decisionNode)
  secondDict = myTree[firstStr]
  plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
  for key in secondDict.keys():
    if type(secondDict[key]).__name__=='dict':
      plotTree(secondDict[key],cntrPt,str(key))
    else:
      plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
      plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff),
        cntrPt, leafNode)
      plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
  plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

def createPlot(tree):
  fig = plt.figure(1, facecolor='white')
  fig.clf()
  axprops = dict(xticks=[], yticks=[])
  createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
  plotTree.totalW = float(getNumLeafs(tree))
  plotTree.totalD = float(getTreeDepth(tree))
  plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
  plotTree(tree, (0.5,1.0), "")
  plt.show()

## main
#tree = retrieveTree(1)
#createPlot(tree)
