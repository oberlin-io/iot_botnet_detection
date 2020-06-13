# IoT botnet detection

Overview of the initial, cyclical stage of a botnet (Antonakakis, April, Bailey, Bernhard et al., 2017; Kumar and Lim, 2019):
- A device (or machine) becomes infected with the malware, either through a phishing campaign that tricks a user into downloading the malware or via another infected device.
- The infected device connects to the command and control (CnC) server.
- The device scans the network and probes random IP addresses by sending TCP SYN packets.
- If it finds another device with an open Telnet port, it attempts to create a connection and log in by trying a dictionary of default or common passwords (bruteforce attack).
- If it gets access, it sends the device IP and credentials to a server that logs into the newly discovered vulnerable device and uploads the botnet malware binary, deletes the file, and obscures the system process name.
- The newly infected device begins the same process of discovery and credential collection.
- Meanwhile all infected devices wait for the daily config file, from which the CnC can direct the network to launch attacks.

Two main botnet network-based detection angles exist: identifying peer-to-peer (P2P) botnet activity that looks at the malicious signatures between devices, and identifying activity between a device and the CnC server. With this in mind, botnet signatures include:
- TCP SYN packets between devices used in the scanning stage.
- Telnet communications between devices would include SYN packets with destination port 23, the standard Telnet port (Internet Assigned Numbers Authority, 2020). Port 2323 has also been observed in Mirai (Alvarez, 2016). And Herwig et al. (2019) list 5258 as a Telnet alternative.
- Keep-alive exchanges using PSH/ACK (push and acknowledgement) packets between the bot and the CnC server.

This project will attempt to extract the relevant features and detect Mirai-like botnets via decision tree classifier on various datasets, including:
- IoT POT
- VirusShare
- IoT Network Intrusion Dataset at IEEE DataPort
- Aposemat IoT-23


