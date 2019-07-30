# **************************************** MODULES ************************************
#  NLTK setup
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

import nltk
nltk.download('wordnet')# Database for English

# Stopword setup
nltk.download('stopwords')
en_stop = set(nltk.corpus.stopwords.words('english'))


# Spacy setup
import spacy
spacy.load('en')
from spacy.lang.en import English
parser = English()

# Other libraries
import pickle
from pymongo import MongoClient
import gensim
from gensim import corpora
import os

# *************************************** FUNCTIONS **********************************

# Creating latent Dirichlet allocation model
def lda_model(text, NTOPIC):
    # Creating text corpus and making bag of words model
    dictionary = corpora.Dictionary(text)
    corpus = [dictionary.doc2bow(token) for token in text]

    # Saving corpus and dictionary for later use
    corpus_filename = '../data/corpus.pkl'
    os.makedirs(os.path.dirname(corpus_filename), exist_ok= True)

    with open(corpus_filename, 'wb') as filename:
        pickle.dump(corpus, filename)

    dictionary.save('../data/dictionary.gensim')

    # Creating model:
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NTOPIC, id2word = dictionary,
                                               passes = 20)
    topics = ldamodel.print_topics(num_words = 3)
    ldamodel.save("../data/lda_model.gensim")

    print("Outputting topics from LDA model: ")
    for topic in topics:
        print(topic)

    return ldamodel, dictionary, topics

def predict_topic(model, text, dictionary):
    # Converting text to bag of words
    text_bow = dictionary.doc2bow(text)

    # Predicting:
    topic_predictions = model.get_document_topics(text_bow)

    print ("Text: ", text)
    print ('Topic predictions: ', topic_predictions)

# Please remember to enter 'mongod' on command line
# Function to extract data from MongoDB collection
def extract_speech_data():
    # Initializing client:
    client = MongoClient('localhost', 27017)

    # Navigating to collection:
    db = client.trudeau_speeches
    collection = db.db_speeches

    speech_tokens = []

    for speech in collection.find():
        speech_tokens.append({
            'tokens': speech['tokens'],
            'speech': speech['details']})

    return speech_tokens

# Puts topics initially found by LDA on training data into database
def db_lda_topic_update(topics, collection_type):
    client = MongoClient('localhost', 27107)

    # Navigating to collection:
    db = client.stellar_algo_reddit

    if collection_type == 'post':
        post_lda_topics = db.post_lda_topics

        # Inserting each topic (ID and topic name) into database
        for topic in topics:
            post_lda_topics.insert_one(topic)

    elif collection_type == 'comment':
        comment_lda_topics = db.comment_lda_topics

        # Inserting each topic (ID and topic name) into database
        for topic in topics:
            comment_lda_topics.insert_one(topic)

# Puts predictions of topics of newly scrapped comments/posts into database
# Make separate collections for post and comment
def db_topic_predictions_update(text, prediction):
    client = MongoClient()

    # Navigating to collection:
    db = client.trudeau_speeches
    collection = db.predictions

    # Inserting speech and prediction into record
    collection.insert_one({
        'speech' : text,
        'topics' : prediction
    })

if __name__ == '__main__':
    print ("Welcome to to the topic modeller script. In this script, a latent Dirichlet allocation model built on previously scrapped speeches is constructed. "
           "Then, we will scrape additional speeches and show the topic probability. ")

    print ("Please enter the number of topics you would like to find in the speches: ")
    num_topics = int(input())

    # Getting speech tokens and actual speeches
    speech_data = extract_speech_data()

    # Separating tokens:
    speech_tokens = []

    for speech in speech_data:
        speech_tokens.append(speech['tokens'])

    # Creating model, dictionary and topics
    lda_model, dictionary, topics = lda_model(speech_tokens, num_topics)

    # STORE TOPICS IN MONGO

    print("Please note the indices of the topics. We will now conduct topic modelling on more speeches")

    # Predicting on speeches
    for speech in speech_tokens:
        prediction = predict_topic(lda_model, speech, dictionary)
        db_topic_predictions_update(speech, prediction)

    print(len(speech_data))