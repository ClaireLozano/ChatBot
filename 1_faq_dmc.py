 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import os
import operator
import json
import codecs
import re
import nltk

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
java_path = "/Library/Java/JavaVirtualMachines/jdk1.8.0_101.jdk/Contents/Home/java.exe"
os.environ['JAVAHOME'] = java_path
pos_tagger = StanfordPOSTagger(model, jar, encoding='utf8' )


# ================================
# =========== GET DATA ===========
# ================================

# Recupérer tous les mots des fichier json trouvé afin de définir une liste de mot les plus récurent avec un vocabulaire particulier
def getDataFromTextFileJson():
	data = []
	for file in os.listdir("."):
		if file.endswith(".json") and file != "3_questions_syp.json":
			with open(file) as inp:
				dict_test = json.load(inp)
				for k, v in dict_test.iteritems():
					words = splitByWord(v[0])
					for w in words:
						data.append(w)
	return data

# ==============================
# =========== SPLIT ============
# ==============================

# Split et enlève les mots dont la taille et plus petite que 3
def splitByWord(text):
	listPronoms = ["je", "tu", "il", "t", "elle", "on", "nous", "vous", "ils", "elles"]
	listWord = []
	for word in text.split():
		# for pronom in listPronoms:
		if "-" in word:
			for mot in word.split("-"):
				if mot in listPronoms:
					print word.split("-") 
				else:
					print "**** pas de trait d\'union' : ",word
			# 	print ""
			# else:
			# 	if "-" in word:
			# 		print "\n****"
			# 		print word
			# 		print "*****\n"

	return re.findall(r"[\w']+", text)

# Compte les mots et enlève les redondances
def sortByWord(words, n):
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

# Création d'un dictionnaire :
#
#	"phrase" : {
#		"reponse" : "phrase"
#		"motCle" : liste de mot clé permettant de déterminer si la réponse correspondrait à la question posé
# 	}
#
def createDictionnary(path, l):
	questions = {}
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
			questions[v[0]] = {"reponse": v[1], "motCle": array}
	return questions

# Suppression des mots de la question qui ferait partie de la liste placé en paramètre
# Cela permet de ne garder uniquement les mot "important"
def createDictionnaryOneQuestion(l, quest):
	words = splitByWord(quest)
	words = lemmatizationList(words)
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
	newList = []
	for w in l:
		newList.append(stemmer.stem(w))
	return newList

# Lemmatiser un mot
def lemmatizationWord(w):
	return stemmer.stem(w)

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
				pourcent += 0.2
		pourcentQuestion[currentQuestion] = pourcent 
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
	res = pos_tagger.tag(s.split())
	print res
	return res

# =================================


# Récupérer tous les mots des fichier json
words = getDataFromTextFileJson()

# Garder les mots qui sont utilisé plus de 8 fois dans tous les fichiers json
listSortedWords = sortByWord(words, int(8))

# Ajouter des mots à la list "listSortedWords"
wordsList = lemmatizationList(['que', 'quels', 'quoi', 'comment', 'pourquoi', 'ou', 'qui', 'comme', 'est', 'sont', 'dans', 'ma', 'mon', 'mes', 'moi', 'se', 'ce'])
listSortedWords = listSortedWords + wordsList

# Supprimer les mots récurrent afin de ne garder que les mots clé
words = createDictionnary("1_faq_dmc.json", listSortedWords)

pprint(words)

questionsList = words.keys()


# print ""
# print ""
# print ""
# print ""
# newQuestion = "Est ce que je peux changer l adresse de livraison selon les tarifs ?"
# newQuestWords = createDictionnaryOneQuestion(listSortedWords, newQuestion)
# result, theQuestion = compareQuestions(newQuestWords, words)
# theAnswer = words[theQuestion]
# print newQuestion
# print "The answer is : ", theAnswer['reponse']
# pprint(result)


# Marche pas - tokenization 
# content_french = "j'aime les plate-formes"
# print word_tokenize(content_french, language='french')
# print d.detokenize(content_french, unescape=False)


