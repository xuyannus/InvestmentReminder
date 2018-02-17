import os
import time
import logging
import pandas as pd

from datetime import datetime, timedelta
from src.data_loader import get_us_stock_historical_price
from src.email_helper import email_bid_prices
from src.plot_helper import plot_alert

SYMBOL_PATH = os.path.dirname(__file__) + "/WIKI-symbol-us.csv"
LOG_PATH = os.path.dirname(__file__) + "/stock_alerts.log"


def check_stock_price_shake():
    symbols = pd.read_csv(SYMBOL_PATH, header=None, names=["symbol", "name"])
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)

    alerts = []
    for _, item in symbols.iterrows():
        data = get_us_stock_historical_price(item['symbol'], start_date, end_date)
        if not is_an_alert(data):
            continue

        file_name = item['symbol'].replace('/', '_')
        plot_path = plot_alert(data, title="{}".format(item['symbol']), file_name=file_name)
        alerts.append({
            "symbol": item.symbol,
            "name": item.name,
            "open": data.iloc[-1]['Open'],
            "close": data.iloc[-1]['Close'],
            "high": data.iloc[-1]['High'],
            "low": data.iloc[-1]['Low'],
            "plot": plot_path
        })

        time.sleep(0.1)
    email_bid_prices(pd.DataFrame(alerts), to_recipient_columns=["symbol", "name", "open", "high", "low", "close"])


def is_an_alert(data):
    if len(data) < 5:
        return False
    if abs(data.iloc[-1]['Close'] - data.iloc[-1]['Open']) >= data.iloc[-1]['Close'] * 0.05:
        return True
    if abs(data.iloc[-1]['High'] - data.iloc[-1]['Low']) >= data.iloc[-1]['Close'] * 0.10:
        return True
    return False


def set_up_logging():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO, filename=LOG_PATH)

if __name__ == '__main__':
    set_up_logging()
    check_stock_price_shake()
