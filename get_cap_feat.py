'''
'''

from datetime import datetime as dt
from io import StringIO
import os
import pandas as pd
import subprocess
from time import sleep
import yaml

def cap(pcap, ism, infektd):
    '''
    pcap .pcap file
    ism  output file name
    infektd  infected IP address 
    '''
    fs_masar='../fs' #add replace fs path with config fs path
    
    
    p=os.path.join(fs_masar, pcap)

    tshk=' '.join([
          'sudo tshark',
          #'-i eth0',
          '-r {}'.format(p),
          #'-a duration:{}'.format(duration),
          '-c 20', #testing
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
    sp=subprocess.Popen(tshk, shell=True, stdin=None,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o,e=sp.communicate()
    o=o.decode(encoding='UTF-8')
    df=pd.read_csv(StringIO(o))

    # Periods are annoying in column names
    for c in df.columns:
        c1=c.replace('.','_')
        df.rename(columns={c:c1}, inplace=True)

    # Infected IP address -- labeling malicious packets essentially


    p=os.path.join(fs_masar, ism)
    df.to_csv(p, index=False)
    return df

if __name__=='__main__':
    cap()
