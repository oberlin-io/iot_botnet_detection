# IoT botnet detection
This project attempts to extract the relevant features
via live packets on the network interface (including replayed PCAP files)
and detect Mirai-like botnets via decision tree classifier on various datasets, including:
- IoT POT
- VirusShare
- IoT Network Intrusion Dataset at IEEE DataPort
- Aposemat IoT-23

Using this Google Sheet to keep track of PCAPs:
https://docs.google.com/spreadsheets/d/1GZ2VQ6B_F8jlzWi_4MJbAmkZilbZp2SVI8hw3uMGo-s/edit?usp=sharing

## Manifest
### sample_ports.py
Use to get a sample of ports that TCP and UDP protocols are using
on the network interface.
The ports list can inform ```utils/config.yaml``` for data capture.
This feature is currently NOT incorporated automatically
into the pcap2vec.py process. 

### utils/config.yaml
Configure the network context, such as:
- PCAP file names and any target IPs (for known malicious IPs or known device type IPs)
- Sampling rate and sample batch duration
- tshark fields to capture and their variable names used in the vector space
- Ports to explicitly label in the vector space

### replay.py
This replays, using tcpreplay, PCAP files in sequence across the interface,
as well as setting the MTU,
informed by ```utils/config.yaml```.

### pcap2vec.py
This captures packet data coming across the interface,
which could be actual, live traffic and/or replayed PCAP files via ```replay.py```.
1. Builds a tshark command from ```utils/config.yaml``` and runs it at the sampling rate.
2. For each batch sample, transforms tshark output to vector space and labels the target IP, if exists.
3. Appends each vector space batch to a project train-test file named ```vecspace_.csv``` 

Add feature: Need to be able to filter out packets with src or dst IPs related
to the VM instance (when replaying PCAP files for testing).

Bug: Vecspace results had a few IP nans. Sportother also had a few nans.

### model.py
Takes the project's vector space file:
- Splits into train and test sets.
- Fits, currently, a random forest classifier.
- Tests predictions, outputting performance measures.

Validation: Seems like the first features are the most important features.
Why? Is random forest using the columns in same order as df.columns?

## Some overview notes on Mirai and detection
### Bootstrapping
Overview of the initial, cyclical stage of a botnet (Antonakakis, April, Bailey, Bernhard et al., 2017; Kumar and Lim, 2019):
- A device (or machine) becomes infected with the malware, either through a phishing campaign that tricks a user into downloading the malware or via another infected device.
- The infected device connects to the command and control (CnC) server.
- The device scans the network and probes random IP addresses by sending TCP SYN packets.
- If it finds another device with an open Telnet port, it attempts to create a connection and log in by trying a dictionary of default or common passwords (bruteforce attack).
- If it gets access, it sends the device IP and credentials to a server that logs into the newly discovered vulnerable device and uploads the botnet malware binary, deletes the file, and obscures the system process name.
- The newly infected device begins the same process of discovery and credential collection.
- Meanwhile all infected devices wait for the daily config file, from which the CnC can direct the network to launch attacks.

## Detection
Two main botnet network-based detection angles exist: identifying peer-to-peer (P2P) botnet activity that looks at the malicious signatures between devices, and identifying activity between a device and the CnC server. With this in mind, botnet signatures include:
- TCP SYN packets between devices used in the scanning stage.
- Telnet communications between devices would include SYN packets with destination port 23, the standard Telnet port (Internet Assigned Numbers Authority, 2020). Port 2323 has also been observed in Mirai (Alvarez, 2016). And Herwig et al. (2019) list 5258 as a Telnet alternative.
- Keep-alive exchanges using PSH/ACK (push and acknowledgement) packets between the bot and the CnC server.
