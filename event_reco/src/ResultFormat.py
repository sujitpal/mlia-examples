from __future__ import division

import pandas as pd

def byDist(x, y):
  return int(y[1] - x[1])

def main():
  # output file
  fout = open("../NewData/final_result.csv", 'wb')
  fout.write(",".join(["User", "Events"]) + "\n")
  resultDf = pd.read_csv("../NewData/result.csv")
  # group remaining user/events
  grouped = resultDf.groupby("user")
  for name, group in grouped:
    user = str(name)
    tuples = zip(list(group.event), list(group.dist), list(group.outcome))
#    tuples = filter(lambda x: x[2]==1, tuples)
    tuples = sorted(tuples, cmp=byDist)
    events = "\"" + str(map(lambda x: x[0], tuples)) + "\""
    fout.write(",".join([user, events]) + "\n")
  fout.close()

if __name__ == "__main__":
  main()