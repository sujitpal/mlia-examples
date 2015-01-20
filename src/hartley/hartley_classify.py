import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from operator import itemgetter
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

DATA_DIR = "../../data/hartley"

def top_n_features(fimps, n):
    return map(lambda x: x[0], sorted(enumerate(fimps), key=itemgetter(1), 
                                       reverse=True)[0:n])
    
plt.figure()

y = np.loadtxt(os.path.join(DATA_DIR, "y.csv"))
for model_id in range(5):    
    Xgray = np.loadtxt(os.path.join(DATA_DIR, "Xgray.csv"), delimiter=" ")
    Xmedian = np.loadtxt(os.path.join(DATA_DIR, "Xmedian.csv"), delimiter=" ")
    if model_id == 0:
        # gray values
        X = Xgray
    elif model_id == 1:
        # gray values minus median values
        X = Xgray - Xmedian
    elif model_id == 2:        
        # gray values concatenated with median values
        X = np.concatenate((Xgray, Xmedian), axis=1)
    elif model_id == 3:
        # combination 1 and 2
        X = np.concatenate((Xgray, Xmedian, Xgray - Xmedian), axis=1)
    elif model_id == 4:
        # mean shift values and add them in
        Xgray_mu = np.mean(Xgray)
        Xgray_ms = Xgray - Xgray_mu
        Xmedian_mu = np.mean(Xmedian)
        Xmedian_ms = Xmedian - Xmedian_mu
        X = np.concatenate((Xgray, Xmedian, Xgray_ms, Xmedian_ms, 
                            Xgray - Xmedian, Xgray_ms - Xmedian_ms), axis=1)
    clf = RandomForestClassifier(n_estimators=200, max_features="auto", 
                                 oob_score=True, n_jobs=-1)
    # Split data train/test = 75/25
    Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.25, 
                                                    random_state=42)
    clf.fit(Xtrain, ytrain)
    print "OOB Score:", clf.oob_score_
    print "Top 5 Features:", top_n_features(clf.feature_importances_, 5)
    # compute ROC curve data
    ypred = clf.predict_proba(Xtest)
    fpr, tpr, threshold = roc_curve(ytest, ypred[:, 1])
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, label="Model#%d (AUC=%.2f)" % (model_id + 1, roc_auc))

# baseline, axes, labels, etc
plt.plot([0, 1], [0, 1], "k--")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.legend(loc="lower right")
plt.show()
    