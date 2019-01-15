import pandas as pd
import matplotlib.pyplot as plt

# Q2: How many neighbors are needed for normalized Lucene to beat 
# personalized mean on RMSE?
# Answer: (approx 43)
def q2():
  df = pd.read_csv("eval-results.csv")
  # select out LuceneNorm rows and only NNbrs and RMSE.ByUser columns
  df_lucenenorm = df.ix[df.Algorithm == "LuceneNorm", 
                        ["NNbrs", "RMSE.ByUser"]]
  # select out PersMean rows and only NNbrs and RMSE.ByUser columns
  # in case of PersMean, neighborhood size does not matter so no 
  # experiments were performed with varying NNbrs, so our plot will
  # be a horizontal line across all NNbrs values.
  df_persmean = df.ix[df.Algorithm == "PersMean", ["RMSE.ByUser"]]
  # we want average RMSE.ByUser values per NNbr in our plot so we
  # create a new DataFrame based on the mean RMSE.ByUser value per NNbr
  df_plot = pd.DataFrame(df_lucenenorm.groupby(["NNbrs"]).mean())
  df_plot.rename(columns={"RMSE.ByUser" : "RMSE.ByUser.LuceneNorm"}, 
    inplace=True)
  persmean_mean = df_persmean["RMSE.ByUser"].mean()
  # add this column to the df_plot
  df_plot["RMSE.ByUser.PersMean"] = persmean_mean
  df_plot.plot()
  plt.show()

# Q3: How many neighbors are needed for normalized Lucene to beat 
# personalized mean on prediction nDCG?
# Answer: (approx 71).
def q3():
  df = pd.read_csv("eval-results.csv")
  df_lucenenorm = df.ix[df.Algorithm == "LuceneNorm", ["NNbrs", "nDCG"]]
  df_persmean = df.ix[df.Algorithm == "PersMean", ["nDCG"]]
  df_plot = pd.DataFrame(df_lucenenorm.groupby(["NNbrs"]).mean())
  df_plot.rename(columns={"nDCG" : "nDCG.LuceneNorm"}, inplace=True)
  persmean_mean = df_persmean["nDCG"].mean()
  df_plot["nDCG.PersMean"] = persmean_mean
  df_plot.plot()
  plt.show()

def plot_all_algos(metric, ref_algos=None, report_file=None):
  df = pd.read_csv("eval-results.csv")
  # Before starting, split algos into neighbor aware and neighbor unaware
  non_nnbr_algos = df.ix[pd.isnull(df.NNbrs)]["Algorithm"].unique()
  nnbr_algos = df.ix[-pd.isnull(df.NNbrs)]["Algorithm"].unique()
  df_plot = None
  for algo in nnbr_algos:
    if ref_algos is not None and algo not in ref_algos: continue
    dfa = df.ix[df.Algorithm == algo, ["NNbrs", metric]]
    if df_plot is None:
      df_plot = pd.DataFrame(dfa.groupby(["NNbrs"]).mean())
    else:
      df_plot = df_plot.join(dfa.groupby(["NNbrs"]).mean())
    df_plot.rename(columns={metric : "%s.%s" % (metric, algo)}, inplace=True)
  # now add in the columns representing the non-nnbr algos
  for algo in non_nnbr_algos:
    if ref_algos is not None and algo not in ref_algos: continue
    algo_mean = df.ix[df.Algorithm == algo, [metric]].mean()[0]
    df_plot["%s.%s" % (metric, algo)] = algo_mean
  if report_file is not None:
    f = open(report_file, 'wb')
    f.write(df_plot.transpose().to_html())
    f.close()
  df_plot.plot(title=metric)
  plt.show()

# Q4: When is Lucene CBF the best algorithm?
# ( ) Never
# (x) On nDCG, when it is normalized and has many neighbors.
# ( ) On RMSE with a medium number of neighbors
def q4():
  # There are two questions here. One has to do with the nDCG metric 
  # and the other the RMSE.ByUser metric, and the question has to be
  # answered over all algorithms
  for metric in ["RMSE.ByUser", "nDCG"]:
    plot_all_algos(metric)

# Q5: What algorithm produces the most diverse Top-10 lists (by our 
# entropy metric)
# ( ) Popular Movies
# ( ) Unnormalized Lucene
# (x) Item/Pers. Mean
# ( ) Normalized Lucene
# ( ) User-User CF
def q5():
  # We can reuse the work for the previous question to plot all
  # the algorithms against TagEntropy@10 metric
  # "most diverse" == "high entropy", so Item/PersMean
  plot_all_algos("TagEntropy@10", report_file="/tmp/entropy.html")

# Q6: Does increasing neighborhood size generally increase or decrease 
# the tag entropy of top-10 lists?
# (x) Increase
# ( ) Decrease
# can be answered from graph in Q5.

# Q8: In practice, recommenders cost money to run and it isnt worthwhile 
# to run recommenders that take a lot of computational power and provide 
# little benefit. Based on this experiment, what algorithm would be best 
# to deploy for recommending items (in ranked lists) from this data set?
# (x) Popular
# ( ) Normalized Lucene
# ( ) User-user CF
# ( ) Mean Rating
# ( ) Unnormalized Lucene
def q8():
  # We want to find recommenders that are not too expensive to /run/
  # so we use TestTime as our metric
  # the lines on the bottom are a bit hard to differentiate, so we 
  # need to find the average value 
  plot_all_algos("TestTime", report_file="/tmp/testtime.html")
  # even though GlobalMean provides the lowest test times, its more
  # of a baseline, the next best is Popular so we choose that.

# Q9: Ignoring entropy, what user-user configuration generally performs 
# the best?
# (x) Normalized w/ Cosine
# ( ) Unnormalized
# ( ) Normalized
def q9():
  # we want to test RMSE.ByRating, RMSE.ByUser, nDCG, and TopN.nDCG
  # metrics against UserUserCosine, UserUser and UserUserNorm algorithms
  # so we add another hook to restrict the algorithms in plot_all_algos
  ref_algos=["UserUserCosine", "UserUser", "UserUserNorm"]
  plot_all_algos("RMSE.ByRating", ref_algos=ref_algos)
  plot_all_algos("RMSE.ByUser", ref_algos=ref_algos)
  plot_all_algos("nDCG", ref_algos=ref_algos)
  plot_all_algos("TopN.nDCG", ref_algos=ref_algos)
  # UserUserCosine is clearly the winner in all of these.

# Q10: One algorithm has increasing entropy for low neighborhood sizes, 
# and then entropy starts going down. Which is it?
# ( ) Unnormalized Lucene
# (x) Lucene with Normalization
# ( ) User-user CF with Cosine
# ( ) Unnormalized User-User CF
# can be answered from graph in Q5

# Q11: What algorithms beat Popular Items in recommendation list entropy?
# [x] Normalized Lucene
# [x] Item/Pers. Mean
# [x] User-user CF
# [ ] Unnormalized Lucene
# can be answered from graph in Q5  and additional report to disambiguate
# between light and dark blue (Lucene and ItemMean)

# Q12: What is the Top-N nDCG of Popular?
# Answer: 0.475202
def q12():
  df = pd.read_csv("eval-results.csv")
  print("TopN.nDCG(Popular) = %f" % 
    (df.ix[df.Algorithm == "Popular", ["TopN.nDCG"]].mean()[0]))

def main():
  #q2()
  #q3()
  q4()
  #q5() 
  #q8()
  #q9()
  #q12()

if __name__ == "__main__":
  main()
