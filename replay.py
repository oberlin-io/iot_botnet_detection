from utils import config
import os
import subprocess

conf = config.conf()

print(conf['network_context'])

fs = conf['fspath']

print('Replaying PCAPs:')
for pcap in conf['pcaps']:
    f = pcap['name'] + '.pcap'
    p = os.path.join(fs, f)
    print(' '.join(['-',f]))

print('Setting MTU (maximum transmission unit) to {}'.format(conf['mtu']))

cmd = 'sudo ip link set -eth0 mtu {}'.format(conf['mtu'])
subprocess.call(cmd)

for pcap in conf['pcaps']:
    f = pcap['name'] + '.pcap'
    p = os.path.join(fs, f)
    print(''.join([f,'...']))
    cmd = 'sudo tcpreplay -i eth0 -K --loop 1 {}'.format(p)
    subprocess.call(cmd)
    '''sp = subprocess.Popen(cmd, shell=True, stdin=None,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o,e = sp.communicate()
    '''


