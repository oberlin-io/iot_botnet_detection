'''
Runs tshark every N seconds for N seconds
on interface
Transforms each sample into vector space
and appends to a vector space file named per the context
set in config
'''
from utils import config
import os
import subprocess
from time import sleep
import pandas as pd
import numpy as np
import sys
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

conf = config.conf()

fs = conf['fspath']
duration = conf['sample']['batch_duration']
every_sec = conf['sample']['every_second']

print(conf['network_context'])
vecspace_p = os.path.join(
        fs,
        ''.join(['vecspace_' + conf['network_context'].replace(' ','_'), '.csv']),
)

fields = list()
print('Setting capture fields...')
for field, values in conf['fields'].items():
    if values['capture']==True:
        fields.append(' '.join(['-e', field]))
        pad = (20-len(field))*'.'
        print(''.join([field, pad, values['aka']]))

tshk = list()
tshk += [
    'sudo tshark',
    '-i eth0',
    #'-r {}'.format(pcap_path),
    '-a duration:{}'.format(duration),
    #'-c 20', #testing
    '-T fields',
]
tshk += fields
tshk += [
    '-E header=y',
    '-E separator=,',
    '-E quote=d',
    '-E occurrence=f',
    #'> {}'.format(csv_path),
]


tshk = ' '.join(tshk)
print(tshk)

while True:
    sp=subprocess.Popen(tshk, shell=True, stdin=None,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print('Capturing for {} seconds...'.format(duration))
    o,e = sp.communicate()

    print('Processing batch...')
    b = o.decode('utf-8')
    b = StringIO(b)

    df = pd.read_csv(b)

    rename = dict()
    for field, values in conf['fields'].items():
        if values['capture']==True:
            rename[field] = values['aka']
    df.rename(columns=rename, inplace=True)

    # Filter out non TCP and UDP. No nulls in all port columns
    df = df[ (df.Sporttcp.notna()) | (df.Sportudp.notna()) ]
            
    # Make comprehensive port columns. Where TCP ports null, fill with UDP ports
    mapp = np.where(df.Sporttcp.isna(), df.Sportudp, df.Sporttcp)
    df['Sport'] = mapp
    mapp = np.where(df.Dporttcp.isna(), df.Dportudp, df.Dporttcp)
    df['Dport'] = mapp

    df.drop(columns=['Sporttcp','Dporttcp','Sportudp','Dportudp'], inplace=True)

    # port selection
    ports = conf['ports']
    for direc in ['Sport', 'Dport',]:
        df.loc[ ~df[direc].isin(ports), direc ] = '{}other'.format(direc)
    
    for port in ports:
        for direc in ['Sport', 'Dport',]:
            x = ''.join([direc, str(port)])
            df.loc[ df[direc]==port, direc ] = x

    # encode ports
    for direc in ['Sport', 'Dport',]:
        df = df.join( pd.get_dummies(df[direc]), how='left' )

    df.drop(columns=['Sport', 'Dport',], inplace=True)

    # add ports in config but not in batch capture (later sort columns to arrange for append)
    for port in ports:
        s = ''.join(['Sport',str(port)])
        d = ''.join(['Dport',str(port)])
        if not s in df.columns: df[s] = 0
        if not d in df.columns: df[d] = 0


    # TCP flags decode-encode
    # See https://www.manitonetworks.com/flow-management/2016/10/16/decoding-tcp-flags
    
    # UDP though has no flags
    df.loc[df.FG.isna(), 'FG'] = 'None'

    flags = ['FGns', 'FGcwr', 'FGece', 'FGurg', 'FGack', 'FGpsh', 'FGrst', 'FGsyn', 'FGfin', ]

    d = dict()
    for f in flags:
        d[f] = list()

    def decode_encode_flags(x):
        if x == 'None':
            b = '0'*9
        else:
            b = bin(int(x, 16))[2:].zfill(9)
        for i in range(9):
            if b[i] == '0':
                d[flags[i]].append(0)
            elif b[i] == '1':
                d[flags[i]].append(1)
    
    #bug some batches have last few rows FG nans
    df = df.sample(frac=1).reset_index(drop=True)
    # Why does this shuffle produce no nans,
    # but excluding the shuffle makes many nans on the tail end?
    
    _ = df.FG.apply(lambda x: decode_encode_flags(x))
    df = df.join( pd.DataFrame(d), how='left')

    df.drop(columns='FG', inplace=True)

    # Label the target via IP
    target_ips = list()
    for pcap in conf['pcaps']:
        if not pcap['target_ips'] is None:
            target_ips += pcap['target_ips']
    for ip in target_ips:
        df.loc[ (df.Sip==ip) | (df.Dip==ip), 'target' ] = 1
        df.target = df.target.fillna(0)
        df.target = df.target.astype('int')
    

    # sort columns alpha for correct append
    cols = df.columns.tolist()
    cols.sort()
    for col in ['Dip', 'Sip', 'Ftime', 'target',]:
        cols.remove(col)
        cols.insert(0, col)
    df = df[cols]
    
    if os.path.isfile(vecspace_p):
        with open(vecspace_p, 'a') as f:
            df.to_csv(f, index=False, header=False)
    else:
        df.to_csv(vecspace_p, index=False)
    
    print(df.head(20).to_string(index=False))


    delta = every_sec-duration #edit minus processing time, or multithread
    print('Sleeping for {} seconds...'.format(delta))
    sleep(delta)



