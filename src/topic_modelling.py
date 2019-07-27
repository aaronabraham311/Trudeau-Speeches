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
spacy.load('en')
from spacy.lang.en import English
parser = English()

# Other libraries
import pickle
from pymongo import MongoClient
import gensim
from gensim import corpora
import praw

# *************************************** FUNCTIONS **********************************

# Creating latent Dirichlet allocation model
def lda_model(text, NTOPIC):
    # Creating text corpus and making bag of words model
    dictionary = corpora.Dictionary(text)
    corpus = [dictionary.doc2bow(token) for token in text]

    # Saving corpus and dictionary for later use
    pickle.dump(corpus, open('../../data/corpus.pkl', 'wb'))
    dictionary.save('../../data/dictionary.gensim')

    # Creating model:
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NTOPIC, id2word = dictionary,
                                               passes = 20)
    topics = ldamodel.print_topics(num_words = 3)
    ldamodel.save("../../data/lda_model.gensim")

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
            'speech': speech['details'])

    return speech_tokens

# Preprocesses all comments and logs into one array
def tokenize_whole_data(collection):
    # Loops through all dataframes, selects content, and passes to analyzer function
    whole_text_data = []

    for data in collection.find():
        attribute = 'details'
        data_content = data[attribute]
        data_content = prepare_text(data_content)
        whole_text_data.append(data_content)

    return whole_text_data


# Puts topics intially found by LDA on training data into database
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
def db_topic_predictions_update(text, prediction, collection_type):
    client = MongoClient()

    # Navigating to collection:
    db = client.stellar_algo_reddit

    # Inserting record into different collections based on whether the text is a comment or post
    if collection_type == 'post':
        post_topic_predictions = db.post_topic_predictions
        post_topic_predictions.insert_one({text: prediction})

    elif collection_type == 'comment':
        comment_topic_predictions = db.comment_topic_predictions
        comment_topic_predictions.insert_one({text: prediction})

if __name__ == '__main__':
    print ("Welcome to to the topic modeller script. In this script, a latent Dirichlet allocation model built on previously scrapped speeches is constructed. "
           "Then, we will scrape additional speeches and show the topic probability. ")

    print ("Please enter the number of topics you would like to find in the comments or posts: ")
    num_topics = int(input())

    # Getting speech tokens and actual speeches
    speech_data = extract_speech_data()

    # Separating tokens:
    speech_tokens = []

    for speech in speech_data:
        speech_tokens.append(speech['tokens'])

    # Creating model, dictionary and topics
    lda_model, dictionary, topics = lda_model(speech_tokens, num_topics)

    print("Please note the indices of the topics. We will now conduct topic modelling on more speeches")
    # Predicting on speeches
    for speech in speech_tokens:
        prediction = predict_topic(lda_model, speech_tokens['tokens'], dictionary)
        db_topic_predictions_update()

    if data_type_choice == 'post':
        processed_posts, actual_posts = scrape_reddit_post(subreddit, 10, reddit_obj)

        for processed_post, actual_post in zip(processed_posts, actual_posts):
            prediction = predict_topic(lda_model, processed_post, dictionary)

            db_topic_predictions_update(actual_post, prediction, 'post')


    elif data_type_choice == 'comment':
        processed_comments, actual_comments = scrape_reddit_comment(subreddit, 10, 10, reddit_obj)

        for processed_comment, actual_comment in zip(processed_comments, actual_comments):
            prediction = predict_topic(lda_model, processed_comment, dictionary)

            actual_comment = actual_comment.replace('.', '')
            db_topic_predictions_update(actual_comment, prediction, 'comment')