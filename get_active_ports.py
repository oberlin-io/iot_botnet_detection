'''
Get list of local most active ports from the main cap.csv file.
This could be wrapped into feature selection,
in concert with or in replace of the ports.yaml list.
'''

import os
import pandas as pd
import yaml

def get_active_ports(n=10):
    '''
    Returns list on integers
    n: Number of most active ports
    '''

    with open('conf.yaml') as f: conf=yaml.safe_load(f.read())

    p=os.path.join(conf['path']['fs'], 'cap.csv')
    df=pd.read_csv(p)

    srcp=df.tcp_srcport.value_counts()
    dstp=df.tcp_dstport.value_counts()

    comnp=(srcp+dstp).nlargest(n).index.astype('int')

    return comnp
