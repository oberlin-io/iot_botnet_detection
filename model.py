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


# Get feature importances
importances = clf.feature_importances_
std = np.std([tree.feature_importances_ for tree in clf.estimators_],axis=0)
indices = np.argsort(importances)[::-1]
#edit put into a csv instead or serve
print("Feature ranking:")
for f in range(X_train.shape[1]):
    print("{}{}{}".format(
        X_train.columns[f],
        ' '*(13-len(X_train.columns[f])),
        round(importances[indices[f]], 4), ))
    
#also see clf.predict_proba(variable 1, variable n)


