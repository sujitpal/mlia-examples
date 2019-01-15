from __future__ import division
import itertools
import numpy as np
import os.path
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

def join_codes(row):
    return " ".join([str(v) for i, v in row.iteritems() if pd.notnull(v)])
    
DATA_DIR = "/home/sujit/Projects/med_data/cms_gov/outpatient_claims"
EPSILON = 0.1

# extract codes as bag of codes from input
opdf = pd.read_csv(
    os.path.join(DATA_DIR, "DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv"),
    low_memory=False)
opdf.head()

colnames = [colname for colname in opdf.columns if "_CD_" in colname]
bcdf = opdf.ix[:, colnames].apply(join_codes, axis=1)

# build a code-document matrix out of the codes
vec = CountVectorizer(min_df=1, binary=True)
X = vec.fit_transform(bcdf)

# compute similarities
# for a code-document matrix, similarity between 2 documents is given
# by the matrix X*X.T. We are looking for similarity between 2 codes
# based on them co-occurring in the same document, so we can generate
# the similarities using X.T * X (verified manually)
sim = X.T * X

# each claim can be thought of as a cluster of "related" codes, where
# the similarity between codes i and j is given by sim(i,j). We assign
# the distance between two concepts as 1/sim(i,j). The cluster density
# is the average root mean square distance betwen all (i,j) pairs.
fout = open(os.path.join(DATA_DIR, "clusters.txt"), 'wb')
for row in range(0, X.shape[0]):
    codes = [code for code in X[row, :].nonzero()][1]
    dists = []
    for i, j in itertools.product(codes, codes):
        if i < j:
            sim_ij = sim.getrow(i).todense()[:, j][0]
            if sim_ij == 0:
                sim_ij = EPSILON
            dists.append(1 / (sim_ij ** 2)) 
    fout.write("%f\n" % (np.sqrt(sum(dists)) / len(dists)))
fout.close()

