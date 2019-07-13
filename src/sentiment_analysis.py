# Importing libraries
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pymongo import MongoClient

# Function to get speech
def extract_speech():

    # Intializing client and navigating to MongoDB database
    client = MongoClient('localhost', 27017)
    db = client.trudeau_speeches
    speeches = db.db_speeches

    return speeches

# Getting sentiment score of each speech
def sentiment_score(speech):
    # Intializing analyzer object
    analyzer = SentimentIntensityAnalyzer()

    # Outputting and returning speech sentiment score
    score = analyzer.polarity_scores(speech)
    print("Speech: ", speech)
    print("Score: ", score)

    return score