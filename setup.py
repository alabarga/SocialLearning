# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import SocialLearning
version = SocialLearning.__version__

setup(
    name='SocialLearning',
    version=version,
    author='',
    author_email='alberto.labarga@gmail.com',
    packages=[
        'SocialLearning',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.6.5',
    ],
    zip_safe=False,
    scripts=['SocialLearning/manage.py'],
)