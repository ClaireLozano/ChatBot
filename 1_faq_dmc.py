 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import os
import operator
import sys 
import json
import codecs
import nltk
import treetaggerwrapper

sys.path.append(os.path.abspath('./dictionnaireSyns'))
nltk.download('nonbreaking_prefixes')
nltk.download('perluniprops')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw')

from pprint import pprint
from SynFranWord import syns
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
                if value in ["VER:infi", "NOM", "ADJ", "VER:pres"]:
                    array.append(lemmatizationWord(key.lower()))
                    array = list(set(array))
            print v[0]
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
def compareQuestions(newQuestWords, words):

	allQuestions = words.keys()
	pourcentQuestion = {}
	
	for currentQuestion in allQuestions:
         pourcent = 0
         for w in newQuestWords:
             if w in words[currentQuestion]['motCle']:
                 pourcent += 1
         if pourcent is 0:
			pourcentQuestion[currentQuestion] = 0
         else:
			pourcentQuestion[currentQuestion] = float(pourcent) / len(words[currentQuestion]['motCle']) 	
	theQuestion = max(pourcentQuestion.iteritems(), key=operator.itemgetter(1))[0]
	return pourcentQuestion, theQuestion


# ================================
# =========== SYNONYME ===========
# ================================

# Trouver des synonymes de mot
def synonyme(w):
	try:
          return syns()[w]
	except:
		return []

# ================================
# ============= TAG ==============
# ================================

# Trouver tout les tags des mots présent dans une phrase sous la forme de tableau :
# 		[(u'Quel', u'ADJWH'), (u'se', u'CLR'), (u'passe-t-il', u'CLO'), (u'si', u'CS'), (u'je', u'CLS'), (u'ne', u'ADV'), (u'suis', u'V'), (u'pas', u'ADV'), (u'chez', u'P'), (u'moi', u'PRO'), (u'pour', u'P'), (u'r\xe9ceptionner', u'VINF'), (u'ma', u'DET'), (u'commande', u'NC'), (u'?', u'PUNC')]
def getTag(s):
    dict_word = {}
    s = splitByWord(s)
    for mot in s :
         tags = tagger.tag_text(mot)
         dict_word[mot] = treetaggerwrapper.make_tags(tags)[0].pos
    return dict_word

# =================================

print ""
print ""
print ""
#dictionnary = raw_input("*** Entrer le json de questions/réponses sous la forme ' *****.json ' : ")
dictionnary = "2_questions_sorbonne.json"
# Creation de dictionnaire avec les mots clé d'une question et sa réponse
words = createDictionnary(dictionnary)

print ""
print "======================"
print "==== DICTIONNARY =====" 
print "======================"
print ""

pprint(words)

print ""
print "========================"
print "========= TEST =========" 
print "========================"
print ""

questionsList = words.keys()
newQuestion = raw_input("*** Quelle est votre question : ")
newQuestWords = createDictionnaryOneQuestion(newQuestion)
result, theQuestion = compareQuestions(newQuestWords, words)
theAnswer = words[theQuestion]

print "*** Voici la réponse à votre question : ", theAnswer['reponse']
print ""
print "Détails de pourcentage de similarité : "
pprint(result[theQuestion])
print theQuestion
print ""
print ""
