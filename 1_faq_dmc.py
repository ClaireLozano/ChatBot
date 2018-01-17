 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import os
import operator
import json
import codecs
import re
import pprint
import nltk
import treetaggerwrapper

nltk.download('nonbreaking_prefixes')
nltk.download('perluniprops')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw')

from pprint import pprint
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn
from nltk.tokenize.moses import MosesTokenizer, MosesDetokenizer
from nltk.tag import StanfordPOSTagger

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
			for t in tags:
				if t[1] in ["VINF", "NC", "ADJ", "VPP"]:
					array.append(lemmatizationWord(t[0].lower()))
					array = array + lemmatizationList(synonyme(t[0]))
					array = list(set(array))
			dictionnary[v[0]] = {"reponse": v[1], "motCle": array}
	return dictionnary

# Suppression des mots de la question qui ferait partie de la liste placé en paramètre
# Cela permet de ne garder uniquement les mot "important"
def createDictionnaryOneQuestion(l, quest):
	words = lemmatizationList(splitByWord(quest))
	array = []
	for w in words:
		if w.lower() not in l:
			array.append(w.lower())
	return array

# =================================
# =========== LEMMATIZE ===========
# =================================

# Lemmatiser une liste de mot
def lemmatizationList(l):
	# newList = []
	# for w in l:
	# 	newList.append(stemmer.stem(w))
	return l
	# return newList

# Lemmatiser un mot
def lemmatizationWord(w):
	# return stemmer.stem(w)
	return w

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
		pourcentQuestion[currentQuestion] = pourcent / len(words[currentQuestion]['motCle']) 
	theQuestion = max(pourcentQuestion.iteritems(), key=operator.itemgetter(1))[0]
	return pourcentQuestion, theQuestion

# ================================
# =========== SYNONYME ===========
# ================================

# Trouver des synonymes de mot
def synonyme(w):
	try:
		return [str(lemma.name()) for lemma in wn.synsets(w, lang="fra")[0].lemmas(lang='fra')]
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


# Creation de dictionnaire avec les mots clé d'une question et sa réponse
words = createDictionnary("1_faq_dmc.json")

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
newQuestion = "Dans quels pays livrez-vous et \xe0 quels tarifs ?"
newQuestWords = createDictionnaryOneQuestion(words, newQuestion)
result, theQuestion = compareQuestions(newQuestWords, words)
theAnswer = words[theQuestion]
print newQuestion
print "The answer is : ", theAnswer['reponse']
pprint(result)


# Marche pas - tokenization 
# content_french = "j'aime les plate-formes"
# print word_tokenize(content_french, language='french')
# print d.detokenize(content_french, unescape=False)

print ""
print "========================"
print "====== LEMMATIZE =======" 
print "========================"
print ""

tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tree-tagger'),TAGINENC='utf-8',TAGOUTENC='utf-8')
tags = tagger.TagText(u"Ceci est un tres court texte a etiqueter.")
tags2 = treetaggerwrapper.make_tags(tags)
pprint(tags2)
print 'lemma : ' , tags2[0][2]
