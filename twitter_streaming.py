import twitter
from credentials import *
from pymongo import MongoClient
import time
from datetime import datetime, timedelta
from email.utils import parsedate_tz

client = MongoClient()
# Access/Initiate Database
db = client['twitter']
# Access/Initiate Table
tab = db['test']

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
#from twitter import OAuth, TwitterHTTPError, TwitterStream



api = twitter.Api(consumer_key=CONSUMER_KEY,
                      consumer_secret=CONSUMER_SECRET,
                      access_token_key=ACCESS_TOKEN,
                      access_token_secret=ACCESS_SECRET)

### Verify credential
#print(api.VerifyCredentials())

#kinesis = boto3.client('kinesis')



def get_id():
    twitter_handle = ''
    results = api.GetSearch(
        raw_query=f"q=to%40{twitter_handle}%20&result_type=recent&lang=en&tweet_mode=extended&since=2018-09-07&count=1")

    # for item in results:
    #     kinesis.put_record(StreamName="twitter", Data=json.dumps(item), PartitionKey="filler")


    json_results = [result.AsDict() for result in results]

    for tweet in json_results:
        recent_id = tweet['id']
        print({'tweet_id':tweet['id'],'created_at':tweet['created_at'],'twitter_handle':twitter_handle,"favorite":tweet.get('favorite_count',0), "retweet":tweet.get('retweet_count',0), 'full_text':tweet['full_text']})
    return recent_id

######### Get tweets using the past_id as a filter for time
def get_tweets(past_id):

    def to_datetime(datestring):
        time_tuple = parsedate_tz(datestring.strip())
        dt = datetime(*time_tuple[:6])
        return dt - timedelta(seconds=time_tuple[-1])

    twitter_handle = 'realdonaldtrump'
    results = api.GetSearch(
        raw_query=f"q=to%40{twitter_handle}%20&result_type=popular&since_id={past_id}&lang=en&tweet_mode=extended&count=10")

    if not results:
        print('no results')
    json_results = [result.AsDict() for result in results]

    for tweet in json_results:
        date_time =  to_datetime(tweet['created_at'])
        print({'tweet_id':tweet['id'],'created_at':date_time,'twitter_handle':twitter_handle,"favorite":tweet.get('favorite_count',0), "retweet":tweet.get('retweet_count',0) ,'full_text':tweet['full_text']})




    '''
    #oauth = api(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

    # Initiate the connection to Twitter Streaming API
    twitter_stream = TwitterStream(api = api)

    # Get a sample of the public data following through Twitter
    iterator = twitter_stream.statuses.sample()

    # Print each tweet in the stream to the screen
    # Here we set it to stop after getting 1000 tweets.
    # You don't have to set it to stop, but can continue running
    # the Twitter API to collect data for days or even longer.
    tweet_count = 1000
    for tweet in iterator:
        tweet_count -= 1
        # Twitter Python Tool wraps the data returned by Twitter
        # as a TwitterDictResponse object.
        # We convert it back to the JSON format to print/score
        print(json.dumps(tweet))

        # The command below will do pretty printing for JSON data, try it out
        # print json.dumps(tweet, indent=4)

        if tweet_count <= 0:
            break
    '''
if __name__ == '__main__':
    past_id = 1040662730410221574
    get_tweets(past_id)

    # for _ in range(5):
    #     print("... sleeping")
    #     recent_id = get_id()
    #     get_tweets(past_id)
    #     print("-"*10)
    #     past_id = recent_id
    #     time.sleep(60*1)
