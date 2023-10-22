# TP1 : Maîtrise réseau du poste

# I. Basics

☀️ **Carte réseau WiFi**

- l'adresse MAC de votre carte WiFi
```
8c:b8:7e:14:e8:2b
```
- l'adresse IP de votre carte WiFi
```
192.168.1.12
```
- le masque de sous-réseau du réseau LAN auquel vous êtes connectés en WiFi
```
255.255.255.0
/24
```
```
Commande :
[axel@fedora]$ ip a
3: wlp0s20f3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 8c:b8:7e:14:e8:2b brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.12/24 brd 192.168.1.255 scope global dynamic noprefixroute wlp0s20f3
       valid_lft 40231sec preferred_lft 40231sec
    inet6 2a01:e0a:a46:ac90:c87c:564c:9505:2678/64 scope global dynamic noprefixroute 
       valid_lft 86329sec preferred_lft 86329sec
    inet6 fe80::71a8:55c3:36c7:7d2d/64 scope link noprefixroute 
       valid_lft forever preferred_lft forever
```

☀️ **Déso pas déso**

- l'adresse de réseau du LAN auquel vous êtes connectés en WiFi
```
192.168.1.0
```
- l'adresse de broadcast
```
192.168.1.255
```
- le nombre d'adresses IP disponibles dans ce réseau
```
254
```
☀️ **Hostname**

- déterminer le hostname de votre PC
```
[axel@fedora ~]$ hostname
fedora
```

☀️ **Passerelle du réseau**

- l'adresse IP de la passerelle du réseau
```
[axel@fedora ~]$ ip r s
default via 192.168.1.254 dev wlp0s20f3 proto dhcp src 192.168.1.12 metric 600
```
- l'adresse MAC de la passerelle du réseau
```
[axel@fedora ~]$ arp -n
Address                  HWtype  HWaddress           Flags Mask            Iface
192.168.1.254            ether   f4:ca:e5:49:d8:67   C                     wlp0s20f3
```

☀️ **Serveur DHCP et DNS**

```
[axel@fedora ~]$ nmcli -f DHCP4 con show Freebox-49D867
DHCP4.OPTION[4]:                        dhcp_server_identifier = 192.168.1.254
DHCP4.OPTION[5]:                        domain_name_servers = 192.168.1.254
```

☀️ **Table de routage**

- dans votre table de routage, laquelle est la route par défaut
```
[axel@fedora ~]$ ip r s
default via 192.168.1.254 dev wlp0s20f3 proto dhcp src 192.168.1.12 metric 600
```

# II. Go further

☀️ **Hosts ?**

- faites en sorte que pour votre PC, le nom `b2.hello.vous` corresponde à l'IP `1.1.1.1`
```
[axel@fedora ~]$ sudo cat /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
1.1.1.1     b2.hello.vous
```
- prouvez avec un `ping b2.hello.vous` que ça ping bien `1.1.1.1`
```
[axel@fedora ~]$ ping b2.hello.vous
PING b2.hello.vous (1.1.1.1) 56(84) bytes of data.
64 bytes from b2.hello.vous (1.1.1.1): icmp_seq=1 ttl=56 time=6.62 ms
64 bytes from b2.hello.vous (1.1.1.1): icmp_seq=2 ttl=56 time=13.9 ms
^C
--- b2.hello.vous ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 6.620/10.242/13.865/3.622 ms
```

☀️ **Go mater une vidéo youtube et déterminer, pendant qu'elle tourne...**

- l'adresse IP du serveur auquel vous êtes connectés pour regarder la vidéo
- le port du serveur auquel vous êtes connectés
- le port que votre PC a ouvert en local pour se connecter au port du serveur distant

```
[axel@fedora ~]$ netstat
Proto Recv-Q Send-Q Local Address           Foreign Address         State        
tcp        0      0 fedora:38392            102.115.120.34.bc:https ESTABLISHED
```
```
IP : 102.115.120.34
Port : 443
Port local : 38392
```

☀️ **Requêtes DNS**

Déterminer...

- à quelle adresse IP correspond le nom de domaine `www.ynov.com`

```
[axel@fedora ~]$ host www.ynov.com
ynov.com has address 172.67.74.226
ynov.com has address 104.26.10.233
ynov.com has address 104.26.11.233
```

- à quel nom de domaine correspond l'IP `174.43.238.89`

```
[axel@fedora ~]$ host 174.43.238.89
89.238.43.174.in-addr.arpa domain name pointer 89.sub-174-43-238.myvzw.com.
```

☀️ **Hop hop hop**

- par combien de machines vos paquets passent quand vous essayez de joindre `www.ynov.com`

```
[axel@fedora ~]$ traceroute www.ynov.com
traceroute to www.ynov.com (104.26.10.233), 30 hops max, 60 byte packets
 1  _gateway (192.168.1.254)  4.702 ms  4.573 ms  4.770 ms
 2  station9.multimania.isdnet.net (194.149.174.106)  6.421 ms  6.825 ms  7.211 ms
 3  station7.multimania.isdnet.net (194.149.174.104)  8.084 ms * iliad.demarc.cogentco.com (149.11.175.170)  8.248 ms
 4  * prs-b3-link.ip.twelve99.net (62.115.46.68)  8.175 ms  8.130 ms
 5  prs-bb2-link.ip.twelve99.net (62.115.118.62)  22.158 ms prs-bb1-link.ip.twelve99.net (62.115.118.58)  21.800 ms  22.112 ms
 6  prs-b1-link.ip.twelve99.net (62.115.125.167)  22.844 ms prs-b1-link.ip.twelve99.net (62.115.125.171)  17.693 ms  17.572 ms
 7  cloudflare-ic-375100.ip.twelve99-cust.net (80.239.194.103)  17.474 ms cloudflare-ic-363840.ip.twelve99-cust.net (213.248.73.69)  3.912 ms  6.159 ms
 8  172.71.128.4 (172.71.128.4)  5.654 ms 141.101.67.54 (141.101.67.54)  5.651 ms 172.71.128.2 (172.71.128.2)  5.658 ms
 9  104.26.10.233 (104.26.10.233)  5.983 ms  5.215 ms  5.900 ms
```
```
Paquets passent par 9 machines
```

☀️ **IP publique**

- l'adresse IP publique de la passerelle du réseau
```
88.169.26.178 selon whatismyip.com
```

☀️ **Scan réseau**

- combien il y a de machines dans le LAN auquel vous êtes connectés
```
[axel@fedora ~]$ nmap -sn 192.168.1.0/24
Starting Nmap 7.93 ( https://nmap.org ) at 2023-10-22 01:42 CEST
Nmap scan report for fedora (192.168.1.12)
Host is up (0.0025s latency).
Nmap scan report for 192.168.1.21
Host is up (0.055s latency).
Nmap scan report for 192.168.1.22
Host is up (0.014s latency).
Nmap scan report for 192.168.1.47
Host is up (0.0051s latency).
Nmap scan report for _gateway (192.168.1.254)
Host is up (0.0015s latency).
Nmap done: 256 IP addresses (5 hosts up) scanned in 4.50 seconds
```

# III. Le requin

☀️ **Capture ARP**

- 📁 fichier `arp.pcap`
- capturez un échange ARP entre votre PC et la passerelle du réseau

[Capture ARP](./arp.pcapng)
```
Filtre : arp
```

☀️ **Capture DNS**

- 📁 fichier `dns.pcap`
- capturez une requête DNS vers le domaine de votre choix et la réponse
- vous effectuerez la requête DNS en ligne de commande

[Capture DNS](./dns.pcapng)
```
[axel@fedora ~]$ host www.ynov.com
```
```
Filtre : dns
```

☀️ **Capture TCP**

- 📁 fichier `tcp.pcap`
- effectuez une connexion qui sollicite le protocole TCP
- je veux voir dans la capture :
  - un 3-way handshake
  - un peu de trafic
  - la fin de la connexion TCP

[Capture TCP](./tcp.pcapng)
```
Filtre : tcp
```