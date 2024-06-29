from dataclasses import dataclass

from trader_tweets_core.model.twitter.simple_tweet import SimpleTweet
from trader_tweets_core.model.tweet_type import TweetType


def create_classified_tweet(tweet: SimpleTweet, classification: TweetType):
    return ClassifiedTweet(
        id=tweet.id,
        text=tweet.text,
        author=tweet.author,
        classification=classification,
        img_url=tweet.img_url,
        timestamp=tweet.timestamp
    )


@dataclass(unsafe_hash=True)
class ClassifiedTweet(SimpleTweet):
    classification: TweetType = TweetType.UNSURE
