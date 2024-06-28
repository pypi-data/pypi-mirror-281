from dataclasses import dataclass


@dataclass
class DbClassifiedTweet:
    tweet_id: int
    text: str
    author: str
    type: str
    timestamp: str
