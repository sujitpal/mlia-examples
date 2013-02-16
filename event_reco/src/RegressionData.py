from __future__ import division

import cPickle
import numpy as np
import scipy.io as sio

class DataRewriter:
  def __init__(self):
    self.userIndex = cPickle.load(open("../Models/PE_userIndex.pkl", 'rb'))
    self.eventIndex = cPickle.load(open("../Models/PE_eventIndex.pkl", 'rb'))
    self.userEventScores = sio.mmread("../Models/PE_userEventScores").todense()
    self.userSimMatrix = sio.mmread("../Models/US_userSimMatrix").todense()
    self.eventPropSim = sio.mmread("../Models/EV_eventPropSim").todense()
    self.eventContSim = sio.mmread("../Models/EV_eventContSim").todense()
    self.numFriends = sio.mmread("../Models/UF_numFriends")
    self.userFriends = sio.mmread("../Models/UF_userFriends").todense()
    self.eventPopularity = sio.mmread("../Models/EA_eventPopularity").todense()
    
  def userReco(self, userId, eventId):
    """
    for item i
      for every other user v that has a preference for i
        compute similarity s between u and v
        incorporate v's preference for i weighted by s into running aversge
    return top items ranked by weighted average
    """
    i = self.userIndex[userId]
    j = self.eventIndex[eventId]
    vs = self.userEventScores[:, j]
    sims = self.userSimMatrix[i, :]
    prod = sims * vs
    try:
      return prod[0, 0] - self.userEventScores[i, j]
    except IndexError:
      return 0

  def eventReco(self, userId, eventId):
    """
    for item i 
      for every item j tht u has a preference for
        compute similarity s between i and j
        add u's preference for j weighted by s to a running average
    return top items, ranked by weighted average
    """
    i = self.userIndex[userId]
    j = self.eventIndex[eventId]
    js = self.userEventScores[i, :]
    psim = self.eventPropSim[:, j]
    csim = self.eventContSim[:, j]
    pprod = js * psim
    cprod = js * csim
    pscore = 0
    cscore = 0
    try:
      pscore = pprod[0, 0] - self.userEventScores[i, j]
    except IndexError:
      pass
    try:
      cscore = cprod[0, 0] - self.userEventScores[i, j]
    except IndexError:
      pass
    return pscore, cscore

  def userPop(self, userId):
    """
    Measures user popularity by number of friends a user has. People
    with more friends tend to be outgoing and are more likely to go
    to events
    """
    if self.userIndex.has_key(userId):
      i = self.userIndex[userId]
      try:
        return self.numFriends[0, i]
      except IndexError:
        return 0
    else:
      return 0

  def friendInfluence(self, userId):
    """
    Measures friends influence by the friends who are known (from the
    training set) to go or not go to an event. The average of scores across
    all friends of the user is the influence score.
    """
    nusers = np.shape(self.userFriends)[1]
    i = self.userIndex[userId]
    return (self.userFriends[i, :].sum(axis=0) / nusers)[0,0]

  def eventPop(self, eventId):
    """
    Measures event popularity by the number attending and not attending.
    """
    i = self.eventIndex[eventId]
    return self.eventPopularity[i, 0]

  def rewriteData(self, start=1, train=True, header=True):
    """
    Create new features based on various recommender scores. This
    is so we can figure out what weights to use for each recommender's
    scores.
    """
    fn = "train.csv" if train else "test.csv"
    fin = open("../Data/" + fn, 'rb')
    fout = open("../NewData/" + fn, 'wb')
    # write output header
    if header:
      ocolnames = ["invited", "user_reco", "evt_p_reco",
        "evt_c_reco", "user_pop", "frnd_infl", "evt_pop"]
      if train:
        ocolnames.append("interested")
        ocolnames.append("not_interested")
      fout.write(",".join(ocolnames) + "\n")
    ln = 0
    for line in fin:
      ln += 1
      if ln < start:
        continue
      cols = line.strip().split(",")
      userId = cols[0]
      eventId = cols[1]
      invited = cols[2]
      print "%s:%d (userId, eventId)=(%s, %s)" % (fn, ln, userId, eventId)
      user_reco = self.userReco(userId, eventId)
      evt_p_reco, evt_c_reco = self.eventReco(userId, eventId)
      user_pop = self.userPop(userId)
      frnd_infl = self.friendInfluence(userId)
      evt_pop = self.eventPop(eventId)
      ocols = [invited, user_reco, evt_p_reco,
        evt_c_reco, user_pop, frnd_infl, evt_pop]
      if train:
        ocols.append(cols[4]) # interested
        ocols.append(cols[5]) # not_interested
      fout.write(",".join(map(lambda x: str(x), ocols)) + "\n")
    fin.close()
    fout.close()

  def rewriteTrainingSet(self):
    self.rewriteData(True)

  def rewriteTestSet(self):
    self.rewriteData(False)

# When running with cython, the actual class will be converted to a .so
# file, and the following code (along with the commented out import below)
# will need to be put into another .py and this should be run.

#import CRegressionData as rd

def main():
  dr = DataRewriter()
  print "rewriting training data..."
  dr.rewriteData(train=True, start=2, header=False)
  print "rewriting test data..."
  dr.rewriteData(train=False, start=2, header=True)
  
    
if __name__ == "__main__":
  main()
