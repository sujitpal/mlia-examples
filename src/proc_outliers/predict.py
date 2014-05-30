from __future__ import division
import operator
import os.path
import pandas as pd

DATA_DIR = "/home/sujit/Projects/med_data/cms_gov/outpatient_claims"
EPSILON = 0.0001

# retrieve vocabulary mapping and X matrix
vocab = {}
fvoc = open(os.path.join(DATA_DIR, "vocab.csv"), 'rb')
for line in fvoc:
    key, value = line.strip().split("\t")
    vocab[int(value)] = key
fvoc.close()
opdf = pd.read_csv(
    os.path.join(DATA_DIR, "DE1_0_2008_to_2010_Outpatient_Claims_Sample_1.csv"),
    low_memory=False)

strong_outlier_cutoff = 0.9801980198019802
mild_outlier_cutoff = 0.36633663366336633

fin = open(os.path.join(DATA_DIR, "clusters.txt"), 'rb')
outliers = []
idx = 0
for line in fin:
    line = line.strip()
    x = EPSILON if line == "nan" else float(line)
    if x > mild_outlier_cutoff and x < 1.0:
       outliers.append((idx, x))
    idx += 1
fin.close()

# find corresponding claim ids and claims for verification
outliers_sorted = sorted(outliers, key=operator.itemgetter(0), 
                         reverse=True)[0:10]
colnames = ["CLM_ID"]
colnames.extend([colname for colname in opdf.columns if "_CD_" in colname])
for idx, score in outliers_sorted:
    claim_id = opdf.ix[idx, colnames[0]]
    codes = opdf.ix[idx, colnames[1:]]
    names = ["_".join(x.split("_")[0:2]) for x in colnames[1:]]
    code_names = [":".join([x[0], x[1]]) for x in zip(names, codes.values) 
                                         if pd.notnull(x[1])]
    print("%s %6.4f %s" % (claim_id, score, str(code_names)))
