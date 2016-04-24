# -*- coding: utf-8 -*-
from __future__ import division
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
from random import shuffle
from sklearn.cross_validation import train_test_split
import nltk
import numpy as np

def tokenize_text(text):
    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            if len(word) < 2:
                continue
            tokens.append(word.lower())
    return tokens
    
def tokenize_tags(label):
    tags = label.split("::")
    tags = map(lambda tok: mark_tag(tok), tags)
    return tags

def jaccard_similarity(labels, preds):
    lset = set(labels)
    pset = set(preds)
    return len(lset.intersection(pset)) / len(lset.union(pset))

def mark_tag(s):
    return "_" + s.replace(" ", "_")
    
def unmark_tag(s):
    return s[1:].replace("_", " ")
 
# read input data
orig_sents = []
sentences = []
fdata = open("../data/tagged_plots.csv", 'rb')
for line in fdata:
    mid, text, label = line.strip().split("\t")
    orig_sents.append(text)
    tokens = tokenize_text(text)
    tags = tokenize_tags(label)
    sentences.append(LabeledSentence(words=tokens, tags=tags))
fdata.close()

# Split model into 90/10 training and test
train_sents, test_sents = train_test_split(sentences, test_size=0.1, 
                                           random_state=42) 

## Build and train model

## PV-DM w/concatenation
#model = Doc2Vec(dm=1, dm_concat=1, size=100, window=5, negative=5, 
#                hs=0, min_count=2)

## PV-DM w/averaging
#model = Doc2Vec(dm=1, dm_mean=1, size=100, window=5, negative=5, 
#                hs=0, min_count=2)                

# PV-DBOW
model = Doc2Vec(dm=0, size=100, negative=5, hs=0, min_count=2)

model.build_vocab(sentences)

alpha = 0.025
min_alpha = 0.001
num_epochs = 20
alpha_delta = (alpha - min_alpha) / num_epochs

for epoch in range(num_epochs):
    shuffle(sentences)
    model.alpha = alpha
    model.min_alpha = alpha
    model.train(sentences)
    alpha -= alpha_delta

# evaluate the model
tot_sim = 0.0
for test_sent in test_sents:
    pred_vec = model.infer_vector(test_sent.words)
    actual_tags = map(lambda x: unmark_tag(x), test_sent.tags)
    pred_tags = model.docvecs.most_similar([pred_vec], topn=5)
    pred_tags = filter(lambda x: x[0].find("_") > -1, pred_tags)
    pred_tags = map(lambda x: (unmark_tag(x[0]), x[1]), pred_tags)
    sim = jaccard_similarity(actual_tags, [x[0] for x in pred_tags])
    tot_sim += sim
print "Average Similarity on Test Set: %.3f" % (tot_sim / len(test_sents))    

# print out random test result
for i in range(5):
    docid = np.random.randint(len(sentences))
    pred_vec = model.infer_vector(sentences[docid].words)
    actual_tags = map(lambda x: unmark_tag(x), sentences[docid].tags)
    pred_tags = model.docvecs.most_similar([pred_vec], topn=5)
    print "Text: %s" % (orig_sents[docid])
    print "... Actual tags: %s" % (", ".join(actual_tags))
    print "... Predicted tags:", map(lambda x: (unmark_tag(
                                     x[0]), x[1]), pred_tags)
