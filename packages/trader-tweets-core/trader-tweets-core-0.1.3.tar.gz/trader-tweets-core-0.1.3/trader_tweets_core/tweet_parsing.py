# find symbols in tweets e.g. $BTC, ETH, MATIC, etc.
import logging
from typing import List, Optional

from trader_tweets_core.model.classified_tweet import ClassifiedTweet
from trader_tweets_core.model.prompt.bullish_bearish import BuyingSelling
from trader_tweets_core.model.prompt.buying_selling import OpeningClosing
from trader_tweets_core.model.trade import Trade, map_to_direction
from trader_tweets_core.repository.gpt_repository import ask_gpt_for_response, OPEN_CLOSE_10, OPEN_CLOSE_50
from trader_tweets_core.strategy.response_parsers import parse_buying_or_selling_response, parse_opening_or_closing_response

not_symbol_words = ['FTX', 'FED', 'SEC', 'FBI', 'CIA', 'FTC', 'DID', 'DOJ', 'EPA', 'FDA', 'WHO', 'CDC', 'NATO', 'CPI',
                    'FUD', 'HODL', 'HOLD', 'HTF', 'LTF', 'LARP', 'ATH' ]
symbols_that_dont_need_usd_suffix = ['SPX', 'SPY', 'ES100', 'NDQ', 'QQQ', 'DXY', 'VIX', 'IWM', 'RUT', 'GLD', 'SLV' ]
other_currencies = ['EUR', 'JPY', 'GBP']


def parse_binance_symbols_from_tweet(tweet: str) -> List[str]:
    symbols = parse_symbols_from_tweet(tweet)
    # replace USD with USDT
    return [symbol.replace('USD', 'USDT') for symbol in symbols]

def parse_symbols_from_tweet(tweet: str) -> List[str]:
    if _is_all_caps_tweet(tweet):
        return []

    symbols = []
    for word in tweet.split(' '):
        # strip out any punctuation
        word = word.strip('.,!?;:\'\\"')

        starts_with_dollar = word.startswith('$')
        is_all_caps = word.isupper()
        is_between_3_and_7_chars = 3 <= len(word) <= 7
        ends_with_usd = word.upper().endswith('USD')
        likely_symbol = starts_with_dollar \
                        or ends_with_usd \
                        or (is_all_caps and is_between_3_and_7_chars)
        if not likely_symbol:
            continue

        symbol = _clean_symbol(word)

        if word in not_symbol_words:
            continue

        if symbol in symbols:
            continue

        if any([currency in symbol for currency in other_currencies]):
            continue

        symbols.append(symbol)

    return symbols


def _clean_symbol(symbol_text):
    symbol_text = symbol_text.upper()
    if symbol_text.startswith('$'):
        symbol_text = symbol_text[1:]

    # add USD to the end if it's not already there
    if _does_need_usd_suffix(symbol_text):
        symbol_text = symbol_text + 'USD'

    return symbol_text


def _does_need_usd_suffix(symbol_text):
    if symbol_text in symbols_that_dont_need_usd_suffix:
        return False

    if all([not symbol_text.endswith(pair)
            or symbol_text == pair for pair in ['USD', 'BTC', 'ETH', 'BNB', 'USDT']]):
        return True

    return False


def is_tweet_tradeable(tweet: ClassifiedTweet) -> bool:
    trade = find_opening_trade_in_tweet(tweet)
    return trade is not None


def find_opening_trade_in_tweet(tweet: ClassifiedTweet) -> Optional[Trade]:
    symbols = parse_binance_symbols_from_tweet(tweet.text)
    if len(symbols) == 0:
        return None

    symbol = symbols[0]

    # ask gpt whether the tweet is about opening a trade or closing a trade
    logging.info(tweet.text)
    opening_or_closing = is_opening_or_closing_trade(tweet.text)
    logging.info(opening_or_closing)
    if opening_or_closing != OpeningClosing.OPENING:
        return None

    buy_or_sell = _is_bullish_or_bearish(tweet.text)

    try:
        direction = map_to_direction[buy_or_sell]
    except KeyError:
        return None

    return Trade(symbol=symbol, direction=direction, date=tweet.timestamp, origin_tweet=tweet)


def _is_all_caps_tweet(tweet: str) -> bool:
    # remove links
    words = [word for word in tweet.split(' ')]
    if len(words) < 3:
        return False

    # filter out words with links
    words_without_links = [word for word in words if not word.startswith('http')]
    return all([word.isupper() for word in words_without_links])

def _is_bullish_or_bearish(tweet_text: str) -> BuyingSelling:
    # ask gpt whether the tweet is more bullish or bearish to determine the trade direction
    # todo: read prompt from file like with other prompts?
    prompt = f"Does the following tweet indicate buying or selling? (buying|selling|neither) \n\n\"{tweet_text}\"\n\nAnswer: The tweet is"
    logging.debug(f"Querying GPT for trade type: {prompt}")
    gpt_response = ask_gpt_for_response(prompt, max_response_tokens=5)
    logging.debug(f"GPT response: {gpt_response}")
    return parse_buying_or_selling_response(gpt_response)

def is_opening_or_closing_trade(tweet_text: str) -> OpeningClosing:
    # try to classify with manual rules first
    manual_rules_result = _is_opening_or_closing_trade_manual_rules(tweet_text)
    if manual_rules_result is not None:
        return manual_rules_result

    # ask gpt whether the tweet is about opening a trade or closing a trade
    logging.info('asking gpt')
    prompt = f"{tweet_text} ->"
    logging.debug(f"Querying GPT for trade type: {prompt}")
    gpt_response = ask_gpt_for_response(prompt, max_response_tokens=1, model=OPEN_CLOSE_50)
    logging.info(f"GPT response: {gpt_response}")
    return parse_opening_or_closing_response(gpt_response)

OPENING_TRADE_KEYWORDS = ['open', 'entry', 'enter', 'buy', 'bought', 'shorted', 'longed', 'fill']
CLOSING_TRADE_KEYWORDS = ['close', 'exit', 'sell', 'sold', 'tp', 'sl', 'stop', 'profit', 'loss']

def _is_opening_or_closing_trade_manual_rules(tweet_text: str) -> Optional[OpeningClosing]:
    # contains opening or closing keywords
    if any([keyword in tweet_text.lower() for keyword in OPENING_TRADE_KEYWORDS]):
        return OpeningClosing.OPENING

    if any([keyword in tweet_text.lower() for keyword in CLOSING_TRADE_KEYWORDS]):
        return OpeningClosing.CLOSING

    return None
