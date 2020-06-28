'''
Takes the raw PCAP CSV and creates the extract, filters, reduces, etc
The extract will then be converted to vector space in modeling, not here
'''
from utils import config
import os
import pandas as pd
import numpy as np
import yaml

conf = config.conf()


csv_path = os.path.join(conf['fspath'], conf['processfile'] + '.csv')
df = pd.read_csv(csv_path)


# Replace tshark field names' periods with underscore
for col in df.columns:
    recol = col.replace('.','_')
    df.rename(columns={col:recol}, inplace=True)


# Filter out non TCP and UDP. No nulls in all port columns
df = df[ (df.tcp_srcport.notna()) | (df.udp_srcport.notna()) ]


# Make comprehensive port columns. Where TCP ports null, fill with UDP ports
mapp = np.where(df.tcp_srcport.isna(), df.udp_srcport, df.tcp_srcport)
df['srcpt'] = mapp
mapp = np.where(df.tcp_dstport.isna(), df.udp_dstport, df.tcp_dstport)
df['dstpt'] = mapp

df.drop(columns=['tcp_srcport', 'tcp_dstport', 'udp_srcport', 'udp_dstport'], inplace=True)


# Label the target
# Where the infected packet is known by its src or dst IP(s)
for ip in conf['infectedip']:
    df.loc[ (df.ip_src==ip) | (df.ip_dst==ip), 'infected' ] = 1
df.infected = df.infected.fillna(0)

df.drop(columns=['ip_src', 'ip_dst'], inplace=True)


# Select ports of interest and label other as other. Reformat naming
with open('utils/ports.yaml') as f:
    ports = yaml.safe_load(f.read())
    
for direction in ['srcpt', 'dstpt',]:
    df.loc[ ~df[direction].isin(ports), direction ] = '{}_other'.format(direction)

# Relabel port format like 'srcport_22', thinking I'll prefer feature labels listed as such
# And to match in format the 'srcport_other'
for port in ports:
    for direction in ['srcpt', 'dstpt',]:
        new = '_'.join([direction, str(port)])
        df.loc[ df[direction]==port, direction ] = new



# Encode ports
for direction in ['srcpt', 'dstpt']:
    df = df.join( pd.get_dummies(df[direction]), how='left' )


# create funcion that takes flag hashes and transforms into text, eg synack
# first get unique list of the hashes
# for each on that list, convert to binary - split into list -
# which is used like a filter against text list in order 
# check https://www.manitonetworks.com/flow-management/2016/10/16/decoding-tcp-flags
    
# UDP though has no flags
df.loc[df.tcp_flags.isna(), 'tcp_flags'] = 'None'


flags = ['tcpfg_ns', 'tcpfg_cwr', 'tcpfg_ece', 'tcpfg_urg', 'tcpfg_ack', 'tcpfg_psh', 'tcpfg_rst', 'tcpfg_syn', 'tcpfg_fin', ]

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


#testing
df = df.sample(frac=1).reset_index(drop=True)
# Why does this shuffle produce no nans,
# but excluding the shuffle makes many nans on the tail end?
#bug many nulls in last half 

_ = df.tcp_flags.apply(lambda x: decode_encode_flags(x))


df = df.join( pd.DataFrame(d), how='left')






select = [
    #'infected',
    #'frame_number',
    #'frame_time',
    #'frame_len',
    #'ip_proto',
    #'_ws_col_Protocol',
    #'tcp_seq',
    'srcpt',
    'dstpt',
    ]

ports_sel = list()
for col in df.columns:
    if 'srcpt_' in col or 'dstpt' in col:
        ports_sel.append(col)

ports_sel += ['srcpt_other', 'srcpt_other']

ports_sel.sort()

select += ports_sel

select += [
    'tcp_flags',
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


p = os.path.join( conf['fspath'], conf['processfile'] + '_extract_TESTING.csv' )
df.to_csv(p, index=False)
print(p)


#flag_df = pd.DataFrame()
'''
for index, row in df.iterrows():
    x = row['tcp_flags']
    if x == 'None':
        sub_df = pd.DataFrame({'None': [0]})
        flag_df.append(sub_df, sort=True)
    else:
        b = list( bin(int(x, 16))[2:].zfill(9) )
        #print(b)
        flags = ['NS', 'CWR', 'ECE', 'URG', 'ACK', 'PSH', 'RST', 'SYN', 'FIN', ]
        #print(flags)
        decoded = list()
        d = dict()
        for i in range(len(flags)):
            if b[i] == '1':
                #decoded.append(flags[i])
                #df.iloc[index][flags[i]] = 1
                d[flags[i]] =  [1]
            elif b[i] == '0':
                d[flags[i]] = [0]
        flags_df = flags_df.append(pd.DataFrame( d ), sort=True)
'''

#df['flagTest'] = df.tcp_flags.apply(lambda x: get_flag(x))




