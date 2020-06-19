from utils import config
import os
import pandas as pd

conf = config.conf()

def uscore(df):
    # Replace tshark field names' periods with underscore
    
    for col in df.columns:
        recol = col.replace('.','_')
        df.rename(columns={col:recol}, inplace=True)


def explore(df):

    # Report on transport layer protocols by IP, scaled
    ipproto = df[['ip_src', 'ip_dst']].join(pd.get_dummies(df.ip_proto))
    ipproto.rename(columns={6:'tcp',17:'udp'}, inplace=True) #add mapping file

    srcsum = ipproto.groupby('ip_src').sum()
    dstsum = ipproto.groupby('ip_dst').sum()

    protosum = srcsum.append(dstsum, sort=True)
    protosum = protosum.groupby(protosum.index).sum()

    protosum['total'] = protosum.sum(axis=1)
    protosum.sort_values(by='total', ascending=False, inplace=True)

    proto_cols = protosum.columns.to_list()
    proto_cols.remove('total')
    for col in proto_cols:
        protosum[col] = protosum[col] / protosum['total'].sum()

    protosum.total = protosum[proto_cols].sum(axis=1)

    for col in protosum.columns:
        protosum[col] = protosum[col].round(4)
    
    csv_path = os.path.join(conf['fspath'], conf['processfile'] + '_transport_protocols_by_ip.csv')
    protosum.to_csv(csv_path)

    print(protosum.to_string())


def select_ports(df):
    with open('utils/ports.yaml') as f:
        ports = yaml.safe_load(f.read())

    #df.

def prep():
    # Main prep function takes dataframe through transformations

    csv_path = os.path.join(conf['fspath'], conf['processfile'] + '.csv')
    df = pd.read_csv(csv_path)
    
    uscore(df)

    explore(df)

    print(df.head().to_string(index=False))
    print(df.tail().to_string(index=False))


if __name__=='__main__':
    prep()
    
