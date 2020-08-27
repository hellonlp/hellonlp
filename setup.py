# -*- coding:utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages
import os

rootdir = os.path.abspath(os.path.dirname(__file__))
LONGDOC = open(os.path.join(rootdir, 'README.md'), encoding='utf-8').read()
LONGDOC2 = """
HelloNLP
========


开发者
========
| Author | Email | 
| ----- | ------ | 
| ChenMing | chenming9109@163.com |


主要功能
========
1. 分词-通过信息熵
2. 分词-通过深度学习（并引入结巴多个分词模式的方式）


## Install 安装
通过`pip`安装
```shell
pip install hellonlp>=0.2.2
```

通过源代码安装最新版本
```shell
git clone https://github.com/hellonlp/hellonlp.git
cd hellonlp
python setup.py install
```

## 调用示例&可视化

```python
from hellonlp.ChineseWordSegmentation import segment_entropy

ngrams = segment_entropy.get_words(["界面又好看",
                            "主要是大像素摄像头",
                            "心理准备一星期",
                            "厂家和快递都好评",
                            "还有听儿歌要下载米兔儿童",
                            "空调三匹太强劲",
                            "HelloNLP会一直坚持开源和贡献",
			    "HelloNLP第一版终于发布了，太激动了",])
                                                
```

"""

setup(
    name="hellonlp",
    version="0.2.19",
    author="Chen Ming",
    author_email="chenming9109@163.com",
    description="NLP tools",
    long_description=LONGDOC,
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/hellonlp/hellonlp",
    packages=find_packages(),
    install_requires=[
        'numpy',
        "requests",
        "pygtrie",
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   keywords = 'NLP,Chinese word segementation',
   package_data={'hellonlp':['ChineseWordSegmentation/data/*','ChineseWordSegmentation/dict/*.txt']}
)

