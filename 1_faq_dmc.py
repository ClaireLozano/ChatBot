# -*- coding: iso-8859-1 -*-

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

data, reponseList = readJson('1_faq_dmc.json')
pprint(data)
pprint(reponseList)
