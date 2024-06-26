#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : setup.py
# @Author: Richard Chiming Xu
# @Date  : 2024/6/24
# @Desc  :
from setuptools import setup, find_packages

with open("README.md","r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dwspark",
    python_requires='>=3.8',
    version="2024.0.2",
    packages=find_packages(),
    install_requires=[
        "spark_ai_python",
        "loguru",
        "cffi",
        "gevent",
        "greenlet",
        "pycparser",
        "six",
        "websockets",
        "websocket-client",
        "chardet",
    ],
    author="datawhale",
    author_email="datawhale@example.com",
    description="DataWhale用于星火杯2024的适配sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
)