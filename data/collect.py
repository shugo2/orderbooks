

import sys
sys.path.append(".")

import requests

from utils import _parse_args
from data.model import db, Quote, path

import pandas as pd

import time
import datetime


def collect(route, db, start, end, headers, sleep_time=1, collected=0):
    if route is None: return collected
    params = {"page_size": "100", "limit_orders": "10"}
    if start is not None:
        start_iso8601 = start.isoformat(timespec="milliseconds") + "Z"
        params["start_time"] = start_iso8601
    if end is not None:
        end_iso8601 = end.isoformat(timespec="milliseconds") + "Z"
        params["end_time"] = end_iso8601
    resp = requests.get(route, headers=headers, params=params)
    resp = resp.json()
    data = resp.get("data", [])
    for i in range(len(data)):
        quote = data[i]
        ts = quote["poll_timestamp"]
        id = hash(config.ticker + market + str(ts))
        mp = quote["mid_price"]
        valid_keys = [k for k in quote.keys() if "ask_volume" in k or "bid_volume" in k]
        volumes = {k: quote[k] for k in valid_keys}
        quote = Quote(id=id, ticker=config.ticker, ts=ts, exchange=market, mid_price=mp, **volumes)
        try:
            db.session.add(quote)
            db.session.commit()
        except:
            db.session.remove()
    time.sleep(1)
    return collect(route=resp.get("next_url"), db=db, start=None, end=None,
                   headers=headers, sleep_time=sleep_time, collected=collected+len(data))

if __name__ == "__main__":

    config, _ = _parse_args()
    headers = {"Accept": "application/json", "X-Api-Key": config.kaiko_key}

    db.create_all()
    already_collected = pd.read_sql("Select * From Quote", path, index_col="id")
    start_time = datetime.datetime.strptime(config.start, "%Y-%m-%d")
    end_time = datetime.datetime.strptime(config.end, "%Y-%m-%d")

    for market in config.markets:

        print("\n\nDownloading : ", market, config.ticker)
        route = "https://us.market-api.kaiko.io/v2/data/order_book_snapshots.v1/exchanges/{0}/perpetual-future/{1}/snapshots/full".format(market, str(config.ticker))
        acdata = already_collected.loc[already_collected.exchange == market]
        acdata = acdata.loc[acdata.ticker == config.ticker]

        first_collected_time = pd.to_datetime(acdata.ts.min(), unit="ms").to_pydatetime() \
        if len(acdata) > 0 else None
        last_collected_time = pd.to_datetime(acdata.ts.max(), unit="ms").to_pydatetime() \
        if len(acdata) > 0 else None

        if first_collected_time is None and last_collected_time is None:
            print("collecting order books from {0} to {1}".format(start_time, end_time))
            c = collect(route=route, db=db, start=start_time, end=end_time, headers=headers, collected=0)
            print("{0} order book(s) collected".format(c))
        else:
            if start_time < first_collected_time:
                print("collecting order books from {0} to {1}".format(start_time, first_collected_time))
                c = collect(route=route, db=db, start=start_time, end=first_collected_time, headers=headers)
                print("{0} order book(s) collected".format(c))
            if end_time > last_collected_time:
                print("collecting order book(s) from {0} to {1}".format(last_collected_time, end_time))
                c = collect(route=route, db=db, start=last_collected_time, end=end_time, headers=headers)
                print("{0} order book(s) collected".format(c))
