# TP3 : On va router des trucs

## I. ARP

### 1. Echange ARP

🌞**Générer des requêtes ARP**

```
John :
ip n s 10.3.1.12
10.3.1.12 dev enp0s8 lladdr 08:00:27:91:66:80 STALE

Marcel :
ip n s 10.3.1.11
10.3.1.11 dev enp0s8 lladdr 08:00:27:33:d4:2e STALE
```

### 2. Analyse de trames

🌞**Analyse de trames**

[ARP request & ARP reply](./tp3_arp.pcap)



## II. Routage


### 1. Mise en place du routage

🌞**Activer le routage sur le noeud `router`**

```
Avant :
sudo firewall-cmd --list-all
masquerade : no

Après :
sudo firewall-cmd --list-all
masquerade : yes

```


🌞**Ajouter les routes statiques nécessaires pour que `john` et `marcel` puissent se `ping`**

```
nano /etc/sysconfig/network-scripts/route-enp0s8
nano /etc/sysconfig/network-scripts/route-enp0s9
```
```
ping 10.3.1.11
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=63 time=0.606 ms
64 bytes from 10.3.1.11: icmp_seq=2 ttl=63 time=0.779 ms

ping 10.3.2.12
PING 10.3.1.11 (10.3.1.11) 56(84) bytes of data.
64 bytes from 10.3.1.11: icmp_seq=1 ttl=63 time=0.606 ms
64 bytes from 10.3.1.11: icmp_seq=2 ttl=63 time=0.779 ms
```

### 2. Analyse de trames

🌞**Analyse des échanges ARP**


```
- John fait un échange ARP avec son réseau (donc le routeur)
- Marcel fait de même
- Le routeur à donc fait un échange ARP avec les 2 VM
```

```
| ordre | type trame  | IP source         | MAC source                 | IP destination | MAC destination              |
|-------|-------------|-------------------|----------------------------|----------------|------------------------------|
| 1     | Requête ARP | x                 | `router``08:00:27:05:50:d3`| x              | Broadcast `00:00:00:00:00:00`|
| 2     | Réponse ARP | x                 | `marcel``08:00:27:91:66:80`| x              | `router` `08:00:27:05:50:d3` |
| ...   | ...         | ...               | ...                        |                |                              |
| 3     | Ping        | routeur 10.3.2.254| x                          | ?              | 10.3.2.12                    |
| 4     | Pong        | marcel 10.3.2.12  | ?                          | ?              | 10.3.2.254                   |
| ...   | ...         | ...               | ...                        |                |                              |
| 5     | Requête ARP | x                 | `marcel``08:00:27:91:66:80`| x              | Broadcast `00:00:00:00:00:00`|
| 6     | Réponse ARP | x                 | `router``08:00:27:05:50:d3`| x              | `marcel` `08:00:27:91:66:80` |
```

[Echange ARP](./tp3_routage_marcel.pcap)

### 3. Accès internet

🌞**Donnez un accès internet à vos machines**

```
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:5c:f5:09 brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic noprefixroute enp0s3
       valid_lft 83180sec preferred_lft 83180sec
    inet6 fe80::a00:27ff:fe5c:f509/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:56:e8:7d brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.254/24 brd 10.3.1.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe56:e87d/64 scope link
       valid_lft forever preferred_lft forever
4: enp0s9: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:05:50:d3 brd ff:ff:ff:ff:ff:ff
    inet 10.3.2.254/24 brd 10.3.2.255 scope global noprefixroute enp0s9
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe05:50d3/64 scope link
```

```
John :
ip route add default via 10.3.1.254 dev enp0s8

ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=108 time=183 ms

ping www.google.com
PING www.google.com (216.58.215.36) 56(84) bytes of data.
64 bytes from par21s17-in-f4.1e100.net (216.58.215.36): icmp_seq=1 ttl=108 time=41.9 ms

Marcel :
ip route add default via 10.3.2.254 dev enp0s8

ping 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=108 time=55.8 ms

ping www.google.com
PING www.google.com (142.250.201.164) 56(84) bytes of data.
64 bytes from par21s23-in-f4.1e100.net (142.250.201.164): icmp_seq=1 ttl=108 time=69.0 ms
```

🌞**Analyse de trames**

- effectuez un `ping 8.8.8.8` depuis `john`
- capturez le ping depuis `john` avec `tcpdump`
- analysez un ping aller et le retour qui correspond et mettez dans un tableau :

| ordre | type trame | IP source          | MAC source                | IP destination     | MAC destination      |     |
|-------|------------|--------------------|---------------------------|--------------------|----------------------|-----|
| 1     | ping       | `john` `10.3.1.11` | `john` `08:00:27:33:d4:2e`| `8.8.8.8`          | `08:00:27:56:e8:7d`  |     |
| 2     | pong       | `8.8.8.8`          | `08:00:27:56:e8:7d`       | `john` `10.3.1.11` |  `08:00:27:33:d4:2e` | ... |

[tp3_routage_internet.pcapng](./tp3_routage_internet.pcapng)
🦈 **Capture réseau `tp3_routage_internet.pcapng`**

## III. DHCP

🌞**Sur la machine `john`, vous installerez et configurerez un serveur DHCP**

```
John :
sudo dnf install dhcp-server

sudo nano /etc/dhcp/dhcpd.conf
default-lease-time 900;
max-lease-time 10800;

authoritative;

subnet 10.3.1.0 netmask 255.255.255.0 {
range 10.3.1.1 10.3.1.254;
option routers 10.3.1.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 8.8.8.8;
```

```
Bob :
nano /etc/sysconfig/network-scripts/ifcfg-enp0s8
NAME=enp0s8
DEVICE=enp0s8

BOOTPROTO=dhcp
ONBOOT=yes

sudo dnf install dhcp-client

reboot
```

🌞**Améliorer la configuration du DHCP**

```
option routers 10.3.1.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 8.8.8.8;
```

```
dhclient -r
dhclient

ip a
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:31:c2:af brd ff:ff:ff:ff:ff:ff
    inet 10.3.1.3/24 brd 10.3.1.255 scope global secondary dynamic enp0s8
       valid_lft 778sec preferred_lft 778sec
    inet6 fe80::cc4a:ab8a:dea5:f9f1/64 scope link noprefixroute
       valid_lft forever preferred_lft forever

ping 10.3.1.254
PING 10.3.1.254 (10.3.1.254) 56(84) bytes of data.
64 bytes from 10.3.1.254: icmp_seq=1 ttl=64 time=0.541 ms
```

```
ip r s
default via 10.3.1.254 dev enp0s8 proto dhcp src 10.3.1.2 metric 100
10.3.1.0/24 dev enp0s8 proto kernel scope link src 10.3.1.2 metric 100

ping 10.3.2.12
PING 10.3.2.12 (10.3.2.12) 56(84) bytes of data.
64 bytes from 10.3.2.12: icmp_seq=1 ttl=63 time=1.17 ms
```

```
dig www.google.com
ANSWER SECTION:
www.google.com.         250     IN      A       216.58.213.68

ping 216.58.213.68
PING 216.58.213.68 (216.58.213.68) 56(84) bytes of data.
64 bytes from 216.58.213.68: icmp_seq=1 ttl=247 time=25.7 ms
```

### 2. Analyse de trames

🌞**Analyse de trames**

[DHCP TP3](./tp3_dhcp.pcap)
