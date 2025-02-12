import ccxt
import pandas as pd
import asyncio
import pymongo
from datetime import datetime
import time
from dateutil import tz
from utility import *

CANDLE_DURATION_IN_MIN = 15
DB_URI = "<MongoDB URI>"
DB_client = pymongo.MongoClient(DB_URI)
bot_db = DB_client["trading_bot"]
markets_collection = bot_db["markets"]

exchange = ccxt.binance({"enableRateLimit": True})


def trading_view_link(symbol):
    return f"https://www.tradingview.com/chart/CtnHaLF3/?symbol=BINANCE%3A{symbol}USDT"


# STEP 1: FETCH THE DATA
async def fetch_ohlcv_as_dataframe(ticker):
    bars, ticker_df = None, None

    try:
        bars = exchange.fetch_ohlcv(
            ticker, timeframe=f"{CANDLE_DURATION_IN_MIN}m", limit=200
        )
    except:
        return

    if bars is not None:
        ticker_df = pd.DataFrame(
            bars[:-1], columns=["at", "open", "high", "low", "close", "vol"]
        )
        ticker_df["date"] = pd.to_datetime(ticker_df["at"], unit="ms")
        ticker_df["symbol"] = ticker

    return ticker_df


def find_doc(symbol):
    return markets_collection.find_one({"symbol": symbol})


async def fetch_ticker(ticker):
    return await exchange.fetch_ticker(ticker)


def calculate_200_SMA(market_data, ohlc):
    return sum(market_data[ohlc]) / 200


async def main():
    markets = await get_markets_by_market_cap()
    # first time upon start, the bot should ONLY calculate the hlv and save the candleOpen

    while True:
        timestamp = get_timestamp_in_GMTPLUS2()
        time_formatted = format(timestamp, "%d/%m/%Y %H:%M")
        print(f"----------- Timestamp {time_formatted} -----------")
        start_time = time.time()

        poteintial_buy_sign_coins = markets_collection.find({"hlv": -1})

        for coin in poteintial_buy_sign_coins:
            await fetch_ohlcv_and_apply_strategy(coin["symbol"])

        print("~ ~ ~ Done with poteintial buy-sign coins ~ ~ ~")

        for market in markets:
            if coin_exists_in_potential_buy_signs(
                market["symbol"], poteintial_buy_sign_coins
            ):
                continue

            if not doc_exists_in_collection(market["symbol"]):
                create_doc(market["symbol"])

            await fetch_ohlcv_and_update_hlv(market["symbol"])

        print(f"Sleeping...")
        time_difference_in_sec = time.time() - start_time
        time.sleep(CANDLE_DURATION_IN_MIN * 60 - time_difference_in_sec)


def get_doc(symbol):
    return markets_collection.find_one({"symbol": symbol})


def doc_exists_in_collection(symbol):
    market_doc = get_doc(symbol)
    return market_doc != None


def create_doc(symbol):
    markets_collection.insert_one({"symbol": symbol, "hlv": None})


def get_timestamp_in_GMTPLUS2():
    return datetime.fromtimestamp(datetime.now().timestamp(), tz=tz.gettz("Etc/GMT-2"))


def reset_all_hlv_in_db():
    markets_collection.update_many({}, {"$set": {"hlv": None}})


def coin_exists_in_potential_buy_signs(symbol, poteintial_buy_sign_coins):
    return symbol in [x.get("symbol") for x in list(poteintial_buy_sign_coins)]


async def fetch_ohlcv_and_apply_strategy(symbol):
    market_data = await fetch_ohlcv_as_dataframe(f"{symbol}/USDT")

    if market_data is None:
        return

    if apply_strategy(symbol, market_data):
        print(f"[{symbol}]: {trading_view_link(symbol)}")


async def fetch_ohlcv_and_update_hlv(symbol):
    market_data = await fetch_ohlcv_as_dataframe(f"{symbol}/USDT")

    if market_data is None:
        return

    prevHlv = find_doc(symbol)["hlv"]
    get_and_update_hlv(symbol, prevHlv, market_data)


def get_and_update_hlv(symbol, prevHlv, market_data):
    sma_200_high = calculate_200_SMA(market_data, "high")
    sma_200_low = calculate_200_SMA(market_data, "low")

    close = market_data["close"][len(market_data) - 1]

    hlv = 1 if close > sma_200_high else -1 if close < sma_200_low else prevHlv

    markets_collection.update_one({"symbol": symbol}, {"$set": {"hlv": hlv}})

    return hlv


def apply_strategy(symbol, market_data):
    prevHlv = find_doc(symbol)["hlv"]
    hlv = get_and_update_hlv(symbol, prevHlv, market_data)

    is_buy_sign = hlv == 1 and prevHlv == -1

    return is_buy_sign


if __name__ == "__main__":
    asyncio.new_event_loop().run_until_complete(main())
