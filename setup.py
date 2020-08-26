#!python
# -*- coding:utf-8 -*-
from __future__ import print_function
from setuptools import setup, find_packages
import mxgames

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="hellonlp",
    version="0.1.0",
    author="MingChen",
    author_email="chenming9109@163.com",
    description="NLP tools",
    license="MIT",
    url="https://github.com/hellonlp/hellonlp",
    packages=find_packages(),

    classifiers=[
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)

