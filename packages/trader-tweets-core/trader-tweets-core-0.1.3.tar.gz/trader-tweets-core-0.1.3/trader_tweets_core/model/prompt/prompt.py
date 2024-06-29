from dataclasses import dataclass
from typing import Callable

from trader_tweets_core.model.prompt.bullish_bearish import BuyingSelling
from trader_tweets_core.model.tweet_type import TweetType
from trader_tweets_core.strategy.response_parsers import parse_letter_response_abc, parse_word_response, \
    parse_letter_response_tpn, parse_buying_or_selling_response


@dataclass
class Prompt:
    filename: str
    max_gpt_response_tokens: int = 3

class TweetTradePromptTemplate(Prompt):
    parser: Callable[[str], TweetType]

    def __init__(self, filename, parser, max_gpt_response_tokens):
        self.filename = filename
        self.parser = parser
        self.max_gpt_response_tokens = max_gpt_response_tokens



class BuyingSellingPrompt(Prompt):
    parser: Callable[[str], BuyingSelling]

    def __init__(self, filename, parser, max_gpt_response_tokens):
        self.filename = filename
        self.parser = parser
        self.max_gpt_response_tokens = max_gpt_response_tokens


@dataclass
class Prompts:
    # classifying as trade, prediction, or not interesting
    simple = TweetTradePromptTemplate(filename='simple.prompt', parser=parse_letter_response_abc, max_gpt_response_tokens=1)
    simple_openai = TweetTradePromptTemplate(filename='simple-openai-example.prompt', parser=parse_word_response, max_gpt_response_tokens=5)
    simple_openai_separator = TweetTradePromptTemplate(filename='simple-openai-example-separator.prompt', parser=parse_word_response, max_gpt_response_tokens=5)
    simple_openai_separator_hyphen = TweetTradePromptTemplate(filename='simple-openai-example-separator-hyphen.prompt', parser=parse_word_response, max_gpt_response_tokens=5)
    simple_openai_hyphen_one_line = TweetTradePromptTemplate(filename='simple-openai-example-hyphen-one-line.prompt', parser=parse_word_response, max_gpt_response_tokens=5)
    examples_letter = TweetTradePromptTemplate(filename='examples-letter.prompt', parser=parse_letter_response_abc,
                                               max_gpt_response_tokens=1)
    examples_letter_2 = TweetTradePromptTemplate(filename='examples-letter-2.prompt', parser=parse_letter_response_tpn,
                                                 max_gpt_response_tokens=1)
    examples_letter_ext = TweetTradePromptTemplate(filename='examples-letter-extended.prompt', parser=parse_letter_response_abc,
                                                   max_gpt_response_tokens=1)
    examples_word = TweetTradePromptTemplate(filename='examples-word.prompt', parser=parse_word_response, max_gpt_response_tokens=3)
    examples_word_2 = TweetTradePromptTemplate(filename='examples-word-2.prompt', parser=parse_word_response, max_gpt_response_tokens=3)
    examples_word_2_test = TweetTradePromptTemplate(filename='examples-word-2-test.prompt', parser=parse_word_response, max_gpt_response_tokens=10)

    # other classifications
    # is_trade_tweet_tradeable = Prompt(filename='is-trade-tweet-tradeable.prompt', parser=parse_yes_no_response)
    is_buying_or_selling = BuyingSellingPrompt(filename='is-buying-or-selling.prompt', parser=parse_buying_or_selling_response, max_gpt_response_tokens=3)
