# -*- coding: utf-8 -*-
from __future__ import division

DATA_FILE = "../../data/moviequotes/%s_moviequotes.txt" 
PRED_FILE = "../../data/moviequotes/%s_pred.txt"

def step(x):
    return -1 if x < 0 else 1
    
def main():
    for m in ["train", "test"]:
        fdata = open(DATA_FILE % m, 'rb')
        label_acts = []
        for line in fdata:
            label_acts.append(int(line.split("|")[0].strip()))
        fdata.close()
        label_preds = []
        fpred = open(PRED_FILE % m, 'rb') 
        for line in fpred:
            label_preds.append(step(float(line.strip())))
        fpred.close()
        num_recs = 0
        num_correct = 0
        for act, pred in zip(label_acts, label_preds):
            if act == pred:
                num_correct += 1
            num_recs += 1
        print("Accuracy for %s: %.3f %%" % (m, 100.0 * num_correct / num_recs))
            
if __name__ == "__main__":
    main()
