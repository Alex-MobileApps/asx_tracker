import matplotlib.pyplot as plt
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
    _DEF_TYPE = 'line'


    # Plot intraday

    @staticmethod
    def intraday(ticker, start, end, **kwargs):
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
    def _fetch_intraday_or_daily(ticker, fetch_fn, start, end):
        fetch_cols = [Database.COL_DATE, Database.COL_OPEN, Database.COL_HIGH, Database.COL_LOW, Database.COL_CLOSE, Database.COL_VOL]
        data = fetch_fn(ticker, *fetch_cols, start=start, end=end)
        if len(data) == 0:
            return
        plot_cols = [Database.COL_DATE, Plot._COL_OPEN, Plot._COL_HIGH, Plot._COL_LOW, Plot._COL_CLOSE, Plot._COL_VOL]
        df = pd.DataFrame(data, columns=plot_cols)
        for col in [Plot._COL_OPEN, Plot._COL_HIGH, Plot._COL_LOW, Plot._COL_CLOSE]:
            df[col] /= 100
        df[Database.COL_DATE] = Date.timestamp_to_datetime(df[Database.COL_DATE])
        df.set_index(Database.COL_DATE, inplace=True)
        return df


    @staticmethod
    def _plot(df, block=True, **kwargs):
        if 'volume' not in kwargs:
            kwargs['volume'] = True
        if 'type' not in kwargs:
            kwargs['type'] = Plot._DEF_TYPE
        mplfinance.plot(df, block=block, **kwargs)


    @staticmethod
    def close():
        plt.close('all')

















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
