from datetime import datetime
from typing import List

import pytz


def cleanse_binance_klines(klines: List[List]) -> List[List[any]]:
    # keep only the first 6 elements of each kline (important ones)
    with_last_elements_removed = [kline[:6] for kline in klines]

    # convert any numbers as strings to floats
    with_numbers_only = [[float(element) if isinstance(element, str) else element for element in kline] for kline in with_last_elements_removed]

    # convert timestamps to datetime objects. element 0 and 6 are timestamps
    # with_datetimes = [[_convert_from_unix_to_iso(kline[0]), *kline[1:]] for kline in with_numbers_only]

    # return with_datetimes
    return with_numbers_only


def _convert_from_unix_to_iso(unix_timestamp: int) -> str:
    return datetime.fromtimestamp(unix_timestamp / 1000)\
        .astimezone(pytz.timezone('UTC'))\
        .isoformat()