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
    speeches = db.db_speeches

    # Updating speech data
    for speech in speeches.find():
        speech_content = speech['details']
        speech_id = speech['_id']
        new_speech = speech_content.replace('CHECK AGAINST DELIVERY', '')

        try:
            speeches.update_one(
                {'_id': speech_id},
                {'$set': {'details': new_speech}}
            )
        except:
            print('Database update not successful')



# Main code block
if __name__ == "__main__":

    # Getting speeches from MongoDB
    #speechList = get_speeches()
    #pprint(speechList)

    get_speeches()

    # Parsing strings together

    # Removing unimportant words

    # Saving speeches in MongoDB database