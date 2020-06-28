from utils import config
from extract import pcap_to_csv, prep
import os


conf = config.conf()
f = conf['functions']

if f['pcap_to_csv']: pcap_to_csv.cap()

if f['prep']: prep.extract()
