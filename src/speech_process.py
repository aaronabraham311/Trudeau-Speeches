# Importing libraries
from pymongo import MongoClient

import nltk
from nltk.util import ngrams
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

# Function to tokenize text
def tokenize_text (text):
    # Initial set up
    lda_tokens = []
    tokens = parser(text)

    for token in tokens:
        if token.orth_.isspace(): # Skips over space tokens
            continue
        lda_tokens.append(token.lower_) # Converts all tokens into lower case

    return lda_tokens

# Converts tokens into bigrams (n = 2) or trigrams (n = 3)
def ngram_text(text, n):
    bigram_list = list(ngrams(text, n))
    return bigram_list

