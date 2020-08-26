# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:08:58 2020

@author: cm
"""


import math
import types
import collections
from operator import mul
from pygtrie import Trie
from functools import reduce
from ChineseWordSegmentation.utils import calcul_word_frequence
from ChineseWordSegmentation.probability import entropy_of_list
from ChineseWordSegmentation.hyperparameters import Hyperparamters as hp
from ChineseWordSegmentation.utils import RemoveWordSpecial
from ChineseWordSegmentation.tokenization import FullTokenizer



tokenizer = FullTokenizer.from_scratch(vocab_file=hp.vocab_file,
                                       do_lower_case=True, 
                                       spm_model_file=None)   




def generate_ngram(corpus,n=2):
    """
    Generate the ngram word-group possible by token_length(2,3,4)
    return: generator (economize IO)
    """
    def generate_ngram_str(text,n):
        text = tokenizer.tokenize(text)
        for i in range(0, len(text)-n+1):
            yield text[i:i+n]
    if isinstance(corpus,str):
        for ngram in generate_ngram_str(corpus,n):
            yield ngram
    elif isinstance(corpus, (list, types.GeneratorType)):
        for text in corpus:
            for ngram in generate_ngram_str(text,n):
                yield ngram

#min_n=2
#max_n = 4
#for ni in [1]+list(range(min_n,max_n+2)):
#    print(ni)
    
def get_ngram_frequence_infomation(corpus, 
                        min_n=2,
                        max_n=4,
                        chunk_size=10000000,
                        min_freq=5,
                         ):
    """
    Get words's frequences
    """
    ngram_freq_total = {}  ## stock word frequence
    ngram_keys = {i: set() for i in range(1, max_n + 2)}  

    def get_frequence_chunk(corpus_chunk):
        """
        Get chunk's frequence
        Chunk: a part of Corpus
        """
        ngram_freq = {}
        for ni in [1]+list(range(min_n,max_n+2)):# 1 2 3 4 5
            #ngram_generator = generate_ngram(corpus_chunk, ni)
            ngram_generator = [tuple(l) for l in generate_ngram(corpus_chunk, ni)]
            # by cm
#            if ni==1:
#                ngram_generator_init = [tuple(l) for l in generate_ngram(corpus_chunk, ni)]
#                ngram_generator = [l for l in ngram_generator_init if RemoveWordSpecial().is_english_word(l[0])]
#            else:
#                ngram_generator = [tuple(l) for l in generate_ngram(corpus_chunk, ni)]
            nigram_freq = dict(collections.Counter(ngram_generator))
            ngram_keys[ni] = (ngram_keys[ni] | nigram_freq.keys())
            ngram_freq = {**nigram_freq, **ngram_freq}
        ngram_freq = {word: count for word, count in ngram_freq.items() if count >= min_freq}  ## 每个chunk的ngram频率统计
        return ngram_freq

    if isinstance(corpus,types.GeneratorType):
        for corpus_chunk in corpus:
            ngram_freq = get_frequence_chunk(corpus_chunk)
            ngram_freq_total = calcul_word_frequence(ngram_freq, ngram_freq_total)
    elif isinstance(corpus,list): 
        len_corpus = len(corpus)  
        for i in range(0,len_corpus,chunk_size):
            corpus_chunk = corpus[i:min(len_corpus,i+chunk_size)]
            ngram_freq = get_frequence_chunk(corpus_chunk)
            ngram_freq_total = calcul_word_frequence(ngram_freq,ngram_freq_total)
    for k in ngram_keys:
        ngram_keys[k] = ngram_keys[k] & ngram_freq_total.keys()
    return ngram_freq_total,ngram_keys


def calcul_ngram_entropy(ngram_freq,
                        ngram_keys,
                        n):
    """
    Calcul entropy by ngram frequences
    """
    # Calcul ngram entropy
    if isinstance(n,collections.abc.Iterable): 
        entropy = {}
        for ni in n:
            entropy = {**entropy,**calcul_ngram_entropy(ngram_freq,ngram_keys,ni)}
        return entropy
    
    
    ngram_entropy = {}
    #target_ngrams = ngram_keys[n]
    parent_candidates = ngram_keys[n+1]
    
    # by cm
    if n!=1:
        target_ngrams = ngram_keys[n]
    else:
        target_ngrams = [l for l in ngram_keys[n] if RemoveWordSpecial().is_english_word(l[0])]       

    if hp.CPU_COUNT == 1:
        # Build trie for n+1 gram 
        left_neighbors = Trie()
        right_neighbors = Trie()

        for parent_candidate in parent_candidates:
            right_neighbors[parent_candidate] = ngram_freq[parent_candidate]
            left_neighbors[parent_candidate[1:]+(parent_candidate[0],)] = ngram_freq[parent_candidate]

        # Calcul entropy
        for target_ngram in target_ngrams:
            try:  
                right_neighbor_counts = (right_neighbors.values(target_ngram))
                right_entropy = entropy_of_list(right_neighbor_counts)
            except KeyError:
                right_entropy = 0
            try:
                left_neighbor_counts = (left_neighbors.values(target_ngram))
                left_entropy = entropy_of_list(left_neighbor_counts)
            except KeyError:
                left_entropy = 0
            ngram_entropy[target_ngram] = (left_entropy,right_entropy)
        return ngram_entropy
    else:
        # Multi process
        pass


def calcul_ngram_pmi(ngram_freq,ngram_keys,n):
    """
    计算 Pointwise Mutual Information 与 Average Mutual Information
    """
    if isinstance(n,collections.abc.Iterable):
        mi = {}
        for ni in n:
            mi = {**mi,**calcul_ngram_pmi(ngram_freq,ngram_keys,ni)}
        return mi
    
    # by cm
    if n!=1:
        target_ngrams = ngram_keys[n]
    else:
        target_ngrams = [l for l in ngram_keys[n] if RemoveWordSpecial().is_english_word(l[0])]       

    n1_totalcount = sum([ngram_freq[k] for k in ngram_keys[1] if k in ngram_freq])
    target_n_total_count = sum([ngram_freq[k] for k in ngram_keys[n] if k in ngram_freq])
    mi = {}
    for target_ngram in target_ngrams:
        target_ngrams_freq = ngram_freq[target_ngram]
        joint_proba = target_ngrams_freq/target_n_total_count
        #indep_proba = reduce(mul,[ngram_freq[char] for char in target_ngram])/((n1_totalcount)**n)
        # by cm
        indep_proba = reduce(mul,[ngram_freq[(char,)] for char in target_ngram])/((n1_totalcount)**n)
        pmi = math.log(joint_proba/indep_proba,2)   #point-wise mutual information
        ami = pmi/len(target_ngram)                 #average mutual information
        mi[target_ngram] = (pmi,ami)
    return mi


def get_scores(corpus,
               min_n = 2,
               max_n = 4,
               chunk_size=1000000,
               min_freq=3):
    """
    基于corpus, 计算所有候选词汇的相关评分.
    :return: 为节省内存, 每个候选词的分数以tuble的形式返回.
    """
    # Get ngram word frequence
    ngram_freq, ngram_keys = get_ngram_frequence_infomation(corpus,min_n,max_n,
                                                 chunk_size=chunk_size,
                                                 min_freq=min_freq)
    # Get left and right ngram entropy
    left_right_entropy = calcul_ngram_entropy(ngram_freq,ngram_keys,range(min_n,max_n+1))
    # Get pmi ngram entropy
    mi = calcul_ngram_pmi(ngram_freq,ngram_keys,range(min_n,max_n+1))
    # Join keys of entropy and keys of pmi
    joint_phrase = mi.keys() & left_right_entropy.keys()
    word_liberalization = lambda le,re: math.log((le * 2 ** re + re * 2 ** le+0.00001)/(abs(le - re)+1),1.5)
    word_info_scores = {word: (mi[word][0],     #point-wise mutual information
                 mi[word][1],                   #average mutual information
                 left_right_entropy[word][0],   #left_entropy
                 left_right_entropy[word][1],   #right_entropy
                 min(left_right_entropy[word][0],left_right_entropy[word][1]),    #branch entropy  BE=min{left_entropy,right_entropy}
                 word_liberalization(left_right_entropy[word][0],left_right_entropy[word][1])+mi[word][1]   #our score
                     )
              for word in joint_phrase}

    # Drop some special word that end with "的" like "XX的,美丽的,漂亮的"
    target_ngrams = word_info_scores.keys()
    start_chars = collections.Counter([n[0] for n in target_ngrams])
    end_chars = collections.Counter([n[-1] for n in target_ngrams])
    threshold = int(len(target_ngrams) * 0.004)
    threshold = max(50,threshold)
    print("Threshold used for removing start end char: {}".format(threshold))
    invalid_start_chars = set([char for char, count in start_chars.items() if count > threshold])
    invalid_end_chars = set([char for char, count in end_chars.items() if count > threshold])
    invalid_target_ngrams = set([n for n in target_ngrams if (n[0] in invalid_start_chars or n[-1] in invalid_end_chars)])
    # Remove some words invalids
    for n in invalid_target_ngrams:  
        word_info_scores.pop(n)
    return word_info_scores




if __name__ == '__main__':
    ## Load data
    from nwr.utils import load_excel_only_first_sheet
    f = 'data/SmoothNLP36kr新闻数据集10k.xlsx'
    contents = load_excel_only_first_sheet(f).fillna('')['content'].tolist()[:1000]
    print(len(contents))
    ## Test
    word_info_scores = get_scores(contents)
    print(list(word_info_scores.keys())[:200])
    
    ## Test simple
    
    
    
    
    ## 参数
    min_n = 2
    max_n = 4
    chunk_size = 1000000
    min_freq = 3
    
#    ## 测试：get_ngram_freq_info
#    ngram_freq, ngram_keys = get_ngram_freq_info(contents,min_n,max_n,
#                                                 chunk_size=chunk_size,
#                                                 min_freq=min_freq)    
#    print(len(ngram_freq),len(ngram_keys))#188011 5    
    
    
    
    ## 整个流程
    ngram_freq_total = {}  ## 记录词频
    ngram_keys = {i: set() for i in range(1, max_n + 2)}  ## 用来存储N=时, 都有哪些词

    def _process_corpus_chunk(corpus_chunk):## 获取词频
        ngram_freq = {}
        
        for ni in [1]+list(range(min_n,max_n+2)):# 1 2 3 4 5
            #ni = 2
            ngram_generator = [tuple(l) for l in generate_ngram(corpus_chunk, ni)]
            
            nigram_freq = dict(collections.Counter(ngram_generator))
            ngram_keys[ni] = (ngram_keys[ni] | nigram_freq.keys())
            ngram_freq = {**nigram_freq, **ngram_freq}
        ngram_freq = {word: count for word, count in ngram_freq.items() if count >= min_freq}  ## 每个chunk的ngram频率统计
        return ngram_freq    
    ##
#    contents = [text]*20
#    a = _process_corpus_chunk(contents)
#    print(len(list(a.keys())),list(a.keys())[:100],list(a.values())[:100])
#    
#
#
#
#   ## 整个流程-多个窗口
#    ngram_keys = {i: set() for i in range(1, max_n + 2)} 
#    ngram_freq = {}
#    for ni in [1]+list(range(min_n,max_n+2)):# 1 2 3 4 5
#        print('='*20)
#        print('ni:',ni)
#        ngram_generator = generate_ngram(contents, ni)
#        nigram_freq = dict(collections.Counter(ngram_generator))
#        print(len(nigram_freq.keys()))
#        ngram_keys[ni] = (ngram_keys[ni] | nigram_freq.keys())
#        ngram_freq = {**nigram_freq, **ngram_freq}
#    print(len(ngram_freq.keys()),len(ngram_freq.values())) ## 一共2570663个组个
#    ngram_freq = {word: count for word, count in ngram_freq.items() if count >= min_freq} ## 删除词频小于min_freq词
#    print(len(ngram_freq.keys()),len(ngram_freq.values())) ## 组成的词的总个数：188011
#    print(list(ngram_freq.keys())[:10]) ## 组成的词
#   
#    ##
#    len_corpus = len(contents)  ## ok(分块处理)
#    for i in range(0,len_corpus,chunk_size):
#        corpus_chunk = contents[i:min(len_corpus,i+chunk_size)]
#        ngram_freq = _process_corpus_chunk(corpus_chunk)
#        ngram_freq_total = calcul_word_frequence(ngram_freq,ngram_freq_total)
#    print(len(ngram_freq.keys())) ## 188011
#    for k in ngram_keys:
#        ngram_keys[k] = ngram_keys[k] & ngram_freq_total.keys()##集合并集
#    print(ngram_keys.keys()) #dict_keys([1, 2, 3, 4, 5])
#    print(list(ngram_keys[2]) [:10])## 两个字的词
#    print(len(list(ngram_keys[1]))) ## 一个字组成词的个数：2820
#    print(len(list(ngram_keys[2]))) ## 两个字组成词的个数：51440
#    print(len(list(ngram_keys[3]))) ## 三个字组成词的个数：69682
#    print(len(list(ngram_keys[4]))) ## 四个字组成词的个数：43188
#    print(len(list(ngram_keys[5]))) ## 五个字组成词的个数：20881
#    ## 总共188011个
#    
#    ## 计算一个词出现在左边和右边的概率
#    left_right_entropy = calcul_ngram_entropy(ngram_freq,ngram_keys,range(min_n,max_n+1))    
#    ## 去除1个字的组合
#    print(len(left_right_entropy.keys()),len(left_right_entropy.values()))
#    print(list(left_right_entropy.keys())[:10],list(left_right_entropy.keys())[-10:])
#    print(list(left_right_entropy.values())[:100],list(left_right_entropy.values())[-100:])
#




