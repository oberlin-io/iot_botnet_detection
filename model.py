import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from utils import config

conf = config.conf()
fs = conf['fspath'] 
# Get the vector space path per config file
print(conf['network_context'])
vecspace_p = os.path.join(
        fs,
        ''.join(['vecspace_' + conf['network_context'].replace(' ','_'), '.csv']),
)

X = pd.read_csv(vecspace_p)

X = X.dropna() # vecspace had a few unexpected nans. Try to resolve in pcap2vec.py

y = X.target.tolist()
X.drop(columns=['target', 'Ftime', 'Sip', 'Dip',], inplace=True)


# Get train and test splits
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=0)


# Fitting random forest
clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X_train, y_train)

# Test prediction
pred = clf.predict(X_test)


# Get scores
acc = accuracy_score(y_test, pred)
print(acc)

con_mx = confusion_matrix(y_test, pred)
# y-axis is actual, x-axis is predicted, top left is origin
cm = pd.DataFrame(data=con_mx,
    index=['true_pos','true_neg'],
    columns=['pred_pos','pred_neg'],)
print(cm)

from sklearn.metrics import roc_curve, auc
prb = clf.predict_proba(X_test)

# Probability distribution
prb = pd.DataFrame({'malicious': y_test, 'pos_prob': prb[:,1], 'neg_prob': prb[:,0]})
prb['probability'] = np.where(prb.malicious==0, prb.neg_prob, prb.pos_prob)
sel = ['malicious', 'probability']
prb = prb[sel]
prb.to_csv('Decision Probability.csv', index=False)

# Feature importance
importances = clf.feature_importances_
imp = pd.DataFrame({'feature': X_test.columns, 'importance': importances})
imp.to_csv('Feature Importances.csv', index=False)

# ROC - Area under the curve
fpr, tpr, _ = roc_curve(y_test, prb[:,0], pos_label=0) # _ thresholds
aucroc = auc(fpr, tpr)
print(aucroc)

pr = pd.DataFrame({'fpr':fpr, 'tpr':tpr})
pr.to_csv('Receiver Operating Characteristic.csv', index=False)

'''
clf.fit(X_train, y_train)
RandomForestClassifier(bootstrap=True, ccp_alpha=0.0, class_weight=None,
criterion='gini', max_depth=2, max_features='auto',
max_leaf_nodes=None, max_samples=None,
min_impurity_decrease=0.0, min_impurity_split=None,
min_samples_leaf=1, min_samples_split=2,
min_weight_fraction_leaf=0.0, n_estimators=100,
n_jobs=None, oob_score=False, random_state=0, verbose=0,
warm_start=False)

'''

