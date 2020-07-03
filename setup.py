# -*- coding: utf-8 -*-
"""
Created on Thu May 30 21:01:45 2019

@author: cm
"""

from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import pkg_resources
from setuptools import setup, find_packages
import os
import codecs
import re
import sys


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with codecs.open(path, encoding='utf-8') as fobj:
        return fobj.read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='word_segmentation',
    version=find_version("word_segmentation", "__init__.py"),
    description='Chinese word segmentation algorithm without corpus',
    author='陈明',
    author_email='chenming9109@163.com',
    license='MIT',
    keywords='NLP,tokenizing,Chinese word segementation',
    url='https://github.com/hellonlp/hellonlp',
    packages = find_packages(),
    package_dir={'wordseg': 'wordseg'},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic',
      ]
)
