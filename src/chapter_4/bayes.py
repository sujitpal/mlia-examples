from numpy import __NUMPY_SETUP__
from __future__ import division
from numpy import *

def loadDataSet():
  postingList = [x.split() for x in [
    "my dog has flea problems help please",
    "maybe not take him to the dog park stupid",
    "my dalmatian is so cute I love him",
    "stop posting stupid worthless garbage",
    "mr licks ate my steak how to stop him",
    "quit buying worthless dog food stupid"
  ]]
  labels = [0, 1, 0, 1, 0, 1] # 1 is abusive, 0 not
  return postingList, labels

def createVocabList(dataset):
  vocab = set()
  for doc in dataset:
    vocab = vocab.union(set(doc))
  # need the ordering to be stable when vectorizing
  return list(vocab)

def setOfWords2Vec(vocabs, words):
  vec = [0] * len(vocabs)
  for word in words:
    if word in vocabs:
      vec[vocabs.index(word)] = 1
  return vec

def bagOfWords2Vec(vocabs, words):
  vec = [0] * len(vocabs)
  for word in words:
    if word in vocabs:
      vec[vocabs.index(word)] += 1
  return vec

def trainNB0(data, labels):
  ndocs = len(data)
  nwords = len(data[0])
  p1 = len(filter(lambda x: x == 1, labels)) / len(labels)
  p0Num = ones(nwords) # laplace correction for underflow
  p1Num = ones(nwords) # was zeros(nwords)
  p0Den = 2.0          # was 0.0
  p1Den = 2.0          #
  for i in range(0, ndocs):
    if labels[i] == 1:
      p1Num += data[i]
      p1Den += sum(data[i])
    else:
      p0Num += data[i]
      p0Den += sum(data[i])
  p1Vec = log(p1Num / p1Den) # prevent underflow
  p0Vec = log(p0Num / p0Den) # prevent underflow
  return p0Vec, p1Vec, p1

def classifyNB(vec, p0Vec, p1Vec, p1):
  pPos = sum(vec * p1Vec) + log(p1)
  pNeg = sum(vec * p0Vec) + log(1.0 - p1)
  return 1 if (pPos > pNeg) else 0

def dalmatianTest():
  """ Dalmatian classification """
  dataset, labels = loadDataSet()
  vocab = createVocabList(dataset)
  #print vocab
  #print setOfWords2Vec(vocab, dataset[0])
  #print setOfWords2Vec(vocab, dataset[4])
  trainmatrix = []
  for doc in dataset:
    trainmatrix.append(setOfWords2Vec(vocab, doc))
  p0Vec, p1Vec, p1 = trainNB0(trainmatrix, labels)
  #print p0Vec
  #print p1Vec
  #print p1
  docs = ["love my dalmatian", "stupid garbage"]
  for doc in docs:
    testvec = array(setOfWords2Vec(vocab, doc.split()))
    print "%s -> %d" % (doc,
      classifyNB(testvec, p0Vec, p1Vec, p1))

def textParse(s):
  import re
  tokens = re.split(r'\W*', s)
  return [token.lower() for token in tokens if len(token) > 2]

def spamTest():
  docs = []
  labels = []
  for i in range(1, 26):
    words = textParse(open("email/spam/%d.txt" % (i)).read())
    docs.append(words)
    labels.append(1)
    words = textParse(open("email/ham/%d.txt" % (i)).read())
    docs.append(words)
    labels.append(0)
  vocab = createVocabList(docs)
  # create a random 70/30 train/test set
  ndocs = len(docs)
  ntrain = int(0.7 * ndocs)
  trainidx = set()
  traindocs = []
  trainlabels = []
  while len(trainidx) < ntrain:
    ri = int(random.uniform(0, ndocs))
    if ri not in trainidx:
      traindocs.append(bagOfWords2Vec(vocab, docs[ri]))
      trainlabels.append(labels[ri])
      trainidx.add(ri)
  p0Vec, p1Vec, p1 = trainNB0(traindocs, trainlabels)
  errorCount = 0.0
  testidx = filter(lambda x: x not in trainidx, range(0, ndocs))
  for idx in testidx:
    vec = bagOfWords2Vec(vocab, docs[idx])
    actLabel = classifyNB(vec, p0Vec, p1Vec, p1)
    if actLabel != labels[idx]:
      print "%d: %d <-> %d" % (idx, actLabel, labels[idx])
      errorCount += 1
  print "error rate: %f" % (errorCount / len(testidx))

def calcMostFreq(vocabs, fulltext):
  import operator
  freqDist = {}
  for token in vocabs:
    freqDist[token] = fulltext.count(token)
  return sorted(freqDist.iteritems(),
    key=operator.itemgetter(1), reverse=True)[:30]

def localWordsTest(feed1Url, feed0Url):
  import feedparser
  feed1 = feedparser.parse(feed1Url)
  feed0 = feedparser.parse(feed0Url)
  docs = []
  fulltext = []
  labels = []
  minlen = min(len(feed1["entries"]), len(feed0["entries"]))
  for i in range(0, minlen):
    wordlist = textParse(feed1["entries"][1]["summary"])
    docs.append(wordlist)
    fulltext.extend(wordlist)
    labels.append(1)
    wordlist = textParse(feed0["entries"][1]["summary"])
    docs.append(wordlist)
    fulltext.extend(wordlist)
    labels.append(0)
  vocabs = createVocabList(docs)
  # remove most frequent words (may also be worth removing
  # stopwords instead)
  top30 = calcMostFreq(vocabs, fulltext)
  for kv in top30:
    if kv[0] in vocabs:
      vocabs.remove(kv[0])
  # create random 70/30 train/test set
  ndocs = len(docs)
  ntrain = int(0.7 * ndocs)
  trainidx = set()
  traindocs = []
  trainlabels = []
  while len(trainidx) < ntrain:
    ri = int(random.uniform(0, ndocs))
    if ri not in trainidx:
      traindocs.append(bagOfWords2Vec(vocab, docs[ri]))
      trainlabels.append(labels[ri])
      trainidx.add(ri)
  p0Vec, p1Vec, p1 = trainNB0(traindocs, trainlabels)
  testidx = filter(lambda x: x not in trainidx, range(0, ndocs))
  errorCount = 0.0
  for idx in testidx:
    vec = bagOfWordsToVec(vocabs, docs[idx])
    actLabel = classifyNB(vec, p0Vec, p1Vec, p1)
    if actLabel != labels[idx]:
      errorCount += 1.0
  print "error rate=", errorCount / len(testidx)
  # find top words in each class
  topSf = []
  topNy = []
  for i in range(p0Vec):
    if p0Vec[i] > -6.0:
      topSf.append((vocabs[i], p0Vec[i]))
    else:
      topNy.append((vocabs[i], p1Vec[i]))
  print "Top SF words", sorted(topSf.iteritems(),
    key=operator.itergetter(1), reverse=True)
  print "Top SF words", sorted(topNy.iteritems(),
    key=operator.itergetter(1), reverse=True)


# Dalmatian example
#dalmatianTest()
#spamTest()
localWordsTest("http://newyork.craigslist.org/stp/index.rss",
  "http://sfbay.craigslist.org/stp/index.rss")
