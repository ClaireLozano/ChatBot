# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 11:30:22 2018

@author: root
"""
import codecs 
dict_syns = {}
fichier = codecs.open('thes_fr.txt','r')
for ligne in fichier:
    if ligne.endswith("1\n"):
        dict_syns[ligne.split("|")[0]] = [x for x in fichier.next().rstrip().split("|") if "(" and ")" not in x]            
fichier.close()

