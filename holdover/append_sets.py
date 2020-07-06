'''
Mixing vec spaces of some infected and benign traffic sources 
'''

from utils import config
import os
import pandas as pd
#import numpy as np
#import yaml

conf = config.conf()


pben='/home/oberljn/iot_bot_det/fs/2018-09-21-capture_vecspace.csv'
pinf='/home/oberljn/iot_bot_det/fs/2018-12-21-15-50-14-192.168.1.195_vecspace.csv'
pinf2='/home/oberljn/iot_bot_det/fs/2019-01-10-19-22-51-192.168.1.198_vecspace.csv'


print('Stacking vector spaces:')
print('- ' + pben)
print('- ' + pinf)
print('...')

df = pd.read_csv(pben).append(pd.read_csv(pinf), sort=True)
df = df.append(pd.read_csv(pinf2), sort=True)

df.fillna(0, inplace=True)
df=df.astype('int')

# Arrange columns
select = [
    'infected',
    ]
ports_sel_s = list()
for col in df.columns:
    if 'srcpt_' in col: ports_sel_s.append(col)
ports_sel_s.sort()
ports_sel_d = list()
for col in df.columns:
    if 'dstpt_' in col: ports_sel_d.append(col)
ports_sel_d.sort()
ports_sel = ports_sel_s + ports_sel_d
select += ports_sel
select += [
    'tcpfg_ns',
    'tcpfg_cwr',
    'tcpfg_ece',
    'tcpfg_urg',
    'tcpfg_ack',
    'tcpfg_psh',
    'tcpfg_rst',
    'tcpfg_syn',
    'tcpfg_fin',
    ]
df = df[select]

# report
print('Percent composition:')
for col in df.columns:
    pct = df[col].sum() / df.shape[0]
    pct = round(pct, 4)
    pad = 15-len(col)
    print(col + ':' + ' '*pad + str(pct))


p = os.path.join( conf['fspath'], 'traintest.csv' )
df.to_csv(p, index=False)
print(p)
