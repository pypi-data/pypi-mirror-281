from trader_tweets_core.model.tweet_mood import TweetMood
from trader_tweets_core.service.classifier.gpt_classifier import classify_tweet as _classify_tweet


def classify_tweet_mood(tweet_text, author=None) -> TweetMood:
    return _classify_tweet(tweet_text, author)
