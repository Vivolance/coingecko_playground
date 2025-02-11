"""
1. Make an API call to coin gecko https://docs.coingecko.com/v3.0.1/reference/coins-list
2. Deserialize JSON into a coin_list data class
"""
from typing import Any

import aiohttp
import requests
from retry import retry
import logging

from src.models.raw_coin_list import RawCoinsList
from src.utils.logger_utils import logger_setup

logger: logging.Logger = logging.Logger(__name__)
logger_setup(logger)


class CoinListExtractor:
    @retry(
        exceptions=aiohttp.ClientError,
        tries=5,
        delay=0.01,
        max_delay=0.08,
        backoff=2,
        jitter=(-0.01, 0.01)
    )
    async def coin_gecko_request(self) -> list[RawCoinsList]:
        url: str = "https://api.coingecko.com/api/v3/coins/list"
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.get(url, ssl=False) as response:
                    if response.status == 200:
                        response_json: list[dict[str, Any]] = await response.json()
        except aiohttp.ClientError as e:
            logger.error(e)
            raise e
        deserialized_response: list[RawCoinsList] = [RawCoinsList.model_validate(item) for item in response_json]
        return deserialized_response


