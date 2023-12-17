# TP6 : Un peu de root-me

## Sommaire

  - [I. DNS Rebinding](#i-dns-rebinding)
  - [II. Netfilter erreurs courantes](#ii-netfilter-erreurs-courantes)
  - [III. ARP Spoofing Ecoute active](#iii-arp-spoofing-ecoute-active)
  - [IV. Trafic Global System for Mobile communications](#iv-trafic-global-system-for-mobile-communications)

## I. DNS Rebinding

🌞 **Write-up de l'épreuve**

[Le write up : ici](./Network-DNS_Rebinding/WriteUp.md)

Pour ce qui est de la remédiation, j'ai modifié le code serveur pour que dans le /grab, le 2ème requête de get_url se fasse vers l'IP du nom de domaine entré et non le nom de domaine. Ce qui évite de faire une requête vers la mauvaise IP.

La nouvelle version est [ici](./Network-DNS_Rebinding/serveur_remediation.py)


## II. Netfilter erreurs courantes

🌞 **Write-up de l'épreuve**

[Voici le write up](./Network-Netfilter_common_mistakes/WriteUp.md)

Pour la remédiation, il faut créer une chaîne qui DROP et LOG les tentatives de brute-force. J'ai donc ajouté cette chaîne :
```
iptables -N LOG_DROP
IP46T -A LOG_DROP -j LOG --log-prefix 'FW_FLOODER '
IP46T -A LOG_DROP -j DROP
```

Puis j'ai envoyé les tentatives de brute-force sur cette chaîne.

[Voici la conf modifiée](./Network-Netfilter_common_mistakes/fw_modified.sh)

## III. ARP Spoofing Ecoute active

🌞 **Write-up de l'épreuve**

[Le write up est ici](./Network-ARP_Spoofing-Active_listening/WriteUp.md)

Pour la remédiation, il faudrait utiliser une méthode d'authentification plus robuste que mysql_native_password.
On pourrait aussi mettre en place un ARP static.