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
from hellonlp.ChineseWordSegmentation.utils import calcul_word_frequence
from hellonlp.ChineseWordSegmentation.probability import entropy_of_list
from hellonlp.ChineseWordSegmentation.hyperparameters import Hyperparamters as hp
from hellonlp.ChineseWordSegmentation.utils import ToolWord
from hellonlp.ChineseWordSegmentation.tokenization import FullTokenizer



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
            ngram_generator = [tuple(l) for l in generate_ngram(corpus_chunk, ni)]
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
    parent_candidates = ngram_keys[n+1]
    if n!=1:
        target_ngrams = ngram_keys[n]
    else:
        target_ngrams = [l for l in ngram_keys[n] if ToolWord().is_english_word(l[0])]       

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
    # Pointwise Mutual Information 
    # Average Mutual Information
    """
    if isinstance(n,collections.abc.Iterable):
        mi = {}
        for ni in n:
            mi = {**mi,**calcul_ngram_pmi(ngram_freq,ngram_keys,ni)}
        return mi

    if n!=1:
        target_ngrams = ngram_keys[n]
    else:
        target_ngrams = [l for l in ngram_keys[n] if ToolWord().is_english_word(l[0])]       

    n1_totalcount = sum([ngram_freq[k] for k in ngram_keys[1] if k in ngram_freq])
    target_n_total_count = sum([ngram_freq[k] for k in ngram_keys[n] if k in ngram_freq])
    mi = {}
    for target_ngram in target_ngrams:
        target_ngrams_freq = ngram_freq[target_ngram]
        joint_proba = target_ngrams_freq/target_n_total_count
        indep_proba = reduce(mul,[ngram_freq[(char,)] for char in target_ngram])/((n1_totalcount)**n)
        pmi = math.log(joint_proba/indep_proba,hp.e)  
        ami = pmi/len(target_ngram)                 
        mi[target_ngram] = (pmi,ami)
    return mi


def get_scores(corpus,
               min_n = 2,
               max_n = 4,
               chunk_size=1000000,
               min_freq=3):
    """
    Calcul the score of words
    :return: tuple with word
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
    # Word liberalization
    word_liberalization = lambda el,er: math.log((el * hp.e ** er+0.00001)/(abs(el - er)+1),hp.e) \
                                       + math.log((er * hp.e ** el+0.00001)/(abs(el - er)+1),hp.e)

    word_info_scores = {word: (mi[word][0],     
                 mi[word][1],                   
                 left_right_entropy[word][0],   
                 left_right_entropy[word][1],   
                 min(left_right_entropy[word][0],left_right_entropy[word][1]),    
                 word_liberalization(left_right_entropy[word][0],left_right_entropy[word][1])+mi[word][1]   
                     )
              for word in joint_phrase}

    # Drop some special word that end with "的" like "XX的,美丽的,漂亮的"
    target_ngrams = word_info_scores.keys()
    start_chars = collections.Counter([n[0] for n in target_ngrams])
    end_chars = collections.Counter([n[-1] for n in target_ngrams])
    threshold = int(len(target_ngrams) * 0.004)
    threshold = max(50,threshold)
    invalid_start_chars = set([char for char, count in start_chars.items() if count > threshold])
    invalid_end_chars = set([char for char, count in end_chars.items() if count > threshold])
    invalid_target_ngrams = set([n for n in target_ngrams if (n[0] in invalid_start_chars or n[-1] in invalid_end_chars)])
    # Remove some words invalids
    for n in invalid_target_ngrams:  
        word_info_scores.pop(n)
    return word_info_scores




if __name__ == '__main__':
    ## Load data
    print('1')




