# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:25:51 2020

@author: cm
"""



from hellonlp.ChineseWordSegmentation.modules import get_scores 
from hellonlp.ChineseWordSegmentation.hyperparameters import Hyperparamters as hp
from hellonlp.ChineseWordSegmentation.utils import sentence_split_regex,remove_characters_irregular

    
    
def get_words(corpus,
               top_k = hp.top_k,
               chunk_size = hp.chunk_size,
               min_n = hp.min_n,
               max_n = hp.max_n,
               min_freq = hp.min_freq):
    '''
    Word segmentation
    '''
    # Sentence segmentation and Clean characters irregulars
    if isinstance(corpus,str):
        corpus_splits = [remove_characters_irregular(sent) for sent in sentence_split_regex(corpus)]
    elif isinstance(corpus,list): 
        corpus_splits = [remove_characters_irregular(sent) for news in corpus for sent in
                                sentence_split_regex(str(news)) if len(remove_characters_irregular(sent)) != 0]
    else:
        corpus_splits = remove_characters_irregular(corpus, chunk_size)
    # Get words and scores
    word_info_scores = get_scores(corpus_splits,min_n,max_n,chunk_size,min_freq)
    # Sorted by score
    new_words = [item[0] for item in sorted(word_info_scores.items(),key=lambda item:item[1][-1],reverse = True)]
    # Get the top k words
    if top_k > 1:             
        return [''.join(l) for l in new_words[:top_k]]
    elif top_k < 1:           
        return [''.join(l) for l in new_words[:int(top_k*len(new_words))]]
    
    
    
if __name__ == '__main__':
    ## 加载数据
    from hellonlp.ChineseWordSegmentation.utils import load_excel_only_first_sheet
    f = 'data/data.xlsx'
    contents = load_excel_only_first_sheet(f).fillna('')['content'].tolist()[:100]
    print(len(contents))  
    #
    #contents = ['23','dsad','dwq']
    words = get_words(contents)  
    print(words[:100])



    
    
    


