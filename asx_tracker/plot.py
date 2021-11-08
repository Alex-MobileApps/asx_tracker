import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import mplfinance
import pandas as pd
from asx_tracker.date import Date
from asx_tracker.database.database import Database

class Plot():

    _COL_OPEN = 'Open'
    _COL_HIGH = 'High'
    _COL_LOW = 'Low'
    _COL_CLOSE = 'Close'
    _COL_VOL = 'Volume'
    _DEF_TYPE = 'candle'


    # Plot intraday

    @staticmethod
    def intraday(ticker, start, end, **kwargs): # type=_DEF_TYPE, mav=None
        title = f'{ticker} intraday data'
        Plot._plot_intraday_or_daily(ticker, Database.fetch_single_intraday, start, end, title=title, **kwargs)


    # Plot daily

    @staticmethod
    def daily(ticker, start, end, **kwargs):
        title = f'{ticker} daily data'
        Plot._plot_intraday_or_daily(ticker, Database.fetch_single_daily, start, end, title=title, **kwargs)


    # Internal

    @staticmethod
    def _plot_intraday_or_daily(ticker, fetch_fn, start, end, **kwargs):
        df = Plot._fetch_intraday_or_daily(ticker, fetch_fn, start, end)
        if df is None:
            print(f'No data found for {ticker}')
        else:
            Plot._plot(df, **kwargs)


    @staticmethod
    def _fetch_intraday_or_daily(ticker, fetch_fn, start=None, end=None):
        # Set start/end dates
        #if end is None:
        #    end = Database.fetch_single_listing(ticker, date_col)[0][0]
        #if start is None:
        #    start = end - Date.WEEK

        fetch_cols = [Database.COL_DATE, Database.COL_OPEN, Database.COL_HIGH, Database.COL_LOW, Database.COL_CLOSE, Database.COL_VOL]
        data = fetch_fn(ticker, *fetch_cols, start=start, end=end)
        if len(data) == 0:
            return
        plot_cols = [Database.COL_DATE, Plot._COL_OPEN, Plot._COL_HIGH, Plot._COL_LOW, Plot._COL_CLOSE, Plot._COL_VOL]
        df = pd.DataFrame(data, columns=plot_cols)
        for col in [Plot._COL_OPEN, Plot._COL_HIGH, Plot._COL_LOW, Plot._COL_CLOSE]:
            df[col] /= 100
        df[Database.COL_DATE] = pd.to_datetime(df[Database.COL_DATE], unit='s')
        df[Database.COL_DATE] = df[Database.COL_DATE].dt.tz_localize(tz='Australia/Sydney')
        df.set_index(Database.COL_DATE, inplace=True)
        return df

    @staticmethod
    def _plot(df, show=True, block=False, **kwargs):
        if 'volume' not in kwargs:
            kwargs['volume'] = True
        mplfinance.plot(df, **kwargs)
        if show:
            plt.show(block=block)



















    #@staticmethod
    #def _plot(df, x_col, y_col, figsize=None, xlab='Time', ylab='Value', ax=None):
    #    if ax is None:
    #        _, ax = plt.subplots(figsize=figsize)
    #    
    #    # X
    #    x = np.arange(len(df))
    #    x_txt = list(df[x_col])
    #    
    #    # Y
    #    y = list(df[y_col])
    #    y_txt = ['${:.2f}'.format(yi) for yi in y]
    #    print(len(x_txt))
    #    print(len(y_txt))
    #    print(len(x))
    #    print(len(y))
    #    
    #    # Plot
    #    ax.plot(x, y)
    #    ax.set_xlabel(xlab)
    #    ax.set_ylabel(ylab)
    #    ax.set_xticks([])
#
    #    # Make interactive
    #    mplcursors.cursor(ax, hover=True).connect('add', lambda sel: Plot._plot_annotate(sel, x_txt, y_txt))
    #    plt.show(block=False)

    @staticmethod
    def _plot_annotate(sel, x_txt, y_txt):
        label = sel.artist.get_label()
        x = int(round(sel.target.index))
        sel.annotation.set_text(f'{label}\n{x_txt[x]}\n{y_txt[label][x]}')
