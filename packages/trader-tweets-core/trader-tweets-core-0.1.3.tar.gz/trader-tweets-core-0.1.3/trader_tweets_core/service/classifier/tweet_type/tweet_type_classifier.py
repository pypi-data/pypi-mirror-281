import logging
from typing import List

from trader_tweets_core.model.classified_tweet import ClassifiedTweet
from trader_tweets_core.model.twitter.simple_tweet import SimpleTweet
from trader_tweets_core.service.classifier.gpt_classifier import classify_tweets_with_gpt
from trader_tweets_core.service.classifier.tweet_type.rule_based_classifier import classify_tweets_with_rules


def classify_tweet_types(tweets: List[SimpleTweet]) -> List[ClassifiedTweet]:
    logging.info('Classifying {num_tweets} tweets: '.format(num_tweets=len(tweets)))
    # first, attempt to classify with rules
    # then classify the remaining tweets with gpt
    classified_tweets = classify_tweets_with_rules(tweets)
    logging.info('Classified {num_tweets} tweets with rules'.format(num_tweets=len(classified_tweets)))

    def is_tweet_in_collection(tweet, collection): return tweet.id in [t.id for t in collection]

    remaining_tweets = [tweet for tweet in tweets if not is_tweet_in_collection(tweet, classified_tweets)]
    classified_with_gpt = classify_tweets_with_gpt(remaining_tweets)
    logging.info('Classified {num_tweets} tweets with gpt'.format(num_tweets=len(classified_with_gpt)))
    classified_tweets.extend(classified_with_gpt)
    return classified_tweets


def classify_tweet_type(tweet: SimpleTweet) -> ClassifiedTweet:
    return classify_tweet_types([tweet])[0]
