# **************************************** MODULES ************************************
#  NLTK setup
import nltk
nltk.download('wordnet')# Database for English
from nltk.stem.wordnet import WordNetLemmatizer # Lemmatizes words
# Stopword setup
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))


# Spacy setup
import spacy
spacy.load('en_core_web_sm')
from spacy.lang.en import English
parser = English()

# Other libraries
import pickle
from pymongo import MongoClient
import gensim
from gensim import corpora