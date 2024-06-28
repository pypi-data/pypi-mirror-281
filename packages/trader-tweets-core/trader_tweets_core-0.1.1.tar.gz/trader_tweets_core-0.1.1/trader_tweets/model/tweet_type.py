from enum import Enum


class TweetType(Enum):
    TRADE = 1  # open or close a trade
    PREDICTION = 2  # a short-term directional view on the market or a coin
    SHITPOSTING = 3
    NOT_INTERESTING = 4
    UNSURE = 5


def map_tweet_type_to_string(tweet_type):
    if tweet_type == TweetType.TRADE:
        return 'trade'
    elif tweet_type == TweetType.PREDICTION:
        return 'prediction'
    elif tweet_type == TweetType.SHITPOSTING:
        return 'shitposting'
    elif tweet_type == TweetType.NOT_INTERESTING:
        return 'not interesting'
    elif tweet_type == TweetType.UNSURE:
        return 'unsure'
    else:
        raise Exception('Invalid tweet_type: {}'.format(tweet_type))
