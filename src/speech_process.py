# Importing libraries
from pymongo import MongoClient

import nltk
import ssl
from nltk.util import ngrams

# Downloading nltk datasets
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet')
nltk.download('stopwords')


from nltk.stem.wordnet import WordNetLemmatizer
en_stop = set(nltk.corpus.stopwords.words('english'))

# Importing spacy
import spacy
spacy.load('en')
from spacy.lang.en import English
parser = English()

# Function to tokenize text
def tokenize_text (text):
    # Tokenizing text
    lda_tokens = nltk.word_tokenize(text)

    # Making all tokens lowercase
    lda_tokens = [token.lower() for token in lda_tokens if token.isalpha()]

    return lda_tokens

# Converts tokens into bigrams (n = 2) or trigrams (n = 3)
def ngram_text(text, n):
    bigram_list = list(ngrams(text, n))
    return bigram_list

# Function to lemmatize text (find synonyms/root)
def get_lemma(text):
    return WordNetLemmatizer().lemmatize(text)

# Overall text preparation function
def prepare_text(text):
    tokens = tokenize_text(text)

    # Removing short tokens and stopword tokens
    tokens = [token for token in tokens if len(tokens) > 3]
    tokens = [token for token in tokens if (token not in en_stop)]

    # Lemmatizing tokens
    tokens = [get_lemma(token) for token in tokens]

    # Getting bigrams and trigrams
    bigrams = ngram_text(tokens, 2)
    trigrams = ngram_text(tokens, 3)

    return tokens, bigrams, trigrams

# Function to get speech
def extract_speech():
    # Intializing client and navigating to MongoDB database
    client = MongoClient('localhost', 27017)
    db = client.trudeau_speeches
    speeches = db.db_speeches

    return speeches

# Function to update the database
def update_db(tokens, bigrams, trigrams, id, collection):
    # Combining filter and information to update
    filter, update_info = {'_id': id}, {'$set' : {'tokens': tokens,
                                                  'bigrams': bigrams,
                                                  'trigrams': trigrams}}

    # Updating:
    collection.update_one(filter, update_info)


# Main function
def main():
    speeches = extract_speech()

    for speech in speeches.find():
        speech_id = speech['_id']
        speech_content = speech['details']

        # Processing speech
        tokens, bigrams, trigrams = prepare_text(speech_content)

        # Putting back into database
        update_db(tokens, bigrams, trigrams, speech_id, speeches)

if __name__ == '__main__':
    main()