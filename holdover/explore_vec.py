import pandas as pd
df = pd.read_csv('../fs/traintest.csv')

X = df.drop(columns='target')

y = df.target.tolist()

del df


# Drop features that are all 0 or 1
drops = list()
for col in X.columns:
    if X[col].value_counts().shape[0]==1:
        drops.append(col)
        
X.drop(columns=drops, inplace=True)




'''
df.shape
(4440465, 22)
'''
'''
df.isna().sum()
infected       0
srcpt_22       0
srcpt_23       0
srcpt_443      0
srcpt_53       0
srcpt_80       0
srcpt_other    0
dstpt_22       0
dstpt_23       0
dstpt_443      0
dstpt_53       0
dstpt_80       0
dstpt_other    0
tcpfg_ns       0
tcpfg_cwr      0
tcpfg_ece      0
tcpfg_urg      0
tcpfg_ack      0
tcpfg_psh      0
tcpfg_rst      0
tcpfg_syn      0
tcpfg_fin      0
'''


#df[df.infected==0]

corr = X.corr()



'''
/var/www/html/img
'''

import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


# mask upper-right triangle
mask = np.triu(np.ones_like(corr, dtype=np.bool))
# mpl figure
f, ax = plt.subplots(figsize=(11, 9))
# diverging colormap
cmap = sns.diverging_palette(10, 220, as_cmap=True)
# heatmap with the mask and aspect ratio
x = sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
plt.savefig('img/corr.png')
