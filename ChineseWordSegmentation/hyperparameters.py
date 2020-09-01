# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 19:31:35 2020

@author: cm
"""


import os
import math
pwd = os.path.dirname(os.path.abspath(__file__))


class Hyperparamters:
    # Parameters
    file_vocabulary = os.path.join(pwd,'dict/vocabulary_word.txt')
    top_k = 1000
    chunk_size = 1000000
    min_n = 1#1#2
    max_n = 4 
    min_freq = 5
    
    #
    e = math.exp(1)

    # CPU number used
    CPU_COUNT = 1 
    #
    vocab_file = os.path.join(pwd,'dict/vocabulary.txt')
