from datetime import datetime
from typing import List, Generator

from google.cloud import firestore

from trader_tweets_core.model.classified_tweet import ClassifiedTweet
from trader_tweets_core.model.db_classified_tweet import DbClassifiedTweet
from trader_tweets_core.model.tweet_type import TweetType


def map_firestore_tweets_to_trader_tweets(db_tweets: Generator[firestore.DocumentSnapshot, None, None]) -> List[ClassifiedTweet]:
    classified_tweets = []
    for db_tweet in db_tweets:
        db_tweet_dict = db_tweet.to_dict()
        tweet = ClassifiedTweet(
            id=db_tweet_dict['tweet_id'],
            text=db_tweet_dict['text'],
            author=db_tweet_dict['author'],
            classification=TweetType[db_tweet_dict['type']],
            # make datetime from timestamp string
            timestamp=datetime.strptime(db_tweet_dict['timestamp'], '%Y-%m-%d %H:%M:%S'),
            img_url=''
        )
        classified_tweets.append(tweet)

    return classified_tweets


def map_tweet_obj_to_db_record(tweet: ClassifiedTweet):
    now_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return DbClassifiedTweet(
        tweet_id=tweet.id,
        text=tweet.text,
        author=tweet.author.username,
        type=tweet.classification.name,
        timestamp=now_timestamp
    )
