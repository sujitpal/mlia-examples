# -*- coding: utf-8 -*-
from __future__ import division, print_function
import operator
import os
import re

DATA_DIR = "../../data/student-alcohol"
DATA_FILES = ["student-por.csv", "student-mat.csv"]

SUBJ_DICT = { "por": 0, "mat": 1 }
SCHOOL_DICT = { "GP": 0, "MS": 1 }
SEX_DICT = { "F": 0, "M": 1 }
ADDR_DICT = { "U" : 0, "R": 1 }
FAMSIZE_DICT = { "LE3": 0, "GT3": 1 }
PSTAT_DICT = { "T": 0, "A": 1 }
JOB_DICT = { "teacher": [1, 0, 0, 0, 0], 
             "health": [0, 1, 0, 0, 0],
             "services": [0, 0, 1, 0, 0],
             "at_home": [0, 0, 0, 1, 0],
             "other": [0, 0, 0, 0, 1] }
REASON_DICT = { "home": [1, 0, 0, 0],
                "reputation": [0, 1, 0, 0],
                "course": [0, 0, 1, 0],
                "other": [0, 0, 0, 1] }
GUARDIAN_DICT = { "mother": [1, 0, 0],
                  "father": [0, 1, 0],
                  "other": [0, 0, 1] }
YORN_DICT = { "yes": 0, "no": 1 }

def expand_options(colvalues):
    options = sorted([(k, v.index(1)) for k, v in colvalues.items()],
                      key=operator.itemgetter(1))
    return [k for k, v in options]
    
def get_output_cols(colnames):
    ocolnames = []
    ocolnames.append("subject")
    for colname in colnames:
        if colname in ["Mjob", "Fjob"]:
            for option in expand_options(JOB_DICT):
                ocolnames.append(":".join([colname, option]))
        elif colname == "reason":
            for option in expand_options(REASON_DICT):
                ocolnames.append(":".join([colname, option]))
        elif colname == "guardian":
            for option in expand_options(GUARDIAN_DICT):
                ocolnames.append(":".join([colname, option]))
        elif colname in ["Dalc", "Walc"]:
            continue
        else:
            ocolnames.append(colname)
    ocolnames.append("alcohol")
    return ocolnames        
        
def preprocess_data(cols, colnames, subj):
    pcols = []
    alc = 0.0
    pcols.append(str(SUBJ_DICT[subj]))
    for i, col in enumerate(cols):
        if colnames[i] == "school":
            pcols.append(str(SCHOOL_DICT[col]))
        elif colnames[i] == "sex":
            pcols.append(str(SEX_DICT[col]))
        elif colnames[i] == "age":
            pcols.append(col)
        elif colnames[i] == "address":
            pcols.append(str(ADDR_DICT[col]))
        elif colnames[i] == "famsize":
            pcols.append(str(FAMSIZE_DICT[col]))
        elif colnames[i] == "Pstatus":
            pcols.append(str(PSTAT_DICT[col]))
        elif colnames[i] in ["Medu", "Fedu"]:
            pcols.append(col)
        elif colnames[i] in ["Mjob", "Fjob"]:
            for v in JOB_DICT[col]:
                pcols.append(str(v))
        elif colnames[i] == "reason":
            for v in REASON_DICT[col]:
                pcols.append(str(v))
        elif colnames[i] == "guardian":
            for v in GUARDIAN_DICT[col]:
                pcols.append(str(v))
        elif colnames[i] in ["traveltime", "studytime", "failures"]:
            pcols.append(col)
        elif colnames[i] in ["schoolsup", "famsup", "paid", 
                             "activities", "nursery", "higher",
                             "internet", "romantic"]:
            pcols.append(str(YORN_DICT[col]))
        elif colnames[i] in ["famrel", "freetime", "goout",
                             "health", "absences", "G1", "G2", "G3"]:
            pcols.append(col)
        elif colnames[i] == "Dalc":
            alc += 5 * int(col)
        elif colnames[i] == "Walc":
            alc += 2 * int(col)
    alc /= 7
    is_drinker = 0 if alc < 3 else 1
    pcols.append(str(is_drinker))
    return ";".join(pcols)

colnames = []
fout = open(os.path.join(DATA_DIR, "merged-data.csv"), "wb")
for data_file in DATA_FILES:
    subj = data_file.split(".")[0].split("-")[1]
    fdat = open(os.path.join(DATA_DIR, data_file), "rb")
    for line in fdat:
        line = line.strip()
        if line.startswith("school;"):
            if len(colnames) == 0:
                colnames = line.split(";")
            continue
        cols = [re.sub("\"", "", x) for x in line.split(";")]
        pline = preprocess_data(cols, colnames, subj)
        fout.write("{:s}\n".format(pline))
    fdat.close()
fout.close()

fcolnames = open(os.path.join(DATA_DIR, "merged-colnames.txt"), "wb")
output_colnames = get_output_cols(colnames)
for ocolname in output_colnames:
    fcolnames.write("{:s}\n".format(ocolname))
fcolnames.close()
