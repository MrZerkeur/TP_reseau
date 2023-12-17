# TP7 SECU : Accès réseau sécurisé

# I. VPN


```
[root@vpntp7secu wireguard]# cat wg0.conf
[Interface]
Address = 10.7.2.0/24
SaveConfig = false
PostUp = firewall-cmd --zone=public --add-masquerade
PostUp = firewall-cmd --add-interface=wg0 --zone=public
PostDown = firewall-cmd --zone=public --remove-masquerade
PostDown = firewall-cmd --remove-interface=wg0 --zone=public
ListenPort = 13337
PrivateKey = WNcToMeptP9Fta6GgAfTfMrNsY6qFbiidxxcpcw5dkA=

[Peer]
PublicKey = 1sZUEvkFx3vqoDNK+IVhUCUkzO6/ca1h5Uw7oaPFASY=
AllowedIPs = 10.7.2.11/32

[Peer]
PublicKey = dv2iHlptS6FpcFF16jPpxEmP4xvxxEilXR3cAXpPNhg=
AllowedIPs = 10.7.2.12/32
```

```
[root@vpntp7secu wireguard]# cat server.key
WNcToMeptP9Fta6GgAfTfMrNsY6qFbiidxxcpcw5dkA=
```
```
[root@vpntp7secu wireguard]# cat server.pub
ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
```
```
[root@vpntp7secu wireguard]# cat clients/martine.key
kCPIaqdr5pnihydoW3a5hBMrbzPVn9+gv58Wst0ll0A=
```
```
[root@vpntp7secu wireguard]# cat clients/martine.pub
1sZUEvkFx3vqoDNK+IVhUCUkzO6/ca1h5Uw7oaPFASY=
```
```
[root@vpntp7secu wireguard]# cat clients/pc.key
ID2a3gRnrJIsoITi3EIcaarvVWS1wwmu7M9XqayFAng=
```
```
[root@vpntp7secu wireguard]# cat clients/pc.pub
dv2iHlptS6FpcFF16jPpxEmP4xvxxEilXR3cAXpPNhg=
```

```
[axel@martinetp7secu wireguard]$ sudo cat martine.conf
[Interface]
Address = 10.7.2.11/24
PrivateKey = kCPIaqdr5pnihydoW3a5hBMrbzPVn9+gv58Wst0ll0A=

[Peer]
PublicKey = ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
AllowedIPs = 0.0.0.0/0
Endpoint = 10.7.1.100:13337
```

```
[axel@fedora wireguard]$ cat pc.conf 
[Interface]
Address = 10.7.2.12/24
PrivateKey = ID2a3gRnrJIsoITi3EIcaarvVWS1wwmu7M9XqayFAng=

[Peer]
PublicKey = ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
AllowedIPs = 0.0.0.0/0
Endpoint = 10.7.1.100:13337
```
```
[root@vpntp7secu wireguard]# wg show
interface: wg0
  public key: ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
  private key: (hidden)
  listening port: 13337

peer: 1sZUEvkFx3vqoDNK+IVhUCUkzO6/ca1h5Uw7oaPFASY=
  endpoint: 10.7.1.11:36132
  allowed ips: 10.7.2.11/32
  latest handshake: 38 seconds ago
  transfer: 24.47 KiB received, 23.67 KiB sent
```

```
[axel@martinetp7secu wireguard]$ sudo wg show
interface: martine
  public key: 1sZUEvkFx3vqoDNK+IVhUCUkzO6/ca1h5Uw7oaPFASY=
  private key: (hidden)
  listening port: 36132
  fwmark: 0xca6c

peer: ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
  endpoint: 10.7.1.100:13337
  allowed ips: 0.0.0.0/0
  latest handshake: 1 minute, 9 seconds ago
  transfer: 23.69 KiB received, 24.92 KiB sent
```
```
[axel@fedora wireguard]$ sudo wg show
interface: pc
  public key: dv2iHlptS6FpcFF16jPpxEmP4xvxxEilXR3cAXpPNhg=
  private key: (hidden)
  listening port: 44364
  fwmark: 0xca6c

peer: ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
  endpoint: 10.7.1.100:13337
  allowed ips: 0.0.0.0/0
  transfer: 0 B received, 296 B sent
```

# II. SSH

## 1. Setup

Confs :
```
[root@vpntp7secu wireguard]# cat wg0.conf
[Interface]
Address = 10.7.2.0/24
SaveConfig = false
PostUp = firewall-cmd --zone=public --add-masquerade
PostUp = firewall-cmd --add-interface=wg0 --zone=public
PostDown = firewall-cmd --zone=public --remove-masquerade
PostDown = firewall-cmd --remove-interface=wg0 --zone=public
ListenPort = 13337
PrivateKey = WNcToMeptP9Fta6GgAfTfMrNsY6qFbiidxxcpcw5dkA=

[Peer]
PublicKey = 1sZUEvkFx3vqoDNK+IVhUCUkzO6/ca1h5Uw7oaPFASY=
AllowedIPs = 10.7.2.11/32

[Peer]
PublicKey = dv2iHlptS6FpcFF16jPpxEmP4xvxxEilXR3cAXpPNhg=
AllowedIPs = 10.7.2.100/32

[Peer]
PublicKey = kMdYjJifb7S7MmVKp+BikieOFcE8N7eWIcMsDabibg0=
AllowedIPs = 10.7.2.12/32

[Peer]
PublicKey = pLWONIWh/QEXgXB0muW/4+jb2lM1VtmXy65vNF7LmSM=
AllowedIPs = 10.7.2.13/32
```
```
[axel@martinetp7secu wireguard]$ sudo cat martine.conf 
[Interface]
Address = 10.7.2.11/24
PrivateKey = kCPIaqdr5pnihydoW3a5hBMrbzPVn9+gv58Wst0ll0A=

[Peer]
PublicKey = ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
AllowedIPs = 0.0.0.0/0
Endpoint = 10.7.1.100:13337
```
```
[axel@bastiontp7secu wireguard]$ cat bastion.conf 
[Interface]
Address = 10.7.2.12/24
PrivateKey = MI1JxlC0OYHkbBWKQazPBhrUWyEA9Q2zy40Cmj5SNEs=

[Peer]
PublicKey = ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
AllowedIPs = 0.0.0.0/0
Endpoint = 10.7.1.100:13337
```
```
[axel@webtp7secu wireguard]$ cat web.conf 
[Interface]
Address = 10.7.2.13/24
PrivateKey = wE3F1lhJzk0e8nGMS9/CrnUrC0B1fG3luKrTz6FdwXI=

[Peer]
PublicKey = ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
AllowedIPs = 0.0.0.0/0
Endpoint = 10.7.1.100:13337
```

Wg show :
```
[root@vpntp7secu wireguard]# wg show
interface: wg0
  public key: ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
  private key: (hidden)
  listening port: 13337

peer: pLWONIWh/QEXgXB0muW/4+jb2lM1VtmXy65vNF7LmSM=
  endpoint: 10.7.1.13:43360
  allowed ips: 10.7.2.13/32
  latest handshake: 15 seconds ago
  transfer: 42.43 KiB received, 36.50 KiB sent

peer: kMdYjJifb7S7MmVKp+BikieOFcE8N7eWIcMsDabibg0=
  endpoint: 10.7.1.12:58277
  allowed ips: 10.7.2.12/32
  latest handshake: 1 minute, 50 seconds ago
  transfer: 41.05 KiB received, 34.58 KiB sent

peer: 1sZUEvkFx3vqoDNK+IVhUCUkzO6/ca1h5Uw7oaPFASY=
  endpoint: 10.7.1.11:34700
  allowed ips: 10.7.2.11/32
  latest handshake: 3 minutes, 35 seconds ago
  transfer: 32.29 KiB received, 28.71 KiB sent

peer: dv2iHlptS6FpcFF16jPpxEmP4xvxxEilXR3cAXpPNhg=
  allowed ips: 10.7.2.100/32
```
```
[axel@martinetp7secu wireguard]$ sudo wg show
interface: martine
  public key: 1sZUEvkFx3vqoDNK+IVhUCUkzO6/ca1h5Uw7oaPFASY=
  private key: (hidden)
  listening port: 34700
  fwmark: 0xca6c

peer: ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
  endpoint: 10.7.1.100:13337
  allowed ips: 0.0.0.0/0
  latest handshake: 4 minutes, 18 seconds ago
  transfer: 25.28 KiB received, 32.18 KiB sent
```
```
[axel@bastiontp7secu wireguard]$ sudo wg show
interface: bastion
  public key: kMdYjJifb7S7MmVKp+BikieOFcE8N7eWIcMsDabibg0=
  private key: (hidden)
  listening port: 58277
  fwmark: 0xca6c

peer: ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
  endpoint: 10.7.1.100:13337
  allowed ips: 0.0.0.0/0
  latest handshake: 33 seconds ago
  transfer: 34.69 KiB received, 41.80 KiB sent
```
```
[axel@webtp7secu wireguard]$ sudo wg show
interface: web
  public key: pLWONIWh/QEXgXB0muW/4+jb2lM1VtmXy65vNF7LmSM=
  private key: (hidden)
  listening port: 43360
  fwmark: 0xca6c

peer: ifDevCUU7F2J7bqV681MeFSBCgbfQH7GHOd6xpHblGw=
  endpoint: 10.7.1.100:13337
  allowed ips: 0.0.0.0/0
  latest handshake: 1 minute, 37 seconds ago
  transfer: 36.52 KiB received, 43.01 KiB sent
```

Pings :
```
[axel@martinetp7secu wireguard]$ ping -c 1 10.7.2.11
PING 10.7.2.11 (10.7.2.11) 56(84) bytes of data.
64 bytes from 10.7.2.11: icmp_seq=1 ttl=64 time=0.452 ms

--- 10.7.2.11 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.452/0.452/0.452/0.000 ms

[axel@martinetp7secu wireguard]$ ping -c 1 10.7.2.12
PING 10.7.2.12 (10.7.2.12) 56(84) bytes of data.
64 bytes from 10.7.2.12: icmp_seq=1 ttl=63 time=3.33 ms

--- 10.7.2.12 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 3.325/3.325/3.325/0.000 ms

[axel@martinetp7secu wireguard]$ ping -c 1 10.7.2.13
PING 10.7.2.13 (10.7.2.13) 56(84) bytes of data.
64 bytes from 10.7.2.13: icmp_seq=1 ttl=63 time=2.96 ms

--- 10.7.2.13 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 2.960/2.960/2.960/0.000 ms
```



🌞 **Générez des confs Wireguard pour tout le monde**


## 2. Bastion

```
[axel@martinetp7secu wireguard]$ sudo firewall-cmd --permanent --new-zone=ssh-limited
[sudo] password for axel: 
success
[axel@martinetp7secu wireguard]$ sudo firewall-cmd --permanent --zone=ssh-limited --add-source=10.7.1.12
success
[axel@martinetp7secu wireguard]$ sudo firewall-cmd --permanent --zone=ssh-limited --add-service=ssh
success
[axel@martinetp7secu wireguard]$ sudo firewall-cmd --permanent --remove-service=ssh
success

sudo firewall-cmd --add-interface=web --zone=ssh-limited --permanent
sucess
[axel@martinetp7secu wireguard]$ sudo firewall-cmd --reload
success

[axel@webtp7secu ~]$ sudo firs82en#
ewall-cmd --list-all --zone=ssh-limited
[sudo] password for axel: 
ssh-limited (active)
  target: default
  icmp-block-inversion: no
  interfaces: web
  sources: 10.7.2.12 10.7.1.12
  services: ssh
  ports: 
  protocols: 
  forward: no
  masquerade: no
  forward-ports: 
  source-ports: 
  icmp-blocks: 
  rich rules:

[axel@fedora ~]$ ssh axel@10.7.1.13
ssh: connect to host 10.7.1.13 port 22: No route to host

[axel@bastiontp7secu wireguard]$ ssh axel@10.7.1.13
axel@10.7.1.13's password: 
Last login: Thu Dec 14 22:27:45 2023 from 10.7.1.12
[axel@webtp7secu ~]$

[axel@fedora wireguard]$ ssh -J axel@10.7.2.12 axel@10.7.2.13
axel@10.7.2.12's password: 
axel@10.7.2.13's password: 
Last login: Fri Dec 15 00:02:48 2023 from 10.7.2.0
[axel@webtp7secu ~]$
```




On va décider que la machine `bastion.tp7.secu` est notre bastion SSH : si on veut se connecter à n'importe quel serveur en SSH, on doit passer par lui.

Par exemple, si on essaie de se connecter à `web.tp7.secu` en direct sur l'IP `10.7.2.13/24`, il dois nous jeter.

En revanche, si on se connecte d'abord à `bastion.tp7.secu`, puis on se connecte à `web.tp7.secu`, alors là ça fonctionne.

On peut faire ça en une seule commande SSH en utilisant la feature de jump SSH. Littéralement : on rebondit sur une machine avant d'arriver sur une autre. Comme ça :

```bash
# on remplace
ssh bastion.tp7.secu
# puis, une fois connecté :
ssh web.tp7.secu

# paaaar une seule commande directe :

# avec les noms
ssh -j bastion.tp7.secu web.tp7.secu
# avec les IPs
ssh -j 10.7.2.12 10.7.2.13
```

🌞 **Empêcher la connexion SSH directe sur `web.tp7.secu`**

- on autorise la connexion SSH que si elle vient de `bastion.tp7.secu`
- avec le firewall : on bloque le trafic à destination du port 22 s'il ne vient pas de `10.7.2.12`
- prouvez que ça fonctionne
  - que le trafic est bien bloqué en direct
  - mais qu'on peut y accéder depuis `bastion.tp7.secu`

🌞 **Connectez-vous avec un jump SSH**

- en une seule commande, vous avez un shell sur `web.tp7.secu`

> Désormais, le bastion centralise toutes les connexions SSH. Il devient un noeud très important dans la gestion du parc, et permet à lui seul de tracer toutes les connexions SSH effectuées.

## 3. Connexion par clé

🌞 **Générez une nouvelle paire de clés pour ce TP**

- vous les utiliserez pour vous connecter aux machines
- vous n'utiliserez **PAS** l'algorithme RSA
- faites des recherches pour avoir l'avis de gens qualifiés sur l'algo à choisir en 2023 pour avoir la "meilleure" clé (sécurité et perfs)

## 4. Conf serveur SSH

🌞 **Changez l'adresse IP d'écoute**

- sur toutes les machines
- vos serveurs SSH ne doivent être disponibles qu'au sein du réseau VPN
- prouvez que vous ne pouvez plus accéder à une sesion SSH en utilisant l'IP host-only (obligé de passer par le VPN)

🌞 **Améliorer le niveau de sécurité du serveur**

- sur toutes les machines
- mettre en oeuvre au moins 3 configurations additionnelles pour améliorer le niveau de sécurité
- 3 lignes (au moins) à changer quoi
- le doc est vieux, mais en dehors des recommendations pour le chiffrement le reste reste très cool : [l'ANSSI avait édité des recommendations pour une conf OpenSSH](https://cyber.gouv.fr/publications/openssh-secure-use-recommendations)

# III. HTTP

## 1. Initial setup

🌞 **Monter un bête serveur HTTP sur `web.tp7.secu`**

- avec NGINX
- une page d'accueil HTML avec écrit "toto" ça ira
- **il ne doit écouter que sur l'IP du VPN**
- une conf minimale ressemble à ça :

```nginx
server {
    server_name web.tp7.secu;

    listen 10.1.1.1:80;

    # vous collez un ptit index.html dans ce dossier et zou !
    root /var/www/site_nul;
}
```

🌞 **Site web joignable qu'au sein du réseau VPN**

- le site web ne doit écouter que sur l'IP du réseau VPN
- le trafic à destination du port 80 n'est autorisé que si la requête vient du réseau VPN (firewall)
- prouvez qu'il n'est pas possible de joindre le site sur son IP host-only

🌞 **Accéder au site web**

- depuis votre PC, avec un `curl`
- vous êtes normalement obligés d'être co au VPN pour accéder au site

## 2. Génération de certificat et HTTPS

### A. Préparation de la CA

On va commencer par générer la clé et le certificat de notre Autorité de Certification (CA). Une fois fait, on pourra s'en servir pour signer d'autres certificats, comme celui de notre serveur web.

Pour que la connexion soit trusted, il suffira alors d'ajouter le certificat de notre CA au magasin de certificats de votre navigateur sur votre PC.

🌞 **Générer une clé et un certificat de CA**

```bash
# mettez des infos dans le prompt, peu importe si c'est fake
# on va vous demander un mot de passe pour chiffrer la clé aussi
$ openssl genrsa -des3 -out CA.key 4096
$ openssl req -x509 -new -nodes -key CA.key -sha256 -days 1024  -out CA.pem
$ ls
# le pem c'est le certificat (clé publique)
# le key c'est la clé privée
```

### B. Génération du certificat pour le serveur web

Il est temps de générer une clé et un certificat que notre serveur web pourra utiliser afin de proposer une connexion HTTPS.

🌞 **Générer une clé et une demande de signature de certificat pour notre serveur web**

```bash
$ openssl req -new -nodes -out web.tp7.secu.csr -newkey rsa:4096 -keyout web.tp7.secu.key
$ ls
# web.tp7.secu.csr c'est la demande de signature
# web.tp7.secu.key c'est la clé qu'utilisera le serveur web
```

🌞 **Faire signer notre certificat par la clé de la CA**

- préparez un fichier `v3.ext` qui contient :

```ext
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = web.tp7.secu
DNS.2 = www.tp7.secu
```

- effectuer la demande de signature pour récup un certificat signé par votre CA :

```bash
$ openssl x509 -req -in web.tp7.secu.csr -CA CA.pem -CAkey CA.key -CAcreateserial -out web.tp7.secu.crt -days 500 -sha256 -extfile v3.ext
$ ls
# web.tp7.secu.crt c'est le certificat qu'utilisera le serveur web
```

### C. Bonnes pratiques RedHat

Sur RedHat, il existe un emplacement réservé aux clés et certificats :

- `/etc/pki/tls/certs/` pour les certificats
  - pas choquant de voir du droit de lecture se balader
- `/etc/pki/tls/private/` pour les clés
  - ici, seul le propriétaire du fichier a le droit de lecture

🌞 **Déplacer les clés et les certificats dans l'emplacement réservé**

- gérez correctement les permissions de ces fichiers

### D. Config serveur Web

🌞 **Ajustez la configuration NGINX**

- le site web doit être disponible en HTTPS en utilisant votre clé et votre certificat
- une conf minimale ressemble à ça :

```nginx
server {
    server_name web.tp7.secu;

    listen 10.7.1.103:443 ssl;

    ssl_certificate /etc/pki/tls/certs/web.tp7.secu.crt;
    ssl_certificate_key /etc/pki/tls/private/web.tp7.secu.key;
    
    root /var/www/site_nul;
}
```

🌞 **Prouvez avec un `curl` que vous accédez au site web**

- depuis votre PC
- avec un `curl -k` car il ne reconnaît pas le certificat là

🌞 **Ajouter le certificat de la CA dans votre navigateur**

- vous pourrez ensuite visitez `https://web.tp7.b2` sans alerte de sécurité, et avec un cadenas vert
- il faut aussi ajouter l'IP de la machine à votre fichier `hosts` pour qu'elle corresponde au nom `web.tp7.b2`

> *En entreprise, c'est comme ça qu'on fait pour qu'un certificat de CA non-public soit trusted par tout le monde : on dépose le certificat de CA dans le navigateur (et l'OS) de tous les PCs. Evidemment, on utilise une technique de déploiement automatisé aussi dans la vraie vie, on l'ajoute pas à la main partout hehe.*

### E. Bonus renforcement TLS

⭐ **Bonus : renforcer la conf TLS**

- faites quelques recherches pour forcer votre serveur à n'utiliser que des méthodes de chiffrement fortes
- ça implique de refuser les connexions SSL, ou TLS 1.0, on essaie de forcer TLS 1.3

![Do you even](img/do_you_even.jpg)