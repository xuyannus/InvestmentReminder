import os

import matplotlib
matplotlib.use('Agg')  # with non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick2_ohlc

TEMP_PLOT_PATH = os.path.dirname(__file__) + "/temp/"


def plot_alert(data_df, title, file_name):
    plt.figure(figsize=(12, 10))
    fig, ax = plt.subplots()
    candlestick2_ohlc(ax, data_df['Open'], data_df['High'], data_df['Low'], data_df['Close'], width=0.6, colorup='g', colordown='r')
    ax.grid(True)

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Price")
    ax.set_ylim(bottom=0)
    fig.autofmt_xdate()
    fig.tight_layout()

    init_folder(TEMP_PLOT_PATH)
    plot_path = TEMP_PLOT_PATH + file_name + ".png"
    plt.savefig(plot_path)
    plt.close()
    return plot_path


def init_folder(path):
    dirpath = os.path.dirname(path)
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)