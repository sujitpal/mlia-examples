import urllib
import json
from time import sleep

def getYahooAppID():
  return open("/Users/sujit/Documents/Personal/yahoo.lic").read()

def geoGrab(stAddress, city):
  apiStem = 'http://where.yahooapis.com/geocode?'
  params = {}
  params['flags'] = 'J'
  params['appid'] = getYahooAppID()
  params['location'] = '%s %s' % (stAddress, city)
  url_params = urllib.urlencode(params)
  yahooApi = apiStem + url_params
  print yahooApi
  c=urllib.urlopen(yahooApi)
  return json.loads(c.read())

def massPlaceFind(fileName):
  fw = open('places.txt', 'w')
  for line in open(fileName).readlines():
    line = line.strip()
    lineArr = line.split('\t')
    retDict = geoGrab(lineArr[1], lineArr[2])
    if int(retDict["ResultSet"]["Error"]) == 0:
      lat = float(retDict['ResultSet']['Results'][0]['latitude'])
      lng = float(retDict['ResultSet']['Results'][0]['longitude'])
      print "%s\t%f\t%f" % (lineArr[0], lat, lng)
      fw.write('%s\t%f\t%f\n' % (line, lat, lng))
    else:
      print "error fetching: %s" % retDict["ResultSet"]["Error"]
    sleep(1)
  fw.close()

# test out API
#print geoGrab('1 VA Center', 'Augusta, ME')
massPlaceFind("portlandClubs.txt")
