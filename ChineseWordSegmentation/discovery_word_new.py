# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 17:16:21 2020

@author: cm
"""


from ChineseWordSegmentation.utils import load_txt
from ChineseWordSegmentation.word_segmentation import get_words
from ChineseWordSegmentation.hyperparameters import Hyperparamters as hp
from ChineseWordSegmentation.utils import load_excel_only_first_sheet,RemoveWordSpecial



vocabulary_set = set(load_txt(hp.file_vocabulary))



def get_words_new(corpus):
    """
    Get these words that not in vocabulary.
    """
    words = get_words(corpus)
    print('Length of words:',len(words))
    words_clean = [l for l in words if RemoveWordSpecial().remove_word_special(l)!='']
    print('Length of words(clean):',len(words_clean))
    return [w for w in words_clean if w not in vocabulary_set]





if __name__ == '__main__':
    ##
    document = ['葫芦屏 武汉 武汉 北京 葫芦屏 葫芦屏 武汉','武汉 武汉 北京 葫芦屏 葫芦屏 武汉 十四是十四四十是四十，']
    ws = get_words(document)
    print(ws)


    ##
    f = 'F:/leek/nwr/data/SmoothNLP36kr新闻数据集10k.xlsx'
    contents = load_excel_only_first_sheet(f).fillna('')['content'].tolist()#[:5000]
    print(len(contents))
    words = get_words(contents)
    print(words[:1000])
    nws = get_words_new(contents)  
    print(nws[:200])
    print(len(nws))
#    nws.index('阿里巴巴')
    
    
#    ##
#    result = get_words(contents)
#    result[:100]
#    words = [str(w).strip() for w in result if len(str(w).strip())>1]
#    words_new = [w for w in words if w not in vocabulary_set]
#    print(words_new[:300])
#    #    
#    words1 =[l for l in words if len(l)>4]
#    words1
#    
#    #
#    jieba.lcut('创业公司')













