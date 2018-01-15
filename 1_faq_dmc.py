# -*- coding: iso-8859-1 -*-

import os
import json
from pprint import pprint
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import FrenchStemmer
nltk.download('punkt')
stemmer = FrenchStemmer()


# =========== GET DATA ===========

def getDataFromTextFile(folder):
	data = []
	for filename in os.listdir(folder):
		with open(folder+ "/" +filename) as inp:
			for line in inp:
				words = splitByWord(line)
				for w in words:
					data.append(w)
	return data

def getDataFromTextFileJson():
	data = []
	for file in os.listdir("."):
		if file.endswith(".json") and file != "3_questions_syp.json":
			print file
			with open(file) as inp:
				dict_test = json.load(inp)
				for k, v in dict_test.iteritems():
					words = splitByWord(v[0])
					for w in words:
						data.append(w)
	return data

# =========== SPLIT ===========

def splitByWord(line):
	wordsList = []
	words = line.split()
	for word in words:
		wordsList.append(word)

	return wordsList


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


def suppressionMot(path, l):
	questions = {}
	with open(path) as inp:
		dict_test = json.load(inp)
		for k, v in dict_test.iteritems():
			words = splitByWord(v[0])
			words = lemmatizationList(words)
			array = []
			for w in words:
				if w.lower() not in l:
					array.append(w.lower())
			questions[v[0]] = array
	return questions

def appendWordTolist(myList, wordsList):
	for word in wordsList:
		myList.append(word.lower())
	return myList



# =========== LEMMATIZE ===========

def lemmatizationList(l):
	newList = []
	for w in l:
		newList.append(stemmer.stem(w))
	return newList


def lemmatizationWord(w):
	return stemmer.stem(w)

# =================================

# get words
# words = getDataFromTextFile("base_appr_fr")
words = getDataFromTextFileJson()


# Sort word - keep les X mots les plus utilises
listSortedWords = sortByWord(words, int(8))

wordsList = lemmatizationList(['que', 'quels', 'comme', 'est', 'sont', 'dans', 'ma', 'mon', 'moi', 'se'])
listSortedWords = appendWordTolist(listSortedWords, wordsList)

print listSortedWords

words = suppressionMot("1_faq_dmc.json", listSortedWords)
pprint(words)


