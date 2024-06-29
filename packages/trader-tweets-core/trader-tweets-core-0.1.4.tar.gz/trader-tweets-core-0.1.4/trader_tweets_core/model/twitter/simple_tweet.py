from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from trader_tweets_core.model.twitter.twitter_user import TwitterUser


@dataclass(unsafe_hash=True)
class SimpleTweet:
    id: int
    text: str
    author: Optional[TwitterUser]
    img_url: Optional[str]
    timestamp: Optional[datetime]

