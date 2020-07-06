from utils import config
import os
import subprocess

conf = config.conf()

print(conf['network_context'])

fs = conf['fspath']

fields = list()
print('Setting capture fields...')
for field in conf['fields']:
    if field['capture']==True:
        fields.append(field)
        pad = (20-len(field))*'.'
        print(''.join(field, pad, field['aka']))


tshk=' '.join([
          'sudo tshark',
          #'-i eth0',
          '-r {}'.format(pcap_path),
          #'-a duration:{}'.format(duration),
          #'-c 20', #testing
          '-T fields',
          << fields here like '-e {field}' >>
          '-E header=y',
          '-E separator=,',
          '-E quote=d',
          '-E occurrence=f',
          '> {}'.format(csv_path),
          ])

    print('Running tshark on {}...'.format(pcap_path))
    sp=subprocess.Popen(tshk, shell=True, stdin=None,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o,e = sp.communicate()
    

    '''
    process batch in memory
    to vec, append to vecspace
    '''

if __name__=='__main__':
    main()

