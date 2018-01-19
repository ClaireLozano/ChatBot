 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import os
import operator
import sys 
import json
import codecs
import nltk
import treetaggerwrapper
import re

sys.path.append(os.path.abspath('./dictionnaireSyns'))

from pprint import pprint
from nltk.tag import StanfordPOSTagger
from SynFranWord import syns
from pathlib import Path

jar = 'stanford-postagger-full-2017-06-09/stanford-postagger-3.8.0.jar'
model = 'stanford-postagger-full-2017-06-09/models/french.tagger'
# Claire's Path 
java_path = "/Library/Java/JavaVirtualMachines/jdk1.8.0_101.jdk/Contents/Home/java.exe"
# Wafaa's Path
# java_path = "/Library/Java/JavaVirtualMachines/jdk1.8.0_102.jdk/Contents/Home/jre/bin/java"os.environ['JAVAHOME'] = java_path
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )

# Construction et configuration du wrapper
#MacOs's path
#tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tree-tagger'),TAGINENC='utf-8',TAGOUTENC='utf-8')
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'treetagger'),TAGINENC='utf-8',TAGOUTENC='utf-8')

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
			for t in tags:
				if t[1] in ["VINF", "NC", "ADJ", "VPP"]:
					array.append(lemmatizationWord(t[0].lower()))
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
        if nb != 0:
            pourcentQuestion[currentQuestion] = {"pourcentage" : float(nb) / len(newQuestWords), "reponse" : words[currentQuestion]['reponse']} 
    if pourcentQuestion:         
        reponse = max(pourcentQuestion.iteritems(), key=operator.itemgetter(1))[1]['reponse']
    else : 
        reponse = ""
    return pourcentQuestion,reponse


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
# 		[(u'Quel', u'ADJWH'), (u'se', u'CLR'), (u'passe-t-il', u'CLO'), (u'si', u'CS'), (u'je', u'CLS'), (u'ne', u'ADV'), (u'suis', u'V'), (u'pas', u'ADV'), (u'chez', u'P'), (u'moi', u'PRO'), (u'pour', u'P'), (u'r\xe9ceptionner', u'VINF'), (u'ma', u'DET'), (u'commande', u'NC'), (u'?', u'PUNC')]
def getTag(s):
	res = pos_tagger.tag(splitByWord(s))
	return res






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


words = {}

# Si l'option -f est présente, on enregistre le dictionnaire dans un fichier json
if jsonForce:
	print "*** Enregistrement du dictionnaire dans un fichier json ... "
	words = createDictionnary(dictionnary)
	f = open('dictionnaire/result_' + nb + ".json", 'w+')
	f.write(json.dumps(words, indent=1))
else:
	print "*** Chargement du dictionnaire si il existe ..."
	my_file = Path('dictionnaire/result_' + nb + ".json")
	if my_file.is_file():
		f = open('dictionnaire/result_' + nb + ".json", 'r')
		words = json.load(f)
		f.close()
	else:
		# Creation de dictionnaire avec les mots clés d'une question et sa réponse
		words = createDictionnary(dictionnary)
		f = open('dictionnaire/result_' + nb + ".json", 'w+')
		f.write(json.dumps(words, indent=1))
		f.close()

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

# Récupération de la question utilisateur
questionsList = words.keys()
newQuestion = raw_input("*** Quelle est votre question : ")
newQuestWords = createDictionnaryOneQuestion(newQuestion)
result,reponse = compareQuestions(newQuestWords, words)

# Reponse à la question posé par l'utilisateur
if reponse != '':
	#theAnswer = words[reponse]
     print "*** Voici la réponse à votre question : ", reponse
     print ""
     print "*** D'autres réponses possibles : "
     for v in result.values():
         if v['pourcentage'] >= float(0.20) and v['reponse'] != reponse:
             print "\n",v['reponse']
             print "\t**************"
         elif max(result.iteritems(), key=operator.itemgetter(1))[1]['pourcentage'] < float(0.20) and v['reponse'] != reponse:
             print "\n",v['reponse']
             print "\t**************"

	# Traitement des réponse du json 3
     s = reponse.split(":")
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
	pprint(sorted(result.iteritems(), key=lambda (k,v): (v,k), reverse=True))
	print ""
