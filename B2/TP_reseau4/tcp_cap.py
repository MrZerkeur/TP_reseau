from scapy.all import IP, TCP, sniff

packet = sniff(filter="tcp[tcpflags] & (tcp-syn|tcp-ack) != 0", count=1)

src_ip = packet[0][IP].src
dst_ip = packet[0][IP].dst
src_port = packet[0][TCP].sport
dst_port = packet[0][TCP].dport
print("TCP SYN ACK reçu !")
print(f"- Adresse IP src : {src_ip}")
print(f"- Adresse IP dst : {dst_ip}")
print(f"- Port TCP src : {src_port}")
print(f"- Port TCP dst : {dst_port}")