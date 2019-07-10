# Libraries to import
import pymongo
from pymongo import MongoClient
from pprint import pprint

# Function to get speeches from MongoDB database and converting to a dictionary
def get_speeches():

    # Establishing connection
    connection = MongoClient('localhost', 27017)

    # Database and document navigation
    db = connection.trudeau_speeches
    speeches = db.speeches

    # Extracting speech data
    cursor = speeches.find()
    speechList = []

    for speech in cursor:
        speechList.append(speech)

    return speechList


# Main code block
if __name__ == "__main__":

    # Getting speeches from MongoDB
    speechList = get_speeches()
    pprint(speechList)

    # Parsing strings together

    # Removing unimportant words

    # Saving speeches in MongoDB database