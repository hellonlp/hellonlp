# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 20:08:33 2020

@author: cm
"""


import re
import pandas as pd



def load_txt(file):
    """
    Load a txt
    """
    with  open(file, encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
        lines = [l.strip() for l in lines]
    return lines


def save_txt(file,lines):
    lines = [l+'\n' for l in lines]
    with  open(file,'w+',encoding='utf-8') as fp:#a+添加
        fp.writelines(lines)
        print("Write data to file (%s) finished !"%file)


def sentence_split_regex(sentence):
    """
    Sentence segmentation
    """
    if sentence is not None:
        sentence = re.sub(r"&ndash;+|&mdash;+", "-", sentence)
        sub_sentence = re.split(r"[。,，！!？?;；\s…~～]+|\.{2,}|&hellip;+|&nbsp+|_n|_t", sentence)
        sub_sentence = [s for s in sub_sentence if s != '']
        if sub_sentence != []:
            return sub_sentence
        else:
            return []
    else:
        return []
    

def remove_characters_irregular(corpus):
    """
    Corpus: type string
    """
    return re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", corpus)


def calcul_word_frequence(dic1,dic2):
    '''
    :param dic1:{'我':200,'喜欢':2000,....}:
    :param dic2:{'我':300,'你':1000,....}:
    :return:{'我':500,'喜欢':2000,'你':1000,....}
    '''
    keys = (dic1.keys()) | (dic2.keys())
    total = {}
    for key in keys:
        total[key] = dic1.get(key, 0) + dic2.get(key, 0)
    return total


def load_excel_only_first_sheet(file, Header=0, Index_col=None, Sheet_name=None):
    """
    :param file: the path of excel
    :param Header: the first line of DataFrame (whether chose the first line of DataFrame as the index name)
    :param Index_col: the first column of DataFrame （whether chose the first column of DataFrame as the column name）
    :param Sheet_name: these sheet-names in the excel
    :return: a lot of sheets
    """
    dfs = pd.read_excel(file,
                        index_col=Index_col,
                        header=Header,
                        sheet_name=Sheet_name)
    sheet_names = list(dfs.keys())
    print('Name of the first sheet:', sheet_names[0])
    return dfs[sheet_names[0]]



class ToolWord():
    """
    Remove some word special
    return: a word or ''
    """
    def remove_word_special(self,word):
        """
        # Word start with number and end with others: ['6氪','5亿美元','99美元']
        # Word start with not number and end with number: ['Q1']
        # Word is all numbers: ['199','16','25']
        # Word has "年","月" or "日": ['年1','年12月','月2','年9月','9年']
        # Word has "个","十","百","千","万","亿": ['500万','20万']
        # English word: ['Goog','Amaz','YouT']
        # Word has "你","我","他","她","它": ['如果你']
        """
        if not self.is_has_english(word) and \
            not self.is_has_person(word) and \
            not self.is_has_number(word):
            return word
        else:
            return ''

    def is_all_number_list(self,words):
        return True if sum([self.is_all_number(word) for word in words]) == len(words) else False
                   
    @staticmethod
    def is_has_english(word):
        pattern = '[a-zA-Z]'
        result = ''.join(re.findall(pattern,word))
        return True if len(result)>0 else False
    
    @staticmethod
    def is_has_person(word):
        pattern = '[你我他她它还为个们就也在了的入回来去走\
                    一二三四五六七八九十个十百千万亿\
                    年月日天时分秒\
                    让多少有不无否会或这那\
                    爸妈哥姐嫂舅伯叔姨弟妹\
                    第季然即很]'
        result = ''.join(re.findall(pattern,word))
        return True if len(result)>0 else False
    
    @staticmethod
    def is_has_number(word):
        pattern = '[0-9]'
        result = ''.join(re.findall(pattern,word))
        return True if len(result)>0 else False

    @staticmethod
    def is_all_number(word):
        pattern = '[0-9]'
        result = ''.join(re.findall(pattern,word))
        return True if result==word else False

    @staticmethod
    def is_english_word(word):
        pattern = '[a-zA-Z]'
        result = ''.join(re.findall(pattern,word))
        return True if result==word and len(word)>1 else False


            
 
if __name__ == '__main__':
    #
    rws = RemoveWordSpecial()
    print(rws.is_all_number('23s2'))
    #
    words = ['2','44','3']
    print(rws.is_all_number_list(words))
    #
    words = '我们'
    print(rws.is_english_word(words))

