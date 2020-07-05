import seaborn as sns
import pandas as pd
df = pd.read_csv('traintest_sums.csv')
ax = sns.barplot(data=df, x='infected', y='feature',)
#ax.tick_params(axis=x, which=major, pad=10)
#ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment=right,
#    fontweight=light,
#    fontsize=x-large
#)
fig = ax.get_figure()
fig.savefig('img/pos_feature_counts_infected.png')

axNot = sns.barplot(data=df, x='not_infected', y='feature',)
#ax.tick_params(axis=x, which=major, pad=10)
#ax.set_xticklabels(ax.get_xticklabels(), rotation=90, horizontalalignment=right,
#    fontweight=light,
#    fontsize=x-large
#)
fig = ax.get_figure()
fig.savefig('img/pos_feature_counts_not_infected.png')

'''
in bash do:
sudo cp -r iot_bot_det/dev/img/ /var/www/html/
'''

