from typing import List

from trader_tweets_core.model.classified_tweet import create_classified_tweet
from trader_tweets_core.model.twitter.simple_tweet import SimpleTweet
from trader_tweets_core.model.tweet_type import TweetType

NON_SERIOUS_WORDS = ['lol', 'hah', 'wtf', 'um', 'uh', '69', 'meme', 'moon', 'bitboy', 'rainbow', 'shill', 'shitcoin', ]
TRADE_WORDS = ['stopped']
PREDICTION_WORDS = ['prediction', 'forecast']


def _is_trade(tweet):
    return any(word for word in TRADE_WORDS if word in tweet.text.lower())


def _is_prediction(tweet):
    return any(word for word in PREDICTION_WORDS if word in tweet.text.lower())


def _is_not_interesting(tweet):
    non_link_text = _get_non_link_text(tweet.text)
    is_just_link = len(non_link_text.strip()) == 0
    is_retweet = non_link_text.lower().startswith('rt')
    contains_non_serious_word = any(word for word in NON_SERIOUS_WORDS if word in tweet.text.lower())

    is_too_short = len(non_link_text) < 10

    return is_just_link \
           or is_retweet \
           or contains_non_serious_word \
           or is_too_short


# filter out urls from the tweet text
def _get_non_link_text(tweet_text):
    return ' '.join(word for word in tweet_text.split(' ') if not word.startswith('https'))


def _can_classify_with_rules(tweet):
    return _is_not_interesting(tweet) \
           or _is_prediction(tweet) \
           or _is_trade(tweet)


def _classify_tweet_with_rules(tweet):
    if _is_trade(tweet):
        return create_classified_tweet(tweet, TweetType.TRADE)
    elif _is_prediction(tweet):
        return create_classified_tweet(tweet, TweetType.PREDICTION)
    else:
        return create_classified_tweet(tweet, TweetType.NOT_INTERESTING)


# attempts to classify each tweet using rules and returns classified tweets
def classify_tweets_with_rules(tweets: List[SimpleTweet]):
    classified_tweets = []
    for tweet in tweets:
        can_classify = _can_classify_with_rules(tweet)
        if can_classify:
            classified_tweets.append(_classify_tweet_with_rules(tweet))
    return classified_tweets
