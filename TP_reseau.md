# TP1 - Premier pas réseau

# I. Exploration locale en solo

## 1. Affichage d'informations sur la pile TCP/IP locale

### En ligne de commande

**🌞 Affichez les infos des cartes réseau de votre PC**

```
Carte réseau sans fil Wi-Fi :
   Adresse physique . . . . . . . . . . . : 8C-B8-7E-14-E8-2B
   Adresse IPv4. . . . . . . . . . . . . .: 10.33.16.57(préféré)
```

```
Carte Ethernet Ethernet :
   Adresse physique . . . . . . . . . . . : B4-45-06-A4-5C-76
```
**🌞 Affichez votre gateway**

```
Passerelle par défaut. . . . . . . . . : 10.33.19.254
```

**🌞 Déterminer la MAC de la passerelle**
```
Adresse Internet      Adresse physique      Type
10.33.19.254          00-c0-e7-e0-04-4e     dynamique
```

### En graphique (GUI : Graphical User Interface)

**🌞 Trouvez comment afficher les informations sur une carte IP (change selon l'OS)**

Panneau de configuration -> Réseau et Internet -> Connexions réseau -> Wi-Fi -> Détails

## 2. Modifications des informations

### A. Modification d'adresse IP (part 1)  

🌞 Utilisez l'interface graphique de votre OS pour **changer d'adresse IP** :

Panneau de configuration -> Réseau et Internet -> Connexions réseau -> Wi-Fi -> Propriétés -> Protocole Internet version 4 (TCP/IPv4)

🌞 **Il est possible que vous perdiez l'accès internet.** 

La connexion peut être perdu car cette IP n'est pas reconnue par le réseau.



# II. Exploration locale en duo

## 3. Modification d'adresse IP

🌞 **Modifiez l'IP des deux machines pour qu'elles soient dans le même réseau**


🌞 **Vérifier à l'aide d'une commande que votre IP a bien été changée**

```
Carte Ethernet Ethernet :
   Adresse IPv4. . . . . . . . . . . . . .: 10.10.10.1(préféré)
   Masque de sous-réseau. . . . . . . . . : 255.255.255.0
   Passerelle par défaut. . . . . . . . . :
```

🌞 **Vérifier que les deux machines se joignent**

```
ping 10.10.10.2

Envoi d’une requête 'Ping'  10.10.10.2 avec 32 octets de données :
Réponse de 10.10.10.2 : octets=32 temps=6 ms TTL=128
```

🌞 **Déterminer l'adresse MAC de votre correspondant**

```
arp -a
Adresse Internet      Adresse physique      Type
10.10.10.2            9c-2d-cd-16-48-33     dynamique
```

## 4. Utilisation d'un des deux comme gateway


🌞**Tester l'accès internet**

```
ping 1.1.1.1

Envoi d’une requête 'Ping'  1.1.1.1 avec 32 octets de données :
Réponse de 1.1.1.1 : octets=32 temps=21 ms TTL=54
```
```
ping 8.8.8.8

Envoi d’une requête 'Ping'  8.8.8.8 avec 32 octets de données :
Réponse de 8.8.8.8 : octets=32 temps=24 ms TTL=113
```
```
ping google.com

Envoi d’une requête 'ping' sur google.com [142.250.179.78] avec 32 octets de données :
Réponse de 142.250.179.78 : octets=32 temps=24 ms TTL=113
```
```
ping 192.168.137.1

Envoi d’une requête 'Ping'  192.168.137.1 avec 32 octets de données :
Réponse de 192.168.137.1 : octets=32 temps<1ms TTL=128
```
🌞 **Prouver que la connexion Internet passe bien par l'autre PC**
```
tracert 192.168.137.1

Détermination de l’itinéraire vers LAPTOP-7TICS219 [192.168.137.1]
avec un maximum de 30 sauts :

  1    <1 ms    <1 ms    <1 ms  LAPTOP-7TICS219 [192.168.137.1]
```

## 5. Petit chat privé



🌞 **sur le PC *serveur*** avec par exemple l'IP 192.168.1.1
```
.\nc.exe -l -p 8888
oui
voilà
```

🌞 **sur le PC *client*** avec par exemple l'IP 192.168.1.2
```
.\nc.exe 192.168.137.1 8888
voilà
oui
```


🌞 **Visualiser la connexion en cours**

```
netstat -a -n -b
TCP    192.168.137.2:53496    192.168.137.1:8888     ESTABLISHED
[nc.exe]
```

🌞 **Pour aller un peu plus loin**

```
netstat -a -n -b | Select-String 8888

  TCP    0.0.0.0:8888           0.0.0.0:0              LISTENING
```
```
netstat -a -n -b | Select-String 8888

  TCP    192.168.137.1:8888     0.0.0.0:0              LISTENING
```

## 6. Firewall


🌞 **Activez et configurez votre firewall**


```
netsh advfirewall firewall add rule name="ICMP Allow incoming V4 echo request" protocol=icmpv6:8,any dir=in action=allow
```
```
Nc marche sans aucun changement ¯\_(ツ)_/¯
Normalement ça ne marcherait pas mais il y a une règle inconnue qui l'autorise.
```
  
# III. Manipulations d'autres outils/protocoles côté client

## 1. DHCP
```
Bail obtenu. . . . . . . . . . . . . . : mardi 4 octobre 2022 13:57:11
Bail expirant. . . . . . . . . . . . . : mercredi 5 octobre 2022 13:57:12
Passerelle par défaut. . . . . . . . . : 10.33.19.254
Serveur DHCP . . . . . . . . . . . . . : 10.33.19.254
```
## 2. DNS


🌞Trouver l'adresse IP du serveur DNS que connaît votre ordinateur
```
Serveurs DNS. . .  . . . . . . . . . . : 8.8.8.8
                                       8.8.4.4
                                       1.1.1.1
```
🌞 Utiliser, en ligne de commande l'outil `nslookup` (Windows, MacOS) ou `dig` (GNU/Linux, MacOS) pour faire des requêtes DNS à la main

```
nslookup google.com
Nom :    google.com
Addresses:2a00:1450:4007:812::200e
          142.250.179.78
```
```
nslookup ynov.com
Nom :    ynov.com
Addresses: 104.26.10.233
           104.26.11.233
           172.67.74.226
```
3 IP car 3 serveurs, pour répartir la charge.

Demande au serveur DNS : 8.8.8.8
```
nslookup 231.34.113.12
*** dns.google ne parvient pas à trouver 231.34.113.12 : Non-existent domain
```
Cette ip n'est pas attribuée.
```
nslookup 78.34.2.17
Nom :    cable-78-34-2-17.nc.de
Address:  78.34.2.17
```
# IV. Wireshark

## 1. Intro Wireshark

🌞 Utilisez le pour observer les trames qui circulent entre vos deux carte Ethernet. Mettez en évidence :

- un `ping` entre vous et votre passerelle
![](https://i.imgur.com/Jf0ruLA.png)

- un `netcat` entre vous et votre mate, branché en RJ45
![](https://i.imgur.com/5bHn67p.png)

- une requête DNS. Identifiez dans la capture le serveur DNS à qui vous posez la question
![](https://i.imgur.com/i2e917F.png)

## 2. Bonus : avant-goût TCP et UDP




🌞 **Wireshark it**

![](https://i.imgur.com/CYeCIt9.png)

↑ Pas sûr