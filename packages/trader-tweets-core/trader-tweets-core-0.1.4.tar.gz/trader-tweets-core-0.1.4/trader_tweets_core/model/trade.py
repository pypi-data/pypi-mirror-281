import enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from trader_tweets_core.model.prompt.prompt import BuyingSelling
from trader_tweets_core.model.twitter.simple_tweet import SimpleTweet


class Direction(enum.Enum):
    LONG = "LONG"
    SHORT = "SHORT"


map_to_buying_selling = {
    Direction.LONG: BuyingSelling.BUYING,
    Direction.SHORT: BuyingSelling.SELLING
}

map_to_direction = {
    BuyingSelling.BUYING: Direction.LONG,
    BuyingSelling.SELLING: Direction.SHORT
}


@dataclass
class Trade:
    symbol: str
    direction: Direction
    date: datetime
    origin_tweet: Optional[SimpleTweet] = None
