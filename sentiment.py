import pprint
from pymongo import MongoClient
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

client = MongoClient()

# Access/Initiate Database
db = client['twitter']
# Access/Initiate Table
collection = db.tab


def main():

        #note: depending on how you installed (e.g., using source code download versus pip install), you may need to import like this:
        #from vaderSentiment import SentimentIntensityAnalyzer

    # --- examples -------
    tweets = []
    print('Total Record for the collection: ' + str(collection.count()))
    for row in collection.find():
        tweets.append(row['full_text'])

    analyzer = SentimentIntensityAnalyzer()
    for tweet in tweets:
        vs = analyzer.polarity_scores(tweet)
        print("{:-<65} \n {}".format(tweet, str(vs)))


if __name__ == '__main__':
    main()
