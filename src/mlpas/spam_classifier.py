from __future__ import division

import re
import nltk
import string
import os
from operator import itemgetter
from nltk.stem import PorterStemmer
from scipy.io import loadmat
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer

def get_vocab(vocab_file):
    vocab = dict()
    fvoc = open(vocab_file, 'rb')
    for line in fvoc:
        cols = line.strip().split("\t")
        vocab[cols[1]] = int(cols[0]) - 1 # Octave is 1-based we need 0-based
    return vocab
        
def preprocess_email(filename, puncts, stemmer):
    fin = open(filename, 'rb')
    text = fin.read()
    fin.close()
    # lowercase
    text = text.lower()
    # strip all HTML
    text = re.sub("<[^<>]+>", "", text)
    # Handle numbers
    text = re.sub("[0-9]+", "number", text)
    # Handle URLs
    text = re.sub("(http|https)://[^\s]*", "httpaddr", text)
    # Handle email addresses
    text = re.sub("[^\s]+@[^\s]+", "emailaddr", text)
    # Handle $ sign
    text = re.sub("[$]+", "dollar", text)
    for sentence in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sentence):
            # get rid of punctuation
            if word in puncts: continue
            # remove non-alpha chars
            word = re.sub("[^a-zA-Z0-9]", "", word)
            # stem the word
            word = stemmer.stem(word)
            # skip word if too short (currently a NOOP)
            if len(word) < 1: continue
            yield word
    

# Preprocess single file and convert to feature vector
vocab = get_vocab("../../data/mlpas/ex6_vocab.txt")
puncts = set(string.punctuation)
stemmer = PorterStemmer()

words = preprocess_email("../../data/mlpas/ex6_emailSample1.txt", puncts, stemmer)
text = " ".join(words)
cv = CountVectorizer(min_df=0, vocabulary=vocab)
feat_vec = cv.fit_transform([text])
print "Length of feature vector:", feat_vec.shape[1]
nzf_vec = feat_vec[0].todense()
print "Number of non-zero entries:", nzf_vec[nzf_vec > 0].shape[1]

# Train Linear SVM for Spam classification
data_train = loadmat("../../data/mlpas/ex6_spamtrain.mat")
Xtrain = data_train["X"]
ytrain = data_train["y"]
clf = LinearSVC(C=0.1)
clf.fit(Xtrain, ytrain.ravel())
ypred = clf.predict(Xtrain)
print "Training accuracy (%):", 100.0 * accuracy_score(ypred, ytrain)

# Test Spam classification
data_test = loadmat("../../data/mlpas/ex6_spamtest.mat")
Xtest = data_test["Xtest"]
ytest = data_test["ytest"]
ypred = clf.predict(Xtest)
print "Test accuracy (%):", 100.0 * accuracy_score(ypred, ytest)

# Top Predictors of spam
# Sort the weights of the SVM to find top 15 features, then match up 
# with reverse mapping of (idx => vocab_word)
weights = sorted([x for x in enumerate(clf.coef_[0])], key=itemgetter(1), 
                  reverse=True)[0:15]
rev_vocab = {vocab[x] : x for x in vocab}
print "Top Predictors of spam"
for top_predictor in [(rev_vocab[w[0]], w[1]) for w in weights]:
    print "%-15s (%5.3f %%)" % (top_predictor[0], top_predictor[1] * 100)
    
# Predict spam against email text
test_files = ["ex6_emailSample1.txt", "ex6_emailSample2.txt", 
              "ex6_spamSample1.txt", "ex6_spamSample2.txt"]
for test_file in test_files:
    words = preprocess_email(os.path.join("../../data/mlpas", test_file), 
                                    puncts, stemmer)
    text = " ".join(words)
    cv = CountVectorizer(min_df=0, vocabulary=vocab)
    feat_vec = cv.fit_transform([text])
    ypred = "Yes" if clf.predict(feat_vec) == 1 else "No"
    print "File: %s, Spam: %s" % (test_file, ypred)
