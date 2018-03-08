# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='RSearcherNLP',
    version='0.1.0',
    description='NLP package for Restaurant Searcher',
    long_description=readme,
    author='Kentaro KAZAMA',
    author_email='kazehara@outlook.com',
    url='https://github.com/kazehara/RestaurantSearcherNLP',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'numpy',
        'gensim'
    ]
)

