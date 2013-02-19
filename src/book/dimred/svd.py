from __future__ import division
from numpy import *

def loadDataSet():
#  return[[1, 1, 1, 0, 0],
#         [2, 2, 2, 0, 0],
#         [1, 1, 1, 0, 0],
#         [5, 5, 5, 0, 0],
#         [1, 1, 0, 2, 2],
#         [0, 0, 0, 3, 3],
#         [0, 0, 0, 1, 1]]
  return[[4, 4, 0, 2, 2],
         [4, 0, 0, 3, 3],
         [4, 0, 0, 1, 1],
         [1, 1, 1, 2, 0],
         [2, 2, 2, 0, 0],
         [1, 1, 1, 0, 0],
         [5, 5, 5, 0, 0]]

def svd(D):
  return linalg.svd(D)

def reconstruct(U, S, VT, n):
  return U[:, 0:n] * mat(diag(S[0:n])) * VT[0:n, :]

def euclideanSim(v1, v2):
  return 1.0 / (1.0 + linalg.norm(v1 - v2))

def pearsonSim(v1, v2):
  if len(v1) < 3:
    return 1.0
  return 0.5 + 0.5 * corrcoef(v1, v2, rowvar=0)[0][1]

def cosineSim(v1, v2):
  num = float(v1.T * v2)
  denom = linalg.norm(v1) * linalg.norm(v2)
  return 0.5 + ((0.5 * num) / denom)

def standEst(dataMat, user, simMeas, item):
  n = shape(dataMat)[1]
  simTotal = 0.0
  ratSimTotal = 0.0
  for j in range(0, n):
    userRating = dataMat[user, j]
    if userRating == 0:
      continue
    overlap = nonzero(logical_and(dataMat[:, item].A > 0,
      dataMat[:, j].A > 0))[0]
    if len(overlap) == 0:
      similarity = 0
    else:
      similarity = simMeas(dataMat[overlap, item], dataMat[overlap, j])
    print "similarity(%d,%d)=%f" % (item, j, similarity)
    simTotal += similarity
    ratSimTotal += similarity * userRating
  if simTotal == 0:
    return 0
  else:
    return ratSimTotal / simTotal

def recommend(dataMat, user, N=3, simMeas=cosineSim, estMethod=standEst):
  unratedItems = nonzero(dataMat[user, :].A == 0)[1]
  if len(unratedItems) == 0:
    return "you rated everything"
  itemScores = []
  for item in unratedItems:
    estimatedScore = estMethod(dataMat, user, simMeas, item)
    itemScores.append((item, estimatedScore))
  return sorted(itemScores, key=lambda jj: jj[1], reverse=True)[:N]

def loadDataSet2():
  return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
         [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
         [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
         [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
         [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
         [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
         [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
         [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
         [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
         [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
         [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]

def svdEst(dataMat, user, simMeans, item):
  n = shape(dataMat)[1]
  simTotal = 0.0
  ratSimTotal = 0.0
  U, S, VT = linalg.svd(dataMat)
  S4 = mat(diag(S[0:4]))
  transformedItems = dataMat.T * U[:, :4] * S4.I
  for j in range(0, n):
    userRating = dataMat[user, j]
    if userRating == 0 or j == item:
      continue
    similarity = simMeans(transformedItems[item, :].T, transformedItems[j, :].T)
    print "similarity(%d,%d)=%f" % (item, j, similarity)
    simTotal += similarity
    ratSimTotal += similarity * userRating
  if simTotal == 0:
    return 0
  else:
    return ratSimTotal / simTotal

def printMat(inMat, threshold=0.8):
  for i in range(0, 32):
    for k in range(0, 32):
      if float(inMat[i, k]) > threshold:
        print 1,
      else:
        print 0,
    print ""

def imgCompress(numSV=3, threshold=0.8):
  myl = []
  for line in open('0_5.txt').readlines():
    newRow = []
    for i in range(0, 32):
      newRow.append(int(line[i]))
    myl.append(newRow)
  myMat = mat(myl)
  print "****original matrix******"
  printMat(myMat, threshold)
  U, S, VT = linalg.svd(myMat)
  SigRecon = mat(diag(S[0:numSV]))
  R = U[:, 0:numSV] * SigRecon * VT[0:numSV, :]
  print "****reconstructed matrix using %d singular values******" % numSV
  printMat(R, threshold)
  


#### running the recommendation system with base data
#myMat = mat(loadDataSet())
#recos = recommend(myMat, 2) # recos for user 2
#print "reco(cosine)=", recos
#recos = recommend(myMat, 2, simMeas=euclideanSim)
#print "reco(euclid)=", recos
#recos = recommend(myMat, 2, simMeas=pearsonSim)
#print "reco(pearson)=", recos

### Check for 90% energy
#myMat = loadDataSet2()
#U, S, VT = linalg.svd(mat(myMat))
#S2 = S ** 2
#totalEnergy_90pc = sum(S2) * 0.9
#print "90% of energy=", totalEnergy_90pc
#print sum(S2[0:3])

#### running the recommendation system with svd
#myMat = mat(loadDataSet2())
#recos = recommend(myMat, 2) # recos for user 2
#print "reco(standard,cosine)=", recos
#recos = recommend(myMat, 2, simMeas=euclideanSim)
#print "reco(standard,euclid)=", recos
#recos = recommend(myMat, 2, simMeas=pearsonSim)
#print "reco(standard,pearson)=", recos
#recos = recommend(myMat, 2, estMethod=svdEst) # recos for user 2
#print "reco(svd,cosine)=", recos
#recos = recommend(myMat, 2, simMeas=euclideanSim, estMethod=svdEst)
#print "reco(svd,euclid)=", recos
#recos = recommend(myMat, 2, simMeas=pearsonSim, estMethod=svdEst)
#print "reco(svd,pearson)=", recos

#### see the sharpening of the file using SVD
#imgCompress(3)

