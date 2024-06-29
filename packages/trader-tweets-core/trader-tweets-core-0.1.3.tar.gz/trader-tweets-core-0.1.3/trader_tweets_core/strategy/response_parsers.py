from trader_tweets_core.model.prompt.bullish_bearish import BuyingSelling
from trader_tweets_core.model.prompt.buying_selling import OpeningClosing
from trader_tweets_core.model.tweet_type import TweetType


def parse_letter_response_abc(response: str) -> TweetType:
    if 'a' in response:
        return TweetType.TRADE
    if 'b' in response:
        return TweetType.PREDICTION
    if 'c' in response:
        return TweetType.NOT_INTERESTING
    return TweetType.UNSURE


def parse_letter_response_tpn(response: str) -> TweetType:
    if response.startswith('P'):
        return TweetType.PREDICTION
    elif response.startswith('T'):
        return TweetType.TRADE
    elif response.startswith('N'):
        return TweetType.NOT_INTERESTING
    else:
        raise ValueError('Invalid response: %s' % response)


def parse_word_response(response: str) -> TweetType:
    if 'trade' in response.lower():
        return TweetType.TRADE
    elif 'prediction' in response.lower():
        return TweetType.PREDICTION
    elif 'not' in response.lower():
        return TweetType.NOT_INTERESTING
    else:
        raise ValueError('Invalid response: \'%s\'' % response)


def parse_yes_no_response(response: str) -> bool:
    if 'yes' in response.lower():
        return True
    elif 'no' in response.lower():
        return False
    return False

def parse_buying_or_selling_response(response: str) -> BuyingSelling:
    if 'buy' in response.lower():
        return BuyingSelling.BUYING
    elif 'sell' in response.lower():
        return BuyingSelling.SELLING
    return BuyingSelling.NEITHER


def parse_opening_or_closing_response(response: str) -> OpeningClosing:
    if 'open' in response.lower():
        return OpeningClosing.OPENING
    elif 'clos' in response.lower():
        return OpeningClosing.CLOSING
    # raise ValueError('Invalid response: \'%s\'' % response)
    return OpeningClosing.CLOSING
