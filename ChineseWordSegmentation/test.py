# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 10:29:02 2020

@author: cm
"""



from nwr.utils import load_txt,save_txt


f = 'dict/vocabulary_init.txt'
lines = load_txt(f)
print(len(lines))


lines2 = [l for l in lines if '#' not in l]
print(len(lines2))
lines3 = [l.split()[0] if '\t' in l else l for l in lines2 ]
print(len(list(set(lines3))))
lines4 = sorted(list(set(lines3)))
f3 = 'dict/vocabulary.txt'
save_txt(f3,lines4)
