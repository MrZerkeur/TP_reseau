# Network - Root Me

## Netfilter - common mistakes

[Config de netfilter](./fw.sh)

Sujet :
```
Un administrateur plein de bonne volonté a essayé de renforcer la sécurité de son serveur en ajustant les règles du pare-feu. Vérifiez qu’il a bien fait son travail !
```

Dans le fichier de configuration lignes 135 et 136 on peut lire ceci :
```
IP46T -A INPUT-HTTP -m limit --limit 3/sec --limit-burst 20 -j LOG --log-prefix 'FW_FLOODER '
IP46T -A INPUT-HTTP -m limit --limit 3/sec --limit-burst 20 -j DROP
```

Donc lorsque la 1ère règle (qui manifestement détecte une attaque de brute force) va être déclenchée, l'évènement sera LOG mais c'est tout, la requête ne sera pas DROP. Puis ce qu'une seule règle peut être déclencée.

Pour résoudre le challenge, il suffit donc de faire plus de 3 requêtes en 1 seconde.
En spammant les F5 ou avec un script bash, python ou n'importe quoi d'autre.