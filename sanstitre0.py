# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:57:50 2018

@author: root
"""
text="plate-forme puis-je"
listPronoms = ["je", "tu", "il", "t", "elle", "on", "nous", "vous", "ils", "elles"]
listWord = []
for word in text.split():
    if "-" in word:
        for mot in word.split("-"):
            print mot
            if mot in listPronoms:
                word = word.replace(mot,"") 
            else:
                listWord.append(word)
print listWord               
