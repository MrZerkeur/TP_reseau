from scapy.all import IP, UDP, DNS, Ether, srp, DNSQR
from sys import argv

def dns_sender(message):
    target = argv[1]
    dns_packet = Ether() / IP(dst=target) / UDP(dport=53) / DNS(qd=DNSQR(qname=message))
    answers, unanswered_packets = srp(dns_packet, timeout=2, verbose=True)

for i in range(0, len(argv[2]), 20):
        substring = argv[2][i:i + 20]
        dns_sender(substring)