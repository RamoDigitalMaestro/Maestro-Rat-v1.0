
[![Instagram](https://img.shields.io/badge/-Instagram-ff69b4?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/rootramo?igsh=c2ptcHhjZGRnMGV2)




This Python script is designed to simulate a backdoor attack. The script, called attacker.py, allows an attacker to send certain commands to the target machine. The script named target.py receives these commands and performs the relevant operations on the target machine.

Attacker.py takes the target IP address and port number as arguments and then connects to the target. It then allows the attacker to enter commands. The user can send commands to the target through various commands and perform operations on the target machine.

Target.py receives the server's IP address and the port number it wants to listen on from the user. Then, it receives certain commands and acts according to those commands. For example, it lists directory contents with the 'ls' command or runs a specific terminal command with the 'execute' command.

These two scripts can be used for scenarios such as malware analysis or cybersecurity training. However, performing such activities on real systems may be illegal and require unauthorized access.

#How to use?

attacker.py -lport (you will enter your active port) -lhost (you will enter your own IP address)

examples;

attacker.py -lhost 192.168.1.33 -lport 8080

When the victim starts target.py you will receive the link.
note: Set the ip and port in target.py according to your needs.
I am not responsible for any misuse.


