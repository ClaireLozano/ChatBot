# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 15:57:57 2018

@author: root
"""

import treetaggerwrapper
# Construction et configuration du wrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr',TAGDIR='/home/hchlih/Documents/projetTAL2018/projet_icone_2018/treetragger',
  TAGINENC='utf-8',TAGOUTENC='utf-8')
# Utilisation
tags = tagger.TagText(u"mangeait")
tags2 = treetaggerwrapper.make_tags(tags)
print tags2