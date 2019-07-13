# Importing libraries
from pymongo import MongoClient

import nltk
nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))

import spacy
spacy.load('en')
from spacy.lang.en import English
parser = English()

import gensim

"""
TO DO:
- Tokenize text
- Bigram and trigram text
- Lemmatize text
- Stopword removal
- Bag-of-words: either in this script or next script
"""

