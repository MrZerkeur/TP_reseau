from scapy.all import ICMP, IP, Ether, srp

ping = ICMP(type=8)

packet = IP(src="192.168.1.12", dst="192.168.1.7")

frame = Ether(src="8c:b8:7e:14:e8:2b", dst="7c:21:4a:de:53:f5")

final_frame = frame/packet/ping

answers, unanswered_packets = srp(final_frame, timeout=10)

print(f"Pong reçu : {answers[0]}")