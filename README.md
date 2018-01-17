# Projet de gestion sémantique des contenues

Ce projet a été réalisé dans le cadre universitaire par des étudiants de master ICONE à l'université de La Rochelle.


## Objectif

L'objectif de ce projet est de déterminer une/des réponse(s) à une question posée. 

Pour cela, nous avons en préalable analysé une série de questions et de leur réponse afin de nous guider dans la réponse à donner.


## Processus TAL

### Etape 1 - Tokenisation

Afin d'analyser la question, il nous faut dans un premier temps découper la question. Pour cela, nous allons utiliser la fonction `split(" ")` et séparer les mots par des espaces. Cependant, il existe des mots composés tel que `plate-forme` mais aussi des mots tel que `puis-je`. Dans le premier cas, `plate-forme` doit garder sa forme alors que dans le deuxième cas, on peut les séparer (dans le but d'une analyse de la phrase). Nous avons donc créé une fonction en plus du split qui, selon la composition du mot composé, va décider si oui ou non le découper :

```
def splitByWord(text):
	listPronoms = ["je", "tu", "il", "t", "elle", "on", "nous," ,"nous", "vous", "ils", "elles"]
	listWord = []
	for word in text.split():
		if len(word.split("-")) is 1:
			listWord.append(word)
		else:
			splitabale = False
			for mot in word.split("-"):
				if mot in listPronoms:
					splitabale = True
			if splitabale is True:
				listWord = listWord + word.split("-")
			else:
				listWord.append(word)

	return listWord
```

### Etape 2 - Recherche de synonyme

### Etape 3 - Lemmatisation

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

### Etape 5 - Analyse d'une question

## Installation

Le projet a été écrit en python 2.7. Il vous faudra donc cette version pour executer le programme. Nous utilisons une liste de librarie qu'il vous faudra installer à l'aide de la commande "pip install LIBRARY_NAME" :
* os
* operator
* json
* codecs
* re
* nltk

Dans le fichier `1_faq_dmc.json` il vous faudra modifier cette ligne en y référencent votre fichier java d'éxecution :

```
java_path = "/Library/Java/JavaVirtualMachines/jdk1.8.0_101.jdk/Contents/Home/java.exe"
```

Pour lancer le terminal, executez cette ligne de commande :

```
> python 1_faq_dmc.py
```

Suite à ça, il vous sera demandé de renseigner le fichier json de questions/réponses à analyser ainsi que une question utilisateur :

```
> *** Entrer le json de questions/réponses sous la forme ' *****.json ' : 1_faq_dmc.json
...
> *** Quelle est votre question : Comment modifier une adresse de livraison incorrecte ?
... 
```