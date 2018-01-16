# -*- coding: iso-8859-1 -*-

import os
import operator
import json
import codecs
import re
import nltk

from pprint import pprint
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import FrenchStemmer
from nltk.corpus import wordnet
from nltk.corpus import wordnet as wn

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw')
stemmer = FrenchStemmer()


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

# Compte les mot et enlève les redondances
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
def suppressionMot(path, l):
	questions = {}
	with open(path) as inp:
		dict_test = json.load(inp)
		for k, v in dict_test.iteritems():
			words = splitByWord(v[0].encode('utf-8'))
			lemmaWords = lemmatizationList(words)
			array = []
			for idx, w in enumerate(lemmaWords):
				if w.lower() not in l:
					array.append(w.lower())
					# print words[idx]
					# print synonyme(words[idx])
					# array.append(synonyme(words[idx]))
			questions[v[0]] = {"reponse": v[1], "motCle": array}
	return questions

# Suppression des mots de la question qui ferait partie de la liste placé en paramètre
# Cela permet de ne garder uniquement les mot "important"
def suppressionMotOneQuestion(l, quest):
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

# Trouve une réponse à la quesion posé en analysant les mots
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

# trouver des synonyme de mot
def synonyme(w):
	return [str(lemma.name()) for lemma in wn.synsets(w, lang="fra")[0].lemmas(lang='fra')]


# =================================


# synonyme("pays")

# Récupérer tous les mots des fichier json
words = getDataFromTextFileJson()

# Garder les mots qui sont utilisé plus de 8 fois dans tous les fichiers json
listSortedWords = sortByWord(words, int(8))

# Ajouter des mots à la list "listSortedWords"
wordsList = lemmatizationList(['que', 'quels', 'quoi', 'comment', 'pourquoi', 'ou', 'qui', 'comme', 'est', 'sont', 'dans', 'ma', 'mon', 'mes', 'moi', 'se', 'ce'])
listSortedWords = listSortedWords + wordsList

# Supprimer les mots récurrent afin de ne garder que les mots clé
words = suppressionMot("1_faq_dmc.json", listSortedWords)

pprint(words)

# questionsList = words.keys()

# print ""
# print ""
# print ""
# print ""
# newQuestion = "Est ce que je peux changer l adresse de livraison ?"
# newQuestWords = suppressionMotOneQuestion(listSortedWords, newQuestion)
# result, theQuestion = compareQuestions(newQuestWords, words)
# theAnswer = words[theQuestion]
# print newQuestion
# print "The answer is : ", theAnswer['reponse']
# pprint(result)

# Test de synonyme
# print synonyme('acheter')



