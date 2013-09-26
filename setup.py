#!/usr/bin/env python

from distutils.core import setup

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(name='orderedlistdict',
      version='0.0.1',
      description='A dictionary where the values are lists and the insertion order is retained',
      author='Deniz Dogan',
      author_email='deniz@dogan.se',
      url='http://orderedlistdict.dogan.se',
      packages=['orderedlistdict'],
      install_requires=requirements,
      classifiers=[
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          ],
     )
