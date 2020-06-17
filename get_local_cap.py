'''
Build or append to local capture file cap.csv
'''

from datetime import datetime as dt
from io import StringIO
import os
import pandas as pd
import subprocess
from time import sleep
import yaml


def get_sample(tshk):
    
    with open('conf.yaml') as f: conf=yaml.safe_load(f.read())
    
    sampletime=dt.now()

    # Run capture into dataframe
    sp=subprocess.Popen(tshk, shell=True, stdin=None,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o,e=sp.communicate()
    o=o.decode(encoding='UTF-8')
    df=pd.read_csv(StringIO(o))

    # Periods are annoying in column names
    for c in df.columns:
        c1=c.replace('.','_')
        df.rename(columns={c:c1}, inplace=True)

    df['sample_time']=sampletime

    #add flag map

    print(''.join([ 'Sample time: ', sampletime.strftime('%Y-%m-%d %H:%M:%S'), '\n',
                    'Packets: ', str(df.shape[0]), '\n']))

    p=os.path.join(conf['path']['fs'], 'cap.csv')
    if os.path.exists(p):
        #add file size check and slice off head (old)
        df.to_csv(p, index=False, mode='a', header=False)
    else:
        df.to_csv(p, index=False)


def cap(duration=60, interim=4*60):
    '''
    duration: Duration of capture
    interim: Time between previous capture completion to start of next
    '''

    print('Capturing packets. Duration {}s, interim {}s.'.format(duration, interim))

    tshk=' '.join([
          'sudo tshark',
          '-i eth0',
          '-a duration:{}'.format(duration),
          #'-c 20',
          '-T fields',
          '-e frame.number',
          '-e frame.time',
          '-e frame.len',
          #'-e eth.src',
          #'-e eth.dst',
          '-e ip.proto',
          '-e _ws.col.Protocol',
          '-e ip.src',
          '-e ip.dst',
          '-e tcp.srcport',
          '-e tcp.dstport',
          '-e tcp.seq',
          '-e tcp.flags',
          #'-e tcp.payload',
          #'-e frame.protocols',
          '-E header=y',
          '-E separator=,',
          '-E quote=d',
          '-E occurrence=f',
          ])

    while True: #add Consider removing and running this file as a routine in the OS
        get_sample(tshk)
        sleep(interim)

if __name__=='__main__':
    cap()
