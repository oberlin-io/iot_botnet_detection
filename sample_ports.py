import pandas as pd
'''
Get TCP and UDP ports in use for a context
assuming context at a baseline state
'''
cmd = '''sudo tshark -i eth0 -c 1000 -T fields -e tcp.srcport -e tcp.dstport -e udp.srcport -e udp.dstport -E header=y -E separator=, -E quote=d -E occurrence=f > gcp_ports.csv'''


df=pd.read_csv('gcp_ports.csv')


all_ports = list()
for col in df.columns:
    all_ports += df[col].tolist()

dfp=pd.DataFrame({'ports': all_ports})
dfp.dropna(inplace=True)
dfp = dfp.astype('int')
dfpc = dfp.ports.value_counts()
ports = dfpc[ dfpc > dfpc.quantile(.75) ].index.tolist()

for i in ports:
    print('- ' + str(i))


