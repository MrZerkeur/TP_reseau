# Network - Root Me

## HTTP - DNS Rebinding

[Code serveur](./serveur.py)

Sujet :
```
Le devops de cette petite application web a peu de temps et peu de moyens. L’interface d’administration est ainsi, comme souvent, embarquée avec l’IHM utilisateur. Pour autant il s’est assuré qu’on ne puisse pas y accéder de l’extérieur !
```

On cherche à acceder au /admin qui n'est accessible que sur l'IP 127.0.0.1.

Nous disposons d'une zone d'input qui effectue une requête vers l'URL qu'on entre, depuis le serveur donc. Sauf que si on fait une requête vers 127.0.0.1/admin, ça ne marche pas.

Il faut donc faire croire au serveur qu'on fait une requête vers une IP publique, tout en faisant une requête vers 127.0.0.1.


Dans la route grab :
```python
@app.route('/grab')
def grab():
    url = flask.request.args.get('url', '')
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    check = check_url(url)
    if check is not None:
        return check
    res = get_url(url, 0)
    return res
```

On voit que le programme appel d'abord la vérification de l'URL puis refait une 2ème requête pour afficher la réponse de cette dernière. Ce qui fait que si la même URL pointe vers une IP publique lors de la vérification puis 127.0.0.1 lors de la requête ***finale*** on aura accès au /admin.

Pour celà, on peut utiliser un site comme https://lock.cmpxchg8b.com/rebinder.html qui permet de faire du DNS rebinding, il suffit d'entrer une IP publique valide, et 127.0.0.1 puis copier l'URL qu'on nous donne.

Rappel : Le DNS rebinding c'est quand un serveur DNS pointe vers 2 IP différentes pour un même nom de domaine, en alternant entre ces 2 IP.

Pour résoudre le challenge, on met dans la zone d'input ceci par exemple :
```
681a0be9.7f000001.rbndr.us/admin:54022
```
Puis spammer, jusqu'à ce que la requête passe au bon moment, pour être sûr de ne pas louper la requêtte, on peut utiliser BurpSuite.