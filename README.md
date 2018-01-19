# Projet de gestion sémantique des contenues

Ce projet a été réalisé dans le cadre universitaire par des étudiants de master ICONE à l'université de La Rochelle.


## Objectif

L'objectif de ce projet est de déterminer une/des réponse(s) à une question posée. 

Pour cela, nous avons en préalable analysé une série de questions et de leur réponse afin de nous guider dans la réponse à donner.


## Processus TAL

### Etape 1 - Tokenisation

Afin d'analyser la question, il nous faut dans un premier temps découper la question. Pour cela, nous allons utiliser la fonction `split(" ")` et séparer les mots par des espaces. Cependant, il existe des mots composés tel que `plate-forme` mais aussi des mots tel que `puis-je`. Dans le premier cas, `plate-forme` doit garder sa forme alors que dans le deuxième cas, on peut les séparer car ils ne forme pas un seul et même mot. Nous avons donc créé une fonction en plus du split qui, selon la composition du mot composé, va décider si oui ou non le découper :

```
# Split et ananlyse des mots composés
def splitByWord(text):
	listPronoms = ["je", "tu", "il", "t", "elle", "on", "nous," ,"nous", "vous", "ils", "elles"]
	ponct = '[ ?.,!/;]'
	listWord = []
	for word in text.split():
		if len(word.split("-")) is 1:
			word = re.sub(ponct, '', word)
			if word != '':
				listWord.append(word)
		else:
			splitabale = False
			for mot in word.split("-"):
				if mot in listPronoms:
					splitabale = True
			if splitabale is True:
				for w in word.split("-"):
					w = w + ','
					w = re.sub(ponct, '', w)
					if w != '':
						listWord.append(w)
			else:
				word = re.sub(ponct, '', word)
				if word != '':
					listWord.append(word)
	return listWord
```
Nous supprimons aussi toutes ponctuations compris dans `[ ?.,!/;]`.

### Etape 2 - Recherche de synonymes

Afin d'élargir notre champ de recherche, nous effectuons une recherche de synonymes sur les mots clés de la question posée par l'utilisateur. Si l'utilisateur utilise le mot `emplette`, celui-ci matchera avec le mot `acheter`.
La recherche de synonymes se fait sur un fichier thésaurus de synonymes téléchargeable à l'adresse suivante: http://www.dicollecte.org/download/fr/thesaurus-v2.3.zip .
On crée un dictionnaire à partir du thésaurus, donc un dictionnaire contenant tous les mots avec leurs synonymes associés.

### Etape 3 - Lemmatisation

Dans le but de simplifier la recherche, nous lemmatisions les mots clés. Cela permet par exemple de passer outre le problème de conjugaison des verbes. `Achetais` deviendra alors `acheter`. 
Nous avons utilisé TreeTagger qui est un outil d'annotation et de tag de texte qui permet de retourner des informations sur la partie du discours et le lemme.

### Etape 4 - Création d'un dictionnaire

Pour stocker les questions/réponses ainsi que leurs mots clés, nous avons décidé de créer un dictionnaire sous la forme : 

```
 u'Mon adresse de livraison est incorrecte, comment la modifier ?': {'motCle': ['suscription',
                                                                                u'adresse',
                                                                                u'livraison',
                                                                                'importation',
                                                                                u'modifier',
                                                                                u'incorrecte,'],
                                                                     'reponse': u"\nVous pouvez vous connecter sur votre compte client et modifier votre adresse de livraison dans la rubrique Mes adresses : Cliquez ici pour vous connecter\n\n\xc0 titre d'indication, les commandes sont pr\xe9par\xe9es le matin du lundi au vendredi.\n\nAinsi, si vous effectuez un changement d'adresse juste apr\xe8s avoir pass\xe9 commande, il pourra dans la majorit\xe9 des cas \xeatre imm\xe9diatement pris en compte.\n\nEn revanche, si vous effectuez ce changement d'adresse le lendemain apr\xe8s-midi de la validation de votre commande, il est possible que votre colis soit d\xe9j\xe0 en cours d'acheminement et nous serons dans l'impossibilit\xe9 de prendre en compte votre demande. Dans ce cas, les frais de retour ainsi que les frais de port pour la livraison \xe0 la nouvelle adresse seront \xe0 votre charge.\n\nPour \xe9viter ce d\xe9sagr\xe9ment, si vous utilisez un compte Paypal pour r\xe9gler votre commande, nous vous conseillons de v\xe9rifier en amont votre adresse de livraison, en vous connectant directement sur votre compte Paypal."},
 u'O\xf9 puis-je acheter les produits de Dans Ma Culotte\xa9 ?': {'motCle': ['emplette',
                                                                             u'acheter',
                                                                             'achat',
                                                                             u'produits',
                                                                             'acquisition'],
                                                                  'reponse': u"\nLes produits de Dans Ma Culotte\xa9 sont disponibles sur notre site internet dansmaculotte.com\n\nVous pouvez \xe9galement les retrouver lors des rendez-vous Marie-No\xeblle. Ces r\xe9unions organis\xe9es \xe0 domicile vous permettent de d\xe9couvrir les produits, de les toucher, et de b\xe9n\xe9ficier de nombreux conseils personnalis\xe9s de la part de nos conseill\xe8res bien-\xeatre. Si vous souhaitez participer \xe0 l'une de ces r\xe9unions en tant qu'invit\xe9(e) ou en organiser une \xe0 votre domicile entour\xe9(e) des personnes de votre choix, contactez-nous par t\xe9l\xe9phone au 02 52 86 00 83 de 10:00 \xe0 17:00  ou par email \xe0 l'adresse suivante: bonjour@lesrdvmarienoelle.fr .\n"},
```

Le dictionnaire sera stocké dans le dossier `dictionnaire` sous le format json.

### Etape 5 - Analyse d'une question

Une fois la question posée, le programme va la récupérer, chercher les synonymes, et comparer les mots clé (ainsi que les synonymes) de la question avec les mots clés des questions présentes dans le dictionnaire. Un pourcentage de mots clés trouvé sera alors calculé .

### Etape 6 - Affichage des réponses
La réponse dont le pourcentage est le max sera affiché comme la plus pertinente. Il y aura d'autres réponses possibles qui seront affichés si le pourcentage est supérieur ou égal au seuil.
Dans le cas où toutes les réponses ont un pourcentage inférieur au seuil, alors on les affichera toutes.


## Installation et lancement

Le projet a été écrit en python 2.7. Il vous faudra donc cette version pour executer le programme. Nous utilisons une liste de librarie qu'il vous faudra installer à l'aide de la commande `pip install LIBRARY_NAME` :
* os
* operator
* json
* sys
* codecs
* re
* nltk
* treetaggerwrapper
* pathlib


Dans le fichier `1_faq_dmc.py` il vous faudra modifier cette ligne en y référencent votre fichier java d'éxecution :

```
java_path = "/Library/Java/JavaVirtualMachines/jdk1.8.0_101.jdk/Contents/Home/java.exe"
```

Pour lancer le terminal, executez cette ligne de commande :

```
> python 1_faq_dmc.py [-v] [-f]
```

* `-v` permet d'avoir tout les détails du processus 
* `-f` permet d'écraser le fichier dictionnaire enregistrer lors des précédents traitement


Suite à ça, il vous sera demandé de renseigner le fichier json de questions/réponses à analyser ainsi que une question utilisateur :

```
> *** Entrer 1, 2, 3 ou 4 pour lire le fichier 1_faq_dmc.json, 2_questions_sorbonne.json, 3_syp.json ou 3_faq_syp.json : 2
...
> *** Quelle est votre question : Comment modifier une adresse de livraison incorrecte ?
... 
```
