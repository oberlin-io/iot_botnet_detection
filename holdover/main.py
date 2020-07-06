from utils import config
import pcap_to_csv
import to_vecspace
import os


conf = config.conf()
f = conf['functions']

if f['pcap_to_csv']: pcap_to_csv.main()
if f['reports']: reports.main()
if f['to_vecspace']: to_vecspace.main()
