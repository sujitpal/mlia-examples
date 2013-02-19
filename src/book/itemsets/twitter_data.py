from __future__ import division
import twitter
from time import sleep
import re
import fpgrowth

def getTwitterAuthData(licfile):
  auth = {}
  for line in open(licfile).readlines():
    kvs = line.strip().split("=")
    auth[str.lower(kvs[0])] = kvs[1]
  return auth

def getLotsOfTweets(searchStr, output):
  auth = getTwitterAuthData("/Users/sujit/Documents/Personal/twitter.lic")
  api = twitter.Api(consumer_key=auth["consumer_key"],
                    consumer_secret=auth["consumer_secret"],
                    access_token_key=auth["access_token"],
                    access_token_secret=auth["access_token_secret"])
  fo = open(output, 'wb')
  for i in range(1, 15):
    print "fetching page:", i
    searchresults = api.GetSearch(searchStr, per_page=100, page=i)
    for searchresult in searchresults:
      fo.write(searchresult.GetText().encode("ascii", "replace") + "\n")
    sleep(6)
  fo.close()

def textParse(bigstring):
  urlsremoved = re.sub('(http[s]?:[/][/]|www.)([a-z]|[A-Z]|[0-9]|[/.]|[~])*',
    '', bigstring)
  listOfTokens = re.split(r'\W*', urlsremoved)
  return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def mineTweets(inputfile, minSup=5):
  parsedList = []
  for line in open(inputfile).readlines():
    parsedList.append(textParse(line.strip()))
  initSet = fpgrowth.createInitSet(parsedList)
  myFPTree, myHeaderTab = fpgrowth.createTree(initSet, minSup)
  myFreqList = []
  fpgrowth.mineTree(myFPTree, myHeaderTab, minSup, set([]), myFreqList)
  return myFreqList

## gather data from twitter
#getLotsOfTweets("RIMM", "rimm.dat")

# how many itemsets occurred in at least 20 docs
listOfTerms = mineTweets("rimm.dat", minSup=20)
for term in listOfTerms:
  print term

