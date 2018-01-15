import json
from pprint import pprint

def readJson(data):
	data = json.load(open(data))
	return data


data = readJson('1_faq_dmc.json')
pprint(data)
