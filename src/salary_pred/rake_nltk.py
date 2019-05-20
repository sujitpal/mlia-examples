
# coding: utf-8

# /mnt/Vancouver/apps/rake/nltk-rake/nltk-rake-py3.py

# SOURCE: http://sujitpal.blogspot.ca/2013/03/implementing-rake-algorithm-with-nltk.html
# [Adapted by author Sujit Pal from: github.com/aneesha/RAKE/rake.py]

# Additionally modified by Victoria Stuart [Nov 2017]: Py2 --> Py3; other edits ...

# ----------------------------------------------------------------------------
# REQUIRE SCRIPT TO RUN IN PYTHON 3.5 VENV:
import os

# FIRST, SEE IF WE ARE IN A CONDA VENV { py27: PYTHON 2.7 | py35: PYTHON 3.5 | tf: TENSORFLOW | thee : THEANO }
try:
    os.environ["CONDA_DEFAULT_ENV"]
except KeyError:
    print("\n\tPlease set the py35 { p3 | Python 3.5 } environment!\n")
    exit()

# IF WE ARE IN A CONDA VENV, REQUIRE THE p3 VENV:
if os.environ['CONDA_DEFAULT_ENV'] != "py35":
    print("\n\tPlease set the py35 { p3 | Python 3.5 } environment!\n")
    exit()
# ----------------------------------------------------------------------------

import operator
import nltk
import string

# http://www.nltk.org/api/nltk.html#nltk.probability.FreqDist
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

def isPunct(word):
    return len(word) == 1 and word in string.punctuation

def isNumeric(word):
    try:
        float(word) if '.' in word else int(word)
        return True
    except ValueError:
        return False

class RakeKeywordExtractor:

    def __init__(self):
        # self.stopwords = set(nltk.corpus.stopwords.words())
        self.stopwords = set(nltk.corpus.stopwords.words('english'))
        # self.top_percent = 0.333  ## consider top third candidate keywords by score
        self.top_percent = 1.0      ## consider all candidate keywords by score

    def generate_candidate_keywords(self, sentences):
        '''Victoria: this is a somewhat roundabout way of doing it, but it works.
        If a "word" (words) maps to a stopword or the end of the phrase maps to
        punctuation, then the phrase terminates, with the non-stopword | punctuation'
        words added to separate lists.  Bottom-line: we end up with lists of phrases,
        each a list of words in that phrase, minus stopwords and punctuation.  E.g.:
        [['compatibility'], ['systems'], ['linear', 'constraints'], ['set'], ['natural', 'numbers'],
        ['criteria'], ['compatibility'], ['system'], ['linear', 'diophantine', 'equations'], ...]'''

        phrase_list = []
        for sentence in sentences:
            words = map(lambda x: "|" if x in self.stopwords else x,
                word_tokenize(sentence.lower()))
            phrase = []
            for word in words:
                if word == "|" or isPunct(word):
                    if len(phrase) > 0:
                        phrase_list.append(phrase)
                        phrase = []
                else:
                    phrase.append(word)
        print('\nphrase list:\n', phrase_list, '\n')    ## phrases = lists ['', '', ...] of words
        return phrase_list

    def calculate_word_scores(self, phrase_list):
        # http://www.nltk.org/api/nltk.html#nltk.probability.FreqDist
        # Victoria: needed to separate these, otherwise freq counts not correct! :
        fdist1 = FreqDist()
        fdist2 = FreqDist()
        word_freq = fdist1
        word_degree = fdist2
        i = 1
        for phrase in phrase_list:
            print('----------\nPhrase %d:' % i)
            i  += 1
            print('phrase:', phrase)
            for word in phrase:
                word_freq[word] +=1
                print(' * cumulative word freq for word "' + word + '": ' + str(word_freq[word]))
                word_degree[word] += len(phrase)
                print('   word degree[word] (cumulative):', word_degree[word])
        # https://codelingo.wordpress.com/2017/05/26/keyword-extraction-using-rake/
        # scoring (see article, above, for an excellent summary!): word score = deg(w) / freq(w)
        word_scores = {}
        for word in word_freq.keys():
            word_scores[word] = word_degree[word] / word_freq[word]
        print()
        return word_scores

    def calculate_phrase_scores(self, phrase_list, word_scores):
        phrase_scores = {}
        for phrase in phrase_list:
            phrase_score = 0
            for word in phrase:
                phrase_score += word_scores[word]
            phrase_scores[" ".join(phrase)] = phrase_score
        return phrase_scores

    def extract(self, text, incl_scores=False):
        sentences = nltk.sent_tokenize(text)
        phrase_list = self.generate_candidate_keywords(sentences)
        word_scores = self.calculate_word_scores(phrase_list)
        phrase_scores = self.calculate_phrase_scores(
            phrase_list, word_scores)
        sorted_phrase_scores = sorted(phrase_scores.items(),
            key=operator.itemgetter(1), reverse=True)
        n_phrases = len(sorted_phrase_scores)
        if incl_scores:
            return sorted_phrase_scores[0:int(n_phrases * self.top_percent)]
        else:
            return map(lambda x: x[0],
                sorted_phrase_scores[0:int(n_phrases * self.top_percent)])

# text1 = "1.0. Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types of systems and systems of mixed types."

text1 = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating sets of solutions for all types of systems are given. These criteria and the corresponding algorithms for constructing a minimal supporting set of solutions can be used in solving all the considered types of systems and systems of mixed types."

text2="Halifax, an Atlantic Ocean port in eastern Canada, is the provincial capital of Nova Scotia. A major business centre, it's also known for its maritime history. The city's dominated by the hilltop Citadel, a star-shaped fort completed in the 1850s. Waterfront warehouses known as the Historic Properties recall Halifax's days as a trading hub for privateers, notably during the War of 1812. Halifax, legally known as the Halifax Regional Municipality (HRM), is the capital of the province of Nova Scotia, Canada. The municipality had a population of 403,131 in 2016, with 316,701 in the urban area centred on Halifax Harbour. The regional municipality consists of four former municipalities that were amalgamated in 1996: Halifax, Dartmouth, Bedford, and the Municipality of Halifax County. Halifax is a major economic centre in Atlantic Canada with a large concentration of government services and private sector companies. Major employers and economic generators include the Department of National Defence, Dalhousie University, Saint Mary's University, the Halifax Shipyard, various levels of government, and the Port of Halifax. Agriculture, fishing, mining, forestry and natural gas extraction are major resource industries found in the rural areas of the municipality. Halifax was ranked by MoneySense magazine as the fourth best place to live in Canada for 2012, placed first on a list of 'large cities by quality of life' and placed second in a list of 'large cities of the future', both conducted by fDi Magazine for North and South American cities. Additionally, Halifax has consistently placed in the top 10 for business friendliness of North and South American cities, as conducted by fDi Magazine. For a city with more pubs and clubs per capita than almost any city in Canada, it's fitting that our most famous brewmaster was also our mayor. Three times. Alexander Keith's original 1820 brewery welcomes visitors with costumed guides, stories and, of course, good ale. Walk across the street from Keith's Brewery to the Halifax waterfront boardwalk that follows the water's edge alongside the world’s second largest ice-free harbour. Stretching from the Canadian Museum of Immigration at Pier 21 - the gateway into Canada for over one million immigrants - to Casino Nova Scotia, you’ll pass unique shops, restaurants, and in the warmer months, graceful tall ships. Hop aboard the ferry, North America's longest running saltwater ferry, in fact, and cross the harbour to the Dartmouth side which is filled with more locally-owned shops, galleries, cafés, restaurants, and pubs. A visit to Halifax is not complete without trying the fabled donair, the official food of Halifax. Become a soldier for a day at Halifax Citadel National Historic Site. Visit a 200-year-old restored fishing village at Fisherman’s Cove. Hear captivating sea stories from small to the Titanic at the Maritime Museum of the Atlantic. Discover the stories of over 1 million immigrants who landed in Halifax at Pier 21. Explore the new Halifax Central Library, named as one of CNN's 10 eye-popping new buildings in 2014. Skate or bike The Emera Oval. The long-track speed skating oval on the Halifax Commons is an outdoor activity destination in summer and in winter. Stroll through the beautiful Victorian flower gardens and grounds at Halifax Public Gardens. Take in one of Canada’s best walks along the Halifax Waterfront. Be inspired by Atlantic Canada’s largest art collection at the Art Gallery of Nova Scotia. Ride the oldest running saltwater ferry service in North America (second oldest in the world) when you take the ferry between Dartmouth and Halifax. Experience the craftsmanship of Canada's only mouth-blown, hand-cut crystal maker, NovaScotian Crystal on the Halifax Waterfront. Venture to McNabs Island, located at the mouth of the Halifax Harbour, for secluded trails, a beautiful beach, and a historic fort. Explore the oldest continuously running farmers' market in North America at the Halifax Seaport Farmers' Market. Visit Alderney Landing on the Dartmouth Waterfront and peruse the shops, art gallery, community theatre, and restaurants. For the golfer - you have plenty of golfing choices to make while golfing in Halifax Metro."

print('\ntext1:\n', text1, '\n')

def test():
    rake = RakeKeywordExtractor()
    keywords = rake.extract(text1, incl_scores=True)
    print(keywords)

if __name__ == "__main__":
    test()
    print()
