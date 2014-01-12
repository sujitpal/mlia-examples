from sklearn.cross_validation import KFold
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.naive_bayes import MultinomialNB
import json
import numpy as np
import operator

def read_data(fname):
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
  vectorizer = CountVectorizer(min_df=0, stop_words="english") 
  if len(vocab) > 0:
    vectorizer = CountVectorizer(min_df=0, stop_words="english", 
      vocabulary=vocab)
  X = vectorizer.fit_transform(texts)
  return vectorizer.vocabulary_, X

def cross_validate(ufc_val, X, y, nfeats):
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
  print ",".join([ufc_val, str(nfeats), 
    str(np.mean([x[0] for x in scores])),
    str(np.mean([x[1] for x in scores])),
    str(np.mean([x[2] for x in scores]))])

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
  texts, ys = read_data("../../data/yelp_ufc/yelp_training_set_review.json")
  print ",".join(["attrtype", "nfeats", "accuracy", "precision", "recall"])
  for ufc_idx, ufc_val in ufc.items():
    y = ys[:, ufc_idx].A1
    V, X = vectorize(texts)
    cross_validate(ufc_val, X, y, -1)
    sorted_feats = sorted_features(ufc_val, V, X, y, 10)
    for nfeats in [1000, 3000, 10000, 30000, 100000]:
      V, X = vectorize(texts, sorted_feats[0:nfeats])
      cross_validate(ufc_val, X, y, nfeats)

if __name__ == "__main__":
  main()
