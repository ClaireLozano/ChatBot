 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import os
import operator
import json
import codecs
import nltk
import treetaggerwrapper

nltk.download('nonbreaking_prefixes')
nltk.download('perluniprops')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw')

from pprint import pprint
from nltk.stem.snowball import FrenchStemmer
#from nltk.corpus import wordnet as wn
from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
from nltk.tag import StanfordPOSTagger
from SynFranWord import dict_syns

t, d = MosesTokenizer(), MosesDetokenizer()
stemmer = FrenchStemmer()
jar = 'stanford-postagger-full-2017-06-09/stanford-postagger-3.8.0.jar'
model = 'stanford-postagger-full-2017-06-09/models/french.tagger'
# Claire's Path 
# java_path = "/Library/Java/JavaVirtualMachines/jdk1.8.0_101.jdk/Contents/Home/java.exe"
# Wafaa's Path
java_path = "/Library/Java/JavaVirtualMachines/jdk1.8.0_102.jdk/Contents/Home/jre/bin/java"
os.environ['JAVAHOME'] = java_path
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )
# Construction et configuration du wrapper
# tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='/home/hchlih/Documents/projetTAL2018/projet_icone_2018/treetragger',TAGINENC='utf-8',TAGOUTENC='utf-8')
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tree-tagger'),TAGINENC='utf-8',TAGOUTENC='utf-8')


# ================================
# =========== GET DATA ===========
# ================================

# Recupérer tous les mots des fichier json trouvé afin de définir une liste de mot les plus récurent avec un vocabulaire particulier
def getDataFromTextFileJson():
	data = []
	for file in os.listdir("."):
		if file.endswith(".json") and file != "3_questions_syp.json":
			with codecs.open(file,'r',"utf-8") as inp:
				dict_test = json.load(inp)
				for k, v in dict_test.iteritems():
					words = splitByWord(v[0])
					for w in words:
						data.append(w)

	return data

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


# Compte les mots et enlève les redondances
def sortByWord(words):
	dictionnary = {}
	for w in words:
		if len(dictionnary):
			if w in dictionnary.keys():
				dictionnary[w] = dictionnary.get(w) + 1
			else:
				dictionnary[w] = 1
		else : 
			dictionnary[w] = 1
	l = sorted([x.lower() for x,y in dictionnary.items() if y > 8], reverse=True)
	return lemmatizationList(l)

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
				if t[1] in ["VINF", "NC", "ADJ", "VPP", "V"]:
					array.append(lemmatizationWord(t[0].lower()))
					array = list(set(array))
			dictionnary[v[0]] = {"reponse": v[1], "motCle": array}
	return dictionnary

# Suppression des mots de la question qui ferait partie de la liste placé en paramètre
# Cela permet de ne garder uniquement les mots "important"
def createDictionnaryOneQuestion(quest):
	words = splitByWord(quest)
	array = []
	for w in words:
		array.append(w.lower().decode('utf-8'))
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
	return tags2


# =========================================
# =========== COMPARE QUESTIONS ===========
# =========================================

# Trouve une réponse à la quesion posée en analysant les mots
def compareQuestions(newQuestWords, words):
	allQuestions = words.keys()
	pourcentQuestion = {}
	
	for currentQuestion in allQuestions:
		pourcent = 0
		newList = [x.encode('utf-8') for x in words[currentQuestion]['motCle']]
		for w in newQuestWords:
			if w in newList: 
				pourcent += 1
		if pourcent is 0:
			pourcentQuestion[currentQuestion] = 0
		else:
			pourcentQuestion[currentQuestion] = float(pourcent) / len(newList) 	
	theQuestion = max(pourcentQuestion.iteritems(), key=operator.itemgetter(1))[0]
	return pourcentQuestion, theQuestion

# ================================
# =========== SYNONYME ===========
# ================================

# Trouver des synonymes de mot
def synonyme(w):
	try:
		return dict_syns[w.encode('utf-8')]
	except:
		return []

# ================================
# ============= TAG ==============
# ================================

# Trouver tout les tags des mots présent dans une phrase sous la forme de tableau :
# 		[(u'Quel', u'ADJWH'), (u'se', u'CLR'), (u'passe-t-il', u'CLO'), (u'si', u'CS'), (u'je', u'CLS'), (u'ne', u'ADV'), (u'suis', u'V'), (u'pas', u'ADV'), (u'chez', u'P'), (u'moi', u'PRO'), (u'pour', u'P'), (u'r\xe9ceptionner', u'VINF'), (u'ma', u'DET'), (u'commande', u'NC'), (u'?', u'PUNC')]
def getTag(s):
	res = pos_tagger.tag(splitByWord(s))
	return res

# =================================

print ""
print ""
print ""
dictionnary = raw_input("*** Entrer le json de questions/réponses sous la forme ' *****.json ' : ")

# Creation de dictionnaire avec les mots clé d'une question et sa réponse
words = createDictionnary(dictionnary)

print ""
print "======================"
print "==== DICTIONNARY =====" 
print "======================"
print ""

pprint(words)

print ""
print "==========================="
print "========= REPONSE =========" 
print "==========================="
print ""

questionsList = words.keys()
newQuestion = raw_input("*** Quelle est votre question : ")
newQuestWords = createDictionnaryOneQuestion(newQuestion)
result, theQuestion = compareQuestions(newQuestWords, words)
theAnswer = words[theQuestion]

print "*** Voici la réponse à votre question : ", theAnswer['reponse']

# Traitement des réponse du json 3
s = theAnswer['reponse'].split(":")
if s[0] ==  u">action_bdd":
	print "Action de la base de donnée : " + s[1]
elif s[0] ==  u">message":
	print "Message générique "
elif s[0] == u">conseiller":
	print "Redirection vers un service : " + s[1]

# print ""
# print "Détails de pourcentage de similarité : "
# pprint(result)
print ""
print ""
