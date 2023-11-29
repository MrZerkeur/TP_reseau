from scapy.all import sniff, DNS

def sniff_printer(packet):
    if DNS in packet and packet[DNS].qr == 1:
        dns_answers = packet[DNS].an
        for answer in dns_answers:
            if answer.type == 1:
                ip_address = answer.rdata
                print(ip_address)

sniff(filter="udp and port 53", prn=sniff_printer, count=2)