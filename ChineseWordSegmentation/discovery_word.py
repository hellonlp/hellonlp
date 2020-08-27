# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 17:16:21 2020

@author: cm
"""


from hellonlp.ChineseWordSegmentation.utils import load_txt
from hellonlp.ChineseWordSegmentation.segment_entropy import get_words
from hellonlp.ChineseWordSegmentation.hyperparameters import Hyperparamters as hp
from hellonlp.ChineseWordSegmentation.utils import load_excel_only_first_sheet,ToolWord



vocabulary_set = set(load_txt(hp.file_vocabulary))



def get_words_new(corpus):
    """
    Get these words that not in vocabulary.
    """
    words = get_words(corpus)
    print('Length of words:',len(words))
    words_clean = [l for l in words if ToolWord().remove_word_special(l)!='']
    print('Length of words(clean):',len(words_clean))
    return [w for w in words_clean if w not in vocabulary_set]





if __name__ == '__main__':
    ##
    document = ['葫芦屏 武汉 武汉 北京 葫芦屏 葫芦屏 武汉','武汉 武汉 北京 葫芦屏 葫芦屏 武汉 十四是十四四十是四十，']
    ws = get_words(document)
    print(ws)
    ##
    f = 'data/data.xlsx'
    contents = load_excel_only_first_sheet(f).fillna('')['content'].tolist()#[:5000]
    print(len(contents))
    words = get_words(contents)
    print(words[:1000])
    nws = get_words_new(contents)  
    print(nws[:200])
    print(len(nws))














