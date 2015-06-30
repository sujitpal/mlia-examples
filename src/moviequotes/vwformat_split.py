# -*- coding: utf-8 -*-
from __future__ import division
from nltk.corpus import brown
import math
import nltk
import random

INPUT_FILE = "../../data/moviequotes/moviequotes.txt"
VW_TRAIN_FILE = "../../data/moviequotes/train_moviequotes.txt"
VW_TEST_FILE = "../../data/moviequotes/test_moviequotes.txt"
TRAIN_TEST_SPLIT = 0.7

def generality(s):
    """
    Counts the number of personal pronouns (PRP), Indefinite articles (a, an)
    and Past Tense (VBD) per word in sentence.
    """
    words = nltk.word_tokenize(s)
    num_words = len(words)
    postags = [x[1] for x in nltk.pos_tag(words)]
    num_prps = len([x for x in postags if x == "PRP"]) / num_words
    num_indef_articles = len([x for x in words 
            if x.lower() == "a" or x.lower() == "an"]) / num_words
    num_vbds = len([x for x in postags if x == "VBD"]) / num_words
    return num_prps, num_indef_articles, num_vbds

def pad_words(words):
    words.insert(0, "_START_")        
    words.append("_END_")
    return words
    
def browncorpus_gram_freqs(gram_size):
    """ 
    Construct a frequency distribution out of news sentences in Brown
    Corpus available in NLTK
    """
    gram_freqs = nltk.FreqDist()
    num_elems = 0
    for sent in brown.sents(categories=["news"]):
        sent = [x.lower() for x in sent]
        sent = pad_words(sent)
        # construct n-grams
        for ngram in nltk.ngrams(sent, 2):
            num_elems += 1
            gram_freqs[ngram] += 1        
    return gram_freqs, num_elems
    
def distinctiveness(s, gram_size, gram_freqs, num_grams):
    """
    Returns probability of the sentence being from Brown Corpus (news)
    based on the probabilities of the n-gram in the sentence being found
    in the Brown corpus.
    """
    words = nltk.word_tokenize(s)
    words = pad_words(words)
    log_prob = 0.0
    for wgram in nltk.ngrams(words, 2):
        p_wgram = (gram_freqs[wgram] + 1) / (num_grams + len(gram_freqs)) 
        log_prob += math.log(p_wgram)
    return log_prob
    
def vw_format(label, text, gram1_freqs, num_grams1, gram2_freqs,
              num_grams2, gram3_freqs, num_grams3):
    vw_label = "1" if int(label) == 1 else "-1"
    prp, ia, pt = generality(text)
    d1 = distinctiveness(text, 1, gram1_freqs, num_grams1)
    d2 = distinctiveness(text, 2, gram2_freqs, num_grams2)
    d3 = distinctiveness(text, 3, gram3_freqs, num_grams3)
    return "%s |s %s|g prp:%.3f ia:%.3f pt:%.3f|d d1:%.3f d2:%.3f d3:%.3f\n" % \
        (vw_label, text, prp, ia, pt, d1, d2, d3)

def main():
    # load up frequency distributions for calculating distinctiveness
    gram1_freqs, num_grams1 = browncorpus_gram_freqs(1)
    gram2_freqs, num_grams2 = browncorpus_gram_freqs(2)
    gram3_freqs, num_grams3 = browncorpus_gram_freqs(3)
    
    fin = open(INPUT_FILE, 'rb')
    ftrain = open(VW_TRAIN_FILE, 'wb')
    ftest = open(VW_TEST_FILE, 'wb')
    for line in fin:
        label, text = line.strip().split("\t")
        # VW can't handle ":" since its a special character
        text = text.replace(":", " ")
        dice = random.random()
        if dice < TRAIN_TEST_SPLIT:
            ftrain.write(vw_format(label, text, gram1_freqs, num_grams1,
                                   gram2_freqs, num_grams2, gram3_freqs,
                                   num_grams3))
        else:
            ftest.write(vw_format(label, text, gram1_freqs, num_grams1,
                                  gram2_freqs, num_grams2, gram3_freqs,
                                  num_grams3))
    ftest.flush()
    ftrain.flush()
    ftest.close()
    ftrain.close()
    fin.close()
    
if __name__ == "__main__":
    main()
