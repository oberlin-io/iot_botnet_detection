'''
Takes the raw PCAP CSV and creates the extract, filters, reduces, etc
The extract will then be converted to vector space in modeling, not here
'''
from utils import config
import os
import pandas as pd
import numpy as np

conf = config.conf()

def uscore(df):
    # Replace tshark field names' periods with underscore
    
    for col in df.columns:
        recol = col.replace('.','_')
        df.rename(columns={col:recol}, inplace=True)
    return df

def prefilter(df):
    #df = df[df._ws_col_Protocol!='ARP']
    #df = df[df.ip_proto.notna()]
    # The above may be filtering the same set in effect
    # This may be sufficient, just ggrabbing TCP and UDP
    df = df[ (df.tcp_srcport.notna()) | (df.udp_srcport.notna()) ]

    return df

def merge_tcpudp_ports(df):
    # Where TCP ports null, fill with UDP ports
    mapp = np.where(df.tcp_srcport.isna(), df.udp_srcport, df.tcp_srcport)
    df['srcport'] = mapp
    mapp = np.where(df.tcp_dstport.isna(), df.udp_dstport, df.tcp_dstport)
    df['dstport'] = mapp

    df.drop(columns=['tcp_srcport', 'tcp_dstport', 'udp_srcport', 'udp_dstport'], inplace=True)

    return df

def label_target(df):
    # Label the target

    # Where the infected packet is known by its src or dst IP(s)
    for ip in conf['infectedip']:
        df.loc[ (df.ip_src==ip) | (df.ip_dst==ip), 'infected' ] = 1
    df.infected.fillna(0)

    return df


def drop(df):
    df.drop(columns=['ip_src', 'ip_dst'], inplace=True)
    #add drop all nulls

    return df

def tcpflag(df):
    # create funcion that takes flag hashes and transforms into text, eg synack
    # first get unique list of the hashes
    # for each on that list, convert to binary - split into list -
    # which is used like a filter against text list in order 
    # check https://www.manitonetworks.com/flow-management/2016/10/16/decoding-tcp-flags
    
    # UDP for example has no flags
    #df.loc[df.tcp_flag.isna(), 'tcp_flag'] = 'None'
    pass
    # This is broken
    '''
    def get_flag(x):
        if not isinstance(x, float):
            b = list( bin(int(x, 16))[2:].zfill(6) )
            print(b)
            f = ['u','a','p','r','s','f']
            print(f)
            flag = list()
            for i in range(len(f)):
                if b[i] == '1': flag.append(f[i])
            return '_'.join(flag)
    df['flagTest'] = df.tcp_flags.apply(lambda x: get_flag(x))
    '''


def select_ports(df):
    with open('utils/ports.yaml') as f:
        ports = yaml.safe_load(f.read())

    for direction in ['srcport', 'dstport',]:
        df.loc[ ~df[direction].isin(ports), direction ] = '{}_other'.format(direction)


    # Relabel port format like 'srcport_22', thinking I'll prefer feature labels listed as such
    # And to match in format the 'srcport_other'
    for port in ports:
        for direction in ['srcport', 'dstport',]:
            new = '_'.join(direction, str(port))
            df.loc[ df[direction]==port, direction ] = new

    return df


def extract():
    # Main prep function takes dataframe through transformations

    #add Should probably just make a class for df
    csv_path = os.path.join(conf['fspath'], conf['processfile'] + '.csv')
    df = pd.read_csv(csv_path)
    df = uscore(df)
    df = prefilter(df)
    df = merge_tcpudp_ports(df) # Also reformats values for encoding
    #reduce(df)
    #tcpflag(df)
    df = label_target(df)

    print(df.head().to_string(index=False))
    print(df.tail().to_string(index=False))

    
    p = os.path.join( conf['fspath'], conf['processfile'] + '_extract_TESTING.csv')
    df.to_csv(p, index=False)
    print(p)

if __name__=='__main__':
    extract()
    
