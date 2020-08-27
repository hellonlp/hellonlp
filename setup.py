# -*- coding:utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages
import os

rootdir = os.path.abspath(os.path.dirname(__file__))
LONGDOC = open(os.path.join(rootdir, 'README.md'), encoding='utf-8').read()


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

