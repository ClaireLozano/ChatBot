# -*- coding: iso-8859-1 -*-
import os
import json
import codecs
from pprint import pprint
def getDataFromTextFileJson():
	data = []
	for file in os.listdir("."):
		if file.endswith(".json") and file != "3_questions_syp.json":
			print file
			with codecs.open(file,'r',"utf-8") as inp:
				dict_test = json.load(inp)
				for k, v in dict_test.iteritems():
					words = splitByWord(v[0])
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
	l = sorted([x for x,y in dictionnary.items() if y > 8], reverse=True)
	return l


def suppressionMot(path, l):
	questions = {}
	with open(path) as inp:
		dict_test = json.load(inp)
		for k, v in dict_test.iteritems():
			words = splitByWord(v[0])
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



# get words
# words = getDataFromTextFile("base_appr_fr")
words = getDataFromTextFileJson()


# Sort word - keep les X mots les plus utilises
listSortedWords = sortByWord(words, int(8))

wordsList = ['que', 'quels', 'comme', 'est', 'sont', 'dans', 'ma', 'mon', 'moi', 'se']
listSortedWords = appendWordTolist(listSortedWords, wordsList)

print listSortedWords

words = suppressionMot("1_faq_dmc.json", listSortedWords)

dict_res = {}
with codecs.open("1_faq_dmc.json") as file_test:
    dict_test = json.load(file_test)
for value in dict_test.values():
    for key,valeur in words.items():
        if key == value[0]:
            dict_res[value[1]] = valeur
pprint(dict_res)            

