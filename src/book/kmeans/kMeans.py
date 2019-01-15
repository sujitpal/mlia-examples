from __future__ import division
from numpy import *

def loadDataSet(filename):
  data = []
  for line in open(filename).readlines():
    data.append(map(lambda x: float(x), line.strip().split("\t")))
  return mat(data)

def euclideanDist(vecA, vecB):
  return sqrt(sum(power(vecA - vecB, 2)))

def randCent(data, k):
  n = shape(data)[1]
  centroids = mat(zeros((k, n)))
  for j in range(0, n):
    minJ = min(data[:, j])
    rangeJ = float(max(data[:, j]) - minJ)
    centroids[:, j] = minJ + (rangeJ * random.rand(k, 1))
  return centroids

def kMeans(data, k, dist=euclideanDist, createCent=randCent):
  m = shape(data)[0]
  clusterAssign = mat(zeros((m, 2)))
  centroids = createCent(data, k)
  clusterChanged = True
  niter = 0
  while clusterChanged:
    clusterChanged = False
    for i in range(0, m):
      minDist = inf
      minIndex = -1
      for j in range(0, k):
        distJI = dist(centroids[j, :], data[i, :])
        if distJI < minDist:
          minDist = distJI
          minIndex = j
      if clusterAssign[i, 0] != minIndex:
        clusterChanged = True
      clusterAssign[i, :] = minIndex, minDist**2
    print "iteration=", niter, "centroids=", centroids
    for ci in range(0, k):
      ptsInCluster = data[nonzero(clusterAssign[:, 0].A == ci)[0]]
      centroids[ci, :] = mean(ptsInCluster, axis=0)
    niter += 1
  return centroids, clusterAssign

def scatterplot(data, assigns, centroids):
  import matplotlib
  import matplotlib.pyplot as plt
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.scatter(data[:, 0].flatten().A[0],
    data[:, 1].flatten().A[0],
    c=assigns[:, 0].flatten().A[0])
  ax.scatter(centroids[:, 0].flatten().A[0],
    centroids[:, 1].flatten().A[0], marker="+", s=300)
  plt.show()

def bisectingKMeans(dataSet, k, distMeas=euclideanDist):
  m = shape(dataSet)[0]
  clusterAssment = mat(zeros((m,2)))
  centroid0 = mean(dataSet, axis=0).tolist()[0]
  centList =[centroid0] #create a list with one centroid
  for j in range(m):#calc initial Error
    clusterAssment[j,1] = distMeas(mat(centroid0), dataSet[j,:])**2
  while (len(centList) < k):
    lowestSSE = inf
    for i in range(len(centList)):
      ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]#get the data points currently in cluster i
      centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
      sseSplit = sum(splitClustAss[:,1])#compare the SSE to the currrent minimum
      sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
      print "sseSplit, and notSplit: ",sseSplit,sseNotSplit
      if (sseSplit + sseNotSplit) < lowestSSE:
        bestCentToSplit = i
        bestNewCents = centroidMat
        bestClustAss = splitClustAss.copy()
        lowestSSE = sseSplit + sseNotSplit
      bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) #change 1 to 3,4, or whatever
      bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
      print 'the bestCentToSplit is: ',bestCentToSplit
      print 'the len of bestClustAss is: ', len(bestClustAss)
      centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids
      centList.append(bestNewCents[1,:].tolist()[0])
      clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reassign new clusters, and SSE
  return mat(centList), clusterAssment

def slcDist(vecA, vecB):
  a = sin(vecA[0, 1] * pi / 180) * sin(vecB[0, 1] * pi / 180)
  b = cos(vecA[0, 1] * pi / 180) * cos(vecB[0, 1] * pi / 180) * \
      cos(pi * (vecB[0, 0] - vecA[0, 0]) / 180)
  return arccos(a + b)*6371.0

def clusterClubs(numClust=5):
  import matplotlib
  import matplotlib.pyplot as plt
  datList = []
  for line in open('places.txt').readlines():
    lineArr = line.split('\t')
    datList.append([float(lineArr[4]), float(lineArr[3])])
  datMat = mat(datList)
  myCentroids, clustAssing = bisectingKMeans(
    datMat, numClust, distMeas=slcDist)
  fig = plt.figure()
  rect=[0.1,0.1,0.8,0.8]
  scatterMarkers=['s', 'o', '^', '8', 'p', 'd', 'v', 'h', '>', '<']
  axprops = dict(xticks=[], yticks=[])
  ax0 = fig.add_axes(rect, label='ax0', **axprops)
  imgP = plt.imread('Portland.png')
  ax0.imshow(imgP)
  ax1 = fig.add_axes(rect, label='ax1', frameon=False)
  for i in range(numClust):
    ptsInCurrCluster = datMat[nonzero(clustAssing[:, 0].A == i)[0], :]
    markerStyle = scatterMarkers[i % len(scatterMarkers)]
    ax1.scatter(ptsInCurrCluster[:, 0].flatten().A[0],
      ptsInCurrCluster[:, 1].flatten().A[0],
      marker=markerStyle, s=90)
    ax1.scatter(myCentroids[:, 0].flatten().A[0],
      myCentroids[:, 1].flatten().A[0], marker='+', s=300)
  plt.show()

# test
#data = loadDataSet("testSet.txt")
#centroids = randCent(data, 2)
#print "centroids=", centroids
#dist = euclideanDist(data[0], data[1])
#print "dist=", dist

### plain kmeans
#centroids, assigns = kMeans(data, 4)
#print "final centroids=", centroids
#print "#-clusters=", len(centroids)
#for ci in range(0, len(centroids)):
#  cluster = []
#  for ri in range(0, shape(assigns)[0]):
#    row = assigns[ri, :]
#    if int(row.A[0][0]) == ci:
#      cluster.append(data[ri, :])
#scatterplot(data, assigns, centroids)

### bisecting kmeans
#data = loadDataSet("testSet2.txt")
#print data
#centroids, assigns = bisectingKMeans(data, 3)
#scatterplot(data, assigns, centroids)

clusterClubs(5)
