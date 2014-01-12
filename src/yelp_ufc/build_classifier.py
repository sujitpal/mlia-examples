import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.feature_selection import chi2
import operator

def read_data(fname):
  # read training data and actual categories into temp variables
  f = open(fname, 'rb')
  texts = []
  ys = []
  for line in f:
    rec = json.loads(line.strip())
    texts.append(rec["text"])
    ys.append([
      1 if int(rec["votes"]["useful"]) > 0 else 0,
      1 if int(rec["votes"]["funny"]) > 0 else 0,
      1 if int(rec["votes"]["cool"]) > 0 else 0])
  f.close()
  return texts, np.matrix(ys)

def vectorize(texts, vocab=[]):
  # vectorize the text
  vectorizer = CountVectorizer(min_df=0, stop_words="english") 
  if len(vocab) > 0:
    vectorizer = CountVectorizer(min_df=0, stop_words="english", 
      vocabulary=vocab)
  X = vectorizer.fit_transform(texts)
  # return vocab, text vector and category matrices
  return vectorizer.vocabulary_, X

def print_report(ufc_val, scores):
  print "----"
  print ufc_val + " accuracy:", np.mean([x[0] for x in scores])
  print ufc_val + " precision:", np.mean([x[1] for x in scores])
  print ufc_val + " recall:", np.mean([x[2] for x in scores])

def cross_validate(ufc_val, X, y):
  nrows = X.shape[0]
  kfold = KFold(nrows, 10)
  scores = []
  for train, test in kfold:
    Xtrain, Xtest, ytrain, ytest = X[train], X[test], y[train], y[test]
    clf = MultinomialNB()
    clf.fit(Xtrain, ytrain)
    ypred = clf.predict(Xtest)
    accuracy = accuracy_score(ytest, ypred)
    precision = precision_score(ytest, ypred)
    recall = recall_score(ytest, ypred)
    scores.append((accuracy, precision, recall))
  print_report(ufc_val, scores)

def sorted_features(ufc_val, V, X, y, topN):
  iv = {v:k for k, v in V.items()}
  chi2_scores = chi2(X, y)[0]
  top_features = [(x[1], iv[x[0]], x[0]) 
    for x in sorted(enumerate(chi2_scores), 
    key=operator.itemgetter(1), reverse=True)]
  print "TOP 10 FEATURES FOR:", ufc_val
  for top_feature in top_features[0:10]:
    print "%7.3f  %s (%d)" % (top_feature[0], top_feature[1], top_feature[2])
  return [x[1] for x in top_features]

def main():
  ufc = {0:"useful", 1:"funny", 2:"cool"}
  texts, ys = read_data("yelp_training_set_review.json")
  for ufc_idx, ufc_val in ufc.items():
    print "*** Analysis for", ufc_val
    y = ys[:, ufc_idx].A1
    V, X = vectorize(texts)
    cross_validate(ufc_val, X, y)
    sorted_feats = sorted_features(ufc_val, V, X, y, 10)
    for nfeats in [100, 300, 10000, 30000, 100000]:
      print "USING %d FEATURES FOR %s" % (nfeats, ufc_val)
      V, X = vectorize(texts, sorted_feats[0:nfeats])
      cross_validate(ufc_val, X, y)

if __name__ == "__main__":
  main()
