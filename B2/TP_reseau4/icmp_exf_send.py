from scapy.all import IP, send, ICMP
from sys import argv

def main():
    target_ip = argv[1]
    letter = argv[2]
    packet = IP(dst=target_ip) / ICMP() / letter
    send(packet)

main()