from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

COINMARKETCAP_API_KEY = "<api key>"


async def get_markets_by_market_cap():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

    parameters = {"start": "1", "limit": "500", "convert": "USD"}

    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        return _filter_stablecoins(data)
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        return None


def _filter_stablecoins(data):
    return list(
        filter(
            lambda coin: not ("stablecoin" in coin["tags"] or "memes" in coin["tags"]),
            data["data"],
        )
    )
