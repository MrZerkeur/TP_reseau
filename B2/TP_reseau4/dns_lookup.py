from scapy.all import IP, UDP, DNS, Ether, srp, DNSQR

dns_packet = Ether() / IP(dst="1.1.1.1") / UDP(dport=53) / DNS(qd=DNSQR(qname="www.ynov.com"))

result = srp(dns_packet, timeout=2, verbose=True)

# response, _ = result
# response.show()