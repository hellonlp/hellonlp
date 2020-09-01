# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 10:30:26 2020

@author: cm
"""


import math
from hellonlp.ChineseWordSegmentation.hyperparameters import Hyperparamters as hp


def entropy_of_list(parent_ngrams_freq):
    """
    Calcul entropy  by candidate's neighbor frequence
    """
    counts = sum(parent_ngrams_freq)
    ngram_probabilitys = map(lambda x: x/counts,parent_ngrams_freq)
    entropy = sum(map(lambda x: -1 * x * math.log(x,hp.e),ngram_probabilitys))
    return entropy



if __name__ == '__main__':
    
    right_neighbor_counts = [12, 16, 3, 6, 9, 5, 5, 3, 5, 4, 4,
                             6, 11, 3, 5, 7, 16, 20, 4, 3, 5]
    print(entropy_of_list(right_neighbor_counts))


    
