from scapy.all import sniff

def icmp_printer(packet):
    if len(packet['Raw'].load) == 1:
        payload_char = chr(packet['Raw'].load[0])
        print(payload_char)
        exit()

sniff(prn=icmp_printer, filter="icmp")
