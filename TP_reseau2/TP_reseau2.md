# TP2 : Ethernet, IP, et ARP

# I. Setup IP


🌞 **Mettez en place une configuration réseau fonctionnelle entre les deux machines**

```
CLIENT
netsh interface ipv4 set address name="Ethernet" static 192.168.26.51 255.255.252.0 192.168.26.50
```
```
SERVEUR
netsh interface ipv4 set address name="Ethernet" static 192.168.26.50 255.255.252.0
```
```
ipconfig /all
Adresse IPv4. . . . . . . . . . . . . .: 192.168.26.51(préféré)
Masque de sous-réseau. . . . . . . . . : 255.255.252.0
Passerelle par défaut. . . . . . . . . : 192.168.26.50
```
```
Broadcast : 192.168.27.255
```



🌞 **Prouvez que la connexion est fonctionnelle entre les deux machines**
```
ping 192.168.26.50

Envoi d’une requête 'Ping'  192.168.26.50 avec 32 octets de données :
Réponse de 192.168.26.50 : octets=32 temps=1 ms TTL=128
```
🌞 **Wireshark it**



[Ping-pong Wireshark](./ping_tp2_reseau.pcapng)

```
Ping
Type : 8 (echo (ping) request)

Pong
Type : 0 (echo (ping) reply)
```

# II. ARP my bro

ARP permet, pour rappel, de résoudre la situation suivante :

- pour communiquer avec quelqu'un dans un LAN, il **FAUT** connaître son adresse MAC
- on admet un PC1 et un PC2 dans le même LAN :
  - PC1 veut joindre PC2
  - PC1 et PC2 ont une IP correctement définie
  - PC1 a besoin de connaître la MAC de PC2 pour lui envoyer des messages
  - **dans cette situation, PC1 va utilise le protocole ARP pour connaître la MAC de PC2**
  - une fois que PC1 connaît la mac de PC2, il l'enregistre dans sa **table ARP**

🌞 **Check the ARP table**

Mon cher mate :
```
arp -a
 Adresse Internet      Adresse physique      Type
  192.168.26.50         54-05-db-d7-f6-e3     dynamique
```
Gateway :
```
10.33.19.254          00-c0-e7-e0-04-4e     dynamique
```

🌞 **Manipuler la table ARP**
```
arp -d
```
```
Interface : 192.168.177.1 --- 0x3
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 192.168.26.51 --- 0x6
  Adresse Internet      Adresse physique      Type
  192.168.26.50         54-05-db-d7-f6-e3     dynamique
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 10.33.16.198 --- 0x7
  Adresse Internet      Adresse physique      Type
  10.33.19.254          00-c0-e7-e0-04-4e     dynamique
  224.0.0.22            01-00-5e-00-00-16     statique

Interface : 192.168.224.1 --- 0x12
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.2.60            01-00-5e-00-02-3c     statique
```
```
Interface : 192.168.177.1 --- 0x3
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique

Interface : 192.168.26.51 --- 0x6
  Adresse Internet      Adresse physique      Type
  192.168.26.50         54-05-db-d7-f6-e3     dynamique
  224.0.0.22            01-00-5e-00-00-16     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique

Interface : 10.33.16.198 --- 0x7
  Adresse Internet      Adresse physique      Type
  10.33.19.254          00-c0-e7-e0-04-4e     dynamique
  224.0.0.22            01-00-5e-00-00-16     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique

Interface : 192.168.224.1 --- 0x12
  Adresse Internet      Adresse physique      Type
  224.0.0.22            01-00-5e-00-00-16     statique
  224.0.2.60            01-00-5e-00-02-3c     statique
  239.255.255.250       01-00-5e-7f-ff-fa     statique
```

🌞 **Wireshark it**

[ARP Wireshark](./arp_tp2_reseau.pcapng)


# III. DHCP you too my brooo

🌞 **Wireshark it**

[DORA Wireshark](./dora_tp2_reseau.pcapng)