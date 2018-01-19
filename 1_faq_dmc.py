 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import os
import operator
import sys 
import json
#import codecs
import treetaggerwrapper
import re

sys.path.append(os.path.abspath('./dictionnaireSyns'))

from pprint import pprint
from SynFranWord import syns

# Construction et configuration du wrapper
#MacOs's path
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tree-tagger'),TAGINENC='utf-8',TAGOUTENC='utf-8')
# tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'treetagger'),TAGINENC='utf-8',TAGOUTENC='utf-8')

# ==============================
# =========== SPLIT ============
# ==============================

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

# ===================================
# =========== DICTIONNARY ===========
# ===================================


# Création d'un dictionnaire :
#
#	"phrase" : {
#		"reponse" : "phrase"
#		"motCle" : liste de mot clé permettant de déterminer si la réponse correspondrait à la question posé
# 	}
#
def createDictionnary(path):
    dictionnary = {}
    with open(path) as inp:
        dict_test = json.load(inp)
        for k, v in dict_test.iteritems():
            array = []
            tags = getTag(v[0])
            for key,value in tags.items():
                if value in ["VER", "NOM", "ADJ", "ADV"]:
                    array.append(lemmatizationWord(key.lower()))
                    array = list(set(array))
            dictionnary[v[0]] = {"reponse": v[1], "motCle": array}
    return dictionnary

# Suppression des mots de la question qui ferait partie de la liste placé en paramètre
# Cela permet de ne garder uniquement les mots "important"
def createDictionnaryOneQuestion(quest):
    words = splitByWord(quest)
    array = []
    for w in words:
        array.append(lemmatizationWord(w.lower().decode('utf-8')))
        listSynon = synonyme(lemmatizationWord(w.lower().decode('utf-8')))
        array = array + listSynon       
    return array

# =================================
# =========== LEMMATIZE ===========
# =================================

# Lemmatiser une liste de mot
def lemmatizationList(l):
    newList = []
    for w in l:
        newList.append(lemmatizationWord(w))
    return newList

# Lemmatiser un mot
def lemmatizationWord(w):
	tags = tagger.TagText(w)
	tags2 = treetaggerwrapper.make_tags(tags)[0].lemma
	return tags2.encode('utf-8')


# =========================================
# =========== COMPARE QUESTIONS ===========
# =========================================

# Trouve une réponse à la quesion posée en analysant les mots
# Si le pourcentage de similarité le plus haut est inférieur à 0,5, on suppose que cette question ne ressemble à aucune des questions présente dans le dictionnaire 
def compareQuestions(newQuestWords, words):

	allQuestions = words.keys()
	pourcentQuestion = {}
	
	for currentQuestion in allQuestions:
		nb = 0
		l = words[currentQuestion]['motCle']
		for w in newQuestWords:
			if w in l: 
				nb += 1
		if nb is 0:
			pourcentQuestion[currentQuestion] = 0
		else:
			pourcentQuestion[currentQuestion] = float(nb) / len(l) 	
	reponse = max(pourcentQuestion.iteritems(), key=operator.itemgetter(1))[0]
	pourcent = max(pourcentQuestion.iteritems(), key=operator.itemgetter(1))[1]
	
	if pourcent > float(0.5):
		return pourcentQuestion, reponse
	else:
		print "Cette question ne ressemble à aucune autre question ..."
		return pourcentQuestion, ''

# ================================
# =========== SYNONYME ===========
# ================================

# Trouver des synonymes d'un mot, return une list aucun synonyme n'est trouvé
def synonyme(w):
	try:
		return syns()[w]
	except:
		return []

# ================================
# ============= TAG ==============
# ================================

# Trouver tout les tags des mots présent dans une phrase sous la forme de dictionnaire :
# 		{u'vous': u'PRO', u'\xe0': u'PRP', u'pays': u'NOM', u'Dans': u'NOM', u'quels': u'PRO', u'livrez': u'VER', u'tarifs': u'NOM', u'et': u'KON', u'?': u'SENT'}
def getTag(s):
	dict_word = {}
	s = splitByWord(s)
	for mot in s :
		tags = tagger.tag_text(mot)
		dict_word[mot] = treetaggerwrapper.make_tags(tags)[0].pos.split(":")[0]
	return dict_word








# =====================================================================================

# Recupération d'arguments
text = False
jsonForce = False

for arg in sys.argv:
	if arg == '-v':
		text = True
	elif arg == '-f':
		jsonForce = True

# Resource à utiliser ? 
print ""
dictionnary =""
nb = raw_input("*** Entrer 1, 2, 3 ou 4 pour lire le fichier 1_faq_dmc.json, 2_questions_sorbonne.json, 3_syp.json ou 3_faq_syp.json : ")
if nb is '1':
	dictionnary = "1_faq_dmc.json"
elif nb is '2':
	dictionnary = "2_questions_sorbonne.json"
elif nb is '3':
	dictionnary = "3_syp.json"
elif nb is '4':
	dictionnary = "3_faq_syp.json"

# Creation de dictionnaire avec les mots clés d'une question et sa réponse
words = createDictionnary(dictionnary)

# Si l'option -v est présente, on affiche le dictionnaire
if text:
	print ""
	print "*** Dictionnaire "

	# Affichage du dictionnaire avec les mots clés
	pprint(words)

	print ""
	print "==========================="
	print "========= REPONSE =========" 
	print "==========================="
	print ""

# Si l'option -f est présente, on enregistre le dictionnaire dans un fichier json
if jsonForce:
	print "*** Enregistrement du dictionnaire dans un fichier json ... "
else:
	print "*** Chargement du dictionnaire si il existe ..."

# Récupération de la question utilisateur
questionsList = words.keys()
newQuestion = raw_input("*** Quelle est votre question : ")
newQuestWords = createDictionnaryOneQuestion(newQuestion)
result, reponse = compareQuestions(newQuestWords, words)

# Reponse à la question posé par l'utilisateur
if reponse != '':
	theAnswer = words[reponse]
	print "*** Voici la réponse à votre question : ", theAnswer['reponse']

	# Traitement des réponse du json 3
	s = theAnswer['reponse'].split(":")
	if re.findall('(>)?action_bdd$', s[0]):
		print "*** Un action sera effectué vers la base de donnée : " + str(s[1])
	elif re.findall('(>)?message$', s[0]):
		print "Un message générique sera envoyé"
	elif re.findall('(>)?conseiller$', s[0]): 
		print "Vous allez être redirigé vers un conseiller : " + str(s[1])
else:
	print "Je ne sais pas."
print ""
print ""

# Si l'option -v est présente, on affiche la totalité des questions enregistrer ainsi que le pourcentage
if text:
	print "*** Liste des résultats : "
	pprint(result)
	print ""

