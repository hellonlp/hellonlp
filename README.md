HelloNLP,NLP with deep learning. Mainly focus on text classification, NER, Chabot , pre-trained models.

GitHub: https://github.com/hellonlp



HelloNLP
^^^^^^^^^^^                     
 - ChineseWordSegmentation：一种无监督的分词工具，通过信息熵实现。
 - 新分词：有监督，通过深度学习（同时引入结巴分词多种分词模式的思维）# 开发中




Example
^^^^^^^^^^^
Quick start

>>>
pip3 install hellonlp
from hellonlp.ChineseWordSegmentation import segment_entropy
words = segment_entropy.get_words(["HelloNLP会一直坚持开源和贡献",
                            "HelloNLP专注于NLP技术",
			    "HelloNLP第一版终于发布了，太激动了",                           
                            "HelloNLP目前支持无监督的分词",
                            "HelloNLP之后还会支持深度学习的分词",
                            "HelloNLP目前只支持python",])
print(words[:10])
