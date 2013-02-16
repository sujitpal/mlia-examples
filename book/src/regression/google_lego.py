from time import sleep
import json
import urllib2

def get_google_key():
  return open("/Users/sujit/Documents/Personal/google.lic").read().strip()

def searchForSet(retX, retY, setNum, yr, numPce, origPrc):
  sleep(10)
  myAPIstr = get_google_key()
  searchURL = 'https://www.googleapis.com/shopping/search/v1/public/products?key=%s&country=US&q=lego+%d&alt=json' % (myAPIstr, setNum)
  pg = urllib2.urlopen(searchURL)
  retDict = json.loads(pg.read())
  for i in range(len(retDict['items'])):
    try:
      currItem = retDict['items'][i]
      if currItem['product']['condition'] == 'new':
        newFlag = 1
      else: newFlag = 0
      listOfInv = currItem['product']['inventories']
      for item in listOfInv:
        sellingPrice = item['price']
        if sellingPrice > origPrc * 0.5:
          # filter out fragments, if asking price is less than
          # half of orig price, then it is probably a fragment.
          print "%d\t%d\t%d\t%f\t%f" %\
            (yr,numPce,newFlag,origPrc, sellingPrice)
          retX.append([yr, numPce, newFlag, origPrc])
          retY.append(sellingPrice)
    except: print 'problem with item %d' % i

def setDataCollect(retX, retY):
  searchForSet(retX, retY, 8288, 2006, 800, 49.99)
  searchForSet(retX, retY, 10030, 2002, 3096, 269.99)
  searchForSet(retX, retY, 10179, 2007, 5195, 499.99)
  searchForSet(retX, retY, 10181, 2007, 3428, 199.99)
  searchForSet(retX, retY, 10189, 2008, 5922, 299.99)
  searchForSet(retX, retY, 10196, 2009, 3263, 249.99)

lgX = []
lgY = []
setDataCollect(lgX, lgY)
