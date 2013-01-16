from __future__ import division
from numpy import *

def loadDataSet():
  return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createC1(data):
  C1 = []
  for txn in data:
    for item in txn:
      if not [item] in C1:
        C1.append([item])
  C1.sort()
  return map(lambda x: frozenset(x), C1)

def scanD(D, Ck, minSupport):
  ssCnt = {}
  for tid in D:
    for can in Ck:
      if can.issubset(tid):
        if not ssCnt.has_key(can):
          ssCnt[can] = 1
        else:
          ssCnt[can] += 1
  numItems = float(len(D))
  retList = []
  supportData = {}
  for key in ssCnt:
    support = ssCnt[key] / numItems
    if support >= minSupport:
      retList.insert(0,key)
    supportData[key] = support
  return retList, supportData

def aprioriGen(Lk, k):
  """ Create Ck """
  retList = []
  lenLk = len(Lk)
  for i in range(0, lenLk):
    for j in range(i + 1, lenLk):
      L1 = list(Lk[1])[:k - 2]
      L2 = list(Lk[j])[:k - 2]
      L1.sort()
      L2.sort()
      if L1 == L2:
        retList.append(Lk[i] | Lk[j])
  return retList

def apriori(dataSet, minSupport=0.5):
  C1 = createC1(dataSet)
  D = map(lambda x: set(x), dataSet)
  L1, supportData = scanD(D, C1, minSupport)
  L = [L1]
  k = 2
  while len(L[k - 2]) > 0:
    Ck = aprioriGen(L[k - 2], k)
    Lk, supK = scanD(D, Ck, minSupport)
    supportData.update(supK)
    L.append(Lk)
    k += 1
  return L, supportData
  
def generateRules(L, supportData, minConf=0.7):
  rules = []
  for i in range(1, len(L)):
    for freqSet in L[i]:
      R1 = [frozenset([item]) for item in freqSet]
      if i > 1:
        rulesFromConseq(freqSet, R1, supportData, rules, minConf)
      else:
        calcConf(freqSet, R1, supportData, rules, minConf)
  return rules

def calcConf(freqSet, R, supportData, rules, minConf=0.7):
  prunedR = []
  for conseq in R:
    conf = supportData[freqSet] / supportData[freqSet - conseq]
    if conf > minConf:
      print freqSet - conseq, "-->", conseq, "conf=", conf
      rules.append((freqSet - conseq, conseq, conf))
      prunedR.append(conseq)
  return prunedR

def rulesFromConseq(freqSet, R, supportData, rules, minConf=0.7):
  m = len(R[0])
  if len(freqSet) > (m + 1):
    Rmp1 = aprioriGen(R, m + 1)
    Rmp1 = calcConf(freqSet, Rmp1, supportData, rules, minConf)
    if len(Rmp1) > 1:
      rulesFromConseq(freqSet, Rmp1, supportData, rules, minConf)

# Votesmart database is no longer free
# Congressional Voting Record dataset from UCI ML Repository
# http://archive.ics.uci.edu/ml/datasets/Congressional+Voting+Records
def loadDataSetForCongressionalVotingRecords():
  transDict = {
    "000" : "democrat",
    "001" : "republican",
    "011" : "handicapped infants (yes)",
    "010" : "handicapped infants (no)",
    "021" : "water project cost sharing (yes)",
    "020" : "water project cost sharing (no)",
    "031" : "adoption of budget resolution (yes)",
    "030" : "adoption of budget resolution (no)",
    "041" : "physician fee freeze (yes)",
    "040" : "physician fee freeze (no)",
    "051" : "el salvador aid (yes)",
    "050" : "el salvador aid (no)",
    "061" : "religious groups in schools (yes)",
    "060" : "religious groups in schools (no)",
    "071" : "anti satellite test ban (yes)",
    "070" : "anti satellite test ban (no)",
    "081" : "aid to nicaraguan contras (yes)",
    "080" : "aid to nicaraguan contras (no)",
    "091" : "mx missile (yes)",
    "090" : "mx missile (no)",
    "100" : "immigration (yes)",
    "101" : "immigration (no)",
    "111" : "synfuels corporation cutback (yes)",
    "110" : "synfuels corporation cutback (no)",
    "121" : "education spending (yes)",
    "120" : "education spending (no)",
    "131" : "superfund right to sue (yes)",
    "130" : "superfund right to sue (no)",
    "141" : "crime (yes)",
    "140" : "crime (no)",
    "151" : "duty free exports (yes)",
    "150" : "duty free exports (no)",
    "161" : "export administration act south africa (yes)",
    "160" : "export administration act south africa (no)",
  }
  dataSet = []
  for line in open("house-votes-84.data").readlines():
    cols = line.strip().split(",")
    trans = []
    trans.append("001" if cols[0] == "republican" else "000")
    for idx in range(1, len(cols)):
      if cols[idx] == "n":
        trans.append(str(idx).zfill(2) + "0")
      elif cols[idx] == "y":
        trans.append(str(idx).zfill(2) + "1")
      else:
        pass
#    print trans
    dataSet.append(trans)
  return transDict, dataSet

## Mushroom dataset
## http://archive.ics.uci.edu/ml/datasets/Mushroom
## Not using this, using mushroom.dat which has been pre-encoded.
def loadMushroomRecords():
  dataset = []
  for line in open("mushroom.dat").readlines():
    dataset.append(line.strip().split())
  return dataset


#print [list(itertools.combinations(stuff, l)) for l in range(0, len(stuff)+1)]
#stuff = [1, 2, 3]
#for L in range(0, len(stuff)+1):
#  for subset in itertools.combinations(stuff, L):
#    print(subset)


#dataSet = loadDataSet()
#C1 = createC1(dataSet)
#print "C1=", C1
#D = map(lambda x: set(x), dataSet)
#print "D=", D
#L1, supportData = scanD(D, C1, 0.5)
#print "L1=", L1
#print "supportData=", supportData

#dataSet = loadDataSet()
##La, suppData = apriori(dataSet)
##print "L(minSupport=0.5)=", La
#L, suppData = apriori(dataSet, minSupport=0.5)
#print "L(minSupport=0.7)=", L
#rules = generateRules(L, suppData, minConf=0.5)
#print "rules", rules

#transDict, dataSet = loadDataSetForCongressionalVotingRecords()
#L, supportData = apriori(dataSet, minSupport=0.5)
#print L
#rules = generateRules(L, supportData)
#for rule in rules:
#  ants = " and ".join(map(lambda x: transDict[x], rule[0]))
#  cons = " and ".join(map(lambda x: transDict[x], rule[1]))
#  conf = rule[2]
#  print "%s -> %s (conf=%f)" % (ants, cons, conf)

dataset = loadMushroomRecords()
L, supportData = apriori(dataset, minSupport=0.7)
#for item in L[3]:
#  if item.intersection("2"):
#    print item
print L