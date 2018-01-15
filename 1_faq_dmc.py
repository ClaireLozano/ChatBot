# -*- coding: iso-8859-1 -*-
import os
import json
from pprint import pprint

def readJson(data):
	data = json.load(open(data))
	reponseList = {} 
	reponseList["1"] = []
	reponseList["2"] = []
	reponseList["3"] = []
	reponseList["4"] = []
	reponseList["5"] = []

	return data, reponseList


def getDataFromTextFile(folder):
	data = []
	# for loop
	for filename in os.listdir(folder):
		with open(folder+ "/" +filename) as inp:
			for line in inp:
				words = splitByWord(line)
				for w in words:
					data.append(w)
	return data


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
	l = sorted([[y, x] for x,y in dictionnary.items()], reverse=True)
	return l[0:n]


# get words
words = getDataFromTextFile("base_appr_fr")
# Sort word - keep les X mots les plus utilises
listSortedWords = sortByWord(words, int(20))

print listSortedWords

# data, reponseList = readJson('1_faq_dmc.json')
# pprint(data)
# pprint(reponseList)
