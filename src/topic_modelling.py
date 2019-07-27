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

# *************************************** FUNCTIONS ***********************************
# Tokenizing text (separating text into individual words
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)

    # Handling tokens that have little to no meaning
    for token in tokens:
        if token.orth_.isspace(): # Skips over spaces
            continue
        elif token.like_url: # Puts in 'URL' instead of actual URL
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'): # Handling social media handles
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_) # Putting all tokens into lowercase
    return lda_tokens

# Getting lemma of a word (A lemma is the morphological basis of a word. Eg. lemma of studies is study)
def get_lemma(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4] # Only selecting tokens that are greater than 4
    tokens = [token for token in tokens if token not in en_stop] # Selecting non-stopwords
    tokens = [get_lemma(token) for token in tokens] # Getting lemma for each word
    return tokens


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
    topics = ldamodel.print_topics(num_words = 4)
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
def extract_data():
    # Initializing client:
    client = MongoClient('localhost', 27017)

    # Navigating to collection:
    db = client.trudeau_speeches
    collection = db.db_speeches

    return collection

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

    collection = extract_data()
    text_data = tokenize_whole_data(collection, data_type_choice)
    lda_model, dictionary, topics = lda_model(text_data, num_topics)

    print ("Please note the indices of the topics. We will now conduct topic modelling on more speeches")

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