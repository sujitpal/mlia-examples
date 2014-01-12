import pandas as pd
import matplotlib.pyplot as plt
import sys

def main():
  assert(len(sys.argv) == 2)
  df = pd.read_csv("all.csv")
  adf = df.ix[df.attrtype == sys.argv[1]]
  adf_all = adf.ix[adf.nfeats < 0]
  adf_rest = adf.ix[adf.nfeats > 0]
  print adf_all
  print adf_rest
  adf_rest = adf_rest.drop("attrtype", 1)
  adf_rest = adf_rest.set_index("nfeats")
  adf_rest["accuracy_all"] = adf_all[["accuracy"]].values[0][0]
  adf_rest["precision_all"] = adf_all[["precision"]].values[0][0]
  adf_rest["recall_all"] = adf_all[["recall"]].values[0][0]
  adf_rest.plot(title=sys.argv[1])
  plt.show()

if __name__ == "__main__":
  main()
