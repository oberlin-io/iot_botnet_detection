# Provenance
Data sources, mappings, and transformations


## IoT-23 - CTU-IoT-Malware-Capture-34-1
Source data consisting of botnet (Mirai-like) activity.
Only of infected IP.

FS file name: 2018-12-21-15-50-14-192.168.1.195.pcap

Download like this, due to SSL certificate issues:
```
wget --no-check-certificate https://mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/IndividualScenarios/CTU-IoT-Malware-Capture-34-1/2018-12-21-15-50-14-192.168.1.195.pcap
```

Malicious label: Where source or destination IP is 192.168.1.195.
See URL for README:
https://mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/IndividualScenarios/CTU-IoT-Malware-Capture-34-1/

## IoT-23 - CTU-Honeypot-Capture-4-1
Source data. Benign scenarios. However, the README says
192.168.1.132
is the infected device.

```
wget --no-check-certificate https://mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/IndividualScenarios/CTU-Honeypot-Capture-4-1/2018-10-25-14-06-32-192.168.1.132.pcap
```

See README:
https://mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/IndividualScenarios/CTU-Honeypot-Capture-4-1/README.html


## IoT-23 - CTU-Honeypot-Capture-5-1
Source data. Benign traffic on Amazon Echo, 192.168.2.3.

```
wget --no-check-certificate https://mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/IndividualScenarios/CTU-Honeypot-Capture-5-1/2018-09-21-capture.pcap
```

README at
https://mcfp.felk.cvut.cz/publicDatasets/IoT-23-Dataset/IndividualScenarios/CTU-Honeypot-Capture-5-1/README.html

## Ports
Feature selection configuration

FS file name: ports.yaml

