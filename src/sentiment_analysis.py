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

# Updating database with score:
def update_db(pos_score, neg_score, neutral_score, compound_score, id, collection):

    update_info = {"_id": id}, {'$set': {'pos_score': pos_score,
                                         'neg_score': neg_score,
                                         'neutral_score': neutral_score,
                                         'compound_score': compound_score}}

    # Updating collection:
    collection.update_one(update_info)

# Main function to coordinate all function calls:
def main():
    # Getting speeches
    speeches = extract_speech()

    for speech in speeches.find():
        speech_content = speech['details']
        speech_id = speech['_id']

        # Getting sentiment scores:
        speech_scores = sentiment_score(speech_content)
        positive_score = speech_scores['pos']
        negative_score = speech_scores['neg']
        neutral_score = speech_scores['neu']
        compound_score = speech_scores['compound']

        # Updating database:
        update_db(positive_score, negative_score, neutral_score, compound_score,
                  speech_id, speeches)
