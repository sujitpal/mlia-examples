from __future__ import division

import os.path

import csv
import scipy.io as sio
import sklearn.feature_extraction.text as sft
import rake as rk
import operator

def extract_keywords(text, stopwords_pattern):
  """
  Calls the RAKE module (from github.com/aneesha/RAKE/rake.py
  with very minor modifications) on the full description to
  create less noisy text for vectorization.
  """
  sentences = rk.splitSentences(text)
  phrase_list = rk.generateCandidateKeywords(sentences, stopwords_pattern)
  word_scores = rk.calculateWordScores(phrase_list)
  keyword_candidates = rk.generateCandidateKeywordScores(
    phrase_list, word_scores)
  sorted_keywords = sorted(keyword_candidates.iteritems(),
    key=operator.itemgetter(1), reverse=True)
  n_keywords = len(sorted_keywords)
  return " ".join(map(lambda x: x[0],
    sorted_keywords[0:int(n_keywords / 3)]))

def build_text_vector(fin, stopwords_pattern):
  """
  Create temporary fields by concatenating text columns to form
  a new column and generate a vector of term frequencies.
  """
  print "Building text vector..."
  fout = str.replace(fin, ".csv", ".text.mtx")
  if os.path.isfile(fout):
    return
  ftmp = str.replace(fin, ".csv", ".tmp")
  reader = csv.reader(open(fin, 'rb'))
  tmpwriter = open(ftmp, 'wb')
  ln = 0
  for row in reader:
    ln += 1
    if ln <= 1:
      continue    # skip header
    if ln % 1000 == 0:
      print "...(processed %d lines)" % (ln)
    title = row[1]
    full_description = extract_keywords(row[2], stopwords_pattern)
    loc_raw = row[3]
    tmpwriter.write(" ".join([
      title, title, title, title, full_description,
      loc_raw, loc_raw]) + "\n")
  tmpwriter.close()
  vectorizer = sft.CountVectorizer(max_features=1000)
#  vectorizer = sft.TfidfVectorizer(
#    charset_error="ignore",
#    strip_accents="ascii",
#    stop_words="english",
#    max_features=100,
#    use_idf=False)
  tmpreader = open(ftmp, 'rb')
  tdmatrix = vectorizer.fit_transform(tmpreader)
  os.remove(ftmp)
  writer = open(fout, 'wb')
  sio.mmwrite(writer, tdmatrix)
  writer.close()

def build_nontext_vector(fin, colname, colidx, normalize):
  """
  Handles the specified column as a categorical variable.
  """
  print "Building category vector for %s" % (colname)
  fout = str.replace(fin, ".csv", "." + colname + ".mtx")
  if os.path.isfile(fout):
    return
  ftmp = str.replace(fin, ".csv", ".tmp")
  reader = csv.reader(open(fin, 'rb'))
  tmpwriter = open(ftmp, 'wb')
  ln = 0
  for row in reader:
    ln += 1
    if ln <= 1:
      continue
    if ln % 1000 == 0:
      print "...(processed %d lines)" % (ln)
    colval = str.lower(row[colidx])
    if normalize:
      colval = str.replace(colval, " ", "_")
    if len(colval.rstrip()) == 0:
      colval = "UNK"
    tmpwriter.write(colval + "\n")
  tmpwriter.close()
  tmpreader = open(ftmp, 'rb')
  vectorizer = sft.CountVectorizer(max_features=100)
  catmatrix = vectorizer.fit_transform(tmpreader)
  os.remove(ftmp)
  writer = open(fout, 'wb')
  sio.mmwrite(writer, catmatrix)
  writer.close()

def main():
  stopword_pattern = rk.buildStopwordRegExPattern("../data/SmartStoplist.txt")
  # training file
  build_text_vector("../data/Train.csv", stopword_pattern)
  build_nontext_vector("../data/Train.csv", "LocationNorm", 4, True)
  build_nontext_vector("../data/Train.csv", "ContractType", 5, True)
  build_nontext_vector("../data/Train.csv", "ContractTime", 6, True)
  build_nontext_vector("../data/Train.csv", "Company", 7, True)
  build_nontext_vector("../data/Train.csv", "Category", 8, True)
  build_nontext_vector("../data/Train.csv", "SourceName", 11, True)
  # test file
  build_text_vector("../data/Valid.csv", stopword_pattern)
  build_nontext_vector("../data/Valid.csv", "LocationNorm", 4, True)
  build_nontext_vector("../data/Valid.csv", "ContractType", 5, True)
  build_nontext_vector("../data/Valid.csv", "ContractTime", 6, True)
  build_nontext_vector("../data/Valid.csv", "Company", 7, True)
  build_nontext_vector("../data/Valid.csv", "Category", 8, True)
  build_nontext_vector("../data/Valid.csv", "SourceName", 9, True)
  
if __name__ == "__main__":
  main()
