# TP2 : Environnement virtuel

# I. Topologie réseau

## Compte-rendu

☀️ Sur **`node1.lan1.tp2`**

- afficher ses cartes réseau
```
[axel@node1lan1tp1 ~]$ ip a
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:f9:2a:1d brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fef9:2a1d/64 scope link 
       valid_lft forever preferred_lft forever
```
- afficher sa table de routage
```
[axel@node1lan1tp1 ~]$ ip r s
10.1.1.0/24 dev enp0s8 proto kernel scope link src 10.1.1.11 metric 100 
10.1.2.0/24 via 10.1.1.254 dev enp0s8 proto static metric 100
```
- prouvez qu'il peut joindre `node2.lan2.tp2`
```
[axel@node1lan1tp1 ~]$ ping 10.1.2.12
PING 10.1.2.12 (10.1.2.12) 56(84) bytes of data.b
64 bytes from 10.1.2.12: icmp_seq=1 ttl=63 time=0.942 ms
64 bytes from 10.1.2.12: icmp_seq=2 ttl=63 time=0.825 ms
^C
--- 10.1.2.12 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 0.825/0.883/0.942/0.058 ms
```
- prouvez avec un `traceroute` que le paquet passe bien par `router.tp2`
```
[axel@node1lan1tp1 ~]$ traceroute 10.1.2.12
traceroute to 10.1.2.12 (10.1.2.12), 30 hops max, 60 byte packets
 1  10.1.1.254 (10.1.1.254)  0.481 ms  0.447 ms  0.433 ms
 2  10.1.2.12 (10.1.2.12)  1.359 ms !X  1.341 ms !X  1.325 ms !X
```
# II. Interlude accès internet

☀️ **Sur `router.tp2`**

- prouvez que vous avez un accès internet (ping d'une IP publique)
```
[axel@routertp1 ~]$ ping 172.67.74.226
PING 172.67.74.226 (172.67.74.226) 56(84) bytes of data.
64 bytes from 172.67.74.226: icmp_seq=1 ttl=63 time=70.7 ms
^C
--- 172.67.74.226 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 70.745/70.745/70.745/0.000 ms
```
- prouvez que vous pouvez résoudre des noms publics (ping d'un nom de domaine public)
```
[axel@routertp1 ~]$ ping google.com
PING google.com (142.250.179.78) 56(84) bytes of data.
64 bytes from par21s19-in-f14.1e100.net (142.250.179.78): icmp_seq=1 ttl=63 time=23.4 ms
^C
--- google.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 23.408/23.408/23.408/0.000 ms
```

☀️ **Accès internet LAN1 et LAN2**


```
[axel@node2lan1tp1 ~]$ cat /etc/sysconfig/network-scripts/route-enp0s8
default via 10.1.1.254 dev enp0s8
```
```
[axel@node2lan1tp1 ~]$ cat /etc/resolv.conf 
nameserver 8.8.8.8
```
```
[axel@node2lan1tp1 ~]$ ping 172.67.74.226
PING 172.67.74.226 (172.67.74.226) 56(84) bytes of data.
64 bytes from 172.67.74.226: icmp_seq=1 ttl=61 time=20.6 ms
64 bytes from 172.67.74.226: icmp_seq=2 ttl=61 time=15.7 ms
^C
--- 172.67.74.226 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 15.666/18.137/20.609/2.471 ms
```
```
[axel@node2lan1tp1 ~]$ ping google.com
PING google.com (142.250.74.238) 56(84) bytes of data.
64 bytes from par10s40-in-f14.1e100.net (142.250.74.238): icmp_seq=1 ttl=61 time=13.6 ms
64 bytes from par10s40-in-f14.1e100.net (142.250.74.238): icmp_seq=2 ttl=61 time=14.1 ms
^C
--- google.com ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1002ms
rtt min/avg/max/mdev = 13.570/13.815/14.060/0.245 ms
```

# III. Services réseau

## 1. DHCP

☀️ **Sur `dhcp.lan1.tp2`**
```
[axel@dhcplan1tp1 ~]$ ip a
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:c9:89:14 brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.253/24 brd 10.1.1.255 scope global noprefixroute enp0s8
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fec9:8914/64 scope link 
       valid_lft forever preferred_lft forever
```
```
[axel@dhcplan1tp1 ~]$ sudo dnf install dhcp-server -y
```
```
[axel@dhcplan1tp1 ~]$ sudo cat /etc/dhcp/dhcpd.conf
default-lease-time 900;
max-lease-time 10800;

authoritative;

subnet 10.1.1.0 netmask 255.255.255.0 {
range 10.1.1.100 10.1.1.200;
option routers 10.1.1.254;
option subnet-mask 255.255.255.0;
option domain-name-servers 1.1.1.1;
}
```
```
[axel@dhcplan1tp1 ~]$ sudo systemctl status dhcpd
● dhcpd.service - DHCPv4 Server Daemon
     Loaded: loaded (/usr/lib/systemd/system/dhcpd.service; enabled; preset: disabled)
     Active: active (running) since Thu 2023-10-19 20:50:16 CEST; 26min ago
       Docs: man:dhcpd(8)
             man:dhcpd.conf(5)
   Main PID: 780 (dhcpd)
     Status: "Dispatching packets..."
      Tasks: 1 (limit: 4604)
     Memory: 7.1M
        CPU: 21ms
     CGroup: /system.slice/dhcpd.service
             └─780 /usr/sbin/dhcpd -f -cf /etc/dhcp/dhcpd.conf -user dhcpd -group dhcpd --no-pid

Oct 19 20:56:46 dhcplan1tp1 dhcpd[780]: DHCPDISCOVER from 08:00:27:f9:2a:1d (node1lan1tp1) via enp0s8
Oct 19 20:56:46 dhcplan1tp1 dhcpd[780]: DHCPOFFER on 10.1.1.100 to 08:00:27:f9:2a:1d (node1lan1tp1) via enp0s8
Oct 19 20:56:46 dhcplan1tp1 dhcpd[780]: DHCPREQUEST for 192.168.56.104 (192.168.56.100) from 08:00:27:f9:2a:1d>
Oct 19 20:56:46 dhcplan1tp1 dhcpd[780]: DHCPNAK on 192.168.56.104 to 08:00:27:f9:2a:1d via enp0s8
Oct 19 21:16:21 dhcplan1tp1 dhcpd[780]: DHCPREQUEST for 192.168.56.104 from 08:00:27:f9:2a:1d via enp0s8: wron>
Oct 19 21:16:21 dhcplan1tp1 dhcpd[780]: DHCPNAK on 192.168.56.104 to 08:00:27:f9:2a:1d via enp0s8
Oct 19 21:16:21 dhcplan1tp1 dhcpd[780]: DHCPDISCOVER from 08:00:27:f9:2a:1d via enp0s8
Oct 19 21:16:21 dhcplan1tp1 dhcpd[780]: DHCPREQUEST for 192.168.56.104 (192.168.56.100) from 08:00:27:f9:2a:1d>
Oct 19 21:16:21 dhcplan1tp1 dhcpd[780]: DHCPNAK on 192.168.56.104 to 08:00:27:f9:2a:1d via enp0s8
Oct 19 21:16:22 dhcplan1tp1 dhcpd[780]: DHCPOFFER on 10.1.1.100 to 08:00:27:f9:2a:1d (node1lan1tp1) via enp0s8
```

☀️ **Sur `node1.lan1.tp2`**

```
[axel@node1lan1tp1 ~]$ ip a
2: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:f9:2a:1d brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.100/24 brd 10.1.1.255 scope global dynamic noprefixroute enp0s8
       valid_lft 544sec preferred_lft 544sec
    inet6 fe80::a00:27ff:fef9:2a1d/64 scope link 
       valid_lft forever preferred_lft forever

```
```
[axel@node1lan1tp1 ~]$ ip r s
default via 10.1.1.254 dev enp0s8 proto dhcp src 10.1.1.100 metric 100 
10.1.1.0/24 dev enp0s8 proto kernel scope link src 10.1.1.100 metric 100 
```
```
[axel@node1lan1tp1 ~]$ ping 10.1.2.11
PING 10.1.2.11 (10.1.2.11) 56(84) bytes of data.
64 bytes from 10.1.2.11: icmp_seq=1 ttl=63 time=0.755 ms
64 bytes from 10.1.2.11: icmp_seq=2 ttl=63 time=0.902 ms
^C
--- 10.1.2.11 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1015ms
rtt min/avg/max/mdev = 0.755/0.828/0.902/0.073 ms
```
## 2. Web web web

Un petit serveur web ? Pour la route ?

On recycle ici, toujours dans un soucis d'économie de ressources, la machine `node2.lan2.tp2` qui devient `web.lan2.tp2`. On va y monter un serveur Web qui mettra à disposition un site web tout nul.

---

La conf du serveur web :

- ce sera notre vieil ami NGINX
- il écoutera sur le port 80, port standard pour du trafic HTTP
- la racine web doit se trouver dans `/var/www/site_nul/`
  - vous y créerez un fichier `/var/www/site_nul/index.html` avec le contenu de votre choix
- vous ajouterez dans la conf NGINX **un fichier dédié** pour servir le site web nul qui se trouve dans `/var/www/site_nul/`
  - écoute sur le port 80
  - répond au nom `site_nul.tp2`
  - sert le dossier `/var/www/site_nul/`
- n'oubliez pas d'ouvrir le port dans le firewall 🌼

---

☀️ **Sur `web.lan2.tp2`**

- n'oubliez pas de renommer la machine (`node2.lan2.tp2` devient `web.lan2.tp2`)
- setup du service Web
  - installation de NGINX
  - gestion de la racine web `/var/www/site_nul/`
  - configuration NGINX
  - service actif
  - ouverture du port firewall
- prouvez qu'il y a un programme NGINX qui tourne derrière le port 80 de la machine (commande `ss`)
- prouvez que le firewall est bien configuré

☀️ **Sur `node1.lan1.tp2`**

- éditez le fichier `hosts` pour que `site_nul.tp2` pointe vers l'IP de `web.lan2.tp2`
- visitez le site nul avec une commande `curl` et en utilisant le nom `site_nul.tp2`

![That's all folks](./img/thatsall.jpg)
