# -*- coding: utf-8 -*-
"""
Created on Wed May  8 17:04:53 2019

@author: smehdi
"""

from setuptools import find_packages, setup

setup(
    name='MTconnect',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)