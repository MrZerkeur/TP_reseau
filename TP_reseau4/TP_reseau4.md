# TP4 : TCP, UDP et services réseau

# I. First steps


🌞 **Déterminez, pour ces 5 applications, si c'est du TCP ou de l'UDP**

```
Steam :
netstat -n
Connexions actives
  Proto  Adresse locale         Adresse distante       État
  TCP    10.33.19.200:64278     23.72.250.6:443        ESTABLISHED
```
[Steam](./../Steam.pcapng)

```
Brave :
netstat -n
Connexions actives

  Proto  Adresse locale         Adresse distante       État
  TCP    10.33.19.200:51789     13.225.34.112:443      ESTABLISHED
```
[Brave - ynov.com](./Brave%20-%20ynov.com.pcapng)

Easy anti cheat
[Easy anti cheat](./Easy%20anti%20cheat.pcapng)

```
Teams :
netstat -n
Connexions actives

  Proto  Adresse locale         Adresse distante       État
  TCP    10.33.19.200:52081     20.50.201.195:443     ESTABLISHED
```
[Teams](./Teams.pcapng)

```
Discord :
netstat -n
Connexions actives
  Proto  Adresse locale         Adresse distante       État
  TCP    10.33.19.200:55368     204.79.197.222:443     ESTABLISHED
```
[Discord](./Discord.pcapng)

VERIFIER

🌞 **Demandez l'avis à votre OS**
METTRE NETSTAT

# II. Mise en place

## 1. SSH

🌞 **Examinez le trafic dans Wireshark**

[SSH VM](./SSH%20VM.pcapng)

🌞 **Demandez aux OS**

```
netstat -n

Connexions actives

  Proto  Adresse locale         Adresse distante       État
  TCP    10.4.1.1:64449         10.4.1.11:22           ESTABLISHED
```

## 2. Routage

# III. DNS

## 1. Présentation

## 2. Setup

🌞 **Dans le rendu, je veux**

- un `cat` des fichiers de conf
```
sudo cat /etc/named.conf
//
// named.conf
//
// Provided by Red Hat bind package to configure the ISC BIND named(8) DNS
// server as a caching only nameserver (as a localhost DNS resolver only).
//
// See /usr/share/doc/bind*/sample/ for example named configuration files.
//

options {
        listen-on port 53 { 127.0.0.1; any; };
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        secroots-file   "/var/named/data/named.secroots";
        recursing-file  "/var/named/data/named.recursing";
        allow-query     { localhost; any; };
        allow-query-cache { localhost; any; };
        /*
         - If you are building an AUTHORITATIVE DNS server, do NOT enable recursion.
         - If you are building a RECURSIVE (caching) DNS server, you need to enable
           recursion.
         - If your recursive DNS server has a public IP address, you MUST enable access
           control to limit queries to your legitimate users. Failing to do so will
           cause your server to become part of large scale DNS amplification
           attacks. Implementing BCP38 within your network would greatly
           reduce such attack surface
        */
        recursion yes;

        dnssec-validation yes;

        managed-keys-directory "/var/named/dynamic";
        geoip-directory "/usr/share/GeoIP";

        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";

        /* https://fedoraproject.org/wiki/Changes/CryptoPolicy */
        include "/etc/crypto-policies/back-ends/bind.config";
};

logging {
        channel default_debug {
                file "data/named.run";
                severity dynamic;
        };
};

zone "tp4.b1" IN {
     type master;
     file "tp4.b1.db";
     allow-update { none; };
     allow-query {any; };
};

zone "1.4.10.in-addr.arpa" IN {
     type master;
     file "tp4.b1.rev";
     allow-update { none; };
     allow-query { any; };
};


include "/etc/named.rfc1912.zones";
include "/etc/named.root.key";
```
```
sudo cat /var/named/tp4.b1.db
$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

; Enregistrements DNS pour faire correspondre des noms à des IPs
dns-server IN A 10.4.1.201
node1      IN A 10.4.1.11
```
```
sudo cat /var/named/tp4.b1.rev
$TTL 86400
@ IN SOA dns-server.tp4.b1. admin.tp4.b1. (
    2019061800 ;Serial
    3600 ;Refresh
    1800 ;Retry
    604800 ;Expire
    86400 ;Minimum TTL
)

; Infos sur le serveur DNS lui même (NS = NameServer)
@ IN NS dns-server.tp4.b1.

;Reverse lookup for Name Server
201 IN PTR dns-server.tp4.b1.
11 IN PTR node1.tp4.b1.
```
- un `systemctl status named` qui prouve que le service tourne bien
```
systemctl status named
● named.service - Berkeley Internet Name Domain (DNS)
     Loaded: loaded (/usr/lib/systemd/system/named.service; enabled; vendor preset: disabled)
     Active: active (running) since Wed 2022-10-26 19:50:10 CEST; 1h 40min ago
   Main PID: 902 (named)
      Tasks: 5 (limit: 5907)
     Memory: 20.6M
        CPU: 149ms
     CGroup: /system.slice/named.service
             └─902 /usr/sbin/named -u named -c /etc/named.conf

Oct 26 19:50:10 localhost.localdomain named[902]: zone localhost.localdomain/IN: loaded serial 0
Oct 26 19:50:10 localhost.localdomain named[902]: zone 1.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.>
Oct 26 19:50:10 localhost.localdomain named[902]: zone localhost/IN: loaded serial 0
Oct 26 19:50:10 localhost.localdomain named[902]: zone 1.0.0.127.in-addr.arpa/IN: loaded serial 0
Oct 26 19:50:10 localhost.localdomain named[902]: zone tp4.b1/IN: loaded serial 2019061800
Oct 26 19:50:10 localhost.localdomain named[902]: all zones loaded
Oct 26 19:50:10 localhost.localdomain systemd[1]: Started Berkeley Internet Name Domain (DNS).
Oct 26 19:50:10 localhost.localdomain named[902]: running
Oct 26 19:50:10 localhost.localdomain named[902]: managed-keys-zone: Initializing automatic trust anchor management for>
Oct 26 19:50:10 localhost.localdomain named[902]: resolver priming query complete
```
- une commande `ss` qui prouve que le service écoute bien sur un port
```
sudo ss -alntp
State     Recv-Q     Send-Q         Local Address:Port         Peer Address:Port    Process
LISTEN    0          10                10.4.1.201:53                0.0.0.0:*        users:(("named",pid=902,fd=21))
```

🌞 **Ouvrez le bon port dans le firewall**

Port 53 (vu dans le ss)

```
sudo firewall-cmd --add-port=53/udp --permanent
success

sudo firewall-cmd --reload
success
```

## 3. Test

🌞 **Sur la machine `node1.tp4.b1`**

```
dig node1.tp4.b1

; <<>> DiG 9.16.23-RH <<>> node1.tp4.b1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 49359
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 71f476cd4911eb1901000000635a57c9a58cd80babc63b69 (good)
;; QUESTION SECTION:
;node1.tp4.b1.                  IN      A

;; ANSWER SECTION:
node1.tp4.b1.           86400   IN      A       10.4.1.11

;; Query time: 0 msec
;; SERVER: 10.4.1.201#53(10.4.1.201)
;; WHEN: Thu Oct 27 12:04:57 CEST 2022
;; MSG SIZE  rcvd: 85
```
```
dig dns-server.tp4.b1

; <<>> DiG 9.16.23-RH <<>> dns-server.tp4.b1
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 62406
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: 9549243e17f3bf7f01000000635a57d60096ef927f58d63c (good)
;; QUESTION SECTION:
;dns-server.tp4.b1.             IN      A

;; ANSWER SECTION:
dns-server.tp4.b1.      86400   IN      A       10.4.1.201

;; Query time: 0 msec
;; SERVER: 10.4.1.201#53(10.4.1.201)
;; WHEN: Thu Oct 27 12:05:10 CEST 2022
;; MSG SIZE  rcvd: 90
```

```
ping www.google.com
PING www.google.com (142.250.179.100) 56(84) bytes of data.
64 bytes from par21s20-in-f4.1e100.net (142.250.179.100): icmp_seq=1 ttl=113 time=23.1 ms
```
